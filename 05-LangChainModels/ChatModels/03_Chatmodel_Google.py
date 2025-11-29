from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import pprint  # This is not strictly necessary for this specific example but is fine to keep

# 1. Load the API key from the .env file into the environment (GEMINI_API_KEY)
load_dotenv()

# 2. Initialize the model. It automatically finds the GEMINI_API_KEY environment variable.
model = ChatGoogleGenerativeAI(model='models/gemini-2.5-flash')

# 3. Invoke the model
result = model.invoke("What is the capital of Pakistan?")

# 4. Print the text content of the response
print(result.content)
# Expected Output: The capital of Pakistan is Islamabad. (or similar)
