from pinecone import Pinecone, ServerlessSpec
import os, json

from agent.openai_api import client
from prompt_template import prompt_json2text
from database.pinecone.utils import extract_first_float

class PineconeIndex:

    records = []

    def __init__(self):
        pc = Pinecone(api_key=os.environ['PINECONE_API_KEY'])
        index_name = os.environ['EMBEDDING_MODEL']

        if not pc.has_index(index_name):
            self.indexModel = pc.create_index(
                name=index_name,
                vector_type="dense",
                dimension=1536,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1",
                ),
                deletion_protection="disabled",
                tags={
                    "environment": os.environ['PINECONE_ENV'],
                }
            )
        else:
            self.indexModel = pc.Index(index_name)

    def upsert(self):
        with open(os.environ["RECORDS_JSON"], "rb") as f:
            records = json.load(f)

        self.indexModel.upsert(records, namespace=os.environ['PINECONE_ENV'])

    def convert2records(self):
        with open(os.environ["SCRAP_JSON"], "rb") as f:
            datas = json.load(f)
        with open(os.environ["RECORDS_JSON"], "rb") as f:
            rs = json.load(f)

        for index, data in enumerate(datas):
            text = self.generate_text(data)
            embedding = self.generate_embedding(text)

            data["text"] = text
            data["embedding"] = embedding
            # data["text"] = rs[index]["metadata"]["text"]
            # data["embedding"] = rs[index]["values"]

            record = {
                "id": data["sku"],
                "values": data["embedding"],
                "metadata": {
                    "showImage": data["showImage"],
                    "name": data["name"],
                    "brand": data["brand"],
                    "department": data["department"],
                    "item_counts_each": extract_first_float(data["itemCounts"]["EACH"]),
                    "dimension_each": data["dimensions"]["EACH"],
                    "weight_each": extract_first_float(data["weights"]["EACH"]),
                    "images": data["images"],
                    "relateds": data["relateds"],
                    "price_each": extract_first_float(data["prices"]["Each"]),
                    "price": extract_first_float(data["prices"]["Each"]),
                    "pricePer": extract_first_float(data["pricePer"]),
                    "sku": data["sku"],
                    "discount": data["discount"],
                    "empty": bool(data["empty"]),
                    "href": data["href"],
                    "text": data["text"],
                    "price_order": data["priceOrder"],
                    "popularity_order": data["popularityOrder"],
                    "weight_unit": data["weights"]["EACH"].split(' ')[-1].strip(),
                    "count_unit": data["itemCounts"]["EACH"].split(' ')[-1].strip(),
                    "price_unit": data["pricePer"].split('/')[-1].strip(),
                }
            }

            if "CASE" in data["itemCounts"].keys():
                record["metadata"]["item_counts_case"] = extract_first_float(data["itemCounts"]["CASE"])
                record["metadata"]["dimension_case"] = data["dimensions"]["CASE"]
                record["metadata"]["weight_case"] = extract_first_float(data["weights"]["CASE"])
                record["metadata"]["price_case"] = extract_first_float(data["prices"]["Case"])

            self.records.append(record)

            print(f"Converting... {index + 1} complete of {len(datas)}, name is {record['metadata']['name']}")

        self.save(os.environ["RECORDS_JSON"])

    def generate_embedding(self, text):
        response = client.embeddings.create(
            input=text,
            model=os.environ['EMBEDDING_MODEL'],
        )

        return response.data[0].embedding

    def generate_text(self, data):
        response = client.responses.create(
            model=os.environ["JSON2TEXT_MODEL"],
            input=[
                {
                    "role": "developer",
                    "content": prompt_json2text
                },
                {
                    "role": "user",
                    "content": json.dumps(data, indent=4, ensure_ascii=False, sort_keys=False)
                }
            ]
        )

        return response.output_text

    def save(self, filename):
        with open(filename, 'w', encoding='utf-8') as json_file:
            json.dump(self.records, json_file, indent=4, ensure_ascii=False, sort_keys=False)

        print(f"Successfully saved records to '{filename}' in a beautiful format.")

    def clear(self):
        self.records = []



if __name__ == "__main__":
    index = PineconeIndex()