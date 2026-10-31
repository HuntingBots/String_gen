#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MIT License

Copyright (c) 19-10-2026 @HuntingBots for MatrixVcBot

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

"""
Telegram String Session Generator
Supports Pyrogram (v2), Pyrofork, and Telethon.
Compatible with GitHub Actions Workflows, Local CLI, VPS, Termux.
Author: @HuntingBots for MatrixVcBot
"""

import os
import sys
import inspect
from pathlib import Path

# Fix stdlib 'string' shadowing if string.py was imported or exists
if __name__ != "__main__":
    import importlib.machinery
    import importlib.util
    _cur_dir = os.path.dirname(os.path.abspath(__file__))
    _stdlib_paths = [p for p in sys.path if p and os.path.abspath(p) != _cur_dir]
    _spec = importlib.machinery.PathFinder.find_spec("string", _stdlib_paths)
    if _spec and _spec.loader:
        _real_string = importlib.util.module_from_spec(_spec)
        _spec.loader.exec_module(_real_string)
        sys.modules["string"] = _real_string
        globals().update(_real_string.__dict__)

BANNER = r"""
╔═══════════════════════════════════════════════════════════════╗
║               TELEGRAM STRING SESSION GENERATOR               ║
║                                                               ║
║   Supported Frameworks:                                       ║
║     [1] Pyrogram (Official v2)                                ║
║     [2] Pyrofork (Modern & Maintained Pyrogram Fork)          ║
║     [3] Telethon (Sync / Async v1)                            ║
║                                                               ║
║   By HuntingBots | Ready for GitHub Actions & Local CLI       ║
╚═══════════════════════════════════════════════════════════════╝
"""

def print_banner():
    print(BANNER)

def get_api_id():
    """Retrieve API_ID from environment variable or prompt the user."""
    env_id = os.environ.get("API_ID", "").strip()
    if env_id:
        try:
            return int(env_id)
        except ValueError:
            pass
    while True:
        try:
            val = input("👉 Enter your Telegram API ID: ").strip()
            if not val:
                print("❌ API ID cannot be empty. Please try again.")
                continue
            return int(val)
        except ValueError:
            print("❌ Invalid API ID! It must be an integer (e.g. 12345678).")

def get_api_hash():
    """Retrieve API_HASH from environment variable or prompt the user."""
    env_hash = os.environ.get("API_HASH", "").strip()
    if env_hash:
        return env_hash
    while True:
        val = input("👉 Enter your Telegram API HASH: ").strip()
        if val:
            return val
        print("❌ API HASH cannot be empty. Please try again.")

def notify_success(framework_name, session_string, sent_to_saved=True, send_error=None):
    """Display generated session string and notify the user."""
    divider = "═" * 70
    print("\n" + divider)
    print(f"🎉 SUCCESS! YOUR {framework_name.upper()} STRING SESSION IS READY:")
    print(divider)
    print(f"\n{session_string}\n")
    print(divider)
    
    if sent_to_saved:
        print("📬 Successfully sent a backup copy to your Telegram 'Saved Messages'!")
    else:
        print(f"⚠️ Notice: Could not send to Saved Messages ({send_error}).")
        print("   Please copy your session string directly from above!")
        
    print("🔒 SECURITY WARNING: Keep this session string strictly private!")
    print("   Anyone with this session string can access your Telegram account.")
    print(divider + "\n")

    # Mark completion flag for automated environments / workflows
    try:
        Path("/tmp/session_done").touch()
    except Exception:
        pass

