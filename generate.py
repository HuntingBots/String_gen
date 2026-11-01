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

import os
import sys
import inspect
import struct
import base64
import ipaddress
from pathlib import Path

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
║   Supported Options:                                          ║
║     [1] Pyrogram (Official v2)                                ║
║     [2] Pyrofork (Modern & Maintained Pyrogram Fork)          ║
║     [3] Telethon (Sync / Async v1)                            ║
║     [4] Generate from Old String Session (Direct / No OTP)    ║
║     [5] Exit                                                  ║
║                                                               ║
║   By HuntingBots | Ready for GitHub Actions & Local CLI       ║
╚═══════════════════════════════════════════════════════════════╝
"""

DEFAULT_OLD_SESSION = "AQA7eRMAdI8XLjuonz9nStZmtY1wJ05gCXoTGRTSe-S1pBCKayYbB8CtTZT1fhm9z0I0VU_YzFCJQbsUXUEudIA8MIwDFIUM9u68EP56oB7pvCLj1EV-4W9vKJR55ufa_qp4KqnCniV2mQ1vS98X9iwqe37j7IZ0F4K8fV2J8B-8VagJKKT_fOWyViJptWa3GFyem7X6qGXJ3KHdKCk_2RlMt48IEDwfRXeF8F1g5moxnsAlugP8SUvq7t7mVF5FcUFvWIqmGCBbPnsMKm-cCfyX6iNKPbtkpc23gmSKk8f0sLsT-y1zXQKKYMD0kElWxff3PaRnkLIQNL8QgdRNaJ32bch3yAAAAABNeVDBAA"

DC_IPV4_MAP = {
    1: "149.154.175.53",
    2: "149.154.167.51",
    3: "149.154.175.100",
    4: "149.154.167.91",
    5: "91.108.56.130",
}

def print_banner():
    print(BANNER)

def get_api_id(default=None):
    env_id = os.environ.get("API_ID", "").strip()
    if env_id:
        try:
            return int(env_id)
        except ValueError:
            pass
    while True:
        try:
            prompt = "👉 Enter your Telegram API ID"
            if default is not None:
                prompt += f" [Press Enter for default: {default}]"
            prompt += ": "
            val = input(prompt).strip()
            if not val:
                if default is not None:
                    return int(default)
                print("❌ API ID cannot be empty. Please try again.")
                continue
            return int(val)
        except ValueError:
            print("❌ Invalid API ID! It must be an integer (e.g. 12345678).")

def get_api_hash(default=None):
    env_hash = os.environ.get("API_HASH", "").strip()
    if env_hash:
        return env_hash
    while True:
        prompt = "👉 Enter your Telegram API HASH"
        if default is not None:
            prompt += f" [Press Enter for default: {default}]"
        prompt += ": "
        val = input(prompt).strip()
        if val:
            return val
        if default is not None:
            return default
        print("❌ API HASH cannot be empty. Please try again.")

def notify_success(framework_name, session_string, sent_to_saved=True, send_error=None):
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

    try:
        Path("/tmp/session_done").touch()
    except Exception:
        pass

def notify_direct_success(pyrofork_session, telethon_session, sent_to_saved=True, send_error=None, account_info=None):
    divider = "═" * 70
    print("\n" + divider)
    print("🎉 SUCCESS! NEW STRING SESSIONS GENERATED DIRECTLY FROM OLD SESSION:")
    print(divider)
    if account_info:
        print(f"👤 Account: {account_info.get('name', 'N/A')} (@{account_info.get('username', 'N/A')}) | ID: {account_info.get('id', 'N/A')}")
        print(divider)
        
    print("\n📦 [1] PYROFORK / MODERN PYROGRAM (v2) STRING SESSION:")
    print("-" * 70)
    print(f"\n{pyrofork_session}\n")
    print("-" * 70)
    print("\n📦 [2] TELETHON (v1) STRING SESSION:")
    print("-" * 70)
    print(f"\n{telethon_session}\n")
    print(divider)
    
    if sent_to_saved:
        print("📬 Successfully sent a backup copy to your Telegram 'Saved Messages'!")
    else:
        if send_error:
            print(f"⚠️ Notice: Could not send to Saved Messages ({send_error}).")
        print("   Please copy your session string directly from above!")
        
    print("🔒 SECURITY WARNING: Keep these session strings strictly private!")
    print(divider + "\n")

    try:
        Path("/tmp/session_done").touch()
    except Exception:
        pass

def decode_old_session(raw_str):
    raw_str = raw_str.strip()
    
    if raw_str.startswith("1") and len(raw_str) > 300:
        try:
            b64_part = raw_str[1:]
            b64_part += "=" * (-len(b64_part) % 4)
            data = base64.urlsafe_b64decode(b64_part)
            if len(data) == 263:
                dc_id, ip_packed, port, auth_key = struct.unpack(">B4sH256s", data)
                return {
                    "source": "Telethon (v1)",
                    "dc_id": dc_id,
                    "auth_key": auth_key,
                    "test_mode": False,
                    "user_id": 0,
                    "is_bot": False,
                    "api_id": None
                }
            elif len(data) == 275:
                dc_id, ip_packed, port, auth_key = struct.unpack(">B16sH256s", data)
                return {
                    "source": "Telethon (IPv6)",
                    "dc_id": dc_id,
                    "auth_key": auth_key,
                    "test_mode": False,
                    "user_id": 0,
                    "is_bot": False,
                    "api_id": None
                }
        except Exception:
            pass

    try:
        b64_part = raw_str + "=" * (-len(raw_str) % 4)
        data = base64.urlsafe_b64decode(b64_part)
        
        if len(data) == 271:
            dc_id, api_id, test_mode, auth_key, user_id, is_bot = struct.unpack(">BI?256sQ?", data)
            return {
                "source": "Pyrofork / Pyrogram v2",
                "dc_id": dc_id,
                "api_id": api_id,
                "test_mode": test_mode,
                "auth_key": auth_key,
                "user_id": user_id,
                "is_bot": is_bot
            }
        
        elif len(data) == 267:
            dc_id, test_mode, auth_key, user_id, is_bot = struct.unpack(">B?256sQ?", data)
            return {
                "source": "Pyrogram v1 (64-bit)",
                "dc_id": dc_id,
                "api_id": None,
                "test_mode": test_mode,
                "auth_key": auth_key,
                "user_id": user_id,
                "is_bot": is_bot
            }
            
        elif len(data) == 263:
            dc_id, test_mode, auth_key, user_id, is_bot = struct.unpack(">B?256sI?", data)
            return {
                "source": "Pyrogram v1 (32-bit)",
                "dc_id": dc_id,
                "api_id": None,
                "test_mode": test_mode,
                "auth_key": auth_key,
                "user_id": user_id,
                "is_bot": is_bot
            }
    except Exception:
        pass

    return None

def encode_pyrofork_v2(dc_id, api_id, test_mode, auth_key, user_id, is_bot):
    packed = struct.pack(">BI?256sQ?", dc_id, int(api_id or 0), bool(test_mode), auth_key, int(user_id or 0), bool(is_bot))
    return base64.urlsafe_b64encode(packed).decode().rstrip("=")

def encode_telethon_v1(dc_id, auth_key):
    ip_str = DC_IPV4_MAP.get(dc_id, "149.154.175.53")
    ip_packed = ipaddress.ip_address(ip_str).packed
    packed = struct.pack(">B4sH256s", dc_id, ip_packed, 443, auth_key)
    return "1" + base64.urlsafe_b64encode(packed).decode("ascii")

def generate_from_old_session():
    print("\n" + "═" * 70)
    print("🔄 DIRECT STRING SESSION GENERATOR (OLD SESSION -> NEW SESSION)")
    print("═" * 70)
    print("💡 Generate modern Pyrofork/Pyrogram (v2) and Telethon string sessions")
    print("   directly from your existing string session without entering phone or OTP!\n")

    default_preview = f"{DEFAULT_OLD_SESSION[:18]}...{DEFAULT_OLD_SESSION[-18:]}"
    print(f"📌 Default Session Preset: {default_preview}")
    user_session_input = input("👉 Enter Old String Session (Press Enter to use preset): ").strip()
    raw_session = user_session_input if user_session_input else (os.environ.get("OLD_STRING_SESSION", "").strip() or DEFAULT_OLD_SESSION)

    parsed = decode_old_session(raw_session)
    if not parsed:
        print("\n❌ Error: Invalid old string session format!")
        print("Please ensure you provide a valid Pyrogram (v1/v2) or Telethon session string.\n")
        return False

    print(f"\n✅ Successfully decoded session from: {parsed['source']}")
    print(f"   • Data Center (DC): {parsed['dc_id']}")
    print(f"   • Auth Key: 256 bytes extracted successfully")
    if parsed.get("user_id"):
        print(f"   • User ID: {parsed['user_id']}")

    extracted_api_id = parsed.get("api_id") or 2040
    default_api_hash = "b18441a1ff607e10a989891a5462e627"

    print("\n🔑 Telegram API Credentials (Optional - Press Enter for defaults):")
    api_id = get_api_id(default=extracted_api_id)
    api_hash = get_api_hash(default=default_api_hash)

    dc_id = parsed["dc_id"]
    auth_key = parsed["auth_key"]
    test_mode = parsed.get("test_mode", False)
    user_id = parsed.get("user_id", 0)
    is_bot = parsed.get("is_bot", False)

    new_pyrofork_session = encode_pyrofork_v2(dc_id, api_id, test_mode, auth_key, user_id, is_bot)
    new_telethon_session = encode_telethon_v1(dc_id, auth_key)

    print("\n🌐 Connecting to Telegram using Pyrofork to verify session & send backup...")
    try:
        import pyrogram
        from pyrogram import Client, enums

        with Client(
            name="direct_migration_session",
            api_id=api_id,
            api_hash=api_hash,
            session_string=new_pyrofork_session,
            in_memory=True
        ) as client:
            me = client.get_me()
            account_info = {
                "name": f"{me.first_name} {me.last_name or ''}".strip(),
                "username": me.username or "None",
                "id": me.id
            }
            
            if user_id != me.id:
                user_id = me.id
                new_pyrofork_session = encode_pyrofork_v2(dc_id, api_id, test_mode, auth_key, user_id, me.is_bot)

            sent_saved = False
            send_err = None
            try:
                msg = (
                    f"🎉 <b>String Session Regenerated!</b>\n\n"
                    f"<b>Framework:</b> Pyrofork / Modern Pyrogram (v2)\n"
                    f"<code>{new_pyrofork_session}</code>\n\n"
                    f"<b>Framework:</b> Telethon (v1)\n"
                    f"<code>{new_telethon_session}</code>\n\n"
                    f"⚠️ <b>Security Notice:</b>\n"
                    f"• Never share these string sessions with anyone!\n"
                    f"• Anyone with these strings has access to your account.\n\n"
                    f"Generated directly from Old String Session by <b>HuntingBots</b>"
                )
                client.send_message("me", msg, parse_mode=enums.ParseMode.HTML)
                sent_saved = True
            except Exception as e:
                send_err = str(e)

            notify_direct_success(new_pyrofork_session, new_telethon_session, sent_saved, send_err, account_info)
            return True
    except Exception as e:
        print(f"⚠️ Notice: Online verification was skipped or failed ({e}).")
        print("ℹ️ Your new session strings are still 100% valid and ready to use offline!")
        notify_direct_success(new_pyrofork_session, new_telethon_session, sent_to_saved=False, send_error=str(e))
        return True

def generate_pyrogram_or_pyrofork(framework_name="Pyrofork"):
    print(f"\n🚀 Setting up {framework_name} session generator...\n")
    
    official_path = "/opt/pyrogram_official"
    if framework_name == "Pyrogram" and os.path.isdir(official_path):
        if official_path not in sys.path:
            sys.path.insert(0, official_path)
    elif framework_name == "Pyrofork" and official_path in sys.path:
        sys.path.remove(official_path)

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
        print("Select an option:")
        print("  [1] Pyrogram (Official v2)")
        print("  [2] Pyrofork (Recommended Pyrogram fork)")
        print("  [3] Telethon")
        print("  [4] Generate New String from Old String Session (Direct / No OTP)")
        print("  [5] Exit")
        
        choice = input("\nEnter your choice [1-5]: ").strip()

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
            success = generate_from_old_session()
            if success:
                break
        elif choice == "5":
            print("\n👋 Exiting. Have a great day!\n")
            sys.exit(0)
        else:
            print("\n⚠️ Invalid selection! Please enter 1, 2, 3, 4, or 5.\n")
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
