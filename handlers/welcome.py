from telegram import Update
from telegram.ext import ChatMemberHandler, ContextTypes
from utils.database import store_user

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.chat_member.new_chat_members:
        group_name = update.effective_chat.title
        full_name = f"{member.first_name} {member.last_name or ''}".strip()
        username = f"@{member.username}" if member.username else "(hakuna username)"
        msg = (
            f"🌟 Karibu sana {full_name}! 🌟\n\n"
            f"🏠 Kundi: {group_name}\n"
            f"🆔 ID: {member.id}\n"
            f"👤 Jina kamili: {full_name}\n"
            f"🔗 Username: {username}\n\n"
            "📜 Tafadhali soma *kanuni za kundi* kwa uangalifu: /kanuni\n"
            "🚀 Furahia ukaribisho na shiriki kikamilifu!\n"
        )
        await context.bot.send_message(chat_id=update.effective_chat.id, text=msg, parse_mode='Markdown')

        store_user(member.id, full_name, member.username)
