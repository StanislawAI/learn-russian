#!/usr/bin/env python3
import os
import re

def extract_phrases_from_script(script_path):
    """Extract the Russian phrases from the generation script."""
    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the phrases list in the script
    phrases_match = re.search(r'phrases\s*=\s*\[(.*?)\]', content, re.DOTALL)
    if not phrases_match:
        raise Exception("Could not find phrases list in script")
    
    phrases_block = phrases_match.group(1)
    
    # Extract each phrase and its comment
    phrase_pattern = r'"([^"]*)",\s*#\s*(.*?)$'
    phrases_with_translations = []
    
    for line in phrases_block.split('\n'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        
        match = re.search(phrase_pattern, line)
        if match:
            russian_text = match.group(1)
            translation = match.group(2).strip()
            phrases_with_translations.append((russian_text, translation))
        else:
            # Try to extract just the Russian phrase without a comment
            phrase_only_match = re.search(r'"([^"]*)"', line)
            if phrase_only_match:
                russian_text = phrase_only_match.group(1)
                phrases_with_translations.append((russian_text, ""))
    
    return phrases_with_translations

def generate_html(phrases_with_translations, output_dir):
    """Generate the HTML file with audio players for each phrase."""
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Russian Audio Phrases</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
        }
        .phrase-container {
            margin-bottom: 20px;
            padding: 15px;
            border: 1px solid #ddd;
            border-radius: 5px;
            background-color: #f9f9f9;
        }
        .russian {
            font-size: 1.5em;
            margin-bottom: 5px;
            color: #2c3e50;
        }
        .translation {
            color: #7f8c8d;
            margin-bottom: 10px;
        }
        audio {
            width: 100%;
        }
        h1 {
            color: #2c3e50;
            text-align: center;
        }
        .phrase-number {
            color: #95a5a6;
            font-size: 0.8em;
            float: right;
        }
    </style>
</head>
<body>
    <h1>Russian Audio Phrases</h1>
    <p>Click on the audio players to hear each phrase pronounced in Russian.</p>
"""

    for i, (phrase, translation) in enumerate(phrases_with_translations, start=1):
        html_content += f"""
    <div class="phrase-container">
        <div class="phrase-number">#{i}</div>
        <div class="russian">{phrase}</div>
        <div class="translation">{translation}</div>
        <audio controls>
            <source src="{output_dir}/phrase_{i}.mp3" type="audio/mpeg">
            Your browser does not support the audio element.
        </audio>
    </div>
"""

    html_content += """
</body>
</html>
"""
    return html_content

def main():
    script_path = "generate_russian_audio.py"
    output_dir = "russian_audio"  # This should match the directory in the script
    html_output_path = "russian-audio-player.html"
    
    # Extract phrases from the script
    try:
        phrases_with_translations = extract_phrases_from_script(script_path)
        print(f"Extracted {len(phrases_with_translations)} phrases from {script_path}")
        
        # Generate HTML content
        html_content = generate_html(phrases_with_translations, output_dir)
        
        # Write to HTML file
        with open(html_output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Successfully updated {html_output_path} with {len(phrases_with_translations)} phrases")
        print(f"Open {os.path.abspath(html_output_path)} in your browser to view the audio player")
    
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 