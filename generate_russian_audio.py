from gtts import gTTS
import os
import sys

# Debug print for the current directory
print(f"Current working directory: {os.getcwd()}")

# List of Russian phrases
phrases = [
    "Привет!",                # Hello!
    "Здравствуйте!",          # Hello! (formal)
    "Доброе утро",            # Good morning
    "Добрый день",            # Good afternoon
    "Добрый вечер",           # Good evening
    "Пока!",                  # Bye!
    "До свидания",            # Goodbye (formal)
    "Как тебя зовут?",        # What's your name?
    "Меня зовут Станислав",   # My name is Stanislav
    "Очень приятно",          # Nice to meet you
    "Как дела?",              # How are you?
    "Хорошо",                 # Good
    "Так себе",               # So-so
    "Плохо",                  # Bad
    "Ты говоришь по-русски?", # Do you speak Russian?
    "Да, немного",            # Yes, a little
    "Где туалет?",            # Where is the bathroom?
    "Сколько это стоит?",     # How much does this cost?
    "Я не понимаю",           # I don't understand
    "Пожалуйста",             # Please
    "Спасибо",                # Thank you
    "Извините",               # Excuse me/Sorry
    "Что будете заказывать?", # What would you like to order?
    "Я хочу кофе, пожалуйста", # I would like coffee, please
    "С вас 200 рублей",       # That will be 200 rubles
    "Сколько это в евро?",    # How much is that in euros?
    "Вот, пожалуйста",        # Here you go
    "Я учу русский язык",     # I am learning Russian
    "Мне нравится русская культура", # I like Russian culture
    "Я хочу говорить по-русски", # I want to speak Russian
    "Русский язык сложный",   # Russian language is difficult
    "Но очень интересный",    # But very interesting
    "Чили",                   # Chili
    "Перец",                  # Pepper
    "Суп",                    # Soup
    "Ресторан",               # Restaurant
    "Я голоден",              # I'm hungry
    "Очень вкусно",           # Very tasty
    "Я бы хотел борщ, пожалуйста.",  # I would like borscht, please.
    "Меню, пожалуйста.",      # The menu, please.
    "Что вы порекомендуете?", # What would you recommend?
    "Можно мне…?",           # Can I have...?
    "Я возьму…",             # I'll take…
    "Счёт, пожалуйста.",      # The bill, please.
    "Где туалет?",            # Where is the toilet?
    "Это острое?",            # Is this spicy?
    "У вас есть вегетарианские блюда?", # Do you have vegetarian dishes?
    "Мне нужна помощь.",      # I need help.
    "Пожалуйста",             # Please / You're welcome
    "Спасибо",                # Thank you
    "Извините"                # Excuse me / I'm sorry
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