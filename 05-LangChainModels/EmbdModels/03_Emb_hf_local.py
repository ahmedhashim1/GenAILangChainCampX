from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv

load_dotenv()

embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

documents = [
    "Islamabad is the capital of Pakistan",
    "Bankgok is the capital of Thailanad",
    "Kualalumpur is the capital of Malaysia"

]

vector = embedding.embed_documents(documents)
print(str(vector))
