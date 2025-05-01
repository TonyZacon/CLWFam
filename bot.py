import logging
import asyncio
import os
import sqlite3
from telegram import Update, ChatMember
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    ChatMemberHandler
)

TOKEN = 'put your token here'
ADMIN_USER_IDS = ['putyour first id', 'second id and so on', 'third id']  # Admin IDs kwa ruhusa za admin commands

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Fungua connection kwa database
def create_connection():
    return sqlite3.connect('bot_users.db')

def create_group_settings_connection():
    return sqlite3.connect('group_settings.db')

# Unda meza za watumiaji
def create_users_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            full_name TEXT,
            username TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Unda meza za group settings
def create_group_settings_table():
    conn = create_group_settings_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            group_id INTEGER PRIMARY KEY,
            rules TEXT
        )
    ''')
    conn.commit()
    conn.close()

create_users_table()
create_group_settings_table()

group_settings = {}
active_users = set()
inactive_users = set()

def is_admin(user_id):
    return user_id in ADMIN_USER_IDS

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Karibu kwenye bot, {update.effective_user.first_name}! 👋")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "Amri unazoweza kutumia:\n"
        "/anza - Karibu\n"
        "/maelezo - Kuhusu bot\n"
        "/wasimamizi - Orodha ya wasimamizi\n"
        "/mwanachama <user_id> - Taarifa za mwanachama\n"
        "/marekebisho kanuni [markdown|markdownv2|html] [kanuni zako] - Sasisha kanuni\n"
        "/kanuni - Angalia kanuni za kundi\n"
        "/washiriki - Orodha ya wanachama\n"
    )
    await update.message.reply_text(help_text)

async def maelezo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🙋‍♂️ **Habari!** Bot hii husaidia kusimamia kundi na kutoa taarifa.\n\n"
        "🛠️ Inaweza:\n"
        "1️⃣ Orodhesha wasimamizi\n"
        "2️⃣ Angalia info ya mwanachama\n"
        "3️⃣ Tuma ujumbe wa kukaribisha\n"
        "4️⃣ Toa msaada kuhusu amri"
    )

async def wasimamizi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    try:
        admins = await context.bot.get_chat_administrators(chat_id)
        names = ", ".join(admin.user.first_name for admin in admins)
        await update.message.reply_text(f"Wasimamizi wa kundi: {names}")
    except Exception as e:
        logger.error(f"Error getting admins: {e}")
        await update.message.reply_text(f"Kosa: Hatuwezi kupata wasimamizi kwa sasa. Tafadhali jaribu tena baadaye.")

async def mwanachama(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Tafadhali weka ID ya mwanachama. Mfano: /mwanachama 123456")
        return
    user_id = context.args[0]
    chat_id = update.effective_chat.id
    try:
        member = await context.bot.get_chat_member(chat_id, int(user_id))
        user = member.user
        status = member.status
        await update.message.reply_text(f"Jina: {user.first_name}\nStatus: {status}")
    except Exception as e:
        logger.error(f"Error fetching member {user_id}: {e}")
        await update.message.reply_text(f"Kosa: Hatukuweza kupata taarifa za mwanachama huyu. Tafadhali hakiki ID.")

def store_user(user_id, full_name, username):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO users (user_id, full_name, username) VALUES (?, ?, ?)
    ''', (user_id, full_name, username))
    conn.commit()
    conn.close()

