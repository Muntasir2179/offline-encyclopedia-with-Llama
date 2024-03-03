from langchain_community.llms import LlamaCpp

llm = LlamaCpp(
    model_path="llama/llama-2-7b.Q3_K_S.gguf",
    temperature=0.1,
    max_tokens=2000,
    top_p=1
)

def response(context, question):
    prompt = f"""Use the following pieces of information to answer the user's question. If you don't know the answer,
    say that you don't know, don't try to make up an answer.
    Context: {context}
    Question: {question}
    Only return the helpful answer, Answer must be detailed and well explained.
    """
    
    return llm.invoke(prompt)