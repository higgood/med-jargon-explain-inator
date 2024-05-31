import nltk
from model.term_def_retrieval.retrieval import get_definition
from model.jargon_identifier.ner import identify_jargon, identify_jargon_llm

def explain(term: str) -> dict:
    return {"term": term}

def define(term: str) -> dict:
    return get_definition(term)

def identify(text: str) -> list[dict]:
    return identify_jargon(text)

def identify_llm(text: str) -> list[dict]:
    return identify_jargon_llm(text)