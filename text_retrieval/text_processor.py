from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dashboard.settings import BASE_DIR


def get_document_chunks():
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n",],
        chunk_size=1000,
        chunk_overlap=90,
        length_function=len
    )

    # loading all documents at once
    loader = DirectoryLoader(path=str(BASE_DIR / "uploads"), glob="**/*.txt")
    documents = loader.load()

    chunks = [chunk.page_content for chunk in text_splitter.split_documents(documents=documents)]

    return chunks