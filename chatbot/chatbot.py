from anthropic import Anthropic
from config import IDENTITY, TOOLS, MODEL, get_quote
from dotenv import load_dotenv

load_dotenv()

class ChatBot:
    def __init__(self, session_state):
       self.anthropic = Anthropic()
       self.session_state = session_state

    def generate_message(
       self,
       messages,
       max_tokens,
   ):
        """
        Generates a response using the Anthropic Claude API with the specified messages and token limit.

        Args:
            messages (list): A list of message objects containing the conversation history
                and user input to generate a response for.
            max_tokens (int): The maximum number of tokens to generate in the response.

        Returns:
            dict: Either the complete API response object from Anthropic containing the 
                generated message, or a dict with an 'error' key containing the error message
                if an exception occurred.

        Raises:
            No exceptions are raised directly as they are caught and returned as part of
            the error response dictionary.

        Example:
            messages = [{"role": "user", "content": "Hello"}]
            response = generate_message(messages, max_tokens=100)
            if "error" in response:
                print(f"Error occurred: {response['error']}")
            else:
                print(response.content)
            """
        try:
            response = self.anthropic.messages.create(
                model=MODEL,
                system=IDENTITY,
                max_tokens=max_tokens,
                messages=messages,
                tools=TOOLS,
            )
            return response
        except Exception as e:
            return {"error": str(e)}


    def process_user_input(self, user_input):
        """
        Processes user input by generating responses through the Anthropic API and handling any tool use requests.

        This function manages the conversation flow by:
        1. Adding the user's input to the session history
        2. Generating an initial response
        3. Handling any tool use requests from the assistant
        4. Generating follow-up responses if needed
        5. Managing the conversation state throughout the process

        Args:
            user_input (str): The input text from the user to be processed.

        Returns:
            str: The final response text to be shown to the user. This could be either:
                - The direct text response from the assistant
                - A follow-up response after tool use
                - An error message if something went wrong

        Raises:
            Exception: If the response type from the API is neither a tool use request nor text.

        Example:
            response = process_user_input("What's the weather like today?")
            print(response)  # Prints either the response or an error message

        Flow:
            1. If the assistant responds with text:
            - The text is stored in session state and returned
            2. If the assistant requests tool use:
            - The tool is executed
            - Results are added to conversation
            - A follow-up response is generated
            - Final response is stored and returned
            3. If an error occurs at any step:
            - An error message is returned
        """        
        self.session_state.messages.append({"role": "user", "content": user_input})

        response_message = self.generate_message(
            messages=self.session_state.messages,
            max_tokens=2048,
        )

        if "error" in response_message:
            return f"An error occurred: {response_message['error']}"

        if response_message.content[-1].type == "tool_use":
            tool_use = response_message.content[-1]
            func_name = tool_use.name
            func_params = tool_use.input
            tool_use_id = tool_use.id

            result = self.handle_tool_use(func_name, func_params)
            
            self.session_state.messages.append(
                {"role": "assistant", "content": response_message.content}
            )
            
            self.session_state.messages.append({
                "role": "user",
                "content": [{
                    "type": "tool_result",
                    "tool_use_id": tool_use_id,
                    "content": f"{result}",
                }],
            })

            follow_up_response = self.generate_message(
                messages=self.session_state.messages,
                max_tokens=2048,
            )

            if "error" in follow_up_response:
                return f"An error occurred: {follow_up_response['error']}"

            response_text = follow_up_response.content[0].text
            
            self.session_state.messages.append(
                {"role": "assistant", "content": response_text}
            )
            return response_text
        
        elif response_message.content[0].type == "text":
            response_text = response_message.content[0].text
            self.session_state.messages.append(
                {"role": "assistant", "content": response_text}
            )
            return response_text
        
        else:
            raise Exception("An error occurred: Unexpected response type")

    def handle_tool_use(self, func_name, func_params):
        if func_name == "get_quote":
            premium = get_quote(**func_params)
            return f"Quote generated: ${premium:.2f} per month"

        raise Exception("An unexpected tool was used")