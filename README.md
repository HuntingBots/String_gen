# ⚡ Telegram String Session Generator

A fast, modern, and secure Telegram **String Session Generator** supporting **Pyrogram (v2)**, **Pyrofork**, and **Telethon**.

You can run this generator directly via **GitHub Actions** (directly from your browser without installing anything!) or locally on **Linux, macOS, Windows, VPS, and Termux**.

---

## ✨ Features

- 🚀 **Multi-Framework & Direct Migration Support:**
  - **Pyrogram** (Official v2)
  - **Pyrofork** (Modern, actively maintained Pyrogram fork)
  - **Telethon** (Telethon v1)
  - **Direct Old -> New Session Generation (Option 4)**: Convert/Regenerate directly from an old string session without phone number or OTP!
- 🌐 **GitHub Actions Ready:**
  - **Web Terminal:** Open an interactive shell directly in your web browser (supports mobile & desktop) via Cloudflare Quick Tunnel — **no SSH keys needed!**
  - **SSH Terminal:** Connect via SSH using Upterm if you prefer local terminal debugging.
- 📬 **Auto-Backup to Saved Messages:** The generated session string is automatically sent to your Telegram **"Saved Messages"** (`me`).
- 🖥️ **Console Display:** The session string is also printed in the terminal so you can copy it immediately.
- 🛡️ **Safe & Secure:** Sessions are generated in-memory; credentials and strings are never stored or logged anywhere.

---

## 🚀 How to Run via GitHub Actions (No Setup Required)

You don't need to install Python or clone the repository to your device. You can run it directly on GitHub runners!

### Step 1: Fork or Open this Repository
1. Fork or open this repository in your GitHub account.

### Step 2: Trigger the Workflow
1. Go to the **Actions** tab in your repository.
2. In the left sidebar, click on **Telegram String Session Generator**.
3. Click the **Run workflow** dropdown on the right:
   - **Connection Method:** Choose `web_terminal` *(Recommended - works right in your browser!)* or `ssh_upterm` (SSH).
   - *(Optional)* You can prefill your `API_ID` and `API_HASH`, or leave them blank to enter them interactively.
4. Click the green **Run workflow** button.

### Step 3: Open the Terminal & Generate Session
1. Click into the active workflow run.
2. In the **Summary** tab (or in the job logs), you will see:
   - **🌐 Web Terminal URL:** `https://xxxx.trycloudflare.com`
   - **👤 Username:** `admin`
   - **🔑 Password:** `<generated_password>`
3. Click the URL to open the terminal in your browser.
4. Log in with the username and password provided.
5. Follow the on-screen prompts:
   - Choose your option: `1` for Pyrogram, `2` for Pyrofork, `3` for Telethon, or `4` to generate directly from an old string session without OTP.
   - Enter your **API ID** and **API HASH** (obtainable from [my.telegram.org](https://my.telegram.org)).
   - Enter your **phone number** with country code (e.g. `+919876543210`).
   - Enter the **OTP login code** sent to your Telegram app.
   - Enter your **2FA Password** (if enabled).
6. 🎉 Done! Your session string will be printed on screen and sent directly to your Telegram **Saved Messages**!
7. Close the browser tab and cancel the workflow run.

---

## 💻 How to Run Locally / VPS / Termux

### Prerequisites
- Python 3.9 or higher
- Git

### 1. Clone the repository
```bash
git clone https://github.com/HuntingBots/String_gen.git
cd String_gen
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

*(Optional: If you want official Pyrogram alongside Pyrofork, install Pyrogram in a separate directory or venv)*

### 3. Run the script
```bash
python3 main.py
```
*(You can also run `python3 generate.py` or `python3 string.py`)*

---

## 🔑 How to Get API_ID and API_HASH

1. Visit [my.telegram.org](https://my.telegram.org) and log in with your Telegram account.
2. Click on **API development tools**.
3. Fill in the app title and short name.
4. Copy your **API_ID** and **API_HASH**.

---

## 🔒 Security Notice

> [!WARNING]
> Your String Session gives full access to your Telegram account.
> - **NEVER** share your session string with anyone.
> - **NEVER** commit your session string to GitHub or any public space.
> - If you suspect your session string was compromised, immediately terminate active sessions via Telegram app: **Settings > Devices > Terminate all other sessions**.

---

## 👨‍💻 Author & Credits

- Maintained by **[@HuntingBots](https://github.com/HuntingBots)** for **MatrixVcBot**
- Powered by [Telethon](https://github.com/LonamiWebs/Telethon) and [Pyrofork](https://github.com/Mayuri-Chan/pyrofork)

---

## 📄 License

```text
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
```
