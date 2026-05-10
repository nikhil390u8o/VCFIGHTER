# ╔══════════════════════════════════════════════════════════════╗
# ║         VCFIGHTER — In-Memory Database (No MongoDB)          ║
# ║         MongoDB hata diya — sab kuch RAM mein store hoga     ║
# ╚══════════════════════════════════════════════════════════════╝

import time
from typing import Any

from VCFIGHTERS.logging import LOGGER

log = LOGGER("MemDB")

# ─────────────────────────────────────────────
# IN-MEMORY STORAGE
# ─────────────────────────────────────────────

_store: dict[str, dict] = {
    "settings":   {},
    "ffmpeg":     {},
    "userbots":   {},
    "targets":    {},
    "sudo":       {},
    "recordings": {},
    "kv":         {},
}

db = None  # kept for compatibility (Settings.py ping check)


async def init_db():
    """No-op — MongoDB nahi hai, sirf log karo."""
    global db
    db = _FakeDB()
    log.info("✅ In-Memory DB ready (MongoDB removed)")


class _FakeDB:
    """Settings.py mein db.command('ping') ke liye dummy class."""
    async def command(self, cmd):
        return {"ok": 1}


# ══════════════════════════════════════════════
#  SETTINGS
# ══════════════════════════════════════════════

_DEFAULT_SETTINGS = {
    "_id":         "global",
    "mode":        "dm",
    "logger_chat": None,
    "pytgcalls": {
        "stream_type":       "audio",
        "quality":           "medium",
        "noise_suppression": False,
    },
}


async def get_settings() -> dict:
    return _store["settings"].get("global", _DEFAULT_SETTINGS.copy())


async def save_settings(fields: dict):
    current = await get_settings()
    current.update(fields)
    _store["settings"]["global"] = current


async def get_mode() -> str:
    s = await get_settings()
    return s.get("mode", "dm")


async def set_mode(mode: str):
    await save_settings({"mode": mode})


async def get_logger_chat() -> int | None:
    s = await get_settings()
    return s.get("logger_chat")


async def get_pytgcalls_settings() -> dict:
    s = await get_settings()
    return s.get("pytgcalls", _DEFAULT_SETTINGS["pytgcalls"].copy())


async def save_pytgcalls_settings(pytg: dict):
    await save_settings({"pytgcalls": pytg})


# ══════════════════════════════════════════════
#  FFMPEG
# ══════════════════════════════════════════════

_DEFAULT_FFMPEG = {
    "_id":        "global",
    "volume":     1.0,
    "compressor": False,
    "limiter":    False,
    "bass":       0,
    "pitch":      "normal",
    "echo":       False,
}


async def get_ffmpeg_settings() -> dict:
    return _store["ffmpeg"].get("global", _DEFAULT_FFMPEG.copy())


async def save_ffmpeg_settings(fields: dict):
    current = await get_ffmpeg_settings()
    current.update(fields)
    _store["ffmpeg"]["global"] = current


async def reset_ffmpeg_settings():
    _store["ffmpeg"]["global"] = _DEFAULT_FFMPEG.copy()


# ══════════════════════════════════════════════
#  USERBOTS
# ══════════════════════════════════════════════

async def get_all_userbots() -> list[dict]:
    return list(_store["userbots"].values())


async def get_active_userbots() -> list[dict]:
    return [u for u in _store["userbots"].values() if u.get("active")]


async def get_all_sessions() -> list[str]:
    return [u["session_string"] for u in _store["userbots"].values() if u.get("session_string")]


async def get_userbot_by_phone(phone: str) -> dict | None:
    for u in _store["userbots"].values():
        if u.get("phone") == phone:
            return u
    return None


async def get_userbot_by_session(session: str) -> dict | None:
    return _store["userbots"].get(session)


async def add_userbot(data: dict):
    key = data["session_string"]
    _store["userbots"][key] = data


async def delete_userbot(session: str):
    _store["userbots"].pop(session, None)


