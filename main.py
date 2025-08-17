import os
import re
import sys
import m3u8
import json
import time
import pytz
import httpx
import asyncio
import requests
import subprocess
import urllib
import urllib.parse
import yt_dlp
import tgcrypto
import cloudscraper
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from base64 import b64encode, b64decode
from logs import logging
from bs4 import BeautifulSoup
import saini as helper
from utils import progress_bar
from vars import API_ID, API_HASH, BOT_TOKEN
from aiohttp import ClientSession
from subprocess import getstatusoutput
from pytube import YouTube
from aiohttp import web
import random
from pyromod import listen
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import aiohttp
import aiofiles
import zipfile
import shutil
import ffmpeg
import jwt

# Initialize the bot
API_HASH = "0c9262b17a45cb67b447ffd8e38f1e4d"
API_ID = "22274497"
bot_token = os.getenv("BOT_TOKEN", "")  # Default to empty string if not set
MR = os.getenv("MR", "DefaultMR")       # Default to "DefaultMR" if not set
TOKEN_CP = os.getenv("TOKEN_CP", "")    # Default to empty string if not set
user_id = os.getenv("USER_ID", "")      # Default to empty string if not set
os.environ["TOKEN_CP"] = TOKEN_CP       # Ensure environment is updated with initial value
os.environ["USER_ID"] = user_id         # Ensure environment is updated with initial value

if not bot_token:
    logging.error("BOT_TOKEN not found in environment. Please set it in .env or environment variables.")
    sys.exit(1)

bot = Client("bot",
             api_id=API_ID,
             api_hash=API_HASH,
             bot_token=bot_token)

owner_id = [1003575883]
auth_users = [1003575883]
photo1 = 'https://envs.sh/PQ_.jpg'
getstatusoutput(f"wget {photo1} -O 'photo.jpg'")
photo = "photo.jpg"

cookies_file_path = os.getenv("cookies_file_path", "youtube_cookies.txt")
api_url = "http://master-api-v3.vercel.app/"
api_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNzkxOTMzNDE5NSIsInRnX3VzZXJuYW1lIjoi4p61IFtvZmZsaW5lXSIsImlhdCI6MTczODY5MjA3N30.SXzZ1MZcvMp5sGESj0hBKSghhxJ3k1GTWoBUbivUe1I"
adda_token = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJkcGthNTQ3MEBnbWFpbC5jb20iLCJhdWQiOiIxNzg2OTYwNSIsImlhdCI6MTc0NDk0NDQ2NCwiaXNzIjoiYWRkYTI0Ny5jb20iLCJuYW1lIjoiZHBrYSIsImVtYWlsIjoiZHBrYTU0NzBAZ21haWwuY29tIiwicGhvbmUiOiI3MzUyNDA0MTc2IiwidXNlcklkIjoiYWRkYS52MS41NzMyNmRmODVkZDkxZDRiNDkxN2FiZDExN2IwN2ZjOCIsImxvZ2luQXBpVmVyc2lvbiI6MX0.0QOuYFMkCEdVmwMVIPeETa6Kxr70zEslWOIAfC_ylhbku76nDcaBoNVvqN4HivWNwlyT0jkUKjWxZ8AbdorMLg"
photologo = 'https://tinypic.host/images/2025/02/07/DeWatermark.ai_1738952933236-1.png'
photoyt = 'https://tinypic.host/images/2025/03/18/YouTube-Logo.wine.png'
photocp = 'https://tinypic.host/images/2025/03/28/IMG_20250328_133126.jpg'
photozip = 'https://envs.sh/cD_.jpg'

# Romantic Inline keyboard for start command
BUTTONSCONTACT = InlineKeyboardMarkup([[InlineKeyboardButton(text="💖 Contact my Love", url="https://t.me/saini_contact_bot")]])

keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="💌 Contact me, my heart", url="https://t.me/telegram"),
            InlineKeyboardButton(text="💫 Need help? I'm here for you", url="https://t.me/username"),
        ],
    ]
)

# Image URLs for the random image feature
image_urls = [
    "https://graph.org/file/afd34ac822b2381e0b990-ea8f7cf121fb415062.jpg",
    "https://graph.org/file/f9b1af4cc9d226fa73cec-202a079f204f580f13.jpg",
    "https://graph.org/file/485300967efc7e54e2963-fad7066368b5698aff.jpg",
    "https://graph.org/file/147af465fe7efeeae7369-e618ced441552b055c.jpg",
    "https://graph.org/file/36da365f0be74530e977c-30aafab98bce6c9be6.jpg",
    "https://graph.org/file/6d872ce712164c95131d2-ee0bd11966d776bb6e.jpg",
    "https://graph.org/file/b4b3fa51cbf569346c072-09ae1deb4da24abc11.jpg",
    "https://graph.org/file/a4fe1defbd6e4f1cd069c-f70e92963ea47ad386.jpg",
    "https://graph.org/file/3261f0f6b78c8009da698-ed433d7f6046a9f03e.jpg",
    "https://graph.org/file/72ae00b1730a261efa4bf-13d0693da6ba9f8ced.jpg",
    "https://graph.org/file/01c7c4d12740d8d9dc431-756bf607004488bee7.jpg",
    "https://graph.org/file/f8e2742fc8a71d3fb1423-7f52a462d0c65ae2f0.jpg",
    "https://graph.org/file/350587d29aeeb8b6d0cc6-e3fb46f75daf63c245.jpg",
    "https://graph.org/file/636fd52bf4bb5fe270053-a8bb98c52205d28b6a.jpg",
    "https://graph.org/file/38245d816276e9ac6bb73-998f37e0320fc95ff4.jpg",
    "https://graph.org/file/f7f1c6cb463c68cbe30fe-6f329b6f696d11df3b.jpg",
    "https://graph.org/file/a67b484a8bb87ae09d979-3995a7aa25e91a2e55.jpg",
    "https://graph.org/file/ae22e8d57b393ed24aa44-7337a24c71983fbf9f.jpg",
    "https://graph.org/file/18829ff4b5e9d36c4dbb5-18179eb5a200a42df9.jpg",
]

