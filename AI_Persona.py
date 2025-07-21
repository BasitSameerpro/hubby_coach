from config import PERSONAS as p

class RoleSelector:
    def __init__(self):
        self.persona = p
        self.selected_role=None
        self.selected_character = None
        self.prompt = None

    def get_role(self,user_input):
        """
        This function is used to get the role from these option
        Fitness, Training , Motivation and Personal(More assistant like)
        """
        for role in self.persona.keys():
            if user_input.lower()==role.lower():
                return self.persona[role]
            
        return None

    def get_characters(self,role):
        """
        Extract character names from roles
        """
        return list(role.get("characteristics",{}).keys())


    def create_prompt(self,role,character):
        """
        Used for genrating the prompt
        """
        characteristic = role.get('characteristics',{}).get(character,{})
        return{
            "name": role.get("name"),
            "description": role.get("description"),
            "character": characteristic.get("name"),
            "style": characteristic.get("style"),
            "Sample Responses": characteristic.get("sample_responses",[])
        } 
    
    def select_role(self):
        """Interactive role selection with validation"""
        print("Choose your coach/assistant from these options")
        print("Fitness, Training, Motivational, Personal")
        
        while True:
            role = input("User: ").strip()
            user_role = self.get_role(role)
            
            if user_role is None:
                print("The input is invalid please enter from these options")
                print("Fitness, Training, Motivational, Personal")
            else:
                self.selected_role = user_role
                break
    

    def select_character(self):
        """
        Interactive Character selection 
        """
        if self.selected_role==None: print("Please select the role first"); return

        character_options = self.get_characters(self.selected_role)
        while True:
            user_character = input(f"Select characters from these option {', '.join(character_options)}: ")
            if user_character in character_options:
                self.selected_character = user_character
                return
            else: print(f"Please select characters from these options {', '.join(character_options)}")

    def generate_prompt(self):
        if self.selected_role == None or self.selected_character == None:
            print("Please select role and character")
            return None
        # If role and character is selected
        self.prompt = self.create_prompt(self.selected_role,self.selected_character)
        return self.prompt
    
    def run(self):
        """
        This method will be used to select AI persona
        """
        self.select_role()
        self.select_character()
        self.generate_prompt()
        return self.prompt

if __name__ == "__main__":
    selector = RoleSelector()
    prompt = selector.run()
    