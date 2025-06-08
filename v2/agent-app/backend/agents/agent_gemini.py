import json
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
# Define the model. 'gemini-pro' is a powerful and free model.
model = genai.GenerativeModel('gemini-1.5-flash')

# Define available support groups
SUPPORT_GROUPS = config.SUPPORT_GROUPS

def get_support_group_definitions():
    """Format support groups for the AI prompt."""
    return "\n".join([f"- {group}: {desc}" for group, desc in SUPPORT_GROUPS.items()])

def get_llm_generate_content(prompt):
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
        final_response = json_text.strip()
    except Exception as e:
        print(f"Error during model inference: {e}")
        final_response = "None"
        
    return final_response

class TicketAssistantAgent:
    def review_ticket(self, issue):
        """Processes a draft issue and returns a support ticket."""

        # --- PROMPT ASSEMBLY ---
        # 1. Get the prompt template from the config file.
        prompt_template = config.REVISE_DETAIL_PROMPT

        # 2. Fill in the placeholders with the ticket's data.
        prompt = prompt_template.format(
            rough_text = issue["text"]
        )

        support_ticket = get_llm_generate_content(prompt)

        try:
            return json.loads(support_ticket)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            return None  # Return None or handle the error as needed


    def assign_ticket(self, ticket):
        """Processes a support ticket and returns the assigned group."""

        # --- PROMPT ASSEMBLY ---
        # 1. Get the prompt template from the config file.
        prompt_template = config.SUGGEST_SUPPORT_PROMPT

        # 2. Fill in the placeholders with the ticket's data.
        prompt = prompt_template.format(
            group_definitions = get_support_group_definitions(),
            subject = ticket["subject"],
            description = ticket["description"]
        )
        
        assigned_group = get_llm_generate_content(prompt)
            
        return assigned_group if assigned_group in SUPPORT_GROUPS else "Unclassified"