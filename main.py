import os
from urllib import response
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from prompts import system_prompt
from functions.call_function import available_functions, call_function

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

    for _ in range(20):
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

        if response.candidates:
            model_content = response.candidates[0].content
            messages.append(model_content)
        else:
            break
        

        # Print response and other metadata
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        
        function_parts = []
        has_function_call = False

        # 2. Process all parts in the response
        for part in model_content.parts:
            if part.function_call:
                has_function_call = True
                # Call your local tool
                function_call_result = call_function(part.function_call, verbose=args.verbose)
                
                # The tool result is a Part; collect it
                # Ensure call_function returns a types.Part(function_response=...)
                function_parts.append(function_call_result.parts[0])
            
            elif part.text and args.verbose:
                print(f"Model: {part.text}")

        # 3. If there were function calls, send the results back to the model
        if has_function_call:
            # Crucial: The role must be 'function' (or 'user' depending on SDK version/preference, 
            # but usually 'function' for tool results)
            messages.append(types.Content(role="tool", parts=function_parts))
        else:
            # If no function calls, the model has given its final answer
            if not args.verbose:
                print(response.text)
            break

    exit(1)

if __name__ == "__main__":
    main()
