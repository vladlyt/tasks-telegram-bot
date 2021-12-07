import datetime
import logging
from enum import auto, IntEnum

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, Filters, ConversationHandler

from src.db import Session
from src.models import Task

logger = logging.getLogger(__name__)


class NewTaskStates(IntEnum):
    TITLE = auto()
    DESCRIPTION = auto()
    DATE = auto()
    PLACE = auto()
    CONFIRM = auto()


def new_task(update: Update, context: CallbackContext):
    reply_keyboard = [['/cancel']]
    update.message.reply_text('Enter your task title:', reply_markup=ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True,
    ))

    return NewTaskStates.TITLE


def get_task_title(update: Update, context: CallbackContext):
    context.user_data['title'] = update.message.text

    reply_keyboard = [['/skip', '/cancel']]

    update.message.reply_text('Enter task description:', reply_markup=ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True,
    ))

    return NewTaskStates.DESCRIPTION


def get_task_description(update: Update, context: CallbackContext):
    if update.message.text == '/skip':
        context.user_data['description'] = None
    else:
        context.user_data['description'] = update.message.text

    reply_keyboard = [['/skip', '/cancel']]
    update.message.reply_text('Enter task date!', reply_markup=ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True,
    ))

    return NewTaskStates.DATE


def get_task_date(update: Update, context: CallbackContext):
    if update.message.text == '/skip':
        context.user_data['date'] = None
    else:
        context.user_data['date'] = datetime.datetime.strptime(update.message.text, "%d/%m/%Y")
    reply_keyboard = [['/skip', '/cancel']]
    update.message.reply_text('Enter place!', reply_markup=ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True,
    ))

    return NewTaskStates.PLACE


def get_task_place(update: Update, context: CallbackContext):
    if update.message.text == '/skip':
        context.user_data['place'] = None
    else:
        context.user_data['place'] = update.message.text

    task = Task(
        title=context.user_data["title"],
        description=context.user_data["description"],
        when_date=context.user_data["date"],
        place=context.user_data["place"],
    )
    reply_keyboard = [['YES', 'NO']]
    update.message.reply_text(f'Here is your task!\n{task.display()}', reply_markup=ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True, input_field_placeholder='Create (Yes/No)?'
    ))

    return NewTaskStates.CONFIRM


def create_task(update: Update, context: CallbackContext):
    with Session() as session:
        user_new_task = Task(
            user_id=update.effective_user.id,
            title=context.user_data['title'],
            description=context.user_data['description'],
            when_date=context.user_data['date'],
            place=context.user_data['place'],
        )
        session.add(user_new_task)
        session.commit()
    update.message.reply_text('Hooray, your task is created!')

    return ConversationHandler.END


def cancel_creation_task(update: Update, context: CallbackContext):
    update.message.reply_text('See you...')

    return ConversationHandler.END


new_task_conversation_handler = ConversationHandler(
    entry_points=[CommandHandler('new_task', new_task)],
    states={
        NewTaskStates.TITLE: [MessageHandler(Filters.text & ~Filters.command, get_task_title)],
        NewTaskStates.DESCRIPTION: [MessageHandler(Filters.text, get_task_description)],
        NewTaskStates.DATE: [
            MessageHandler(Filters.regex('^\d{2}\/\d{2}\/\d{4}$') | Filters.regex('^/skip$'), get_task_date),
        ],
        NewTaskStates.PLACE: [MessageHandler(Filters.text, get_task_place)],
        NewTaskStates.CONFIRM: [
            MessageHandler(Filters.regex('^(YES)$') & ~Filters.command, create_task),
            MessageHandler(Filters.regex('^(NO)$') & ~Filters.command, cancel_creation_task),
        ],
    },
    fallbacks=[
        CommandHandler('cancel', cancel_creation_task),
    ],
)
