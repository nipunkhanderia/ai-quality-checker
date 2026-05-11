# ============================================================
# checker/api_caller.py
# ============================================================
# PURPOSE:
#   This file handles ONE job only - talking to the Claude AI.
#   It sends a prompt and gets back a response.
#   Think of it as the "phone" that calls Claude.
#
# WHY SEPARATE FILE:
#   Keeping API logic separate means if Anthropic changes their
#   API tomorrow, we only fix THIS file, nothing else breaks.
# ============================================================

import anthropic       # Official Anthropic library
import os              # Used to read environment variables
from dotenv import load_dotenv  # Reads our .env file

# Load the .env file so our API key is available
load_dotenv()


def call_claude(prompt: str, max_tokens: int = 500) -> str:
    """
    Sends a prompt to Claude and returns the text response.

    Parameters:
        prompt     : The question or instruction you send to Claude
        max_tokens : Maximum length of Claude's response (default 500 words approx)

    Returns:
        A string containing Claude's response text
        OR an error message string if something goes wrong

    Example usage:
        response = call_claude("What is cloud computing?")
        print(response)
    """

    # Step 1: Read the API key from our .env file
    api_key = os.getenv("ANTHROPIC_API_KEY")

    # Step 2: Check if the API key exists - if not, tell the user clearly
    if not api_key:
        return "ERROR: No API key found. Please add your ANTHROPIC_API_KEY to the .env file."

    # Step 3: Create the Anthropic client (like logging into a service)
    client = anthropic.Anthropic(api_key=api_key)

    # Step 4: Try to call the API and handle errors gracefully
    try:
        # This is the actual API call - sending the prompt to Claude
        message = client.messages.create(
            model="claude-opus-4-20250514",   # Which Claude model to use
            max_tokens=max_tokens,             # How long the response can be
            messages=[
                {
                    "role": "user",            # We are the "user" in the conversation
                    "content": prompt          # This is our actual question/prompt
                }
            ]
        )

        # Step 5: Extract just the text from Claude's response
        # message.content is a list, we want the first item's text
        return message.content[0].text

    except anthropic.AuthenticationError:
        # This happens when the API key is wrong
        return "ERROR: Invalid API key. Please check your ANTHROPIC_API_KEY in .env file."

    except anthropic.RateLimitError:
        # This happens when we call the API too many times too fast
        return "ERROR: Rate limit hit. Please wait a moment and try again."

    except Exception as e:
        # Catch any other unexpected errors
        return f"ERROR: Something went wrong - {str(e)}"