async def update_token_cp():
    global TOKEN_CP, user_id
    while True:
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                print(f"Fetching new token at {time.strftime('%H:%M:%S', time.localtime())}...")
                response = await client.get("https://jaatcptokenapi.vercel.app/api/jaatcptokengen")
                print(f"API response status: {response.status_code}, text: {response.text[:100]}...")
                max_retries = 3
                for attempt in range(max_retries):
                    if response.status_code == 200:
                        new_token = response.text.strip()
                        if new_token:
                            TOKEN_CP = new_token
                            os.environ["TOKEN_CP"] = new_token
                            try:
                                user_id = jwt.decode(new_token, options={"verify_signature": False})["id"]
                                os.environ["USER_ID"] = str(user_id)
                                print(f"Decoded user_id from token: {user_id}")
                            except Exception as e:
                                print(f"Error decoding user_id from token: {str(e)}")
                                user_id = "decode_failed"  # Fallback value
                                os.environ["USER_ID"] = user_id
                            # Update .env file
                            env_file_path = '.env'
                            env_content = ""
                            if os.path.exists(env_file_path):
                                with open(env_file_path, 'r') as file:
                                    env_content = file.read()
                            token_regex = r'^TOKEN_CP=.*$'
                            user_id_regex = r'^USER_ID=.*$'
                            if re.search(token_regex, env_content, re.MULTILINE):
                                env_content = re.sub(token_regex, f'TOKEN_CP={new_token}', env_content, flags=re.MULTILINE)
                            else:
                                env_content += f'\nTOKEN_CP={new_token}'
                            if re.search(user_id_regex, env_content, re.MULTILINE):
                                env_content = re.sub(user_id_regex, f'USER_ID={user_id}', env_content, flags=re.MULTILINE)
                            else:
                                env_content += f'\nUSER_ID={user_id}'
                            with open(env_file_path, 'w') as file:
                                file.write(env_content.strip())  # Remove trailing whitespace
                            print(f"TOKEN_CP and USER_ID updated to: {new_token[:50]}... and {user_id}")
                            logging.info(f"TOKEN_CP and USER_ID updated to: {new_token[:50]}... and {user_id}")
                            break
                        else:
                            print(f"Attempt {attempt + 1}/{max_retries}: Empty token received, retrying...")
                            logging.warning(f"Attempt {attempt + 1}/{max_retries}: Empty token received, retrying...")
                            await asyncio.sleep(5)
                            if attempt < max_retries - 1:
                                response = await client.get("https://jaatcptokenapi.vercel.app/api/jaatcptokengen")
                            else:
                                print("All retries failed: Empty token after max attempts")
                                logging.error("All retries failed: Empty token after max attempts")
                    else:
                        print(f"Attempt {attempt + 1}/{max_retries} failed: HTTP {response.status_code} - {response.text}")
                        logging.error(f"Attempt {attempt + 1}/{max_retries} failed: HTTP {response.status_code} - {response.text}")
                        if attempt < max_retries - 1:
                            await asyncio.sleep(5)
                            response = await client.get("https://jaatcptokenapi.vercel.app/api/jaatcptokengen")
                        else:
                            print("All retries failed: HTTP error after max attempts")
                            logging.error("All retries failed: HTTP error after max attempts")
        except httpx.RequestError as e:
            print(f"Network error fetching token: {str(e)}")
            logging.error(f"Network error fetching token: {str(e)}")
        except Exception as e:
            print(f"Unexpected error updating TOKEN_CP: {str(e)}")
            logging.error(f"Unexpected error updating TOKEN_CP: {str(e)}")
        await asyncio.sleep(120)  # Wait 2 minutes (120 seconds) before next update

# Start the token update task after bot startup
@bot.on_message(filters.command(["startx"]))
async def startx_command(bot: Client, message: Message):
    random_image_url = random.choice(image_urls)
    caption = (
        "**➦hᥱᥣᥣo bᥲbყ😉❤️**\n\n"
        "☛ **ι ᥲm txt to vιdᥱo υρᥣoᥲdᥱr bot.**\n\n"
        "☛ **for υsᥱ mᥱ sᥱᥒd /DRM**.\n\n"
        "☛ **for gυιdᥱ sᥱᥒd /help**."
    )
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=random_image_url,
        caption=caption,
        reply_markup=keyboard
    )
    # Start the token update task only once
    if not hasattr(bot, "token_update_started"):
        try:
            bot.loop.create_task(update_token_cp())
            logging.info("Token update task started on bot startup")
            bot.token_update_started = True  # Flag to prevent multiple tasks
        except Exception as e:
            logging.error(f"Error starting token update task on startup: {str(e)}")
            await message.reply_text(f"Error starting token update task: {str(e)}")

@bot.on_message(filters.command("mfile") & filters.private)
async def get_main_file_handler(client: Client, m: Message):
    try:
        await client.send_document(
            chat_id=m.chat.id,
            document=m_file_path,
            caption="Here is the `main.py` file."
        )
    except Exception as e:
        await m.reply_text(f"⚠️ An error occurred: {str(e)}")

