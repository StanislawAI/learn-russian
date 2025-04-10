from gtts import gTTS
import os
import sys

# Debug print for the current directory
print(f"Current working directory: {os.getcwd()}")

# List of Russian phrases
phrases = [
    "Привет!",
    "Здравствуйте!",
    "Доброе утро",
    "Добрый день",
    "Добрый вечер",
    "Пока!",
    "До свидания",
    "Как тебя зовут?",
    "Меня зовут Станислав",
    "Очень приятно",
    "Как дела?",
    "Хорошо",
    "Так себе",
    "Плохо",
    "Ты говоришь по-русски?",
    "Да, немного",
    "Где туалет?",
    "Сколько это стоит?",
    "Я не понимаю",
    "Пожалуйста",
    "Спасибо",
    "Извините",
    "Что будете заказывать?",
    "Я хочу кофе, пожалуйста",
    "С вас 200 рублей",
    "Сколько это в евро?",
    "Вот, пожалуйста"
]

# Create output directory
output_dir = "russian_audio"
print(f"Creating directory: {output_dir}")
os.makedirs(output_dir, exist_ok=True)

# Generate and save each phrase as MP3
print("Starting to generate audio files...")
for i, phrase in enumerate(phrases, start=1):
    try:
        print(f"Generating audio for phrase {i}: {phrase}")
        tts = gTTS(text=phrase, lang='ru')
        file_path = os.path.join(output_dir, f"phrase_{i}.mp3")
        tts.save(file_path)
        print(f"Saved: {file_path}")
    except Exception as e:
        print(f"Error generating audio for phrase {i}: {e}", file=sys.stderr)

print("\n✅ All audio files generated!")
print(f"Audio files should be in: {os.path.abspath(output_dir)}")