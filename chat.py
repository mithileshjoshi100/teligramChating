from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Bot token from BotFather
TOKEN = ""

# Temporary storage for user matching
users_queue = []  # Queue to match users
active_chats = {}  # Dictionary of active chat pairs

# Command to start the bot
def start(update, context):
    chat_id = update.message.chat_id
    if chat_id not in active_chats:
        if chat_id not in users_queue:
            users_queue.append(chat_id)
            update.message.reply_text("You have been added to the queue. Waiting for a partner...")
            check_and_connect(update, context)
        else:
            update.message.reply_text("You are already in the queue.")
    else:
        update.message.reply_text("You are already chatting with someone.")

# Command to disconnect
def disconnect(update, context):
    chat_id = update.message.chat_id
    if chat_id in active_chats:
        partner_id = active_chats.pop(chat_id)
        active_chats.pop(partner_id, None)
        context.bot.send_message(partner_id, "Your partner has disconnected.")
        update.message.reply_text("You have been disconnected.")
    elif chat_id in users_queue:
        users_queue.remove(chat_id)
        update.message.reply_text("You left the queue.")
    else:
        update.message.reply_text("You are not in a chat or queue.")

# Message handler to relay messages
def message_handler(update, context):
    chat_id = update.message.chat_id
    print(update)
    print(update.message)
    if chat_id in active_chats:
        partner_id = active_chats[chat_id]
        context.bot.send_message(partner_id, update.message.text)
    else:
        update.message.reply_text("You are not connected to anyone. Use /start to join the chat queue.")

# Check and connect users
def check_and_connect(update, context):
    if len(users_queue) >= 2:
        user1 = users_queue.pop(0)
        user2 = users_queue.pop(0)
        active_chats[user1] = user2
        active_chats[user2] = user1
        context.bot.send_message(user1, "You are now connected! Say hi!")
        context.bot.send_message(user2, "You are now connected! Say hi!")

# Main function to run the bot
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Add command and message handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("disconnect", disconnect))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, message_handler))

    # Start the bot with long polling
    print("Bot is running...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
