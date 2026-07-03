from config import Config

def main():
    print("API Key:", Config.OPENAI_API_KEY)
    print("Base URL:", Config.OPENAI_BASE_URL)
    print("Model:", Config.MODEL_NAME)


if __name__ == "__main__":
    main()