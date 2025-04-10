#!/usr/bin/env python3

import subprocess
import webbrowser
import os
import sys

def run_script(script_name, input_text=None):
    """Runs a Python script using the same Python interpreter and checks for errors.
    
    Args:
        script_name: Name of the Python script to run
        input_text: Optional text to provide as input to the script
    """
    print(f"Running {script_name}...")
    try:
        # Use sys.executable to ensure the same Python interpreter is used
        process = subprocess.Popen(
            [sys.executable, script_name],
            stdin=subprocess.PIPE if input_text else None,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        stdout, stderr = process.communicate(input=input_text)
        
        print(f"Successfully ran {script_name}.")
        print(f"Output:\n{stdout}")
        
        if process.returncode != 0:
            print(f"Error running {script_name}:")
            print(stderr)
            sys.exit(f"Script {script_name} failed with exit code {process.returncode}")
            
    except FileNotFoundError:
        print(f"Error: Script '{script_name}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error running {script_name}: {e}")
        sys.exit(1)

def open_html_file(file_path):
    """Opens the specified HTML file in the default web browser.
    Tries multiple methods to ensure the file opens."""
    print(f"Opening {file_path}...")
    abs_path = os.path.abspath(file_path)
    
    # Check if file exists first
    if not os.path.exists(abs_path):
        print(f"Error: File {file_path} does not exist.")
        return
    
    # Try multiple methods to open the browser
    try:
        # Method 1: Use webbrowser module
        webbrowser.open(f"file://{abs_path}")
        print(f"Opened {file_path} using Python webbrowser module.")
        return
    except Exception as e:
        print(f"Python webbrowser module failed: {e}")
    
    # Method 2: Try platform-specific commands
    try:
        if sys.platform == "darwin":  # macOS
            subprocess.run(["open", abs_path], check=True)
            print(f"Opened {file_path} using 'open' command.")
            return
        elif sys.platform == "win32":  # Windows
            os.startfile(abs_path)
            print(f"Opened {file_path} using os.startfile().")
            return
        elif sys.platform.startswith("linux"):  # Linux
            subprocess.run(["xdg-open", abs_path], check=True)
            print(f"Opened {file_path} using 'xdg-open' command.")
            return
    except Exception as e:
        print(f"Platform-specific open command failed: {e}")
    
    # Final fallback: Print instructions
    print(f"\nCouldn't automatically open the browser. Please manually open this file:")
    print(f"file://{abs_path}")
    # We don't exit here, as we still want the script to complete successfully

if __name__ == "__main__":
    # Run the scripts directly (fix_russian_script.py has been removed)
    scripts_to_run = [
        "generate_russian_audio.py",
        "update_audio_player.py"
    ]

    for script in scripts_to_run:
        run_script(script)

    html_file = "russian-audio-player.html"
    open_html_file(html_file)

    print("\nAll steps completed successfully.") 