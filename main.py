# main.py
from llm import llm as SingleShotLLM
from llm_agent import LanggraphllmChat

def main():
    print("Welcome to Hubby Coach!")
    print("Choose your interaction mode:")
    print("1. Single Shot (Ask a question, get one response)")
    print("2. Interactive Chat (Continuous conversation)")

    while True:
        choice = input("Enter your choice (1 or 2): ").strip()
        if choice == '1':
            print("\n--- Single Shot Mode ---")
            single_shot_bot = SingleShotLLM()
            single_shot_bot.run()
            break
        elif choice == '2':
            print("\n--- Interactive Chat Mode ---")
            chat_system = LanggraphllmChat()
            chat_system.run()
            break
        else:
            print("Invalid choice. Please enter '1' or '2'.")

if __name__ == "__main__":
    main()