async def delete_all_userbots():
    _store["userbots"].clear()


async def set_userbot_active(session: str, active: bool):
    if session in _store["userbots"]:
        _store["userbots"][session]["active"] = active


async def userbot_count() -> int:
    return len(_store["userbots"])


async def active_userbot_count() -> int:
    return sum(1 for u in _store["userbots"].values() if u.get("active"))


# ══════════════════════════════════════════════
#  TARGETS
# ══════════════════════════════════════════════

async def get_all_targets() -> list[dict]:
    return list(_store["targets"].values())


async def get_target_by_chat_id(chat_id: int) -> dict | None:
    return _store["targets"].get(str(chat_id))


async def get_primary_target() -> dict | None:
    targets = list(_store["targets"].values())
    if not targets:
        return None
    return sorted(targets, key=lambda x: x.get("added_at", 0), reverse=True)[0]


async def add_target(data: dict):
    _store["targets"][str(data["chat_id"])] = data


async def delete_target(chat_id: int):
    _store["targets"].pop(str(chat_id), None)


async def delete_all_targets():
    _store["targets"].clear()


async def update_target_joined(chat_id: int, phone: str):
    key = str(chat_id)
    if key in _store["targets"]:
        joined = _store["targets"][key].setdefault("userbots_joined", [])
        if phone not in joined:
            joined.append(phone)


# ══════════════════════════════════════════════
#  SUDO USERS
# ══════════════════════════════════════════════

async def get_sudo_users() -> list[int]:
    return [d["user_id"] for d in _store["sudo"].values()]


async def get_sudo_users_full() -> list[dict]:
    return list(_store["sudo"].values())


async def add_sudo_user(data: dict):
    uid = str(data["user_id"])
    if uid not in _store["sudo"]:
        _store["sudo"][uid] = data


async def remove_sudo_user(user_id: int):
    _store["sudo"].pop(str(user_id), None)


async def is_sudo_user(user_id: int) -> bool:
    return str(user_id) in _store["sudo"]


# ══════════════════════════════════════════════
#  RECORDINGS
# ══════════════════════════════════════════════

async def save_recording(file_path: str, user_id: int) -> str:
    key = f"{user_id}_{int(time.time())}"
    _store["recordings"][key] = {
        "file_path": file_path,
        "user_id":   user_id,
        "timestamp": int(time.time()),
    }
    return key


async def get_recording(user_id: int) -> dict | None:
    user_recs = [v for v in _store["recordings"].values() if v["user_id"] == user_id]
    if not user_recs:
        return None
    return sorted(user_recs, key=lambda x: x["timestamp"], reverse=True)[0]


async def delete_recording(file_path: str):
    keys = [k for k, v in _store["recordings"].items() if v["file_path"] == file_path]
    for k in keys:
        _store["recordings"].pop(k, None)


async def delete_all_recordings_for_user(user_id: int):
    keys = [k for k, v in _store["recordings"].items() if v["user_id"] == user_id]
    for k in keys:
        _store["recordings"].pop(k, None)


async def cleanup_old_recordings(older_than_seconds: int = 3600):
    cutoff = int(time.time()) - older_than_seconds
    keys = [k for k, v in _store["recordings"].items() if v["timestamp"] < cutoff]
    for k in keys:
        _store["recordings"].pop(k, None)
    if keys:
        log.info(f"🧹 Cleaned up {len(keys)} old recording(s)")


# ══════════════════════════════════════════════
#  GENERIC KEY-VALUE
# ══════════════════════════════════════════════

async def get_value(collection: str, key: str, default: Any = None) -> Any:
    return _store["kv"].get(f"{collection}:{key}", default)


async def set_value(collection: str, key: str, value: Any):
    _store["kv"][f"{collection}:{key}"] = value


async def db_stats() -> dict:
    return {
        "userbots":  await userbot_count(),
        "active_ub": await active_userbot_count(),
        "targets":   len(_store["targets"]),
        "sudo":      len(_store["sudo"]),
    }
