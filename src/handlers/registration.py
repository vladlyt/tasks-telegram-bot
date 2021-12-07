from telegram import Update
from telegram.ext import CallbackContext, CommandHandler

from src.db import Session
from src.models import User


def register_user(update: Update, context: CallbackContext):
    telegram_id = update.effective_user.id
    with Session() as session:
        existing_user = session.query(User).get(telegram_id)
        if existing_user is None:
            user = User(
                telegram_id=telegram_id,
                username=update.effective_user.username,
                first_name=update.effective_user.first_name,
                last_name=update.effective_user.last_name,
            )
            session.add(user)
            session.commit()
            update.message.reply_text(
                "You are registered!",
            )
        else:
            update.message.reply_text(
                f"You are already registered, "
                f"{update.effective_user.username if update.effective_user.username is not None else 'Incognito'}! "
                f"Stop it, I'm tired...",
            )


register_user_handler = CommandHandler('start', register_user)
