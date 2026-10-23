import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")


def main():
    if not api_key:
        print("ERROR: API key .env file madhye sapadli nahi.")
        return

    try:
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents="Reply with: Hello! Gemini is working."
        )

        print("SUCCESS! Gemini API works.")
        print(response.text)

    except Exception as error:
        print("API test failed.")
        print("Error type:", type(error).__name__)
        print("Details:", str(error))
        print("Please check your API key, model and free quota.")


if __name__ == "__main__":
    main()