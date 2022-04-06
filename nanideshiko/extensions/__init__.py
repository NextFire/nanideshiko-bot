import logging
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from discord.ext.commands import Bot

logger = logging.getLogger(__name__)

extensions_dir = Path(__file__).parent


def load_extensions(bot: "Bot"):
    for extension_file in extensions_dir.iterdir():
        extension = extension_file.stem

        if extension.startswith('_'):
            continue

        module_name = f"{__package__}.{extension}"
        bot.load_extension(module_name)
        logger.info(f"Extension '{module_name}' loaded")
