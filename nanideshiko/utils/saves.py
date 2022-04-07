import json
from contextlib import suppress
from importlib import resources

from ..config import saves


def sload(key: str):
    with suppress(FileNotFoundError):
        return json.loads(resources.read_binary(saves, f"{key}.json"))


def sdump(key: str, data):
    with resources.path(saves, f"{key}.json") as p:
        with open(p, 'w') as f:
            json.dump(data, f, ensure_ascii=False, sort_keys=True, indent=2)
