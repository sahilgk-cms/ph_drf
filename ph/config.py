import os
from dotenv import load_dotenv
from datetime import datetime
from dateutil.relativedelta import relativedelta


load_dotenv()

GOOGLE_API_KEY_1 = os.getenv("GOOGLE_API_KEY_1")
GOOGLE_API_KEY_2 = os.getenv("GOOGLE_API_KEY_2")
GOOGLE_API_KEYS = [GOOGLE_API_KEY_1, GOOGLE_API_KEY_2]
GEMINI_MODEL_NAME = "models/gemini-2.0-flash"

TIMESPAN_DICT = {
    'this week': datetime.now() - relativedelta(days=7),
    'this month': datetime.now().replace(day=1),
    'past 3 months': datetime.now() - relativedelta(months=3),
    'past 6 months': datetime.now() - relativedelta(months=6),
    'past 1 year': datetime.now() - relativedelta(years=1),
    'all time': datetime.now() - relativedelta(years=100),
}