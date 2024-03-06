from deepsparse import TextGeneration
import re


# loading the tiny llama model
model = TextGeneration(model="llama/TinyLlama")


# for clearing up the model's response
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