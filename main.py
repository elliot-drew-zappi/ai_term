import argparse
import openai
import os
from tenacity import retry, wait_exponential, stop_after_attempt
import tiktoken
import traceback
import sys
import time
from termcolor import colored

openai.api_key = os.environ["OPENAI_USER_KEY"]
openai.organization = os.environ["OPENAI_ORG_KEY"]

encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

def greet(name):
    print(f"Hello, {name}!")

def calculate_history_length(conversation, max, completion_max):
    allowed_tokens = max - completion_max
    current_length = 0
    r_conversation = conversation[::-1] # reverse the conversation_history
    new_conversation = []
    for message in r_conversation:
        len_message = len(encoding.encode(message['content']))
        if (current_length + len_message) <= allowed_tokens:
            new_conversation.append(message)
            current_length += len_message
            
        else:
            break
    return new_conversation[::-1]

def main():
    parser = argparse.ArgumentParser(description="A simple chat-like CLI app with GPT-3 integration.")
    parser.add_argument('-n', '--name', type=str, default='World', help='The name of the person to greet (default: World)')

    args = parser.parse_args()

    conversation_history = []
    completion_max = 500
    print(colored("Start chatting below or type /quit to exit.\n", "cyan"))
    while True:
        user_input = input(">")

        if user_input.lower() == '/quit':
            print(colored("Goodbye!", 'cyan'))
            break

        conversation_history.append({'role': 'user', 'content': user_input})
        conversation_history = calculate_history_length(conversation_history, 3600, completion_max)

        try:
            reply = ""
            for chunk in openai.ChatCompletion.create(
                    temperature = 0.6,
                    max_tokens = completion_max,
                    model="gpt-3.5-turbo",
                    messages=conversation_history,
                    stream=True
                    ):
                content = chunk["choices"][0].get("delta", {}).get("content")
                if content is not None: 
                    print(colored(content, "green"), end='', flush=True)
                    reply += content
            
            conversation_history.append({'role': 'assistant', 'content': reply})
            
        except Exception as e:
            traceback.print_exc(e)
            print(colored("Assistant: There was an error. Please try again.\n", 'red'))
        print("\n\n")

if __name__ == "__main__":
    main()
