#!/usr/bin/env python3

import os
import argparse
from Messages import get_help
from conversations import Conversation

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

    chip_options.add_argument("-t",
    "--tokens",
    dest="tokens",
    type=int,
    default=100
    )

    chip_options.add_argument("-m",
    "--model",
    dest="model",
    default="gpt-3.5-turbo"
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

    return parser.parse_args()

def packet_builder(args):
    packet = ""
    if args.query:
        packet += args.query
    if args.input_file:
        packet += args.input_file.read().strip()
    return packet

def outfile_handler(args, response):
    if args.output_file:
        args.output_file.write(response)
    else:
        print(response)

def main(args): 
    tokens = args.tokens  
    c = Conversation(tokens, args.model)
    print("Tokens: " + str(tokens) + "  |  Model: " + args.model)

    if args.help:
        print(get_help())
    elif args.input_file:
        response = c.send_to_chip(packet_builder(args), tokens)
        outfile_handler(args, response)        
    elif args.query:
        if args.output_file:
            response = c.send_to_chip(tokens, initial_input=args.query)
            outfile_handler(args, response)
        else:
            c.interactive_mode(tokens, initial_input=args.query)
    else:
        c.interactive_mode(tokens)

if __name__ == "__main__":
    args = get_args()
    main(args)