@bot.on_message(filters.command("cookies") & filters.private)
async def cookies_handler(client: Client, m: Message):
    await m.reply_text(
        "Please upload the cookies file (.txt format).",
        quote=True
    )
    try:
        input_message: Message = await client.listen(m.chat.id)
        if not input_message.document or not input_message.document.file_name.endswith(".txt"):
            await m.reply_text("Invalid file type. Please upload a .txt file.")
            return
        downloaded_path = await input_message.download()
        with open(downloaded_path, "r") as uploaded_file:
            cookies_content = uploaded_file.read()
        with open(cookies_file_path, "w") as target_file:
            target_file.write(cookies_content)
        await input_message.reply_text(
            "✅ Cookies updated successfully.\n📂 Saved in `youtube_cookies.txt`."
        )
    except Exception as e:
        await m.reply_text(f"⚠️ An error occurred: {str(e)}")

@bot.on_message(filters.command(["king"]))
async def text_to_txt(client, message: Message):
    user_id = str(message.from_user.id)
    editable = await message.reply_text(f"<blockquote>Welcome to the Text to .txt Converter!\nSend the **text** for convert into a `.txt` file.</blockquote>")
    input_message: Message = await bot.listen(message.chat.id)
    if not input_message.text:
        await message.reply_text("🚨 **error**: Send valid text data")
        return
    text_data = input_message.text.strip()
    await input_message.delete()
    await editable.edit("**🔄 Send file name or send /d for filename**")
    inputn: Message = await bot.listen(message.chat.id)
    raw_textn = inputn.text
    await inputn.delete()
    await editable.delete()
    if raw_textn == '/d':
        custom_file_name = 'txt_file'
    else:
        custom_file_name = raw_textn
    txt_file = os.path.join("downloads", f'{custom_file_name}.txt')
    os.makedirs(os.path.dirname(txt_file), exist_ok=True)
    with open(txt_file, 'w') as f:
        f.write(text_data)
    await message.reply_document(document=txt_file, caption=f"`{custom_file_name}.txt`\n\nYou can now download your content! 📥")
    os.remove(txt_file)

UPLOAD_FOLDER = '/path/to/upload/folder'
EDITED_FILE_PATH = '/path/to/save/edited_output.txt'

@bot.on_message(filters.command(["y2t"]))
async def youtube_to_txt(client, message: Message):
    user_id = str(message.from_user.id)
    editable = await message.reply_text(
        f"Send YouTube Website/Playlist link for convert in .txt file"
    )
    input_message: Message = await bot.listen(message.chat.id)
    youtube_link = input_message.text.strip()
    await input_message.delete(True)
    await editable.delete(True)
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'skip_download': True,
        'force_generic_extractor': True,
        'forcejson': True,
        'cookies': 'youtube_cookies.txt'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            result = ydl.extract_info(youtube_link, download=False)
            if 'entries' in result:
                title = result.get('title', 'youtube_playlist')
            else:
                title = result.get('title', 'youtube_video')
        except yt_dlp.utils.DownloadError as e:
            await message.reply_text(
                f"<pre><code>🚨 Error occurred {str(e)}</code></pre>"
            )
            return
    videos = []
    if 'entries' in result:
        for entry in result['entries']:
            video_title = entry.get('title', 'No title')
            url = entry['url']
            videos.append(f"{video_title}: {url}")
    else:
        video_title = result.get('title', 'No title')
        url = result['url']
        videos.append(f"{video_title}: {url}")
    txt_file = os.path.join("downloads", f'{title}.txt')
    os.makedirs(os.path.dirname(txt_file), exist_ok=True)
    with open(txt_file, 'w') as f:
        f.write('\n'.join(videos))
    await message.reply_document(
        document=txt_file,
        caption=f'<a href="{youtube_link}">__**Click Here to Open Link**__</a>\n<pre><code>{title}.txt</code></pre>\n'
    )
    os.remove(txt_file)

m_file_path = "main.py"
@bot.on_message(filters.command("getcookies") & filters.private)
async def getcookies_handler(client: Client, m: Message):
    try:
        await client.send_document(
            chat_id=m.chat.id,
            document=cookies_file_path,
            caption="Here is the `youtube_cookies.txt` file."
        )
    except Exception as e:
        await m.reply_text(f"⚠️ An error occurred: {str(e)}")

@bot.on_message(filters.command("mfile") & filters.private)
async def getcookies_handler(client: Client, m: Message):
    try:
        await client.send_document(
            chat_id=m.chat.id,
            document=m_file_path,
            caption="Here is the `main.py` file."
        )
    except Exception as e:
        await m.reply_text(f"⚠️ An error occurred: {str(e)}")

@bot.on_message(filters.command(["stop"]))
async def restart_handler(_, m):
    await m.reply_text("**STOPPED BABY**", True)
    os.execl(sys.executable, sys.executable, *sys.argv)

@bot.on_message(filters.command(["start"]))
async def start_command(bot: Client, message: Message):
    random_image_url = random.choice(image_urls)
    caption = (
        "**➦hᥱᥣᥣo bᥲbყ😉❤️**\n\n"
        "☛ **ι ᥲm txt to vιdᥱo υρᥣoᥲdᥱr bot.**\n\n"
        "☛ **for υsᥱ mᥱ sᥱᥒd /DRM**.\n\n"
        "☛ **for gυιdᥱ sᥱᥒd /help**."
    )
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=random_image_url,
        caption=caption,
        reply_markup=keyboard
    )

