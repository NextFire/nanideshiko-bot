FROM python:slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --no-cache-dir \
    aiohttp \
    asyncio \
    asyncpraw \
    discord.py[voice] \
    youtube_dl

COPY . /bot

WORKDIR /bot

ENTRYPOINT ./entrypoint.sh
