import datetime
import logging
import os

from telegram.ext import Updater

from create_db import create_db
from handlers.registration import register_user_handler
from handlers.tasks.create import new_task_conversation_handler
from handlers.tasks.schedule import today_tasks
from handlers.tasks.show import (
    show_tasks_handler,
    mark_task_complete_handler,
    show_tasks_buttons_handler,
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

PORT = int(os.getenv('PORT', 5001))
TOKEN = os.getenv('TOKEN', 'TOKEN_NOT_PROVIDED')


def start_bot():
    create_db()
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    job_queue = updater.job_queue

    dispatcher.add_handler(register_user_handler)
    dispatcher.add_handler(new_task_conversation_handler)
    dispatcher.add_handler(show_tasks_handler)
    dispatcher.add_handler(show_tasks_buttons_handler)
    dispatcher.add_handler(mark_task_complete_handler)

    job_queue.run_daily(today_tasks, days=tuple(range(7)), time=datetime.time(hour=8, minute=0, second=0))

    logger.info("Starting bot on port %s...", PORT)
    updater.start_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=f'https://task-telegram.herokuapp.com/{TOKEN}',
    )

    updater.idle()


if __name__ == '__main__':
    start_bot()