def generate_pyrogram_or_pyrofork(framework_name="Pyrofork"):
    """Generate session string using Pyrogram or Pyrofork."""
    print(f"\n🚀 Setting up {framework_name} session generator...\n")
    
    # Check if isolated official pyrogram path exists
    official_path = "/opt/pyrogram_official"
    if framework_name == "Pyrogram" and os.path.isdir(official_path):
        if official_path not in sys.path:
            sys.path.insert(0, official_path)
    elif framework_name == "Pyrofork" and official_path in sys.path:
        sys.path.remove(official_path)

    # Clean cached pyrogram modules to allow dynamic framework switching
    for mod in list(sys.modules.keys()):
        if mod == "pyrogram" or mod.startswith("pyrogram."):
            del sys.modules[mod]

    try:
        import pyrogram
        from pyrogram import Client, enums
    except ImportError:
        print(f"\n❌ Error: '{framework_name.lower()}' is not installed.")
        print(f"Please install it using: pip install {framework_name.lower()} tgcrypto\n")
        return False

    version = getattr(pyrogram, "__version__", "unknown")
    print(f"ℹ️  Loaded module: pyrogram version {version}")

    api_id = get_api_id()
    api_hash = get_api_hash()

    print("\n📱 Initiating login flow...")
    print("💡 Note: You will be asked for your phone number (+countrycode), OTP code, and 2FA password (if enabled).\n")

    try:
        with Client(name=f"{framework_name.lower()}_session", api_id=api_id, api_hash=api_hash, in_memory=True) as client:
            session_result = client.export_session_string()
            if inspect.isawaitable(session_result):
                import asyncio
                session_string = asyncio.run(session_result)
            else:
                session_string = str(session_result)

            sent_saved = False
            send_err = None
            try:
                client.send_message(
                    "me",
                    f"🎉 <b>{framework_name} String Session Generated!</b>\n\n"
                    f"<code>{session_string}</code>\n\n"
                    f"⚠️ <b>Security Notice:</b>\n"
                    f"• Never share this string session with anyone!\n"
                    f"• Anyone with this string has full access to your account.\n\n"
                    f"Generated by <b>HuntingBots String Generator</b>",
                    parse_mode=enums.ParseMode.HTML
                )
                sent_saved = True
            except Exception as e:
                send_err = str(e)

            notify_success(framework_name, session_string, sent_saved, send_err)
            return True
    except Exception as e:
        print(f"\n❌ Failed to generate {framework_name} session string!")
        print(f"Reason: {e}\n")
        return False

def generate_telethon():
    """Generate session string using Telethon."""
    print("\n🚀 Setting up Telethon session generator...\n")

    try:
        from telethon.sync import TelegramClient
        from telethon.sessions import StringSession
        import telethon
    except ImportError:
        print("\n❌ Error: 'telethon' is not installed.")
        print("Please install it using: pip install telethon\n")
        return False

    version = getattr(telethon, "__version__", "unknown")
    print(f"ℹ️  Loaded Telethon version {version}")

    api_id = get_api_id()
    api_hash = get_api_hash()

    print("\n📱 Initiating login flow...")
    print("💡 Note: You will be asked for your phone number (+countrycode), OTP code, and 2FA password (if enabled).\n")

    try:
        with TelegramClient(StringSession(), api_id, api_hash) as client:
            session_string = client.session.save()
            
            sent_saved = False
            send_err = None
            try:
                client.send_message(
                    "me",
                    f"🎉 <b>Telethon String Session Generated!</b>\n\n"
                    f"<code>{session_string}</code>\n\n"
                    f"⚠️ <b>Security Notice:</b>\n"
                    f"• Never share this string session with anyone!\n"
                    f"• Anyone with this string has full access to your account.\n\n"
                    f"Generated by <b>HuntingBots String Generator</b>",
                    parse_mode="html"
                )
                sent_saved = True
            except Exception as e:
                send_err = str(e)

            notify_success("Telethon", session_string, sent_saved, send_err)
            return True
    except Exception as e:
        print(f"\n❌ Failed to generate Telethon session string!")
        print(f"Reason: {e}\n")
        return False

def main():
    print_banner()

    while True:
        print("Select the framework you want to generate a string session for:")
        print("  [1] Pyrogram (Official v2)")
        print("  [2] Pyrofork (Recommended Pyrogram fork)")
        print("  [3] Telethon")
        print("  [4] Exit")
        
        choice = input("\nEnter your choice [1-4]: ").strip()

        if choice == "1":
            success = generate_pyrogram_or_pyrofork(framework_name="Pyrogram")
            if success:
                break
        elif choice == "2":
            success = generate_pyrogram_or_pyrofork(framework_name="Pyrofork")
            if success:
                break
        elif choice == "3":
            success = generate_telethon()
            if success:
                break
        elif choice == "4":
            print("\n👋 Exiting. Have a great day!\n")
            sys.exit(0)
        else:
            print("\n⚠️ Invalid selection! Please enter 1, 2, 3, or 4.\n")
            continue

        retry = input("Would you like to try again? (y/n): ").strip().lower()
        if retry not in ("y", "yes"):
            print("\n👋 Exiting.\n")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Process cancelled by user. Exiting.\n")
        sys.exit(0)
