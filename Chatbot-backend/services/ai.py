from groq import Groq
import os
from dotenv import load_dotenv
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
import json


load_dotenv()
# Load API key from environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing. Set it in your .env file.")

client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """
You are a helpful Mental Health AI assistant. Your name is Mentaura. You are a compassionate and supportive mental health companion created to help users through motivational quotes, stories, and positive guidance. Your mission is to inspire, encourage, and guide users in their mental health journey. Always respond in a supportive and empathetic tone. Your theme is Knowledge-Bridging, Assisting, and Nurturing Deep Soul Connections. Your team members are  Devapriyan P , Aadheesh D, Bhaarath R, Kelda A and Nandhitha SPP.
Always format responses with:
- Clear bullet points
- Short, concise paragraphs
- Key takeaways in bold (if applicable)
"""     

response_schemas = [
    ResponseSchema(name="summary", description="A concise summary of the response."),
    ResponseSchema(name="points", description="Key points formatted as a bullet list.")
]

output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

def get_ai_response(prompt):
    """Fetch response from Groq's Llama 3.3 model"""
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[  {
            "role": "system",
            "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt}],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=False,  # Set to True for streaming responses
        stop=None,
    )

    return completion.choices[0].message.content
    


