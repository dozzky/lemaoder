import asyncio
from collections import Counter
from twitchio.ext import commands
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Глобальный счетчик для эмотов
emote_counter = Counter()

# Список эмотов для отслеживания
tracked_emotes = ["Kappa", "PogChamp", "LUL", "FeelsBadMan", "FeelsGoodMan"]

# Конфигурация графика
fig, ax = plt.subplots()

# Обновление графика
def update_chart(frame):
    ax.clear()  # Очистка графика перед обновлением
    ax.set_title("Количество эмотов в чате Twitch")
    ax.set_xlabel("Эмоты")
    ax.set_ylabel("Частота")
    ax.set_ylim(0, max(emote_counter.values(), default=10))  # Ограничение по Y

    # Получение данных для графика
    emotes, counts = zip(*[(emote, emote_counter[emote]) for emote in tracked_emotes]) if emote_counter else ([], [])
    ax.bar(emotes, counts, color="skyblue")

# Twitch Bot
class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            token="",  # Замените на ваш токен
            prefix="!",
            initial_channels=["quin69"]  # Замените на имя вашего канала
        )

    async def event_ready(self):
        print(f"Bot is ready | Logged in as {self.nick}")

    async def event_message(self, message):
        if message.echo:
            return

        # Считываем все слова сообщения
        words = message.content.split()

        # Фильтруем только эмоты из списка tracked_emotes
        for word in words:
            if word in tracked_emotes:
                emote_counter[word] += 1

        # Выводим сообщение в консоль (опционально)
        print(f"{message.author.name}: {message.content}")

# Создание и запуск бота
bot = Bot()

# Запуск анимации
ani = FuncAnimation(fig, update_chart, interval=1000, cache_frame_data=False)

async def main():
    plt.ion()  # Включение интерактивного режима
    plt.show(block=False)  # Показать график в неблокирующем режиме
    await bot.start()

# Основной запуск
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError:  # Если цикл уже запущен
        import nest_asyncio
        nest_asyncio.apply()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
