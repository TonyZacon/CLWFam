from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from utils.database import get_user, store_user

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
