from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(model='gpt-4', temperature=0, max_completion_tokens=50)
result = model.invoke(
    "Suggest me 5 Top Malaysia places for family tour in September, also suggest cheap flights and hotels.")
print(result.content)
