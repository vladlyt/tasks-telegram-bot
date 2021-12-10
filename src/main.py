from dotenv import load_dotenv

try:
    load_dotenv()
except Exception as e:
    print("Not found .env", e)

from run import start_bot

if __name__ == '__main__':
    start_bot()
