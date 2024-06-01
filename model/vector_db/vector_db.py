import json
import os
from os.path import basename, dirname, join
from pathlib import Path
from pprint import pprint
from langchain_chroma import Chroma
from langchain_core.documents.base import Document
from langchain_community.embeddings import HuggingFaceEmbeddings

# SET GLOBAL VARIABLES: -----------------------------------
# find root of repo:
dir = os.getcwd()
while basename(dir) != "med-jargon-explain-inator":
    dir = dirname(dirname(dir))

# get absolute paths to the data files:
# NOTE: assumes that the data file structure will not change.
vectorstore_path = join(dir, "data/vector_db")

"""
Takes our two definition files and squashes them into a giant list of Documents (https://api.python.langchain.com/en/latest/documents/langchain_core.documents.base.Document.html)
So that our Vector DB can create embeddings and store them.
@return A List of Documents where each Document looks like
Document(page_content="definition", metadata={term:"term", cui:"cui", source_dict:"source_dictionary"})
"""
def process_definitions():
    cui_to_def_path=join(dir, 'data/cui_to_def_simplified.json')
    cui_to_def = json.loads(Path(cui_to_def_path).read_text())
    term_to_cui_path=join(dir, 'data/term_to_cui_final.json')
    term_to_cui = json.loads(Path(term_to_cui_path).read_text())

    document_list = []
    for key in term_to_cui:
        for cui in term_to_cui[key]:
            if cui in cui_to_def:
                for source_dict in cui_to_def[cui]:
                    metadata = {
                        "term": key,
                        "cui": cui,
                        "source_dict": source_dict
                    }
                    document_list.append(Document(page_content=cui_to_def[cui][source_dict], metadata=metadata))
    
    return document_list

data = process_definitions()

def create_vector_db(documents):
    vectorstore = Chroma.from_documents(documents=documents, embedding=HuggingFaceEmbeddings(), persist_directory=vectorstore_path)
    vectorstore.persist()
    return vectorstore

db = create_vector_db(data)

# vectorstore = Chroma(persist_directory=vectorstore_path, embedding_function=HuggingFaceEmbeddings())
retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 6})
# query = "Give me all the information about nerves"
# retrieved_docs = db.similarity_search(query)
# pprint(retrieved_docs)
# print(retrieved_docs[0].page_content)