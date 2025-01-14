import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Setting up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
# Define a function that handles the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! I am your bot. Send me a message, and I will print it here.')
# Define functions to process text messages
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    print(f"Received message: {user_message}")
    await update.message.reply_text(f"You said: {user_message}")
if __name__ == '__main__':
    # Create an application instance and pass in API token
    application = ApplicationBuilder().token('7830105491:AAF8t7FlaxWNykNPMdUN3KsdRr3_Vdh0fKM').build()
    # Adding a Command Processor and Message Processor
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    # Activate the robot.
    application.run_polling()
