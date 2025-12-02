from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

embedding = OpenAIEmbeddings(model='text-embedding-3-large', dimensions=32)

documents = [
    "Islamabad is the capital of Pakistan",
    "Bankgok is the capital of Thailanad",
    "Kualalumpur is the capital of Malaysia"

]

result = embedding.embed_documents(documents)
print(str(result))
