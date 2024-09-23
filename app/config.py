import os
from openai import OpenAI
from pathlib import Path

home = Path.home()
def get_api_key():
    # Retrieve the OpenAI API key from a hidden file or prompt the user to enter it.
    key_file = home / ".openai_api_key"

    if key_file.exists():
        with open(key_file, "r") as f:
            api_key = f.read().strip()
            if api_key:
                return api_key

    # Prompt the user for the API key if not found
    api_key = input("Please enter your OpenAI API key: ").strip()
    if not api_key:
        print("API key is required to use this tool.")
        exit(1)

    # Save the API key to a hidden file for future use
    with open(key_file, "w") as f:
        f.write(api_key)
    os.chmod(key_file, 0o600)  # Restrict file permissions for security
    return api_key

        
