import datetime

from telegram.ext import Updater

from src.handlers.registration import register_user_handler
from src.handlers.tasks.create import new_task_conversation_handler
from src.handlers.tasks.schedule import today_tasks
from src.handlers.tasks.show import (
    show_tasks_handler,
    mark_task_complete_handler,
    show_tasks_buttons_handler,
)


def run(token):
    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher
    job_queue = updater.job_queue

    dispatcher.add_handler(register_user_handler)
    dispatcher.add_handler(new_task_conversation_handler)
    dispatcher.add_handler(show_tasks_handler)
    dispatcher.add_handler(show_tasks_buttons_handler)
    dispatcher.add_handler(mark_task_complete_handler)

    job_queue.run_daily(today_tasks, days=tuple(range(7)), time=datetime.time(hour=8, minute=0, second=0))

    updater.start_polling()
    updater.idle()
