import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from prompts import system_prompt
from functions.call_function import available_functions

def main():
    # Ensure API key is loaded from .env file
    load_dotenv()
    if api_key := os.environ.get("GEMINI_API_KEY"):
        print("API Key loaded successfully.")
    else:
        raise RuntimeError("GEMINI_API_KEY not found in environment variables. Please set it in the .env file.")


    # Parse user input from command line
    parser = argparse.ArgumentParser(description="Gemini API Example")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    # Set up agent
    client = genai.Client(api_key=api_key)

    # Query model
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
            temperature=0
        ),
    )

    # Print response and other metadata
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    print(response.text)
    print("Function calls made:")
    candidate = response.candidates[0]
    for part in candidate.content.parts:
        if part.function_call:
            call = part.function_call
            print(f"Function called: {call.name}")
            # print(f"ID: {call.id}") # Optional: ID is used for multi-turn tracking
            print(f"Arguments: {call.args}")
            
        else:
            print("No function call found in this part.")
            # If there is no function call, there might be text
            if part.text:
                print(f"Model text: {part.text}")

if __name__ == "__main__":
    main()
