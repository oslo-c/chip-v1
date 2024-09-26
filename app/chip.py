#!/usr/bin/env python3

import os
import argparse
import openai
from openai import OpenAI
from config import get_api_key
from helpMessage import get_help

api_key = get_api_key()

def get_args():
    parser = argparse.ArgumentParser(prog = "CHIP",
    description="Chip: an command line interface for querying ChatGPT on linux",
    add_help=False
    )
    
    chip_options = parser.add_argument_group("Chip Settings")
    input_options = parser.add_argument_group("Input Options")
    output_options = parser.add_argument_group("Output Options")
    
    # Chip Options
    chip_options.add_argument("-h",
    "--help",
    dest="help",
    action="store_true",
    )

    chip_options.add_argument("-v",
    "--verbosity",
    dest="verbosity",
    type=int,
    default=100
    )

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

def interactive_mode(verbosity, api_key = api_key, initial_input = ""):
    # Start an interactive mode where the user can continually input commands.
    # print("Interactive mode (type 'exit' to quit):")

    if initial_input != "":    
        response = send_to_chatgpt(initial_input, api_key, verbosity)
        print(response)

    while True:
        # Get input from the user
        user_input = input("Chip> ")
        
        if user_input.lower() in ['exit', 'quit']:
            break
        else:
            # Send the input to ChatGPT and display the response
            response = send_to_chatgpt(user_input, api_key, verbosity)
            print(response)

    

def send_to_chatgpt(input, api_key, verbosity): #
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
            max_tokens = verbosity,
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

def main(args):   
    verbosity = args.verbosity
    print("Verbosity setting: " + str(verbosity) + " tokens")

    if args.help:
        print(get_help())
    elif args.input_file:
        response = send_to_chatgpt(packet_builder(args), api_key, verbosity) #
        output_handler(args, response)        
    elif args.query:
        interactive_mode(verbosity, initial_input=args.query)
    else:
        interactive_mode(verbosity, initial_input="<Your name is chip, you are an ai help bot and I have just activated you.> Hello!")

if __name__ == "__main__":
    args = get_args()
    main(args)

