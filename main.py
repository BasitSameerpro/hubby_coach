from llm import llm
from llm_agent import LanggraphllmChat

if __name__ == "__main__":
    print('='* 60)
    print("Please choose the interaction mode with hubbycoach.\n"
          "There are 2 options\n"
          "Single shot llm and interactive chat session. Choose 1 for single shot and 2 for the interactive mode"
          )
    print('='*60)
    user_choise = int(input("User: "))
    if user_choise == 1:
        llm = llm()
        llm.run()
    else:
        Chat_llm = LanggraphllmChat()
        Chat_llm.run()
    