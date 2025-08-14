from telegram.ext import Updater, CommandHandler
from datetime import datetime

# Replace with your bot token
BOT_TOKEN = "8113983053:AAGFw-EVPsk05Cmcg2Dc7Iw7jCb0O7_SxIc"

# Command: /report <total_personnel>
def report(update, context):
    try:
        total_personnel = int(context.args[0]) if context.args else 38  # default 38

        # Format today’s date
        date_str = datetime.now().strftime("%d-%m-%Y")

        # Report template
        report_message = f"""*🚧 Flagman Distribution Report – {date_str}*

*GIS + MB (7)* – Cocklain x2, Bobcut, JCB, Compactor, Excavator, Roller  
*Chiller Area (6)* – JCB, Roller, Compactor, Mini Roller, Bobcat, Dumper  
*SSD (5)* – Hydra, DCM, Roller, Trailer, Bobcat  
*Gate (5)* – Tough Rider, Unicrane, Loader, Hydra, Forklift  
*NCC Office (5)* – Main Lift, Hydra, Bobcat, DCM, Dumper  
*Store (5)* – Assigned x5  
*Additional Allocation (5)* – Deployed as per site requirement  
*Supervisor (1)* – Site Coordination  

*Total Personnel: {total_personnel} (37 Flagmen + 1 Supervisor)*
"""

        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=report_message,
            parse_mode="Markdown"
        )

    except Exception as e:
        update.message.reply_text(f"Error: {e}")

def start(update, context):
    update.message.reply_text("Welcome! Use /report <total_personnel> to get today’s distribution report.")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("report", report))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
