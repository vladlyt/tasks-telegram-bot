import logging
import os

from dotenv import load_dotenv
from src.run import run

if __name__ == '__main__':
    load_dotenv()

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO,
    )
    logger = logging.getLogger(__name__)

    run(os.getenv('TOKEN'))
