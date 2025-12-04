from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="google/gemma-2-2b-it",
    task="text-generation"
)
model = ChatHuggingFace(llm=llm)
parser = JsonOutputParser()

# template = PromptTemplate(
#     template='Give me the name, age & city of a fictional person \n {format_instruction}',
#     input_variables=[],
#     partial_variables={'format_instruction': parser.get_format_instructions()},
# )
template = PromptTemplate(
    template='Give me 5 facts about {topic} \n {format_instruction}',
    input_variables=['topic'],
    partial_variables={'format_instruction': parser.get_format_instructions()},
)

chain = template | model | parser
final_result = chain.invoke({'topic': "AI Revolution"})  # sending blank dict because we do not have any input variables
# prompt = template.format()
# result = model.invoke(prompt)
#
# # print(result)
# final_result = parser.parse(result.content)
print(final_result)

# print(final_result['name'])
# print(final_result['age'])
# print(final_result['city'])
