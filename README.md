<h1>🎤 Telegram Voice-to-Text Bot</h1>

  <p>Этот бот позволяет пользователям Telegram отправлять голосовые сообщения или аудиофайлы (MP3, WAV, OGG), 
  которые будут автоматически преобразованы в текст с помощью модели 
  <a href="https://github.com/openai/whisper" target="_blank">OpenAI Whisper</a>.</p>

  <h2>🚀 Возможности</h2>
  <ul>
    <li>Поддержка форматов: <code>.mp3</code>, <code>.wav</code>, <code>.ogg</code></li>
    <li>Автоматическое определение языка</li>
    <li>Распознавание с использованием модели Whisper (<code>small</code>)</li>
    <li>Безопасная обработка: данные не сохраняются</li>
    <li>Логи ошибок и событий</li>
  </ul>

  <h2>🛠️ Установка</h2>
  <ol>
    <li>
      <p>Клонируйте репозиторий:</p>
      <pre><code>git clone https://github.com/your-username/telegram-voice-bot.git
cd telegram-voice-bot</code></pre>
    </li>
    <li>
      <p>Установите зависимости:</p>
      <pre><code>pip install -r requirements.txt</code></pre>
    </li>
    <li>
      <p><strong>Установите FFmpeg</strong>, если он не установлен:</p>
      <p><strong>Linux / macOS:</strong></p>
      <pre><code>sudo apt install ffmpeg</code></pre>
      <p><strong>Windows:</strong> скачайте с <a href="https://ffmpeg.org/download.html" target="_blank">официального сайта FFmpeg</a> и добавьте ffmpeg.exe в системный PATH.</p>
    </li>
    <li>
      <p>Настройте токен бота:</p>
      <p>Создайте файл <code>config.py</code> и добавьте в него ваш токен:</p>
      <pre><code>BOT_TOKEN = "ваш_токен_бота"</code></pre>
      <p>Или установите переменную окружения:</p>
      <pre><code>export BOT_TOKEN=ваш_токен_бота</code></pre>
    </li>
  </ol>

  <h2>▶️ Запуск</h2>
  <pre><code>python bot.py</code></pre>

  <h2>📦 Структура проекта</h2>
  <pre><code>.
├── bot.py             # Основной код Telegram-бота
├── config.py          # (опционально) токен бота
├── .logs/             # Папка для логов
└── requirements.txt   # Зависимости Python
  </code></pre>

  <h2>🧠 Используемые технологии</h2>
  <ul>
    <li><a href="https://github.com/eternnoir/pyTelegramBotAPI" target="_blank">python-telegram-bot</a></li>
    <li><a href="https://github.com/openai/whisper" target="_blank">OpenAI Whisper</a></li>
    <li>FFmpeg для конвертации аудио</li>
    <li>Модуль <code>logging</code> для логирования</li>
  </ul>

  <h2>❗ Важно</h2>
  <p>Убедитесь, что вы не загружаете конфиденциальные данные.</p>
  <p>Аудиофайлы временно сохраняются и автоматически удаляются после обработки.</p>

  <h2>📜 Лицензия</h2>
  <p>MIT License</p>
