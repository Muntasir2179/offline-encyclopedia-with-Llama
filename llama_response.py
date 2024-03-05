# from langchain_community.llms import LlamaCpp

# llm = LlamaCpp(
#     model_path="llama/llama-2-7b.Q3_K_S.gguf",
#     temperature=0.1,
#     max_tokens=2000,
#     top_p=1
# )

# def response(context, question):
#     prompt = f"""Use the following pieces of information to answer the user's question. If you don't know the answer,
#     say that you don't know, don't try to make up an answer.
#     Context: {context}
#     Question: {question}
#     Only return the helpful answer, Answer must be detailed and well explained.
#     """
    
#     return llm.invoke(prompt)

from deepsparse import TextGeneration
import re


# loading the tiny llama model
model = TextGeneration(model="llama/TinyLlama")


def clean_text(input_text):
    cleaned_text = re.sub(r'[^a-zA-Z0-9\s]', '', input_text)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
    return cleaned_text


def response(context, question):
    formatted_prompt = f"""
    <<SYS>>
    Your task is to analyze the texts in the 'Context' and generate answer for the question in 'Question'.\n
    If you do not know the answer simply say you do not know.\n

    Context:{context}\n
    <</SYS>>
    [INST]
    Question:{question}\n
    [/INST]\n

    Assistant:
    """

    return clean_text(model(formatted_prompt, max_new_tokens=500).generations[0].text)