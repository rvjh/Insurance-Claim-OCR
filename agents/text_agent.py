from agno.agent import Agent
from services.groq_client import chat_completion

text_agent = Agent(
    name="TextAgent",
    role="Extract structured claim data"
)

def process_text(text):
    prompt = f"""
    Extract from the text:
    - policy number
    - user name
    - accident date

    Text:
    {text}
    """

    return chat_completion(prompt)