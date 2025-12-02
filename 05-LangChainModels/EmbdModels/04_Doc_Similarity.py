from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

load_dotenv()

embedding = OpenAIEmbeddings(model='text-embedding-3-large', dimensions=300)

documents = [
    "Hanoi: The capital and cultural heart, famous for its bustling Old Quarter and ancient temples.",
    "Ho Chi Minh City (Saigon): The dynamic, massive southern metropolis and Vietnam's economic engine.",
    "Da Nang: A rapidly growing coastal hub known for its beautiful beaches, modern infrastructure, and the iconic Dragon Bridge.",
    "Hue: The former Imperial capital, steeped in history and home to the UNESCO-listed Citadel and royal tombs.",
    "Can Tho: The largest city in the Mekong Delta, famous for its vibrant floating markets and river life."
]

query = "Tell me about which city of Vietnam is home to UNESCO-listed Citadel?"
doc_emb = embedding.embed_documents(documents)
query_emb = embedding.embed_query(query)

cosine_sim = cosine_similarity([query_emb], doc_emb)[0]
# print(sorted(list(enumerate(cosine_sim)), key=lambda x: x[1])[-1])
index, score = sorted(list(enumerate(cosine_sim)), key=lambda x: x[1])[-1]

print(query)
print(documents[index])
print("Similarity score is: " + str(score))
