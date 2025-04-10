#!/usr/bin/env python3
import re
import os
import sys
import subprocess

def fix_phrases_format():
    """
    Fix the generate_russian_audio.py file by converting string-formatted phrases to dictionary format
    and automatically detecting their topics.
    """
    input_file = "generate_russian_audio.py"
    backup_file = "generate_russian_audio.py.bak"
    
    # Create a backup of the original file
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        with open(backup_file, 'w', encoding='utf-8') as f:
            f.write(original_content)
        print(f"✅ Created backup at {backup_file}")
    except Exception as e:
        print(f"❌ Error creating backup: {e}")
        return

    # Find the phrases list
    phrases_match = re.search(r'phrases\s*=\s*\[(.*?)\]', original_content, re.DOTALL)
    if not phrases_match:
        print("❌ Could not find phrases list in the script")
        return
        
    phrases_block = phrases_match.group(1)
    
    # Find any lines that are in string format instead of dictionary format
    string_entries = []
    for line in phrases_block.split('\n'):
        # Skip dictionary entries and empty lines
        if '{' in line or '}' in line or not line.strip():
            continue
            
        # Look for string entries with comments
        string_match = re.search(r'\s*"([^"]+)"\s*,?\s*#\s*(.*?)$', line.strip())
        if string_match:
            russian_text = string_match.group(1)
            translation = string_match.group(2).strip()
            string_entries.append((russian_text, translation))
    
    if not string_entries:
        print("✅ No string format phrases found - everything is already in dictionary format")
        return
    
    # Detect topics for string entries
    def detect_topic(text, translation):
        """Simple topic detection based on keywords in text or translation"""
        # Define keywords for each topic
        topic_keywords = {
            "Directions": ["где", "как пройти", "направо", "налево", "прямо", "поверните", "угол", "turn", "where is", "how do i get", "corner", "straight", "right", "left", "далеко", "потерялся", "lost", "far"],
            "Greetings": ["привет", "здравствуйте", "доброе утро", "добрый день", "добрый вечер", "пока", "до свидания", "hello", "hi", "bye", "goodbye", "morning", "evening", "afternoon"],
            "Restaurant": ["ресторан", "меню", "счет", "заказ", "restaurant", "menu", "bill", "order", "food", "eat"],
            "Shopping": ["магазин", "купить", "сколько стоит", "дорого", "скидк", "shop", "buy", "cost", "expensive", "discount"],
            "Emergency": ["помощь", "помогите", "экстренный", "help", "emergency", "urgent", "doctor"],
            "Language": ["говорить", "понимать", "русский", "язык", "speak", "understand", "language", "russian"],
            "Food": ["еда", "вкусно", "блюдо", "food", "tasty", "dish", "eat", "drink"],
            "Money": ["деньги", "рубли", "наличн", "карты", "money", "cash", "card", "rubles", "euros"],
            "Conversation": ["как дела", "хорошо", "плохо", "так себе", "how are you", "good", "bad", "so-so"],
            "Common Phrases": ["пожалуйста", "спасибо", "извините", "да", "нет", "please", "thank you", "sorry", "yes", "no"]
        }
        
        text_lower = text.lower()
        translation_lower = translation.lower()
        combined = text_lower + " " + translation_lower
        
        # Score each topic by counting keyword matches
        topic_scores = {}
        for topic, keywords in topic_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword.lower() in combined:
                    score += 1
            if score > 0:
                topic_scores[topic] = score
        
        # Return the topic with the highest score, or "Common Phrases" if no matches
        if topic_scores:
            return max(topic_scores.items(), key=lambda x: x[1])[0]
        return "Directions"  # Default to Directions for navigation-related phrases
    
    # Process each string entry
    converted_entries = []
    for i, (russian_text, translation) in enumerate(string_entries):
        topic = detect_topic(russian_text, translation)
        converted_entries.append(f'    {{"text": "{russian_text}", "translation": "{translation}", "topic": "{topic}"}}')
    
    # Replace string entries with dictionary entries
    new_phrases_block = phrases_block
    for i, line in enumerate(phrases_block.split('\n')):
        # Skip dictionary entries and empty lines
        if '{' in line or '}' in line or not line.strip():
            continue
            
        # Look for string entries with comments
        string_match = re.search(r'\s*"([^"]+)"\s*,?\s*#\s*(.*?)$', line.strip())
        if string_match:
            # Get the indentation
            indentation = re.match(r'(\s*)', line).group(1)
            # Replace this line with the converted entry plus a comma if needed
            converted_entry = converted_entries.pop(0)
            if i < len(phrases_block.split('\n')) - 1:  # Not the last line
                converted_entry += ','
            new_phrases_block = new_phrases_block.replace(line, indentation + converted_entry)
    
    # Replace the old phrases block in the original content
    new_content = original_content.replace(phrases_match.group(0), f'phrases = [\n{new_phrases_block}\n]')
    
    # Write the updated content back to the file
    try:
        with open(input_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✅ Successfully fixed {input_file}")
        print(f"   - Converted {len(string_entries)} string phrases to dictionary format")
        print(f"   - Automatically detected topics for new phrases")
        
        # Update the HTML player with the new phrases
        update_html_player()
        
    except Exception as e:
        print(f"❌ Error writing to {input_file}: {e}")
        print(f"   Original file is preserved in {backup_file}")

def update_html_player():
    """Run the update_audio_player.py script to update the HTML file"""
    print("\n📝 Updating HTML audio player...")
    try:
        result = subprocess.run(['python3', 'update_audio_player.py'], 
                               capture_output=True, text=True, check=True)
        print(result.stdout)
        print("✅ HTML player updated successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error updating HTML player: {e}")
        print(f"Error output: {e.stderr}")
    except Exception as e:
        print(f"❌ Error: {e}")

def generate_new_audio():
    """Generate audio for any new phrases"""
    print("\n🔊 Generating audio for new phrases...")
    try:
        result = subprocess.run(['python3', 'generate_russian_audio.py'], 
                               capture_output=True, text=True, check=True)
        print(result.stdout)
        print("✅ Audio files generated successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error generating audio: {e}")
        print(f"Error output: {e.stderr}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🔄 Russian Phrases Script Fixer")
    print("============================")
    fix_phrases_format()
    
    # Ask user if they want to generate audio files for new phrases
    response = input("\nDo you want to generate audio for any new phrases? (y/n): ")
    if response.lower() == 'y':
        generate_new_audio() 