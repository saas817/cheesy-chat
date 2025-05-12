from openai import OpenAI
from dotenv import load_dotenv
import os

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])