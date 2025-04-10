#!/usr/bin/env python3
import os
import re
import json

def extract_phrases_from_script(script_path):
    """Extract the Russian phrases with topics from the generation script."""
    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the phrases list in the script
    phrases_match = re.search(r'phrases\s*=\s*\[(.*?)\]', content, re.DOTALL)
    if not phrases_match:
        raise Exception("Could not find phrases list in script")
    
    phrases_block = phrases_match.group(1)
    
    phrases_data = []
    # Try to parse each phrase entry as a dictionary
    try:
        # Convert the phrases block to a valid json array
        cleaned_block = "[" + phrases_block + "]"
        # Replace single quotes with double quotes for JSON compatibility
        cleaned_block = cleaned_block.replace("'", '"')
        phrases_data = json.loads(cleaned_block)
    except json.JSONDecodeError:
        # Fallback to regex parsing if JSON parsing fails
        pattern = r'{"text":\s*"([^"]*)",\s*"translation":\s*"([^"]*)",\s*"topic":\s*"([^"]*)"}'
        matches = re.findall(pattern, phrases_block)
        phrases_data = [{"text": r, "translation": t, "topic": topic} for r, t, topic in matches]
    
    return phrases_data

def generate_html(phrases_with_topics, output_dir):
    """Generate the HTML file with audio players for each phrase and topic filtering."""
    # Get unique topics for filtering
    topics = sorted(set(phrase["topic"] for phrase in phrases_with_topics))
    
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
            margin-bottom: 15px;
            padding: 15px;
            border: 1px solid #ddd;
            border-radius: 8px;
            background-color: #f9f9f9;
            display: flex;
            align-items: center;
            flex-wrap: wrap;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        .phrase-content {
            flex: 1;
            min-width: 300px;
            margin-right: 15px;
        }
        .audio-controls {
            display: flex;
            align-items: center;
            gap: 15px;
            padding: 5px;
        }
        .russian {
            font-size: 1.4em;
            margin-bottom: 5px;
            color: #2c3e50;
        }
        .translation {
            color: #7f8c8d;
            margin-bottom: 5px;
            font-size: 1.1em;
        }
        .custom-player {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .play-button {
            background-color: #3498db;
            color: white;
            border: none;
            border-radius: 50%;
            width: 48px;
            height: 48px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2em;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            transition: all 0.2s ease;
        }
        .play-button:hover {
            background-color: #2980b9;
            transform: scale(1.05);
        }
        .play-button:active {
            transform: scale(0.95);
        }
        .loop-button {
            background-color: #2ecc71;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 8px 15px;
            cursor: pointer;
            font-size: 1em;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            transition: all 0.2s ease;
        }
        .loop-button:hover {
            background-color: #27ae60;
            transform: scale(1.05);
        }
        .loop-button:active {
            transform: scale(0.95);
        }
        .loop-active {
            background-color: #e74c3c;
        }
        h1 {
            color: #2c3e50;
            text-align: center;
        }
        .phrase-number {
            color: #95a5a6;
            font-size: 1.1em;
            font-weight: bold;
            margin-left: 5px;
            padding: 5px 10px;
            background-color: #ecf0f1;
            border-radius: 20px;
        }
        .topic-tag {
            background-color: #3498db;
            color: white;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 0.8em;
            margin-right: 8px;
            display: inline-block;
            margin-bottom: 5px;
        }
        .filter-container {
            margin: 20px 0;
            padding: 15px;
            background-color: #f5f5f5;
            border-radius: 8px;
            border: 1px solid #ddd;
        }
        .filter-title {
            font-weight: bold;
            margin-bottom: 10px;
        }
        .topic-filter {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-bottom: 15px;
        }
        .topic-button {
            background-color: #ecf0f1;
            border: 1px solid #bdc3c7;
            border-radius: 20px;
            padding: 5px 15px;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        .topic-button:hover {
            background-color: #d5dbdb;
        }
        .topic-button.active {
            background-color: #3498db;
            color: white;
            border-color: #2980b9;
        }
        .reset-button {
            background-color: #e74c3c;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 8px 15px;
            cursor: pointer;
            transition: all 0.2s ease;
            margin-top: 10px;
        }
        .reset-button:hover {
            background-color: #c0392b;
        }
    </style>
</head>
<body>
    <h1>Russian Audio Phrases</h1>
    <p>Click on the play button to hear each phrase. Toggle the loop button to repeat automatically until stopped.</p>

    <div class="filter-container">
        <div class="filter-title">Filter phrases by topic:</div>
        <div class="topic-filter" id="topicFilter">
"""

    # Add topic filter buttons
    for topic in topics:
        html_content += f'            <button class="topic-button" data-topic="{topic}">{topic}</button>\n'

    html_content += """        </div>
        <button class="reset-button" id="resetFilter">Show All Phrases</button>
    </div>
    
    <!-- Audio phrase containers will be generated here by JavaScript -->
    <div id="phraseContainer">
"""

    # Add each phrase
    for i, phrase in enumerate(phrases_with_topics, start=1):
        html_content += f"""
        <div class="phrase-container" data-topic="{phrase['topic']}">
            <div class="phrase-content">
                <div class="russian">{phrase['text']}</div>
                <div class="translation">{phrase['translation']}</div>
                <span class="topic-tag">{phrase['topic']}</span>
            </div>
            <div class="audio-controls">
                <div class="custom-player">
                    <button class="play-button" data-index="{i}">▶</button>
                    <button class="loop-button" data-index="{i}">Loop</button>
                </div>
                <div class="phrase-number">#{i}</div>
            </div>
            <audio id="audio-{i}">
                <source src="{output_dir}/phrase_{i}.mp3" type="audio/mpeg">
                Your browser does not support the audio element.
            </audio>
        </div>
"""

    html_content += """
    </div>
    
    <script>
        // Add event listeners for play and loop buttons
        document.querySelectorAll('.play-button').forEach(button => {
            button.addEventListener('click', function() {
                const index = this.getAttribute('data-index');
                const audio = document.getElementById(`audio-${index}`);
                
                if (audio.paused) {
                    // Stop all other audio first
                    document.querySelectorAll('audio').forEach(a => {
                        if (!a.paused) {
                            a.pause();
                            a.currentTime = 0;
                            const playButton = document.querySelector(`.play-button[data-index="${a.id.split('-')[1]}"]`);
                            playButton.innerHTML = '▶';
                        }
                    });
                    
                    audio.play();
                    this.innerHTML = '⏸';
                } else {
                    audio.pause();
                    audio.currentTime = 0;
                    this.innerHTML = '▶';
                }
            });
        });

        document.querySelectorAll('.loop-button').forEach(button => {
            button.addEventListener('click', function() {
                const index = this.getAttribute('data-index');
                const audio = document.getElementById(`audio-${index}`);
                
                if (this.classList.contains('loop-active')) {
                    // Deactivate loop
                    this.classList.remove('loop-active');
                    audio.loop = false;
                    if (!audio.paused) {
                        audio.pause();
                        audio.currentTime = 0;
                        const playButton = document.querySelector(`.play-button[data-index="${index}"]`);
                        playButton.innerHTML = '▶';
                    }
                } else {
                    // Activate loop
                    this.classList.add('loop-active');
                    audio.loop = true;
                    if (audio.paused) {
                        audio.play();
                        const playButton = document.querySelector(`.play-button[data-index="${index}"]`);
                        playButton.innerHTML = '⏸';
                    }
                }
            });
        });

        // Handle audio ending event
        document.querySelectorAll('audio').forEach(audio => {
            audio.addEventListener('ended', function() {
                if (!this.loop) {
                    const index = this.id.split('-')[1];
                    const playButton = document.querySelector(`.play-button[data-index="${index}"]`);
                    playButton.innerHTML = '▶';
                }
            });
        });

        // Topic filtering functionality
        document.querySelectorAll('.topic-button').forEach(button => {
            button.addEventListener('click', function() {
                const topic = this.getAttribute('data-topic');
                
                // Update active button state
                document.querySelectorAll('.topic-button').forEach(btn => {
                    btn.classList.remove('active');
                });
                this.classList.add('active');
                
                // Filter phrases
                document.querySelectorAll('.phrase-container').forEach(phrase => {
                    if (phrase.getAttribute('data-topic') === topic) {
                        phrase.style.display = 'flex';
                    } else {
                        phrase.style.display = 'none';
                    }
                });
            });
        });

        // Reset filter
        document.getElementById('resetFilter').addEventListener('click', function() {
            // Show all phrases
            document.querySelectorAll('.phrase-container').forEach(phrase => {
                phrase.style.display = 'flex';
            });
            
            // Remove active state from topic buttons
            document.querySelectorAll('.topic-button').forEach(btn => {
                btn.classList.remove('active');
            });
        });
    </script>
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
        phrases_with_topics = extract_phrases_from_script(script_path)
        print(f"Extracted {len(phrases_with_topics)} phrases from {script_path}")
        
        # Generate HTML content
        html_content = generate_html(phrases_with_topics, output_dir)
        
        # Write to HTML file
        with open(html_output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Successfully updated {html_output_path} with {len(phrases_with_topics)} phrases")
        print(f"Open {os.path.abspath(html_output_path)} in your browser to view the audio player")
    
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 