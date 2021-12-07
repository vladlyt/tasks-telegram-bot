import datetime
import logging
from enum import IntEnum, auto

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler

from src.db import Session
from src.models import Task

logger = logging.getLogger(__name__)


class ShowTasks(IntEnum):
    ALL = auto()
    TODAY = auto()
    TOMORROW = auto()
    COMPLETED = auto()
    NOT_COMPLETED = auto()

    def to_string(self):
        return f'show-tasks-{self.value}'


class TaskCompletion(IntEnum):
    COMPLETED = auto()
    NOT_COMPLETED = auto()


def get_tasks(update: Update, context: CallbackContext):
    update.message.reply_text(
        'Select one of the buttons:',
        reply_markup=InlineKeyboardMarkup.from_column(
            [
                InlineKeyboardButton(text='All tasks', callback_data=ShowTasks.ALL.to_string()),
                InlineKeyboardButton(text='Today tasks', callback_data=ShowTasks.TODAY.to_string()),
                InlineKeyboardButton(text='Tomorrow tasks', callback_data=ShowTasks.TOMORROW.to_string()),
                InlineKeyboardButton(text='Completed tasks', callback_data=ShowTasks.COMPLETED.to_string()),
                InlineKeyboardButton(text='Not completed tasks', callback_data=ShowTasks.NOT_COMPLETED.to_string()),
            ]
        ),
    )


def show_tasks_callback(update: Update, context: CallbackContext) -> None:
    update.callback_query.answer()
    with Session() as session:
        query = session.query(Task).filter_by(user_id=update.effective_user.id).order_by(Task.creation_date)
        if update.callback_query.data == ShowTasks.ALL.to_string():
            query = query.all()
        elif update.callback_query.data == ShowTasks.TODAY.to_string():
            query = query.filter(Task.when_date <= datetime.date.today()).filter(Task.is_completed == False)
        elif update.callback_query.data == ShowTasks.TOMORROW.to_string():
            query = query.filter(Task.when_date > datetime.date.today()).filter(Task.is_completed == False)
        elif update.callback_query.data == ShowTasks.COMPLETED.to_string():
            query = query.filter(Task.is_completed == True)
        elif update.callback_query.data == ShowTasks.NOT_COMPLETED.to_string():
            query = query.filter(Task.is_completed == False)
        else:
            logger.info("Not supported event")
            return

        tasks = list(query)
        if len(tasks):
            for task in tasks:
                update.effective_message.reply_markdown_v2(
                    task.display_markdown(),
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
                )
        else:
            update.effective_message.reply_text('There are no tasks!')


def mark_task_completion_callback(update: Update, context: CallbackContext):
    update.callback_query.answer()
    with Session() as session:
        query = session.query(Task).filter_by(user_id=update.effective_user.id).order_by(Task.creation_date)
        _, completion, task_id = update.callback_query.data.split('$')

        task = query.filter(Task.id == int(task_id)).first()
        if task is None:
            logger.info("Not found task in user tasks")
            return

        completion = TaskCompletion(int(completion))
        if completion == TaskCompletion.COMPLETED:
            task.is_completed = True
        elif completion == TaskCompletion.NOT_COMPLETED:
            task.is_completed = False
        else:
            logger.info("Not valid completion value")
            return
        session.commit()
        update.effective_message.edit_text(
            task.display_markdown(),
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


mark_task_complete_handler = CallbackQueryHandler(
    mark_task_completion_callback,
    pattern='^mark-task',
)

show_tasks_buttons_handler = CommandHandler('tasks', get_tasks)
show_tasks_handler = CallbackQueryHandler(
    show_tasks_callback,
    pattern='^show-tasks',
)
