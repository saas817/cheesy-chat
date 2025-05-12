import asyncio
import json, os
import nest_asyncio
nest_asyncio.apply()# ADJUST THIS PATH!

from database.pinecone.PineconeIndex import PineconeIndex
from database.scrap.Scraper import Scraper
from database.mongo.MongoDB import MongoDB
from agent.cheese_bot.ChatAgent import ChatAgent

from prompt_template import hello

if __name__ == '__main__':
    scraper = Scraper()
    mongo = MongoDB()
    pinecone_index = PineconeIndex()
    agent = ChatAgent(pinecone_index.indexModel)

    # pinecone_index.convert2records()
    # pinecone_index.upsert()

    mongo.update()

    # print(f"Bot: {hello}")
    # while True:
    #     user_query = input("You: ")
    #     if user_query.lower() in ["quit", "exit", "bye"]:
    #         print("Bot: Goodbye! Hope you enjoyed our cheesy chat!")
    #         break
    #
    #     if not user_query.strip():
    #         continue
    #
    #     response = agent.get_response(user_query)
    #
    #     print(f"Bot: {response}")

