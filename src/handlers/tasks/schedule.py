import datetime

from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext

from handlers.tasks.show import TaskCompletion
from models import User, Task
from db import Session


def today_tasks(context: CallbackContext):
    with Session() as session:
        for user in session.query(User).filter(User.show_notifications == True):
            for task in user.tasks.filter(Task.is_completed == False).filter(Task.when_date <= datetime.datetime.now()):
                context.bot.send_message(
                    chat_id=user.telegram_id,
                    text=task.display_markdown(),
                    reply_markup=InlineKeyboardMarkup.from_row(
                        [
                            InlineKeyboardButton(
                                text='✅️',
                                callback_data=f'mark-task${TaskCompletion.COMPLETED}${task.id}',
                            ),
                            InlineKeyboardButton(
                                text='❌️',
                                callback_data=f'mark-task${TaskCompletion.NOT_COMPLETED}${task.id}',
                            ),
                        ]
                    ),
                    parse_mode=ParseMode.MARKDOWN_V2,
                )