@bot.on_message(filters.command(["id"]))
async def id_command(client, message: Message):
    chat_id = message.chat.id
    await message.reply_text(f"<blockquote>The ID of this chat id is:</blockquote>\n`{chat_id}`")

@bot.on_message(filters.private & filters.command(["info"]))
async def info(bot: Client, update: Message):
    text = (
        f"╭────────────────╮\n"
        f"│✨ **__Your Telegram Info__** ✨\n"
        f"├──────────────────\n"
        f"├🔹**Name:** `{update.from_user.first_name} {update.from_user.last_name if update.from_user.last_name else 'No last name'}`\n"
        f"├🔹**Username:** @{update.from_user.username}\n"
        f"├🔹**User ID:** `{update.from_user.id}`\n"
        f"├🔹**Profile Link:** {update.from_user.mention}\n"
        f"│💖 **In a world full of billions, I’m lucky to have you here.** 💫\n"
        f"│🌙 **Your presence makes everything brighter, just like the stars.** 🌟\n"
        f"╰────────────────╯"
    )
    await update.reply_text(
        text=text,
        disable_web_page_preview=True,
        reply_markup=BUTTONSCONTACT
    )

@bot.on_message(filters.command(["help"]))
async def txt_handler(client: Client, m: Message):
    await bot.send_message(m.chat.id, text=(
        f"🎉 **Congratulations, my love!** You're now using **king 🖤**! 🎉\n\n"
        f"🔹 **Send me a link** to extract the content you desire 🔗\n\n"
        f"❓ **Got questions?** I'm always here for you, darling!\n"
        f"📱 **Reach out anytime:** [**rajasthni king**](https://t.me/username)\n\n"
        f"✨ <b> Enjoy the magic, and stay tuned for more updates, my love! </b> ✨"
    ))

@bot.on_message(filters.command(["logs"]))
async def send_logs(client: Client, m: Message):
    try:
        with open("logs.txt", "rb") as file:
            sent = await m.reply_text("**📤 Sending you ....**")
            await m.reply_document(document=file)
            await sent.delete()
    except Exception as e:
        await m.reply_text(f"Error sending logs: {e}")

@bot.on_message(filters.command("changetoken") & filters.private)
async def changetoken_handler(client: Client, message: Message):
    args = message.text.split(" ", 1)
    if len(args) < 2:
        await message.reply_text("⚠️ Please provide the new token! Usage: /changetoken <new_token>")
        return
    new_token = args[1].strip()
    try:
        env_file_path = '.env'
        env_content = ""
        if os.path.exists(env_file_path):
            with open(env_file_path, 'r') as file:
                env_content = file.read()
        token_regex = r'^TOKEN_CP=.*$'
        if re.search(token_regex, env_content, re.MULTILINE):
            env_content = re.sub(token_regex, f'TOKEN_CP={new_token}', env_content, flags=re.MULTILINE)
        else:
            env_content += f'\nTOKEN_CP={new_token}'
        with open(env_file_path, 'w') as file:
            file.write(env_content)
        os.environ['TOKEN_CP'] = new_token
        await message.reply_text("✅ TOKEN_CP updated successfully! Bot may need a restart for changes to take effect.")
    except Exception as e:
        await message.reply_text(f"⚠️ Error updating token: {str(e)}")

