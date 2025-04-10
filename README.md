# Learn Russian

A simple set of Python scripts to help learn Russian vocabulary by generating audio phrases and providing an interactive HTML audio player.

## Features

*   Generates MP3 audio files for Russian phrases using Google Text-to-Speech (gTTS).
*   Provides a simple HTML interface (`add_phrase.html`) to help format new phrases correctly.
*   Updates an HTML audio player (`russian-audio-player.html`) with all phrases, categorized by topic and including playback controls.
*   Includes a reference section for the Russian (Cyrillic) alphabet in the audio player.
*   Combines all steps (audio generation, player update) into a single script (`run_all.py`).

## Project Structure

```
.learn-russian/
├── venv/                   # Python Virtual Environment
├── russian_audio/          # Directory for generated MP3 files
├── add_phrase.html         # Helper page to format new phrases
├── generate_russian_audio.py # Script containing phrases and generating audio
├── generate_russian_audio.py.bak # Backup of the phrase script
├── README.md               # This file
├── requirements.txt        # Python dependencies
├── run_all.py              # Main script to run all steps
├── russian-audio-player.html # The generated HTML audio player
└── update_audio_player.py  # Script to update the HTML player
```

## Setup

1.  **Clone the Repository (if applicable):**
    ```bash
    # git clone <repository-url>
    # cd learn-russian
    ```

2.  **Create and Activate Virtual Environment:**
    This project uses a Python virtual environment (`venv`) to manage dependencies. If you don't have one set up yet:
    ```bash
    python3 -m venv venv 
    ```
    Activate the environment:
    *   macOS/Linux: `source venv/bin/activate`
    *   Windows (Git Bash): `source venv/Scripts/activate`
    *   Windows (Command Prompt): `venv\Scripts\activate.bat`
    *   Windows (PowerShell): `venv\Scripts\Activate.ps1`
    You should see `(venv)` at the beginning of your terminal prompt.

3.  **Install Dependencies:**
    Make sure your virtual environment is active, then install the required libraries:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

**Adding New Phrases:**

1.  Open the `add_phrase.html` file in your web browser.
2.  Paste one or more phrases into the top text area. Each phrase *must* be on its own line and follow the format:
    ```
    "Russian Text Here" # English Translation Here
    ```
3.  Enter a single **Topic** for all the phrases you pasted.
4.  Click the **"Generate Python Strings"** button.
5.  The correctly formatted Python dictionary strings will appear in the bottom text area.
6.  Click the **"Copy to Clipboard"** button.
7.  Open the `generate_russian_audio.py` file in your code editor.
8.  Locate the `phrases = [` list.
9.  Paste the copied block of strings **inside** the list, usually just before the closing square bracket `]`.
10. **Ensure the last phrase entry in the entire list does *not* have a trailing comma.** All other entries *must* end with a comma.
11. Save the `generate_russian_audio.py` file.

**Generating Audio & Updating Player:**

1.  Make sure your virtual environment is **active** (`source venv/bin/activate` or equivalent).
2.  Run the main script:
    ```bash
    python3 run_all.py
    ```
3.  This will:
    *   Run `generate_russian_audio.py` to create/update `.mp3` files in the `russian_audio/` directory.
    *   Run `update_audio_player.py` to regenerate the `russian-audio-player.html` file.
    *   Automatically open the updated `russian-audio-player.html` in your default web browser.

## Dependencies

*   **gTTS:** Google Text-to-Speech library, used to generate the audio files. (`pip install gTTS`)

*(Note: The scripts themselves use standard Python libraries like `os`, `sys`, `re`, `subprocess`, `json`, `webbrowser` which don't require separate installation if you have Python 3 installed.)*
