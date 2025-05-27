import sys
import asyncio
import discord
from discord.ext import commands

# Вставьте сюда ваш user token (например: abc.def.ghi)
TOKEN = ""

# ID чата (DM-канала), в котором нужно удалить все ваши сообщения
DM_CHANNEL_ID = XXXX  # замените на нужный ID канала

# Проверка формата токена
if "." not in TOKEN or len(TOKEN) < 20:
    print("Ошибка: похоже, вы вставили не user token. Проверьте правильность токена.")
    sys.exit(1)

# Инициализация self-бота
bot = commands.Bot(command_prefix="!", self_bot=True)

@bot.event
async def on_ready():
    print(f"Запущен как {bot.user} (ID {bot.user.id})")

    try:
        channel = await bot.fetch_channel(DM_CHANNEL_ID)
    except Exception as e:
        print(f"Не удалось получить DM-канал по ID {DM_CHANNEL_ID}: {e}")
        await bot.close()
        return

    deleted = 0
    async for msg in channel.history(limit=None):
        if msg.author.id == bot.user.id:
            try:
                await msg.delete()
                deleted += 1
                await asyncio.sleep(1)  # задержка для избежания rate limit
            except Exception as e:
                print(f"Ошибка удаления {msg.id}: {e}")

    print(f"Готово. Удалено {deleted} сообщений.")
    await bot.close()

if __name__ == "__main__":
    try:
        bot.run(TOKEN)
    except discord.errors.LoginFailure:
        print("Ошибка входа: токен неверный или просрочен.")
        sys.exit(1)
    except Exception as e:
        print(f"Неожиданная ошибка при запуске: {e}")
        sys.exit(1)
