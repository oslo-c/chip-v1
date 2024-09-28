from os import sys
import openai
from openai import OpenAI
from config import get_api_key
from Messages import get_help

class Conversation:
    models=["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"]
    conversation_history=[{"role": "system",
        "content": "You are a cheerful and intellegent assistant named Chip."
        },
    ]

    def __init__(self, tokens, model):
        self.tokens=tokens
        self.model=model
    
    def send_to_chip(self, input, tokens):
        self.conversation_history.append({"role": "user", "content": input},)
        try:
            client=OpenAI(api_key=get_api_key())
            response=client.chat.completions.create(
                messages=self.conversation_history, 
                model=self.model,
                max_tokens=self.tokens,
                temperature=0.5
            )
            chip_response = response.choices[0].message.content.strip()
            self.conversation_history.append({"role": "system", "content": chip_response})
            return chip_response
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)

    def interactive_mode(self, tokens, initial_input = ""):
        if initial_input != "":    
            response = self.send_to_chip(initial_input, tokens)
            print(response)

        while True:
            user_input = input("Chip> ")
            if user_input.lower() in ["exit", "quit"]:
                break
            elif user_input.lower().startswith("-t"):
                self.set_tokens() 
            elif user_input.lower().startswith("-m"):
                self.set_model()
            elif user_input.lower().startswith("-h"):
                print(get_help())
                self.print_current_settings() #129
            else:
                response = self.send_to_chip(user_input, tokens)
                print(response)

    def set_tokens(self):
        new_tokens=input('Input new tokens setting (max 4097): ')
        tokens=int(new_tokens)
        if (tokens < 0):
            print("Invalid setting.\n")
            self.tokens=100
        elif (tokens > 4097):
            print("Invalid setting.\n")
            self.tokens=4097
        self.tokens=tokens
        print("Token setting changed to: " + str(tokens))

    def set_model(self):
        print(Conversation.models)
        while True:
            model_set=input("Please select a model from the above: ")
            if model_set.lower() in self.models:
                self.model=model_set
                print("Model setting changed to: " + self.model)
                break
            else:
                print("Invalid setting. (Hint: don't include quotes, type the name exactly.)")
    
    def print_current_settings(self):
        settings="[Current Settings]\nTokens: " + str(self.tokens) + "  |  Model: " + self.model
        print(settings)
