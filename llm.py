from AI_Persona import RoleSelector
from langchain_ollama import OllamaLLM
from langchain_core.messages import HumanMessage , SystemMessage

selector = RoleSelector()
class llm:
    def __init__(self):
        self.user_preference = None
        self.model_name = None
        self.model = None
        self.Query= None
        self.prompt = None
        self.model_response = None

    def get_user_preference(self):
        self.user_preference = selector.run()
        return self.user_preference
    
    def get_model_name(self):
        print("Please input your model name from ollama. For better model the responses will be much better")
        try:
            self.model_name = input("""Please input a model name this is running locally in the cpu with ollama.\n 
To check list of running model type `ollama list` in cmd\n
Model Name: """)
        except ValueError as e: print(f"Error occured {e}")
        return self.model_name

    def model_initialization(self):
        """ I want to add cache support in the morning so everytime i do not have to load it or add langgraph continous chat"""
        self.model = OllamaLLM(model=self.model_name)
        return self.model
    
    def get_query(self):
        self.Query = input("What do you want to ask. User: ")

    def prompt_generation(self):
        user_choise = self.user_preference
        self.prompt = [
            SystemMessage(
                content=f"""You are {user_choise['name']} who is a {user_choise['description']} 
with a personality of {user_choise['character']} and with style of {user_choise['style']}. Now acts as the persona that is described above.
Here are some of the responses they are short but will help you understand your personality {user_choise['Sample Responses']}"""
            ),HumanMessage(
                content=f"""User: {self.Query}"""
            )
        ]
        return self.prompt
    
    
    def invoke(self):
        model = self.model
        self.model_response = model.invoke(self.prompt)
        print(f'Assistent: {self.model_response}')
        return self.model_response
    
    def run(self):
        self.get_user_preference()
        self.get_model_name()
        self.model_initialization()
        self.get_query()
        self.prompt_generation()
        self.invoke()
        return self.model_response
    
if __name__ == "__main__":
    llm1 = llm()
    print(llm1.run())
