import telebot
import traceback
import whisper
import subprocess
import os
import logging
from telebot import types

# --- Настройка логов ---
LOG_FOLDER = '.logs'
if not os.path.exists(LOG_FOLDER):
    os.makedirs(LOG_FOLDER)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename=f'{LOG_FOLDER}/app.log'
)
logger = logging.getLogger('telegram-bot')


# --- Загрузка токена ---
def get_bot_token():
    token = os.environ.get('BOT_TOKEN')
    if not token:
        try:
            from config import BOT_TOKEN
            token = BOT_TOKEN
        except ImportError:
            pass
    if not token:
        raise ValueError("Токен бота не найден! Укажите его в config.py или переменных окружения.")
    return token


bot = telebot.TeleBot(get_bot_token())
model = whisper.load_model("small")


# --- Команды ---
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "🎤 *Голосовой бот*\n"
        "Отправьте голосовое сообщение или аудиофайл (MP3, WAV, OGG), "
        "и я преобразую его в текст. Автоматически определяю язык!\n\n"
        "Команды:\n"
        "/help - справка",
        parse_mode='Markdown'
    )


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(
        message.chat.id,
        "❓ *Помощь*\n\n"
        "Поддерживаемые форматы:\n"
        "- Голосовые сообщения\n"
        "- Аудиофайлы (MP3, WAV, OGG)\n\n"
        "Бот не поддерживает: фото, видео, стикеры, GIF-анимации и другие медиафайлы.",
        parse_mode='Markdown'
    )


# --- Обработка неподдерживаемых типов сообщений ---
@bot.message_handler(content_types=[
    'sticker', 'animation', 'video_note',
    'location', 'contact', 'poll', 'dice'
])
def handle_unsupported(message):
    content_type = {
        'sticker': 'стикер',
        'animation': 'GIF-анимацию',
        'video_note': 'кружочек',
        'location': 'геолокацию',
        'contact': 'контакт',
        'poll': 'опрос',
        'dice': 'игральный кубик'
    }.get(message.content_type, 'этот тип сообщения')

    bot.reply_to(
        message,
        f"❌ Я не поддерживаю {content_type}.\n\n"
        "Я умею работать только с голосовыми сообщениями и аудиофайлами (MP3, WAV, OGG).\n"
        "Попробуйте отправить мне аудио или используйте /help для справки."
    )


# --- Обработка медиафайлов (фото, видео) ---
@bot.message_handler(content_types=['photo', 'video'])
def handle_media(message):
    if message.photo:
        bot.reply_to(message, "📷 Я вижу фото, но работаю только с аудио! Отправьте голосовое сообщение или аудиофайл.")
    elif message.video:
        bot.reply_to(message, "🎥 Я вижу видео, но работаю только с аудио! Отправьте голосовое сообщение или аудиофайл.")


# --- Обработка текстовых сообщений ---
@bot.message_handler(content_types=['text'])
def handle_text(message):
    bot.reply_to(
        message,
        "🤖 Я бот для распознавания голоса!\n\n"
        "Отправьте мне голосовое сообщение или аудиофайл (MP3, WAV, OGG), "
        "и я преобразую его в текст.\n\n"
        "Используйте /help для получения справки.",
        parse_mode='Markdown'
    )


# --- Обработка аудио ---
@bot.message_handler(content_types=['voice', 'audio', 'document'])
def handle_audio(message):
    try:
        # Определяем тип файла
        if message.voice:
            file_id = message.voice.file_id
            file_ext = "ogg"
        elif message.audio:
            file_id = message.audio.file_id
            file_ext = message.audio.file_name.split('.')[-1]
        elif message.document and message.document.mime_type.startswith('audio/'):
            file_id = message.document.file_id
            file_ext = message.document.file_name.split('.')[-1]
        else:
            bot.reply_to(message, "❌ Поддерживаются только аудиофайлы (MP3, WAV, OGG).")
            return

        # Проверка расширения
        if file_ext not in ["mp3", "ogg", "wav"]:
            bot.reply_to(message, "❌ Формат не поддерживается. Нужен MP3, WAV или OGG.")
            return

        # Скачивание файла
        file_info = bot.get_file(file_id)
        bot.send_chat_action(message.chat.id, 'typing')
        downloaded_file = bot.download_file(file_info.file_path)
        input_file = f"audio.{file_ext}"

        with open(input_file, 'wb') as f:
            f.write(downloaded_file)

        # Конвертация в MP3 (если нужно)
        if file_ext != "mp3":
            subprocess.run(['ffmpeg', '-i', input_file, 'audio.mp3', '-y'], check=True)
            audio_file = "audio.mp3"
        else:
            audio_file = input_file

        # Распознавание текста
        result = model.transcribe(audio_file)
        text = result["text"]
        language = result["language"]

        # Отправка результата
        bot.reply_to(
            message,
            f"🔊 *Результат ({language})*:\n\n{text}",
            parse_mode='Markdown'
        )

    except subprocess.CalledProcessError:
        bot.reply_to(message, "❌ Ошибка конвертации аудио. Убедитесь, что установлен FFmpeg.")
        logger.error("FFmpeg не установлен!")
    except Exception as e:
        bot.reply_to(message, "❌ Ошибка распознавания. Попробуйте ещё раз.")
        logger.error(f"Ошибка: {e}\n{traceback.format_exc()}")
    finally:
        # Удаление временных файлов
        for f in ["audio.mp3", "audio.ogg", "audio.wav"]:
            if os.path.exists(f):
                os.remove(f)


if __name__ == '__main__':
    logger.info("Бот запущен")
    bot.infinity_polling()
