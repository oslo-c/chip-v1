#!/usr/bin/env python3

import os
import argparse
import openai
from openai import OpenAI
from config import get_api_key

api_key = get_api_key()

def get_args():
    parser = argparse.ArgumentParser(prog = "CHIP", description = "Chip: an command line interface for querying ChatGPT on linux")
    
    chip_options = parser.add_argument_group("Chip Settings")
    input_options = parser.add_argument_group("Input Options")
    output_options = parser.add_argument_group("Output Options")
    
    # Input Options
    input_options.add_argument("-q",
        "--quick",
        dest = "query",
        metavar = "",
        type=str,
        help = "Submit question directly, surrounded by quotes. Ex: $ chip -f 'your query here'"
        )
    

    input_options.add_argument("-if",
        "--input-file",
        dest = "input_file",
        metavar = "",
        type = argparse.FileType("r"),
        help = "Use the content of a file as input. Combine with -q flag to add query related to input file."
        )
    
    # Output Options
    output_options.add_argument("-of",
        "--output-file",
        dest = "output_file",
        metavar = "",
        type = argparse.FileType("w"), 
        help = "Export query result to named file. Ex: $ Chip -el -of example.txt"
        )

    #verbosity options?

    return parser.parse_args()

def interactive_mode(api_key = api_key):
    # Start an interactive mode where the user can continually input commands.
    print("Interactive mode (type 'exit' to quit):")
    
    while True:
        # Get input from the user
        user_input = input("Chip> ")
        
        # Exit if the user types 'exit' or 'quit'
        if user_input.lower() in ['exit', 'quit']:
            print("Exiting interactive mode.")
            break
        
        # Send the input to ChatGPT and display the response
        response = send_to_chatgpt(user_input, api_key)
        print(response)

def send_to_chatgpt(input, api_key, max_tokens = 1000):
    #os.system("resetListener")
    try:
        client = OpenAI(api_key = api_key)
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": input
                    }
                ],
            model = "gpt-3.5-turbo",  # Use the appropriate modelChatCompletion.create
            max_tokens = max_tokens,
            temperature = 0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def packet_builder(args):
    packet = ""
    
    if args.query:
        packet += args.query
    
    if args.input_file:
        packet += args.input_file.read().strip()
    
    return packet

def output_handler(args, response):
    if args.output_file:
        args.output_file.write(response)
    else:
        print(response)

def main():   
    args = get_args()
    
    if args.query or args.input_file:
        response = send_to_chatgpt(input = packet_builder(args), api_key = api_key)
        output_handler(args, response)
    else:
        interactive_mode()

if __name__ == "__main__":
    main()

