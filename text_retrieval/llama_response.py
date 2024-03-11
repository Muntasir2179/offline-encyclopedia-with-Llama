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
    prompt = f'''
    Given the following information answer the following question only once:

    {context}

    Question: {question}
    '''
    formatted_prompt =  f"<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n"

    return clean_text(model(formatted_prompt, max_new_tokens=500).generations[0].text)