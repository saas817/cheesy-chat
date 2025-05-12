import os

from agent.openai_api import client

def limit_chat_history(history):
    max_pair = int(os.environ["LIMIT_CHAT_PAIR"])

    if len(history) > max_pair:
        if history[-1]["role"] == "user":
            history = history[-max_pair * 2 - 1:]
        else:
            history = history[-max_pair * 2:]

    return history

def get_embedding(query):
    response = client.embeddings.create(
        input=query,
        model=os.environ['EMBEDDING_MODEL'],
    )
    return response.data[0].embedding