def get_user(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def store_group_settings(group_id, rules):
    conn = create_group_settings_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO settings (group_id, rules) VALUES (?, ?)
    ''', (group_id, rules))
    conn.commit()
    conn.close()

def get_group_settings(group_id):
    conn = create_group_settings_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM settings WHERE group_id = ?', (group_id,))
    settings = cursor.fetchone()
    conn.close()
    return settings

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
        active_users.add(member.id)
        inactive_users.discard(member.id)

async def marekebisho(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("Huna ruhusa ya kufanya mabadiliko haya.")
        return

    group_id = update.effective_chat.id

    if len(context.args) < 2:
        await update.message.reply_text(
            "Tumia: /marekebisho kanuni [markdown|markdownv2|html] [kanuni zako]\n\n"
            "Mfano: /marekebisho kanuni markdown *Heshimu kila mmoja*"
        )
        return

    setting_type = context.args[0].lower()
    format_type = context.args[1].lower()
    rules = " ".join(context.args[2:])

    if setting_type == "kanuni":
        if format_type not in ['markdown', 'markdownv2', 'html']:
            await update.message.reply_text("Aina ya formatting haijulikani. Tumia: markdown, markdownv2, au html.")
            return

        store_group_settings(group_id, f"{format_type}|{rules}")
        await update.message.reply_text(
            f"Kanuni zimeboreshwa:\n\n{rules}",
            parse_mode=format_type.upper()
        )
    else:
        await update.message.reply_text("Kipengele hiki hakipo. Tumia 'kanuni' kubadilisha sheria.")

async def kanuni(update: Update, context: ContextTypes.DEFAULT_TYPE):
    group_id = update.effective_chat.id
    settings = get_group_settings(group_id)

    if not settings:
        await update.message.reply_text("Hakuna kanuni zilizowekwa bado.")
        return

    raw_value = settings[1]
    if "|" in raw_value:
        format_type, rules = raw_value.split("|", 1)
    else:
        format_type, rules = "markdown", raw_value

    await update.message.reply_text(
        f"Kanuni za {update.effective_chat.title}:\n\n{rules}",
        parse_mode=format_type.upper()
    )

async def washiriki(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    try:
        # Angalia kama mtumiaji ni admin
        chat_member = await context.bot.get_chat_member(chat_id, update.effective_user.id)

        # Angalia kama mtumiaji ni admin au owner
        if chat_member.status not in ['administrator', 'creator']:
            await update.message.reply_text("Huna ruhusa ya kutuma orodha ya wanachama. Ruhusa hii ni ya wasimamizi pekee.")

            # Omba ID ili kuthibitisha kama mtumiaji ni admin
            await update.message.reply_text("Tafadhali tuma ID yako ili tuweze kuthibitisha kama wewe ni msimamizi.")
            return

        # Pata orodha ya wanachama wa kundi
        members = await context.bot.get_chat_members(chat_id)

        # Hesabu idadi ya wanachama
        member_count = len(members)

        # Pata orodha ya wasimamizi
        admins = await context.bot.get_chat_administrators(chat_id)
        admin_names = [admin.user.first_name for admin in admins]

        # Jibu kwa orodha ya washiriki na wasimamizi
        response = f"🧑‍🤝‍🧑 **Washiriki wa Kundi**: {member_count}\n\n"
        response += f"👑 **Wasimamizi**: {', '.join(admin_names)}\n"

        await update.message.reply_text(response)
    except Exception as e:
        logger.error(f"Error in /washiriki command: {e}")
        await update.message.reply_text(f"Kosa: Hatukuweza kupata orodha ya wanachama. Tafadhali jaribu tena baadaye.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("anza", start))
    app.add_handler(CommandHandler("msaada", help_command))
    app.add_handler(CommandHandler("maelezo", maelezo))
    app.add_handler(CommandHandler("wasimamizi", wasimamizi))
    app.add_handler(CommandHandler("mwanachama", mwanachama))
    app.add_handler(CommandHandler("marekebisho", marekebisho))
    app.add_handler(CommandHandler("kanuni", kanuni))
    app.add_handler(CommandHandler("washiriki", washiriki))
    app.add_handler(ChatMemberHandler(welcome))

    app.run_polling()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except RuntimeError as e:
        if "event loop is already running" in str(e):
            import nest_asyncio
            nest_asyncio.apply()
            asyncio.get_event_loop().run_until_complete(main())
        else:
            raise
