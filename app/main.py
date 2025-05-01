import asyncio
from app.bots import run_company_bot, run_blogger_bot


async def main():
    # Запускаем оба бота параллельно
    await asyncio.gather(run_company_bot(), run_blogger_bot())


if __name__ == "__main__":
    asyncio.run(main())
