from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv

load_dotenv()

model = ChatAnthropic(model='claude-sonnet-4-5-20250929')
result = model.invoke("What is the capital of Thailand?")
print(result.content)
