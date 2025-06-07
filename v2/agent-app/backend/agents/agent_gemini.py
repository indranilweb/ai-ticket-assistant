import re
import google.generativeai as genai
import config
import secret

# --- CONFIGURATION ---
# IMPORTANT: Replace "YOUR_API_KEY" with your actual Google AI Studio API key.
# Get your key from https://aistudio.google.com/app/apikey
# try:
#     from google.colab import userdata
#     # Used if running in Google Colab
#     GOOGLE_API_KEY = userdata.get('GOOGLE_API_KEY')
# except ImportError:
    # Used if running locally
GOOGLE_API_KEY = secret.GEMINI_KEY # "YOUR_API_KEY"

genai.configure(api_key=GOOGLE_API_KEY)

# Define available support groups
SUPPORT_GROUPS = config.SUPPORT_GROUPS

def get_support_group_definitions():
    """Format support groups for the AI prompt."""
    return "\n".join([f"- {group}: {desc}" for group, desc in SUPPORT_GROUPS.items()])

class TicketAssignmentAgent:
    def assign_ticket(self, ticket):
        """Processes a support ticket and returns the assigned group."""
        # Define the model. 'gemini-pro' is a powerful and free model.
        model = genai.GenerativeModel('gemini-1.5-flash')

        # This is the "prompt" that instructs the LLM.
        prompt = f"""
        You are an intelligent IT support ticket assignment agent. Your task is to analyze a new support ticket and assign it to the correct support group.

        Here are the available support groups and their responsibilities:
        {get_support_group_definitions()}

        Analyze the following ticket and determine the most appropriate support group.

        Ticket Subject: {ticket["subject"]}
        Ticket Description: {ticket["description"]}

        Provide only the name of the correct support group as your answer. Do not add any other text. Do not add anything after your answer.
        """
        try:
            response = model.generate_content(prompt)
            # LLMs sometimes add ```json ... ``` markers
            cleaned_response = re.search(r'```json\n({.*})\n```', response.text, re.DOTALL)
            if cleaned_response:
                json_text = cleaned_response.group(1)
            else:
                # If no markdown, assume the response is the JSON object itself
                json_text = response.text
                
            print(f"\nResponse --> {response}")
            print(f"\nCleaned response --> {cleaned_response}")
            # raw_response = response['text'].strip()
            print(f"\nFinal response --> {json_text}")
            # assigned_group = json_text.split("\n")[-1].strip()
            assigned_group = json_text.strip()
        except Exception as e:
            print(f"Error during model inference: {e}")
            assigned_group = "Unclassified"
            
        return assigned_group if assigned_group in SUPPORT_GROUPS else "Unclassified"