from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from datetime import datetime
import asyncio

# Replace with your bot token
BOT_TOKEN = "8113983053:AAGFw-EVPsk05Cmcg2Dc7Iw7jCb0O7_SxIc"

# Command: /report <total_personnel>
async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Get total personnel from command argument, default to 38
        total_personnel = int(context.args[0]) if context.args else 38
        
        # Calculate flagmen (assuming 1 supervisor always)
        flagmen_count = total_personnel - 1
        
        # Format today's date
        date_str = datetime.now().strftime("%d-%m-%Y")
        
        # Report template with dynamic total
        report_message = f"""*🚧 Flagman Distribution Report – {date_str}*

*GIS + MB (7)* – Cocklain x2, Bobcut, JCB, Compactor, Excavator, Roller

*Chiller Area (6)* – JCB, Roller, Compactor, Mini Roller, Bobcat, Dumper

*SSD (5)* – Hydra, DCM, Roller, Trailer, Bobcat

*Gate (5)* – Tough Rider, Unicrane, Loader, Hydra, Forklift

*NCC Office (5)* – Main Lift, Hydra, Bobcat, DCM, Dumper

*Store (5)* – Assigned x5

*Additional Allocation (5)* – Deployed as per site requirement

*Supervisor (1)* – Site Coordination

*Total Personnel: {total_personnel} ({flagmen_count} Flagmen + 1 Supervisor)*"""

        await update.message.reply_text(
            text=report_message,
            parse_mode="Markdown"
        )
        
    except ValueError:
        await update.message.reply_text("Please provide a valid number. Usage: /report <number>")
    except IndexError:
        await update.message.reply_text("Please provide the total personnel count. Usage: /report <number>")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = """Welcome to Flagman Distribution Bot! 🚧

Use `/report <total_personnel>` to get today's distribution report.

Example: `/report 30` for 30 total personnel"""
    
    await update.message.reply_text(welcome_message)

def main():
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("report", report))
    
    print("Bot started successfully!")
    
    # Run the bot
    application.run_polling()

if __name__ == "__main__":
    main()