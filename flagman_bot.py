import os
import logging
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from flask import Flask, request
import asyncio
import threading

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get bot token and port
BOT_TOKEN = os.getenv('BOT_TOKEN', "8113983053:AAGFw-EVPsk05Cmcg2Dc7Iw7jCb0O7_SxIc")
PORT = int(os.getenv('PORT', 5000))

# Flask app for webhook
app = Flask(__name__)

# Global variable to store the application
telegram_app = None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    welcome_message = """🚧 *Welcome to Flagman Distribution Bot!*

Use `/report <total_personnel>` to get today's distribution report.

*Examples:*
• `/report 30` for 30 total personnel
• `/report 45` for 45 total personnel
• `/report` (uses default of 38)

The bot will automatically calculate flagmen count (total - 1 supervisor)."""
    
    try:
        await update.message.reply_text(
            text=welcome_message,
            parse_mode="Markdown"
        )
    except Exception as e:
        logger.error(f"Error in start command: {e}")
        await update.message.reply_text("Welcome to Flagman Distribution Bot!")

async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generate flagman distribution report."""
    try:
        # Get total personnel from command argument, default to 38
        if context.args and len(context.args) > 0:
            total_personnel = int(context.args[0])
            if total_personnel < 1:
                raise ValueError("Personnel count must be positive")
        else:
            total_personnel = 38
        
        # Calculate flagmen (assuming 1 supervisor always)
        flagmen_count = max(0, total_personnel - 1)
        
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

*Total Personnel: {total_personnel} ({flagmen_count} Flagmen + 1 Supervisor)*

Generated at: {datetime.now().strftime("%H:%M:%S")}"""

        await update.message.reply_text(
            text=report_message,
            parse_mode="Markdown"
        )
        
        logger.info(f"Report generated for {total_personnel} personnel")
        
    except ValueError:
        error_msg = "❌ Please provide a valid positive number.\n\n*Usage:* `/report <number>`\n*Example:* `/report 30`"
        await update.message.reply_text(error_msg, parse_mode="Markdown")
        
    except Exception as e:
        logger.error(f"Error in report command: {e}")
        await update.message.reply_text("❌ An error occurred while generating the report. Please try again.")

@app.route('/')
def health_check():
    return "Flagman Bot is running! 🚧", 200

@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def webhook():
    """Handle incoming webhook updates."""
    try:
        json_data = request.get_json(force=True)
        update = Update.de_json(json_data, telegram_app.bot)
        
        # Process the update in a new thread
        def process_update():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(telegram_app.process_update(update))
            loop.close()
        
        thread = threading.Thread(target=process_update)
        thread.start()
        
        return "OK", 200
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return "ERROR", 500

def setup_telegram_app():
    """Set up the Telegram application."""
    global telegram_app
    
    # Create application without polling
    telegram_app = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    telegram_app.add_handler(CommandHandler("start", start))
    telegram_app.add_handler(CommandHandler("report", report))
    
    logger.info("Telegram application set up successfully!")

def main():
    """Start the bot with webhook."""
    try:
        # Set up telegram app
        setup_telegram_app()
        
        print("🚧 Flagman Distribution Bot starting...")
        logger.info("Bot starting with webhook method")
        
        # Start Flask app
        app.run(host='0.0.0.0', port=PORT, debug=False)
        
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        print(f"❌ Bot failed to start: {e}")

if __name__ == "__main__":
    main()