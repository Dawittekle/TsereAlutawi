import os
from dotenv import load_dotenv
from telegram import Update, ChatMemberOwner, ChatPermissions
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from database import add_warning, get_warnings, reset_warnings, is_admin, add_admin, remove_admin, list_admins
from nlp_model import classify_text

# Load environment variables
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("BOT_TOKEN is not set in .env file")

# Function to check if a user is the group owner
async def is_group_owner(update: Update, context: CallbackContext, user_id):
    chat = await context.bot.get_chat(update.message.chat_id)
    administrators = await context.bot.get_chat_administrators(chat.id)

    for admin in administrators:
        if admin.user.id == user_id and isinstance(admin, ChatMemberOwner):
            return True
    return False

# Function to handle messages and detect hate speech
async def message_handler(update: Update, context: CallbackContext):
    message = update.message.text
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id
    username = update.message.from_user.username or update.message.from_user.full_name

    # Classify the message using NLP
    label, confidence = classify_text(message)

    if label in ["toxic", "hate"]:
        # Delete the message
        await update.message.delete()

        # Add warning to the user
        add_warning(user_id, chat_id)
        warnings = get_warnings(user_id, chat_id)

        # Notify the user PRIVATELY
        try:
            await context.bot.send_message(
                chat_id=user_id,
                text=f"⚠️ Warning {warnings}/5: Your message was flagged as hate speech and deleted."
            )
        except Exception as e:
            print(f"Failed to send warning to user {user_id}: {e}")

        # Notify group admins PRIVATELY
        admin_list = list_admins()
        admin_message = f"🚨 *Hate Speech Alert*\nUser: @{username} (ID: {user_id})\nMessage: {message}\nWarnings: {warnings}/5"
        
        for admin_id in admin_list:
            try:
                await context.bot.send_message(chat_id=admin_id, text=admin_message)
            except Exception as e:
                print(f"Failed to send message to admin {admin_id}: {e}")

        # If user reaches 5 warnings, remove them from the group
        if warnings >= 5:
            await context.bot.ban_chat_member(chat_id, user_id)
            await update.message.reply_text(f"User @{username} has been removed after 5 warnings.")

# Command to add an admin (only the group owner can do this)
async def add_admin_command(update: Update, context: CallbackContext):
    if len(context.args) == 0:
        await update.message.reply_text("Usage: /addadmin <user_id>")
        return

    admin_id = int(context.args[0])
    requester_id = update.message.from_user.id

    if not await is_group_owner(update, context, requester_id):
        await update.message.reply_text("Only the group owner can add admins.")
        return

    add_admin(admin_id)
    await update.message.reply_text(f"User {admin_id} has been added as an admin.")

# Command to remove an admin (only the group owner can do this)
async def remove_admin_command(update: Update, context: CallbackContext):
    if len(context.args) == 0:
        await update.message.reply_text("Usage: /removeadmin <user_id>")
        return

    admin_id = int(context.args[0])
    requester_id = update.message.from_user.id

    if not await is_group_owner(update, context, requester_id):
        await update.message.reply_text("Only the group owner can remove admins.")
        return

    remove_admin(admin_id)
    await update.message.reply_text(f"User {admin_id} has been removed as an admin.")

# Command to list all admins
async def list_admins_command(update: Update, context: CallbackContext):
    admins = list_admins()
    if admins:
        admin_list = "\n".join([f"- {admin}" for admin in admins])
        await update.message.reply_text(f"👑 *Admin List:*\n{admin_list}")
    else:
        await update.message.reply_text("No admins are registered.")

# Command to unban a user (only admins or group owner can use this)
async def unban_command(update: Update, context: CallbackContext):
    if len(context.args) == 0:
        await update.message.reply_text("Usage: /unban <user_id>")
        return

    user_id = int(context.args[0])
    chat_id = update.message.chat_id
    requester_id = update.message.from_user.id

    # Check if the requester is the group owner or an admin
    if not await is_group_owner(update, context, requester_id) and not is_admin(requester_id):
        await update.message.reply_text("Only the group owner or an admin can unban users.")
        return

    await context.bot.unban_chat_member(chat_id, user_id)
    reset_warnings(user_id, chat_id)
    await update.message.reply_text(f"User {user_id} has been unbanned and warnings have been reset.")

# Command to show the user's Telegram ID
async def id_command(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    await update.message.reply_text(f"Your User ID: `{user_id}`", parse_mode="Markdown")

# Command to display all available commands
async def help_command(update: Update, context: CallbackContext):
    help_text = (
        "🤖 *Hate Speech Monitor Bot* 📢\n"
        "This bot detects and removes hate speech in group chats, warns users, and notifies admins.\n\n"
        "📌 *Available Commands:*\n"
        "🔹 `/help` - Show this help message.\n"
        "🔹 `/id` - Get your Telegram user ID.\n\n"
        "👑 *Admin Commands:*\n"
        "🔹 `/addadmin <user_id>` - Add a user as an admin (Only group owner).\n"
        "🔹 `/removeadmin <user_id>` - Remove an admin (Only group owner).\n"
        "🔹 `/listadmins` - Show all registered admins.\n"
        "🔹 `/unban <user_id>` - Unban a user and reset their warnings (Admins & group owner only).\n\n"
        "⚠️ The bot will *automatically delete* hate speech messages and issue warnings.\n"
        "After *5 warnings*, the user will be *removed from the group*.\n"
        "Admins will receive *private alerts* about violations.\n\n"
        "💡 *Tip:* Use `/id` to get your user ID before adding yourself as an admin!"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")

# Main function to start the bot
def main():
    app = Application.builder().token(TOKEN).build()

    # Admin Commands
    app.add_handler(CommandHandler("addadmin", add_admin_command))
    app.add_handler(CommandHandler("removeadmin", remove_admin_command))
    app.add_handler(CommandHandler("listadmins", list_admins_command))
    app.add_handler(CommandHandler("unban", unban_command))

    # Utility Commands
    app.add_handler(CommandHandler("id", id_command))
    app.add_handler(CommandHandler("help", help_command))

    # Message Handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
jhb