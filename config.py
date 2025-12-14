import os
from dotenv import load_dotenv

load_dotenv()

class Setting():
    def __init__(self):
        self.LLM_URI=os.getenv("LLM_URI")
        self.DB_URI=os.getenv("DB_URI")
        self.BOT_TOKEN=os.getenv("BOT_TOKEN")


settings = Setting()