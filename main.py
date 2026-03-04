import asyncio
import os
from typing import List
from telethon import TelegramClient, functions, types, errors
from telethon.tl.functions.messages import GetDialogFiltersRequest
from telethon.tl.types import DialogFilter, TextWithEntities
from colorama import Fore, Style, init
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

init(autoreset=True)

# --- CONFIGURATION FROM ENVIRONMENT ---
API_ID = os.getenv('TG_API_ID')
API_HASH = os.getenv('TG_API_HASH')
SESSION_NAME = 'tg_cleaner_pro'

if not API_ID or not API_HASH:
    print(f"{Fore.RED}Error: TG_API_ID or TG_API_HASH not found in .env file!")
    exit(1)

client = TelegramClient(SESSION_NAME, int(API_ID), API_HASH)

class TGCleaner:
    def __init__(self, whitelist: List[str]):
        self.whitelist = [item.strip().lower().lstrip('@') for item in whitelist]

    def is_safe(self, title: str, username: str, chat_id: int) -> bool:
        if chat_id == 'me' or title == "Saved Messages":
            return True
        for item in self.whitelist:
            if not item: continue
            if (username and item == username.lower()) or (item in title.lower()) or (item == str(chat_id)):
                return True
        return False

    async def secure_delete(self, peer, title: str, index: int, total: int):
        status_prefix = f"{Fore.CYAN}[{index}/{total}]{Style.RESET_ALL}"
        try:
            entity = await client.get_entity(peer)
            username = getattr(entity, 'username', None)
            chat_id = getattr(entity, 'id', 0)

            if self.is_safe(title, username, chat_id):
                print(f"{status_prefix} {Fore.YELLOW}SKIP: {title}")
                return

            try:
                await client(functions.messages.UpdatePinnedDialogRequest(peer=peer, pinned=False))
            except: pass

            if isinstance(entity, types.User) and entity.bot:
                await client(functions.contacts.BlockRequest(id=peer))
                await client.delete_dialog(peer)
                print(f"{status_prefix} {Fore.RED}REMOVED BOT: {title}")
            elif isinstance(entity, types.User):
                await client(functions.messages.DeleteHistoryRequest(peer=peer, max_id=0, just_clear=False, revoke=True))
                await client.delete_dialog(peer)
                print(f"{status_prefix} {Fore.RED}REMOVED USER/GHOST: {title}")
            else:
                await client.delete_dialog(peer)
                print(f"{status_prefix} {Fore.RED}LEFT GROUP/CHANNEL: {title}")

            await asyncio.sleep(0.8)

        except errors.FloodWaitError as e:
            await asyncio.sleep(e.seconds)
        except Exception:
            try:
                await client.delete_dialog(peer)
                print(f"{status_prefix} {Fore.RED}FORCE REMOVED: {title}")
            except: pass

async def get_folder_peers(folder_name: str):
    result = await client(GetDialogFiltersRequest())
    for f in result.filters:
        if isinstance(f, DialogFilter):
            title = f.title.text if isinstance(f.title, TextWithEntities) else str(f.title)
            if title.lower() == folder_name.lower():
                return f.include_peers
    return None

async def main_menu():
    print(f"\n{Fore.GREEN}{Style.BRIGHT}=== TELEGRAM PRO CLEANER CLI ===")
    wl_input = input(f"{Fore.BLUE}Enter Whitelist (comma separated): {Style.RESET_ALL}")
    cleaner = TGCleaner(wl_input.split(','))

    print(f"\n1. NUCLEAR MODE (Full Wipe)")
    print(f"2. FOLDER MODE (Specific Folder)")
    print(f"3. EXIT")
    choice = input(f"\n{Fore.CYAN}Selection: {Style.RESET_ALL}")

    if choice == '1':
        if input(f"{Fore.RED}Type 'CONFIRM' to wipe: ") != "CONFIRM": return
        dialogs = await client.get_dialogs()
        for i, d in enumerate(dialogs, 1):
            await cleaner.secure_delete(d.input_entity, d.name, i, len(dialogs))
    elif choice == '2':
        folder = input(f"{Fore.BLUE}Folder Name: {Style.RESET_ALL}").strip()
        peers = await get_folder_peers(folder)
        if peers:
            for i, peer in enumerate(peers, 1):
                try:
                    ent = await client.get_entity(peer)
                    name = getattr(ent, 'title', getattr(ent, 'first_name', "Ghost"))
                    await cleaner.secure_delete(peer, name, i, len(peers))
                except: pass

if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main_menu())