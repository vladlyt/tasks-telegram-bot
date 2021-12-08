import logging
import os
from dotenv import load_dotenv

load_dotenv()

from src.run import run
from src.create_db import create_db

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

PORT = int(os.environ.get('PORT', 5000))
TOKEN = os.getenv('TOKEN')

if __name__ == '__main__':
    create_db()
    run(TOKEN, PORT)
