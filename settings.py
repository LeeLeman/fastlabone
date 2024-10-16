import os
from dotenv import load_dotenv


load_dotenv()

SECRET_KEY = os.getenv("RECAPTCHA_SECRET_KEY")
SITE_KEY = os.getenv("RECAPTCHA_SITE_KEY")
