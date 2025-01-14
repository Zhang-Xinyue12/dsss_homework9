!pip install torch transformers flask pyTelegramBotAPI
!pip install python-telegram-bot --upgrade
!pip install transformers

import nest_asyncio
import asyncio

# Allow other event loops to be nested within the running event loop
nest_asyncio.apply()

import os
from transformers import AutoModelForCausalLM, AutoTokenizer
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes
from telegram.ext import filters

# Loading TinyLlama Models and Splitters
def load_model():
    tokenizer = AutoTokenizer.from_pretrained("TinyLlama/TinyLlama-1.1B-Chat-v1.0")  # Using the TinyLlama model
    model = AutoModelForCausalLM.from_pretrained("TinyLlama/TinyLlama-1.1B-Chat-v1.0")  # Using the TinyLlama model
    return tokenizer, model
tokenizer, model = load_model()

# Processing user input and generating responses
def process_with_llm(input_text):
    inputs = tokenizer.encode(input_text, return_tensors="pt")
    outputs = model.generate(inputs, max_length=150, do_sample=True, temperature=0.7, top_p=0.9)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

# /start Handling Functions for Commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hello！I am your AI.')

# Handling user messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    response = process_with_llm(user_message)
    await update.message.reply_text(response)

# Main function, set robot
def main():
    # set TELEGRAM_BOT_TOKEN
    TELEGRAM_BOT_TOKEN = '7830105491:AAF8t7FlaxWNykNPMdUN3KsdRr3_Vdh0fKM'  
    
    if not TELEGRAM_BOT_TOKEN:
        print("please set TELEGRAM_BOT_TOKEN.")
        return

    # Create Application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    # Registering Handlers for the /start Command
    application.add_handler(CommandHandler("start", start))
    # Registering a Message Handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    # Activate the robot.
    application.run_polling()

if __name__ == '__main__':
    main()
