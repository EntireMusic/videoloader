import logging
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import yt_dlp
import asyncio

logger = logging.getLogger(__name__)


class Downloader:
    def __init__(self) -> None:
        # Можно добавить сюда настройки yt_dlp, если нужно
        pass

    def timestamp_filename(self, prefix: str, ext: str = "mp4") -> str:
        ts = datetime.now().strftime("%Y%m%d%H%M%S")
        ext = ext.lstrip(".")
        folder = Path("downloads") / prefix
        folder.mkdir(parents=True, exist_ok=True)
        return str(folder / f"{prefix}_{ts}.{ext}")

    # ====================== DOWNLOAD FUNCTIONS ======================
    def download_tiktok(self, url: str) -> str:
        output = self.timestamp_filename("tiktok")
        ydl_opts = {"outtmpl": output}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        logger.info(f"Saved TikTok → {output}")
        return output

    def download_facebook(self, url: str) -> str:
        output = self.timestamp_filename("facebook")
        ydl_opts = {"outtmpl": output}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        logger.info(f"Saved Facebook → {output}")
        return output

    def download_youtube(self, url: str) -> str:
        output = self.timestamp_filename("youtube")
        ydl_opts = {
            "outtmpl": output,
            "format": "bestvideo+bestaudio/best",
            "merge_output_format": "mp4",
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        logger.info(f"Saved YouTube → {output}")
        return output

    def download_instagram(self, url: str) -> str:
        output = self.timestamp_filename("instagram")
        ydl_opts = {"outtmpl": output}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        logger.info(f"Saved Instagram → {output}")
        return output

    def parse_link(self, full_url: str) -> str:
        host = urlparse(full_url).hostname or ""
        parts = host.split(".")
        domain = parts[-2] if len(parts) >= 2 else host
        return domain.lower()

    # ====================== ГЛАВНАЯ АСИНХРОННАЯ ФУНКЦИЯ ======================
    async def download_video(self, link: str) -> str | None:
        site = self.parse_link(link)
        logger.info(f"Start downloading: {site} | {link}")

        try:
            if site == "tiktok" or site in "tiktok":
                path = await asyncio.to_thread(self.download_tiktok, link)
            elif site == "youtube" or site in "youtube":
                path = await asyncio.to_thread(self.download_youtube, link)
            elif site == "facebook" or site in "facebook":
                path = await asyncio.to_thread(self.download_facebook, link)
            elif site == "instagram" or site in "instagram":
                path = await asyncio.to_thread(self.download_instagram, link)
            else:
                logger.warning(f"Unknown site: {site}")
                return None

            # Дополнительная проверка (на всякий случай)
            if Path(path).exists() and Path(path).stat().st_size > 1024:  # >1 КБ
                logger.info(f"File download successfully: {path}")
                return path
            else:
                logger.error(f"File not found or empty: {path}")
                return None

        except yt_dlp.utils.DownloadError as e:
            logger.error(f"Download error yt_dlp: {e}")
            raise
        except Exception as e:
            logger.exception(f"Unknown download error: {e.__class__.__name__}: {e}")
            raise