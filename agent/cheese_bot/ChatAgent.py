import json, os

from agent.openai_api import client
from prompt_template import isCheeseChat, query2filter, system, query2mongo, general
from database.mongo.MongoDB import MongoDB
from .utils import limit_chat_history, get_embedding

class ChatAgent():
    messages = []

    def __init__(self, indexModel, mongo):
        self.indexModel = indexModel
        self.mongo = mongo

    def is_query_about_cheese(self, query):
        prompts =[{"role": "developer", "content": isCheeseChat}] + self.messages + [{"role": "user", "content": query}]
        response = client.chat.completions.create(
            model=os.environ["IS_CHEESE_CHAT_MODEL"],
            messages=prompts,
            max_tokens=10,
            temperature=0.0
        )
        return response.choices[0].message.content.strip().lower() == "yes"

    def get_meta_filter(self, query):
        prompts =[{"role": "developer", "content": query2filter}] + self.messages + [{"role": "user", "content": query}]
        response = client.chat.completions.create(
            model=os.environ["QUERY2FILTER_MODEL"],
            messages=prompts,
            response_format={"type": "json_object"},
            temperature=0.1
        )

        filter_data = json.loads(response.choices[0].message.content)

        if not isinstance(filter_data, dict) or "filter" not in filter_data or "limit" not in filter_data:
            print("Warning: LLM returned malformed filter JSON. Using default.")
            return {"filter": {}, "limit": 30}

        if not isinstance(filter_data["filter"], dict):
            print("Warning: 'filter' key in LLM output is not an object. Using empty filter.")
            filter_data["filter"] = {}

        if not isinstance(filter_data["limit"], int) or filter_data["limit"] <= 0:
            print("Warning: 'limit' key in LLM output is invalid. Defaulting to 5.")
            filter_data["limit"] = 30

        filter_data["limit"] = min(max(1, filter_data["limit"]), 30)  # Ensure limit is between 1 and 10

        print(f"DEBUG: Parsed metadata filter: {filter_data}")
        return filter_data

    def get_mongo_filter(self, query):
        prompts = [{"role": "developer", "content": query2mongo}] + self.messages + [{"role": "user", "content": query}]
        response = client.chat.completions.create(
            model=os.environ["QUERY2MONGO_MODEL"],
            messages=prompts,
            response_format={"type": "json_object"},
            temperature=0.1
        )

        filter_data = json.loads(response.choices[0].message.content)
        return filter_data

    def search_pinecone(self, query, filter, limit):
        embedding = get_embedding(query)

        results = self.indexModel.query(
            vector=embedding,
            filter=filter,
            top_k=limit,
            include_metadata=True,
            namespace=os.environ["PINECONE_ENV"]
        )
        return results.get("matches", [])

    def get_response(self, query):
        isCheese = self.is_query_about_cheese(query)
        print(f"      isCheese: {isCheese}")

        if isCheese:
            # filter_data = self.get_meta_filter(query)
            filter_data = self.get_mongo_filter(query)
            print(f"      filter_data: {json.dumps(filter_data, indent=4)}")

            if filter_data["search_type"]:
                skus = list(self.mongo.get_skus(filter_data["filter"], filter_data["sort"], filter_data["limit"]))
                flag = True
            else:
                skus, flag = list(self.mongo.aggregate(filter_data["pipeline"]))
            print(skus)

            if flag:
                results = self.search_pinecone(query, {"sku": {"$in": skus}}, filter_data["limit"])
                context = "\n\n-----------------------------------------\n\n".join([json.dumps(result.get('metadata', {}), indent=4, ensure_ascii=False, sort_keys=False) for result in results])
            else:
                results = skus
                context = json.dumps(results, indent=4, ensure_ascii=False, sort_keys=False)
            print(f"      results: {len(results)}, {flag}")

            prompts = [{"role": "developer", "content": system + context}] + self.messages + [{"role": "user", "content": query}]
            stream = client.chat.completions.create(
                model=os.environ["SYSTEM_CHAT_MODEL"],
                messages=prompts,
                stream=True
            )

        else:
            prompts = [{"role": "developer", "content": general}] + self.messages + [{"role": "user", "content": query}]
            stream = client.chat.completions.create(
                model=os.environ["GENERAL_CHAT_MODEL"],
                messages=prompts,
                stream=True
            )
        text = ''
        for event in stream:
            if event.choices[0].finish_reason == "stop":
                continue
            text += event.choices[0].delta.content
            yield text

        self.messages = limit_chat_history(self.messages + [{"role": "user", "content": query}, {"role": "assistant", "content": text}])

    def clear_history(self):
        self.messages = []

