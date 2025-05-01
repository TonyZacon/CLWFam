from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from utils.database import get_user

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
        await update.message.reply_text(f"Kosa: Hatukuweza kupata taarifa za mwanachama huyu. Tafadhali hakiki ID.")

async def washiriki(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    try:
        chat_member = await context.bot.get_chat_member(chat_id, update.effective_user.id)

        if chat_member.status not in ['administrator', 'creator']:
            await update.message.reply_text("Huna ruhusa ya kutuma orodha ya wanachama. Ruhusa hii ni ya wasimamizi pekee.")
            await update.message.reply_text("Tafadhali tuma ID yako ili tuweze kuthibitisha kama wewe ni msimamizi.")
            return

        members = await context.bot.get_chat_members(chat_id)
        member_count = len(members)
        admins = await context.bot.get_chat_administrators(chat_id)
        admin_names = [admin.user.first_name for admin in admins]

        response = f"🧑‍🤝‍🧑 **Washiriki wa Kundi**: {member_count}\n\n"
        response += f"👑 **Wasimamizi**: {', '.join(admin_names)}\n"

        await update.message.reply_text(response)
    except Exception as
