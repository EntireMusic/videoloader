import asyncio
import logging
from pathlib import Path

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile

from config import settings
from downloader import Downloader


dp = Dispatcher()
dn = Downloader()


logging.basicConfig(level=logging.INFO, format='%(name)s: %(levelname)-8s - %(message)s')


# Command handler
@dp.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    await message.answer("👋 Привіт. Просто надішли мені посилання на будь яке відкрите відео з соцмереж.")


@dp.message(F.from_user, F.chat.type == "private")
async def download_video_handler(message: Message) -> None:
    url = message.text.strip()
    if not url.startswith(("http://", "https://")):
        await message.answer("❌ Посилання повинно починатися з с http:// или https://")
        return

    await message.answer("⏳ Чекай, йде завантаження. Це може зайняти деякий час...")

    try:
        file_path = await dn.download_video(url)

        if file_path and Path(file_path).exists():
            await message.answer_video(
                video=FSInputFile(file_path),
                caption="✅ Готово!"
            )
            Path(file_path).unlink(missing_ok=True)
        else:
            await message.answer("❌ Не вдалося завантажити відео (моливо приватне або видалено)")

    except Exception as e:
        await message.answer(f"❌ Помилка: {type(e).__name__}\n{e}", disable_web_page_preview=True)


# Run the bot
async def main() -> None:
    bot = Bot(token=settings.bot.token)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