@bot.on_message(filters.command(["drm"]))
async def txt_handler(bot: Client, m: Message):
    editable = await m.reply_text(f"**⚡𝗦𝖾𝗇𝖽 𝗧𝗑𝗍 𝗙𝗂𝗅𝖾⚡**")
    input: Message = await bot.listen(editable.chat.id)
    y = await input.download()
    await input.delete(True)
    file_name, ext = os.path.splitext(os.path.basename(y))

    if file_name.endswith("_helper"):
        x = decrypt_file_txt(y)  # Ensure this function is defined in saini.py
        await input.delete(True)
    else:
        x = y

    path = f"./downloads/{m.chat.id}"
    pdf_count = 0
    img_count = 0
    zip_count = 0
    other_count = 0

    try:
        with open(x, "r") as f:
            content = f.read()
        content = content.split("\n")
        links = []
        for i in content:
            if "://" in i:
                url = i.split("://", 1)[1]
                links.append(i.split("://", 1))
                if ".pdf" in url:
                    pdf_count += 1
                elif url.endswith((".png", ".jpeg", ".jpg")):
                    img_count += 1
                elif ".zip" in url:
                    zip_count += 1
                else:
                    other_count += 1
        os.remove(x)
    except:
        await m.reply_text("<pre><code>🔹Invalid file input.</code></pre>")
        os.remove(x)
        return

    await editable.edit(f"`🔹Total 🔗 links found are {len(links)}\n\n🔹Img : {img_count}  🔹PDF : {pdf_count}\n🔹ZIP : {zip_count}  🔹Other : {other_count}\n\n🔹Send From where you want to download.`")
    input0: Message = await bot.listen(editable.chat.id)
    raw_text = input0.text
    await input0.delete(True)

    b_name = file_name.replace('_', ' ')
    quality = "720p"
    res = "1280x720"
    CR = '{MR}'
    

    await editable.delete()
    await m.reply_text(f"__**🎯Target Batch : {b_name}**__")

    failed_count = 0
    count = int(raw_text)
    arg = int(raw_text)
    try:
        for i in range(arg-1, len(links)):
            Vxy = links[i][1].replace("file/d/", "uc?export=download&id=").replace("www.youtube-nocookie.com/embed", "youtu.be").replace("?modestbranding=1", "").replace("/view?usp=sharing", "")
            url = "https://" + Vxy
            link0 = "https://" + Vxy

            name1 = links[i][0].replace("(", "[").replace(")", "]").replace("_", "").replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").replace("https", "").replace("http", "").strip()
            name = f'{name1[:60]}'

            if "visionias" in url:
                async with ClientSession() as session:
                    async with session.get(url, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Pragma': 'no-cache', 'Referer': 'http://www.visionias.in/', 'Sec-Fetch-Dest': 'iframe', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'cross-site', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Linux; Android 12; RMX2121) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36', 'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"', 'sec-ch-ua-mobile': '?1', 'sec-ch-ua-platform': '"Android"',}) as resp:
                        text = await resp.text()
                        url = re.search(r"(https://.*?playlist.m3u8.*?)\"", text).group(1)

            if "acecwply" in url:
                cmd = f'yt-dlp -o "{name}.%(ext)s" -f "bestvideo[height<=720]+bestaudio" --hls-prefer-ffmpeg --no-keep-video --remux-video mkv --no-warning "{url}"'

            elif "edge.api.brightcove.com" in url:
                new_bcov_token = "bcov_auth=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3NDc0NzY5MzEsImNvbiI6eyJpc0FkbWluIjpmYWxzZSwiYXVzZXIiOiJVMFZ6TkdGU2NuQlZjR3h5TkZwV09FYzBURGxOZHowOSIsImlkIjoiUkZCSFpGUmhObWhEZFhZMFNUSTFhM0FyU1RVemR6MDkiLCJmaXJzdF9uYW1lIjoiTndwbGFWcFNOVXRUTm1sU1JFdGpLelpuYm1SQ1FUMDkiLCJlbWFpbCI6IlkxaHdNelZVUTFjeE1IQmpTMmhDYVdWYVZuRkZlazVwWVRKbU4zbGFkRGhJV1VWbVNHRktVV3BoY3owPSIsInBob25lIjoiZWtZdk1rUmxURVpEZURSdlUyaHpZbGRpV0drM2R6MDkiLCJhdmF0YXIiOiJLM1ZzY1M4elMwcDBRbmxrYms4M1JEbHZla05pVVQwOSIsInJlZmVycmFsX2NvZGUiOiJhemhKSzNwbFZHeDFXa2xKYWxWTFdscEpiMEphUVQwOSIsImRldmljZV90eXBlIjoiYW5kcm9pZCIsImRldmljZV92ZXJzaW9uIjoiUShBbmRyb2lkIDEwLjApIiwiZGV2aWNlX21vZGVsIjoiWGlhb21pIE0yMDA3SjIwQ0kiLCJyZW1vdGVfYWRkciI6IjE4LjIxMy4xMTUuMTA1In19.hUp4gzFCXKUg6jhosLP0YXkHHAvU7K9uwXT22k02UALahUtcRI_EwVnVaheS54n-GUBCvFjQokhqsNfWyNTiljbx_hRAA19X67qzTBU8qdJuNxfhgKloGpR9aB7qybkqN4QzOBliSb7JNPAICQ_TtfUIqH1N5DCnLldvBBLoayejefCTTe012VHHkTCnsp3HnypcgMFu5Tsaw-Gvzz80e6RwlWVgivU5s2h9OtMgbrKMVbvnsvnRQS08zbu0Z7-4ZN_HzfoQ9SGliXqlpxJKVZCCBwHM5UVUTSqMNamHv-YnsjPVfAJoOTzkRY0Ka_AU5SWSXJhpPqh7fHGWtT8KYw"
                if "bcov_auth=" in url:
                    url = url.split("bcov_auth=")[0].rstrip("?&")
                separator = "&" if "?" in url else "?"
                url = f"{url}{separator}{new_bcov_token}"

            elif "/khansirvod4" in url and "akamaized" in url:
                url = url.replace(url.split("/")[-1], "720+.m3u8")

            elif "https://cpvod.testbook.com/" in url or "classplusapp.com/drm/" in url:
                url = url.replace("https://cpvod.testbook.com/", "https://media-cdn.classplusapp.com/drm/")
                api_url = f"https://cpapi-rjbs-1l0p.onrender.com/extract_keys?url={url}@bots_updatee&user_id={USER_ID}"
                mpd, keys = helper.get_mps_and_keys(api_url)
                url = mpd
                keys_string = " ".join([f"--key {key}" for key in keys])

            elif "classplusapp.com/drm/" in url:
                api_url = f"https://cpapi-rjbs-1l0p.onrender.com/extract_keys?url={url}@bots_updatee&user_id={USER_ID}"
                mpd, keys = helper.get_mps_and_keys(api_url)
                url = mpd
                keys_string = " ".join([f"--key {key}" for key in keys])

            elif any(domain in url for domain in [
                'videos.classplusapp.com',
                'tencdn.classplusapp.com',
                'webvideos.classplusapp.com',
                'media-cdn.classplusapp.com',
                'media-cdn-alisg.classplusapp.com',
                'media-cdn-a.classplusapp.com'
            ]):
                try:
                    headers = {
                        'x-access-token': TOKEN_CP,
                        'accept-language': 'en',
                        'api-version': '52',
                        'app-version': '1.4.65.3',
                        'build-number': '35',
                        'connection': 'Keep-Alive',
                        'content-type': 'application/json',
                        'device-details': 'Mobile-Android',
                        'device-id': '39F093FF35F201D9',
                        'region': 'IN',
                        'user-agent': 'Mobile-Android',
                        'accept-encoding': 'gzip'
                    }
                    if "media-cdn" in url:
                        headers['X-CDN-Tag'] = 'empty'
                    api = f'https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={url}'
                    response = requests.get(api, headers=headers, timeout=10)
                    if response.status_code == 200:
                        signed_url = response.json().get("url")
                        if signed_url:
                            url = signed_url
                        else:
                            url += "  [❌ SIGNED URL FAILED: Empty response]"
                    else:
                        url += f"  [❌ SIGNED URL FAILED: HTTP {response.status_code}]"
                except requests.exceptions.Timeout:
                    url += "  [❌ SIGNED URL FAILED: Timeout]"
                except Exception as e:
                    url += f"  [❌ SIGNED URL FAILED: {str(e)}]"

            elif "childId" in url and "parentId" in url:
                url = f"https://anonymousrajputplayer-9ab2f2730a02.herokuapp.com/pw?url={url}&token={TOKEN_CP}"

            elif "d1d34p8vz63oiq" in url or "sec1.pw.live" in url:
                url = f"https://anonymousrajputplayer-9ab2f2730a02.herokuapp.com/pw?url={url}&token={TOKEN_CP}"

            if ".pdf*" in url:
                url = f"https://dragoapi.vercel.app/pdf/{url}"
            if ".zip" in url:
                url = f"https://video.pablocoder.eu.org/appx-zip?url={url}"

            elif 'encrypted.m' in url:
                appxkey = url.split('*')[1]
                url = url.split('*')[0]

            if "youtu" in url:
                ytf = f"b[height<=720][ext=mp4]/bv[height<=720][ext=mp4]+ba[ext=m4a]/b[ext=mp4]"
            elif "embed" in url:
                ytf = f"bestvideo[height<=720]+bestaudio/best[height<=720]"
            else:
                ytf = f"b[height<=720]/bv[height<=720]+ba/b/bv+ba"

            if "jw-prod" in url:
                cmd = f'yt-dlp -o "{name}.mp4" "{url}"'
            elif "webvideos.classplusapp." in url:
               cmd = f'yt-dlp --add-header "referer:https://web.classplusapp.com/" --add-header "x-cdn-tag:empty" -f "{ytf}" "{url}" -o "{name}.mp4"'
            elif "youtube.com" in url or "youtu.be" in url:
                cmd = f'yt-dlp --cookies youtube_cookies.txt -f "{ytf}" "{url}" -o "{name}".mp4'
            else:
                cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"'

            try:
                cc = f'**╭━━━━━━━━━━━╮**\n**💫 𝐕ɪᴅᴇⱺ 𝐈𝐃** : **{str(count).zfill(3)}**\n**╰━━━━━━━━━━━╯**\n**📁𝐓ɪᴛʟᴇ : {name1}** **({res}) {MR} .mkv\n** \n**📚𝐂ⱺᴜʀꜱᴇ** : **{b_name}**\n\n**⚡Dⱺw𐓣𝗅ⱺ𝖺𝖽ed By** : **{MR}** </blockquote>'
                cc1 = f'**╭━━━━━━━━━━╮**\n**💫 𝐅ɪʟᴇ 𝐈𝐃** : **{str(count).zfill(3)}**\n**╰━━━━━━━━━━╯**\n**📁𝐓ɪᴛʟᴇ : {name1}** **{MR} .pdf\n** \n**📚𝐂ⱺᴜʀꜱᴇ** : **{b_name}**\n\n**⚡Dⱺw𐓣𝗅ⱺ𝖺𝖽ed By** : **{MR}** '
                cczip = f'**——— ✦ {str(count).zfill(3)} ✦ ———**\n\n**📁 Title :** `{name1} .zip`\n\n**📚 Course :** `{b_name}`\n\n**🌟 Extracted By :** {MR}'
                ccimg = f'**╭━━━━━━━━━━━╮**\n**💫 𝐈ᴍᴀɢᴇ 𝐈𝐃** : **{str(count).zfill(3)}**\n**╰━━━━━━━━━━━╯**\n\n**📁𝐓ɪᴛʟᴇ** : **{name1}** **{MR} .JPG**\n\n**📚𝐂ⱺᴜʀꜱᴇ** : **{b_name}**\n\n**⚡Dⱺw𐓣𝗅ⱺ𝖺𝖽ed By** : **{MR}** '
                ccm = f'**——— ✦ {str(count).zfill(3)} ✦ ———**\n\n**🎵 Title :** `{name1} .mp3`\n\n**📚 Course :** `{b_name}`\n\n**🌟 Extracted By :** {MR}'
                cchtml = f'**——— ✦ {str(count).zfill(3)} ✦ ———**\n\n**🌐 Title :** `{name1} .html`\n\n**📚 Course :** `{b_name}`\n\n**🌟 Extracted By :** {MR}'

                if "drive" in url:
                    try:
                        ka = await helper.download(url, name)
                        copy = await bot.send_document(chat_id=m.chat.id, document=ka, caption=cc1)
                        count += 1
                        os.remove(ka)
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue

                elif ".pdf" in url:
                    if "cwmediabkt99" in url:
                        max_retries = 15
                        retry_delay = 4
                        success = False
                        failure_msgs = []
                        for attempt in range(max_retries):
                            try:
                                await asyncio.sleep(retry_delay)
                                url = url.replace(" ", "%20")
                                scraper = cloudscraper.create_scraper()
                                response = scraper.get(url)
                                if response.status_code == 200:
                                    with open(f'{name}.pdf', 'wb') as file:
                                        file.write(response.content)
                                    await asyncio.sleep(retry_delay)
                                    copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1)
                                    count += 1
                                    os.remove(f'{name}.pdf')
                                    success = True
                                    break
                                else:
                                    failure_msg = await m.reply_text(f"Attempt {attempt + 1}/{max_retries} failed: {response.status_code} {response.reason}")
                                    failure_msgs.append(failure_msg)
                            except Exception as e:
                                failure_msg = await m.reply_text(f"Attempt {attempt + 1}/{max_retries} failed: {str(e)}")
                                failure_msgs.append(failure_msg)
                                await asyncio.sleep(retry_delay)
                                continue
                        for msg in failure_msgs:
                            await msg.delete()
                        if not success:
                            await m.reply_text(f"Failed to download PDF after {max_retries} attempts.\n⚠️**Downloading Failed**⚠️\n**Name** =>> {str(count).zfill(3)} {name1}\n**Url** =>> {link0}", disable_web_page_preview)
                    else:
                        try:
                            cmd = f'yt-dlp -o "{name}.pdf" "{url}"'
                            download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                            os.system(download_cmd)
                            copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1)
                            count += 1
                            os.remove(f'{name}.pdf')
                        except FloodWait as e:
                            await m.reply_text(str(e))
                            time.sleep(e.x)
                            continue

                elif ".ws" in url and url.endswith(".ws"):
                    try:
                        await helper.pdf_download(f"{api_url}utkash-ws?url={url}&authorization={api_token}", f"{name}.html")
                        time.sleep(1)
                        await bot.send_document(chat_id=m.chat.id, document=f"{name}.html", caption=cchtml)
                        os.remove(f'{name}.html')
                        count += 1
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue

                elif ".zip" in url:
                    try:
                        BUTTONSZIP = InlineKeyboardMarkup([[InlineKeyboardButton(text="🎥 ZIP STREAM IN PLAYER", url=f"{url}")]])
                        await bot.send_photo(chat_id=m.chat.id, photo=photozip, caption=cczip, reply_markup=BUTTONSZIP)
                        count += 1
                        time.sleep(1)
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue

                elif any(ext in url.lower() for ext in [".jpg", ".jpeg", ".png", ".webp"]):
                    try:
                        ext = url.split('.')[-1].split("?")[0]
                        filename = f"{name}.{ext}"
                        async with httpx.AsyncClient() as client:
                            r = await client.get(url)
                            if r.status_code == 200:
                                with open(filename, "wb") as f:
                                    f.write(r.content)
                            else:
                                await m.reply_text("❌ Failed to download image.")
                                return
                        if ext == "webp":
                            from PIL import Image
                            img = Image.open(filename).convert("RGB")
                            jpg_file = f"{name}.jpg"
                            img.save(jpg_file, "JPEG")
                            os.remove(filename)
                            filename = jpg_file
                        copy = await bot.send_photo(chat_id=m.chat.id, photo=filename, caption=ccimg)
                        count += 1
                        os.remove(filename)
                    except FloodWait as e:
                        await asyncio.sleep(e.x)
                        continue
                    except Exception as e:
                        await m.reply_text(f"⚠️ Error: {e}")

                elif any(ext in url for ext in [".mp3", ".wav", ".m4a"]):
                    try:
                        ext = url.split('.')[-1]
                        cmd = f'yt-dlp -o "{name}.{ext}" "{url}"'
                        download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                        os.system(download_cmd)
                        copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.{ext}', caption=ccm)
                        count += 1
                        os.remove(f'{name}.{ext}')
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue

                elif 'encrypted.m' in url:
                    remaining_links = len(links) - count
                    progress = (count / len(links)) * 100
                    Show = (
                        f"<b><i>🌸 Hey cutie, I'm working my magic just for you 💖</i></b>\n"
                        f"<b><i>╰━━━━━━━━━━━━━━━━━━━━━━━━╯</i></b>\n"
                        f"<b><i>📈 Progress: {progress:.2f}%</i></b>\n"
                        f"<b><i>🧩 Links processed: {count} / {len(links)}</i></b>\n"
                        f"<b><i>🍬 Only {remaining_links} links left to go 🥰</i></b>\n"
                        f"<b><i>━━━━━━━━━━━━━━━━━━</i></b>\n"
                        f"<b><i>⏳ Downloading your dreamy content... because dreams are made to come true ☁️✨</i></b>\n"
                        f"<b>🫶 For: {CR}</b>\n"
                        f"<b><i>🎀 Batch: {b_name}</i></b>\n"
                        f"<b><i>━━━━━━━━━━━━━━━━━━</i></b>\n"
                        f"<b><i>📚 Title: {name}</i></b>\n"
                        f"<b><i>💫 Quality: {quality}</i></b>\n"
                        f"<b><i>🔗 Original Link: <a href='{link0}'>Click me, love 💌</a></i></b>\n"
                        f"<b><i>🖇️ API Link: only my heart knows it 💘</i></b>\n"
                        f"<b><i>━━━━━━━━━━━━━━━━━━</i></b>\n"
                        f"<b><i>💭 Feeling tired? Send /stop and I'll wait patiently for you like a good boy 🐶💖</i></b>\n"
                        f"<b><i>🦋 With all my love, always yours —</i></b> <b><a href='https://t.me/username'>king 🖤</a></b>"
                    )
                    prog = await m.reply_text(Show, disable_web_page_preview=True)
                    res_file = await helper.download_and_decrypt_video(url, cmd, name, appxkey)
                    filename = res_file
                    await prog.delete(True)
                    await bot.send_video(
                        chat_id=m.chat.id,
                        video=filename,
                        caption=cc,
                        supports_streaming=True
                    )
                    os.remove(filename)
                    count += 1
                    await asyncio.sleep(1)
                    continue

                elif 'drmcdni' in url or 'drm/wv' in url:
                    remaining_links = len(links) - count
                    progress = (count / len(links)) * 100
                    Show = (
                        f"<b><i>🌸 Hey cutie, I'm working my magic just for you 💖</i></b>\n"
                        f"<b><i>╰━━━━━━━━━━━━━━━━━━━━━━━━╯</i></b>\n"
                        f"<b><i>📈 Progress: {progress:.2f}%</i></b>\n"
                        f"<b><i>🧩 Links processed: {count} / {len(links)}</i></b>\n"
                        f"<b><i>🍬 Only {remaining_links} links left to go 🥰</i></b>\n"
                        f"<b><i>━━━━━━━━━━━━━━━━━━</i></b>\n"
                        f"<b><i>⏳ Downloading your dreamy content... because dreams are made to come true ☁️✨</i></b>\n"
                        f"<b>🫶 For: {CR}</b>\n"
                        f"<b><i>🎀 Batch: {b_name}</i></b>\n"
                        f"<b><i>━━━━━━━━━━━━━━━━━━</i></b>\n"
                        f"<b><i>📚 Title: {name}</i></b>\n"
                        f"<b><i>💫 Quality: {quality}</i></b>\n"
                        f"<b><i>🔗 Original Link: <a href='{link0}'>Click me, love 💌</a></i></b>\n"
                        f"<b><i>🖇️ API Link: only my heart knows it 💘</i></b>\n"
                        f"<b><i>━━━━━━━━━━━━━━━━━━</i></b>\n"
                        f"<b><i>💭 Feeling tired? Send /stop and I'll wait patiently for you like a good boy 🐶💖</i></b>\n"
                        f"<b><i>🦋 With all my love, always yours —</i></b> <b><a href='https://t.me/username'>king 🖤</a></b>"
                    )
                    prog = await m.reply_text(Show, disable_web_page_preview=True)
                    res_file = await helper.decrypt_and_merge_video(mpd, keys_string, path, name, 720)
                    filename = res_file
                    await prog.delete(True)
                    await bot.send_video(
                        chat_id=m.chat.id,
                        video=filename,
                        caption=cc,
                        supports_streaming=True
                    )
                    os.remove(filename)
                    count += 1
                    await asyncio.sleep(1)
                    continue

                else:
                    remaining_links = len(links) - count
                    progress = (count / len(links)) * 100
                    Show = (
                        f"<b><i>🌸 Hey cutie, I'm working my magic just for you 💖</i></b>\n"
                        f"<b><i>╰━━━━━━━━━━━━━━━━━━━━━━━━╯</i></b>\n"
                        f"<b><i>📈 Progress: {progress:.2f}%</i></b>\n"
                        f"<b><i>🧩 Links processed: {count} / {len(links)}</i></b>\n"
                        f"<b><i>🍬 Only {remaining_links} links left to go 🥰</i></b>\n"
                        f"<b><i>━━━━━━━━━━━━━━━━━━</i></b>\n"
                        f"<b><i>⏳ Downloading your dreamy content... because dreams are made to come true ☁️✨</i></b>\n"
                        f"<b>🫶 For: {CR}</b>\n"
                        f"<b><i>🎀 Batch: {b_name}</i></b>\n"
                        f"<b><i>━━━━━━━━━━━━━━━━━━</i></b>\n"
                        f"<b><i>📚 Title: {name}</i></b>\n"
                        f"<b><i>💫 Quality: {quality}</i></b>\n"
                        f"<b><i>🔗 Original Link: <a href='{link0}'>Click me, love 💌</a></i></b>\n"
                        f"<b><i>🖇️ API Link: only my heart knows it 💘</i></b>\n"
                        f"<b><i>━━━━━━━━━━━━━━━━━━</i></b>\n"
                        f"<b><i>💭 Feeling tired? Send /stop and I'll wait patiently for you like a good boy 🐶💖</i></b>\n"
                        f"<b><i>🦋 With all my love, always yours —</i></b> <b><a href='https://t.me/username'>king 🖤</a></b>"
                    )
                    prog = await m.reply_text(Show, disable_web_page_preview=True)
                    user_id = os.environ.get("USER_ID")  # Use the globally updated user_id
                    res_file = await helper.download_video(url, cmd, name)
                    filename = res_file
                    await prog.delete(True)
                    await bot.send_video(
                        chat_id=m.chat.id,
                        video=filename,
                        caption=cc,
                        supports_streaming=True
                    )
                    os.remove(filename)
                    count += 1
                    time.sleep(1)

            except FloodWait as e:
                await m.reply_text(str(e))
                time.sleep(e.x)
                continue
            except Exception as e:
                await m.reply_text(
                    f"**downloading failed**\n\n{str(e)}\n\n**Name** - {name}\n**Link** - {url}"
                )
                count += 1
                failed_count += 1
                continue

    except FloodWait as e:
        await m.reply_text(str(e))
        time.sleep(e.x)
    except Exception as e:
        await m.reply_text(str(e))
        time.sleep(2)

    await m.reply_text("**Sᴜᴄᴄᴇsғᴜʟʟʏ Dᴏᴡɴʟᴏᴀᴅᴇᴅ Aʟʟ Lᴇᴄᴛᴜʀᴇs SIR 👿🚀**")

bot.run()
