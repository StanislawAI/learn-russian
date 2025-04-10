from gtts import gTTS
import os
import sys

# Debug print for the current directory
print(f"Current working directory: {os.getcwd()}")

# List of Russian phrases with topics/lessons
phrases = [


    {"text": "Привет!", "translation": "Hello!", "topic": "Greetings"},
    {"text": "Здравствуйте!", "translation": "Hello! (formal)", "topic": "Greetings"},
    {"text": "Доброе утро", "translation": "Good morning", "topic": "Greetings"},
    {"text": "Добрый день", "translation": "Good afternoon", "topic": "Greetings"},
    {"text": "Добрый вечер", "translation": "Good evening", "topic": "Greetings"},
    {"text": "Пока!", "translation": "Bye!", "topic": "Greetings"},
    {"text": "До свидания", "translation": "Goodbye (formal)", "topic": "Greetings"},
    {"text": "Как тебя зовут?", "translation": "What's your name?", "topic": "Introduction"},
    {"text": "Меня зовут Станислав", "translation": "My name is Stanislav", "topic": "Introduction"},
    {"text": "Очень приятно", "translation": "Nice to meet you", "topic": "Introduction"},
    {"text": "Как дела?", "translation": "How are you?", "topic": "Conversation"},
    {"text": "Хорошо", "translation": "Good", "topic": "Conversation"},
    {"text": "Так себе", "translation": "So-so", "topic": "Conversation"},
    {"text": "Плохо", "translation": "Bad", "topic": "Conversation"},
    {"text": "Ты говоришь по-русски?", "translation": "Do you speak Russian?", "topic": "Language"},
    {"text": "Да, немного", "translation": "Yes, a little", "topic": "Language"},
    {"text": "Где туалет?", "translation": "Where is the bathroom?", "topic": "Directions"},
    {"text": "Сколько это стоит?", "translation": "How much does this cost?", "topic": "Shopping"},
    {"text": "Я не понимаю", "translation": "I don't understand", "topic": "Language"},
    {"text": "Пожалуйста", "translation": "Please", "topic": "Common Phrases"},
    {"text": "Спасибо", "translation": "Thank you", "topic": "Common Phrases"},
    {"text": "Извините", "translation": "Excuse me / I'm sorry", "topic": "Common Phrases"},
    {"text": "Что будете заказывать?", "translation": "What would you like to order?", "topic": "Restaurant"},
    {"text": "Я хочу кофе, пожалуйста", "translation": "I would like coffee, please", "topic": "Restaurant"},
    {"text": "С вас 200 рублей", "translation": "That will be 200 rubles", "topic": "Money"},
    {"text": "Сколько это в евро?", "translation": "How much is that in euros?", "topic": "Money"},
    {"text": "Вот, пожалуйста", "translation": "Here you go", "topic": "Common Phrases"},
    {"text": "Я учу русский язык", "translation": "I am learning Russian", "topic": "Language"},
    {"text": "Мне нравится русская культура", "translation": "I like Russian culture", "topic": "Culture"},
    {"text": "Я хочу говорить по-русски", "translation": "I want to speak Russian", "topic": "Language"},
    {"text": "Русский язык сложный", "translation": "Russian language is difficult", "topic": "Language"},
    {"text": "Но очень интересный", "translation": "But very interesting", "topic": "Language"},
    {"text": "Чили", "translation": "Chili", "topic": "Food"},
    {"text": "Перец", "translation": "Pepper", "topic": "Food"},
    {"text": "Суп", "translation": "Soup", "topic": "Food"},
    {"text": "Ресторан", "translation": "Restaurant", "topic": "Food"},
    {"text": "Я голоден", "translation": "I'm hungry", "topic": "Food"},
    {"text": "Очень вкусно", "translation": "Very tasty", "topic": "Food"},
    {"text": "Я бы хотел борщ, пожалуйста.", "translation": "I would like borscht, please.", "topic": "Restaurant"},
    {"text": "Меню, пожалуйста.", "translation": "The menu, please.", "topic": "Restaurant"},
    {"text": "Что вы порекомендуете?", "translation": "What would you recommend?", "topic": "Restaurant"},
    {"text": "Можно мне…?", "translation": "Can I have...?", "topic": "Restaurant"},
    {"text": "Я возьму…", "translation": "I'll take…", "topic": "Restaurant"},
    {"text": "Счёт, пожалуйста.", "translation": "The bill, please.", "topic": "Restaurant"},
    {"text": "Где туалет?", "translation": "Where is the toilet?", "topic": "Directions"},
    {"text": "Это острое?", "translation": "Is this spicy?", "topic": "Food"},
    {"text": "У вас есть вегетарианские блюда?", "translation": "Do you have vegetarian dishes?", "topic": "Food"},
    {"text": "Мне нужна помощь.", "translation": "I need help.", "topic": "Emergency"},
    {"text": "Пожалуйста", "translation": "Please / You're welcome", "topic": "Common Phrases"},
    {"text": "Спасибо", "translation": "Thank you", "topic": "Common Phrases"},
    {"text": "Извините", "translation": "Excuse me / I'm sorry", "topic": "Common Phrases"},
    {"text": "Сколько стоит?", "translation": "How much does it cost?", "topic": "Shopping"},
    {"text": "Это дорого!", "translation": "This is expensive!", "topic": "Shopping"},
    {"text": "Могу я получить скидку?", "translation": "Can I get a discount?", "topic": "Shopping"},
    {"text": "Я возьму это.", "translation": "I'll take this.", "topic": "Shopping"},
    {"text": "Где я могу купить…?", "translation": "Where can I buy…?", "topic": "Shopping"},
    {"text": "Я ищу…", "translation": "I'm looking for…", "topic": "Shopping"},
    {"text": "У вас есть…?", "translation": "Do you have…?", "topic": "Shopping"},
    {"text": "Это свежие продукты?", "translation": "Are these fresh products?", "topic": "Shopping"},
    {"text": "Вы принимаете карты?", "translation": "Do you accept cards?", "topic": "Money"},
    {"text": "Да, конечно.", "translation": "Yes, of course.", "topic": "Common Phrases"},
    {"text": "Нет, только наличными.", "translation": "No, only cash.", "topic": "Money"},
    {"text": "Спасибо за помощь.", "translation": "Thank you for the help.", "topic": "Common Phrases"},
    {"text": "До свидания!", "translation": "Goodbye!", "topic": "Greetings"},
    {"text": "Где находится…?", "translation": "Where is … located?", "topic": "Directions"},
    {"text": "Как пройти к…?", "translation": "How do I get to …?", "topic": "Directions"},
    {"text": "Сколько времени до…?", "translation": "How much time to …?", "topic": "Directions"},
    {"text": "Это далеко?", "translation": "Is it far?", "topic": "Directions"},
    {"text": "Я потерялся.", "translation": "I'm lost.", "topic": "Directions"},
    {"text": "Можете помочь мне?", "translation": "Can you help me?", "topic": "Emergency"},
    {"text": "Поверните направо/налево.", "translation": "Turn right/left.", "topic": "Directions"},
    {"text": "Идите прямо.", "translation": "Go straight.", "topic": "Directions"},
    {"text": "Поверните на следующий угол.", "translation": "Turn at the next corner.", "topic": "Directions"},
    {"text": "Это будет справа/слева.", "translation": "It will be on the right/left.", "topic": "Directions"},
    {"text": "Я заблудился.", "translation": "I am lost.", "topic": "Directions"},
    {"text": "Я изучаю русский язык.", "translation": "I am studying Russian language.", "topic": "Language"},
        {"text": "У меня бронь.", "translation": "I have a reservation.", "topic": "Directions"},
        {"text": "Я забронировал номер.", "translation": "I booked a room.", "topic": "Directions"},
        {"text": "На какое имя?", "translation": "Under which name?", "topic": "Greetings"},
        {"text": "Я хочу забронировать номер.", "translation": "I would like to book a room.", "topic": "Directions"},
        {"text": "Есть ли у вас свободные номера?", "translation": "Do you have any available rooms?", "topic": "Directions"},
        {"text": "Где мой номер?", "translation": "Where is my room?", "topic": "Directions"},
        {"text": "У меня проблемы с Wi-Fi.", "translation": "I have a problem with the Wi-Fi.", "topic": "Directions"},
        {"text": "Могу я получить ключ от другого номера?", "translation": "Can I get the key to another room?", "topic": "Common Phrases"},
        {"text": "Я хочу выселиться.", "translation": "I would like to check out.", "topic": "Directions"},
        {"text": "Сколько я должен заплатить?", "translation": "How much do I owe?", "topic": "Directions"},
        {"text": "Спасибо за ваше обслуживание.", "translation": "Thank you for your service.", "topic": "Common Phrases"},
    {"text": "Сколько это стоит?", "translation": "How much does it cost?", "topic": "Shopping"},
    {"text": "У вас есть другой размер?", "translation": "Do you have another size?", "topic": "Shopping"},
    {"text": "Я примерю это.", "translation": "I'll try this on.", "topic": "Shopping"},
    {"text": "Где примерочная?", "translation": "Where is the fitting room?", "topic": "Shopping"},
    {"text": "Это слишком дорого.", "translation": "This is too expensive.", "topic": "Shopping"},
    {"text": "Можно скидку?", "translation": "Can I get a discount?", "topic": "Shopping"},
    {"text": "Я возьму это.", "translation": "I'll take this.", "topic": "Shopping"}
]

# Create output directory
output_dir = "russian_audio"
print(f"Creating directory: {output_dir}")
os.makedirs(output_dir, exist_ok=True)

# Generate and save each phrase as MP3
print("Starting to generate audio files...")
for i, phrase in enumerate(phrases, start=1):
    try:
        print(f"Generating audio for phrase {i}: {phrase['text']}")
        tts = gTTS(text=phrase['text'], lang='ru')
        file_path = os.path.join(output_dir, f"phrase_{i}.mp3")
        tts.save(file_path)
        print(f"Saved: {file_path}")
    except Exception as e:
        print(f"Error generating audio for phrase {i}: {e}", file=sys.stderr)

print("\n✅ All audio files generated!")
print(f"Audio files should be in: {os.path.abspath(output_dir)}")