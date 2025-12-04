from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="google/gemma-2-2b-it",
    task="text-generation"
)
model = ChatHuggingFace(llm=llm)


class Person(BaseModel):
    name: str = Field(description="Person's name")
    age: int = Field(gt=18, description="Person's age")
    city: str = Field(description="Person's city")


parser = PydanticOutputParser(pydantic_object=Person)
template = PromptTemplate(
    template='Generate name, age & city of a fictional {place} person \n {format_instruction}',
    input_variables=['place'],
    partial_variables={'format_instruction': parser.get_format_instructions()}
)

chain = template | model | parser

# prompt = template.invoke({'place': 'Pakistani'})

# result = model.invoke(prompt)
final_result = chain.invoke({'place': 'Pakistani'})

print(final_result)
