from dotenv import load_dotenv

import os

load_dotenv(verbose=True)


SECRET_KEY = os.getenv('SECRET_KEY')