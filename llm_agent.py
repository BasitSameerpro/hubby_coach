from AI_Persona import RoleSelector
import logging
from langchain_ollama import OllamaLLM
from langchain_core.messages import AIMessage,HumanMessage,SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from typing_extensions import TypedDict , List , Dict , Any ,Optional
from langgraph.graph import StateGraph, START,  END
import uuid
import os , json


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentState(TypedDict):
    messages : List[Dict[str, Any]]
    preference_user : Optional[Dict[str , Any]]
    model_name : Optional[str]
    # session_id : str
    conversation_count: int
    model_last_response : Optional[str]
    user_current_query : Optional[str]
    Context_Summary : Optional[str]
    system_prompt : Optional[str]



class LanggraphllmChat():
    def __init__(self , cache_dir : str ='cache'):
        self.selector = RoleSelector()
        self.model : Optional[OllamaLLM] = None
        self.cache_path = cache_dir
        self.graph = None
        self.session_id = str(uuid.uuid4())

    def _ensure_cache_dir(self):
        if not os.path.exists(self.cache_path):
            os.makedirs(self.cache_path)

    def _get_user_prefrence(self, state: AgentState) -> AgentState:
        if(state.get('preference_user') == None):
            cache_pref = os.path.join(self.cache_path, 'preference_user.json')
            if os.path.exists(cache_pref):
                try: 
                    with open(cache_pref , 'r') as f:
                        state['preference_user'] = json.load(f)
                        return state
                except Exception as e:
                    logger.error(f"Error occured while trying to take prefernce from {e}")
            
            state['preference_user'] = self.selector.run()
            try:
                with open(cache_pref, 'w') as f:
                    json.dump(state['preference_user'] , f)
            except Exception as e:
                logger.error(f"Error occured while saving the user preference {e}")
        
        return state

    def _get_model_name(self, state: AgentState) -> AgentState:
        """Getting model name from the user"""
        model_name = input(
            "Please input a model name running locally with ollama.\n"
            "To check available models, type `ollama list` in cmd\n"
            "Model Name: "
        ).strip()
        state['model_name'] = model_name
        return state
    
    def _model_setup(self,state: AgentState) -> AgentState:
        if (state['model_name'] == None):
            self._get_model_name(state)
        if (self.model == None):
            try:
                logger.info(f"Initializing model {state['model_name']}")
                self.model = OllamaLLM(model=state['model_name'])
            except Exception as e:
                logger.info(f"Error occured while initializing the model {e}")

        return state
    
    def _get_query(self, state: AgentState) -> AgentState:
        """Used for getting the query"""
        try:
            query = input(f"\n[{state['conversation_count'] + 1}] You: ").strip()
            state['conversation_count'] = state.get('conversation_count', 0) + 1
            if query.lower() in ['q', 'quit', 'exit']:
                print("Goodbye!")
                raise KeyboardInterrupt

            if not query:
                print("Query must not be empty.")
                return self._get_query(state)

            state['user_current_query'] = query
            state['messages'].append({
                "role": "user",
                "content": query,
                "timestamp_id": str(uuid.uuid4())
            })

        except KeyboardInterrupt:
            exit()
        except Exception as e:
            logger.error(f"Error during query input: {e}")
        return state

    
    def _build_system_prompt(self, state: AgentState ):
        user_choice = state['preference_user']
        system_message = SystemMessage(
                content=f"""You are {user_choice['name']}, a {user_choice['description']} 
with a personality of {user_choice['character']} and style of {user_choice['style']}. 
Act as this persona consistently throughout our conversation.

Here are sample responses that demonstrate your personality: {user_choice['Sample Responses']}

Maintain this character while being helpful and engaging. Keep responses concise but in character."""
            )
        
        state['system_prompt'] = system_message

        state['messages'].append({
            "role":"system",
            "content": system_message.content,
            "timestamp_id": str(uuid.uuid4()),
        })
        return state

    def _build_context_summary(self,state:AgentState) -> AgentState:
        """This will be a conditional node if the message length is 10 and then for every 5 messages this will be called"""
        summary_prompt = ""
        if (len(state['messages'])>=10) and (len(state["messages"]) % 5 == 0):
            summary_prompt = "I want you to summarize these chats\n"
            for msg in state['messages'][-10:]:
                if msg['role']== 'assistant':
                    summary_prompt+=f"{msg['role']} : {msg['content']}"
        if self.model:
            state['Context_Summary'] = self.model.invoke(summary_prompt)
        return state

    def _prepare_chat_messages(self,state: AgentState):
        chat_message = []
        for msg in state['messages']:
            role=msg['role'].lower()
            if role == "system":
                chat_message.append(SystemMessage(msg['content']))
            elif role == 'user':
                chat_message.append(HumanMessage(msg['content']))
            elif role == 'assistant':
                chat_message.append(AIMessage(msg['content']))

        return chat_message 
    
    def assistant_response(self,state: AgentState) -> AgentState:
        for msg in reversed(state['messages']):
            if(msg['role']== 'assistant'):
                state['model_last_response'] = msg['content']
                break

        return state
    
    def _interactive_chatting(self, state: AgentState) -> AgentState:
        """Generate response using the model"""
        try:
            if state.get('system_prompt') is None:
                state = self._build_system_prompt(state)
            
            chat_messages = self._prepare_chat_messages(state) 
            
            if self.model is None:
                state = self._model_setup(state)

            model_response = self.model.invoke(chat_messages)
            
            state['messages'].append({
                'role': "assistant",  
                "content": model_response,
                "timestamp_id": str(uuid.uuid4()),  
            })
            
            
            state = self._build_context_summary(state)
            
            print(f"\n{state['preference_user']['name']}: {model_response}\n")
            
        except Exception as e:
            logger.error(f"Error in interactive chatting: {e}")
            
        return state
    
    def _should_continue(self, state:AgentState)-> str:
        """To check if the chatting continues"""
        last_message = state['messages'][-1] if state['messages'] else None
        if last_message and last_message['role'] == 'user':
            query = last_message['content'].lower()
            if query in ['q','quit' , 'exit']:
                return "end"
        return 'continue'

    def workflow(self):
        """
        User Preference -> Model setup -> get query
        """
        graphbuilder = StateGraph(AgentState)

        # Nodes in the stateful agent
        graphbuilder.add_node("user_preference", self._get_user_prefrence)
        graphbuilder.add_node("model" , self._model_setup)
        graphbuilder.add_node("query" , self._get_query)
        graphbuilder.add_node("chatting" , self._interactive_chatting)

        # Edges in the agent
        graphbuilder.add_edge(START,'user_preference')
        graphbuilder.add_edge('user_preference','model')
        graphbuilder.add_edge('model' , 'query')
        graphbuilder.add_edge('query','chatting')\
        
        # add a conditional_edge
        graphbuilder.add_conditional_edges(
            'chatting',
            self._should_continue,
            {
                "continue": "query",
                "end" : END
            }
        )

        # compile the graph
        self.graph = graphbuilder.compile()

    def run(self):
        """Run interactive chat session using the graph."""
        print("=" * 60)
        print("LangGraph LLM Chat System - Interactive Mode")
        print("Type 'quit', 'exit', or 'q' to end the conversation")
        print("=" * 60)
        
        if self.graph is None:
            self.workflow()

        # Initialize state
        try:
            state = AgentState(
                messages=[],
                preference_user=None,
                model_name=None,
                conversation_count=0,  
                model_last_response=None,
                user_current_query=None,
                Context_Summary=None,
                system_prompt=None
            )
            final_state = self.graph.invoke(state)
            print(f"\nConversation ended. Total exchanges: {final_state.get('conversation_count', 0)}")
        except KeyboardInterrupt:
            print('\nGoodbye')
        except Exception as e:
            logger.error(f"Error occured while interactuve chatting")
            print(f"Error occured: {e}")

# Example usage
if __name__ == "__main__":
    chat_system = LanggraphllmChat()
    chat_system.run()