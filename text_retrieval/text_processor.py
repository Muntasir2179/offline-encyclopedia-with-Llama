from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dashboard.settings import BASE_DIR
import os


def get_document_chunks():
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n",],
        chunk_size=1000,
        chunk_overlap=90,
        length_function=len
    )

    pdf_files = []
    text_files = []

    for file_name in os.listdir(path=str(BASE_DIR / "uploads")):
        if file_name.split('.')[1] == 'txt':
            text_files.append(file_name)
        else:
            pdf_files.append(file_name)

    all_chunks = []

    # loading all pdf documents at once
    if len(pdf_files) != 0:
        pdf_loader = DirectoryLoader(path=str(BASE_DIR / "uploads"), glob="**/*.pdf")
        pdf_documents = pdf_loader.load()

        for single_chunk in  text_splitter.split_documents(documents=pdf_documents):
            all_chunks.append(str(single_chunk))

    # loading all text files at once
    if len(text_files) != 0:
        text_loader = DirectoryLoader(path=str(BASE_DIR / "uploads"), glob="**/*.txt")
        text_documents = text_loader.load()
        for text_chunk in text_splitter.split_documents(documents=text_documents):
            all_chunks.append(str(text_chunk))

    return all_chunks