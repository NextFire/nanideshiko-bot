import json
import logging
from importlib import resources

from ..config import saves

logger = logging.getLogger(__name__)


def sload(key: str):
    data = {}
    try:
        data = json.loads(resources.read_binary(saves, f"{key}.json"))
        logger.info(f'Loading {key}')
    except FileNotFoundError:
        logger.info(f'{key} not found')
    return data


def sdump(key: str, data):
    with resources.path(saves, f"{key}.json") as p:
        with open(p, 'w') as f:
            json.dump(data, f, ensure_ascii=False, sort_keys=True, indent=2)
    logger.info(f'Saving {key}')
