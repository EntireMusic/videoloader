import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


class BotSettings:
    def __init__(self):
        self.token = os.getenv('BOT_TOKEN')


@dataclass
class Settings:
    bot: BotSettings


settings = Settings(
    BotSettings(),
)
