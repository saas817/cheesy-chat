**Scraping Task Requirements**

Here is the brief description of the test task.
The goal is to build a Chatbot that can answer questions based on the content of the websites.

You need to scrape food data from https://shop.kimelo.com/department/cheese/3365
For the test project, you need to scrape all Cheese data from the website.
After that you need to make the knowledge base for scraped data.
And you need to build a RAG chatbot using this knowledge base.

Here are list of frameworks you need to use:

- Scraping: Use any scraping framework you like. You can use Selenium or Puppeteer.
- Vector DB: Pinecone
- LLM: OpenAI GPT-4o
- Frontend: Python Streamlit

You must deploy app to streamlit cloud as public.
In chat UI, you also need to display the context data you have fetched to answer questions as reference.
In chat UI, you also need to display the context data you have fetched to answer questions as reference.

Here are some points you need to consider while implementing this.

- I will ask a couple of hard questions that relate to anything in the websites and Cheese.
- I will review code structure
- I will review how you ingest data into the knowledge base. Ideally you need to ingest data with proper metadata and implement metadata filtering while querying the knowledge base.
- You need to consider basic UX in streamlit UI - streamming response, proper chat UI, etc
