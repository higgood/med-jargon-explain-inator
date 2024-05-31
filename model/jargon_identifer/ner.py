# Recommended to test on Python 3.7+, openai 0.25+. Use `pip3 install promptify` before calling this script.
# A short script for recognizing name entities using the promptify pipeline and LLM.

import os
from os.path import basename, dirname, join
import json
import regex as re
from nltk.tokenize import word_tokenize
from promptify import Prompter, OpenAI, Pipeline


def get_app_root() -> str:
    """
    Finds the root of the app repo.

    Assumes code is being run from the root or deeper in the file structure.

    Returns:
        str: the absolute path to the app root.
    """
    # find app root
    dir = os.getcwd()
    while basename(dir) != "med-jargon-explain-inator":
        dir = dirname(dirname(dir))
        
    return dir


def get_openai_key():
    """
    Finds and loads a .txt file containing the API user's OpenAI API key.

    Expects API key to be in "med-jargon-explain-inator/openai-api-key.txt".
    This file should contain one line with the key and no
    other characters.

    Returns:
        api_key (str): the key to be used in OpenAI API calls
    """
    dir = get_app_root()

    # read in API key from file
    api_key_file = join(dir, "openai-api-key.txt")
    with open(api_key_file, 'r') as f:
        api_key = f.read()

    return api_key


def load_data(filename: str) -> dict:
    """
    Loads a data file (term-to-cui or cui-to-def).

    Arguments:
        filename (str): the name of the file (e.g., "term_to_cui_final.json")

    Returns:
        dict{}: the loaded file
    """
    dir = get_app_root()
    data_file = join(dir, f"data/{filename}")
    with open(data_file, 'r') as f:
        data_dict = json.load(f)

    return data_dict


def get_term_indices(terms: list[str], text: str) -> list[dict]:
    """
    Identifies the location of term(s) in a given text.

    Arguments:
        terms (list[str]): A list of medical jargon in the text.
        text (str): The text containing potential medical jargon.
    
    Returns:
        list[dict{}, dict{}, ...]
        Each dictionary represents an identified jargon phrase and contains 
        the following keys:
            - char_position_in_text (int): The index of the jargon's first 
                character in the full text
            - term_length (int): The full length of the jargon phrase (offset)

        Generally, len(return_list) >= len(terms). A term seen more than once
        in a text will be given multiple dictionaries to represent those
        positions.
    """
    term_positions = []

    # find each term in the text
    for t in terms:
        match_list = re.finditer(t, text, flags=re.IGNORECASE)
        if match_list:
            for match in match_list:
                start, end = match.span()
                length = end - start
                term_positions.append({"char_position_in_text": start,
                                       "term_length": length})
                
    return term_positions


def identify_jargon_llm(text: str) -> list[dict]:
    """
    Identifies medical jargon in a given text using Promptify.

    Given a text of any length (one or multiple sentences), this function
    identifies the *locations* of potential medical jargon. Each term will
    need to be sliced from the original text using the returned indices.

    This function is similar to identify_jargon(), except that it requires
    an OpenAI API key and sends text data to GPT-3.5.

    Arguments:
        text (str): The text containing potential medical jargon.
    
    Returns:
        list[dict{}, dict{}, ...]
        Each dictionary represents an identified jargon phrase and contains 
        the following keys:
            - char_position_in_text (int): The index of the jargon's first 
                character in the full text
            - term_length (int): The full length of the jargon phrase (offset)
    """
    # get API key from file at root
    api_key = get_openai_key()

    # Input sentence for recognition - runs quickly w/ triple quotes (?)
    sentence =  f"""{text}"""

    # set up promptify model:
    model = OpenAI(api_key)
    prompter = Prompter('ner.jinja')
    pipe = Pipeline(prompter , model)

    # call promptify:
    result = pipe.fit(sentence, domain="medical", labels=None)

    # find jargon in model output:
    completion = result[0]['parsed']['data']['completion']
    terms = [term['E'] for term in completion if 'E' in term.keys()]

    # find term indices in original text:
    return get_term_indices(terms, text)


def identify_jargon(text: str) -> list[dict]:
    """
    Identifies medical jargon in a given text using text processing techniques.

    Given a text of any length (one or multiple sentences), this function
    identifies the *locations* of potential medical jargon. Each term will
    need to be sliced from the original text using the returned indices.

    This is similar to identify_jargon_llm(), except that it purely uses text
    processing and checks for exact phrase matches in our list of terms. It may
    take longer, given longer texts, but it is (1) less likely to error out (at
    least not for reasons outside of our control) and (2) not sending private
    data to an LLM host.

    Arguments:
        text (str): The text containing potential medical jargon.
    
    Returns:
        list[dict{}, dict{}, ...]
        Each dictionary represents an identified jargon phrase and contains 
        the following keys:
            - char_position_in_text (int): The index of the jargon's first 
                character in the full text
            - term_length (int): The full length of the jargon phrase (offset)
    """
    # load our term dictionary
    term_to_cui_dict = load_data("term_to_cui_final.json")
    recognized_term_list = term_to_cui_dict.keys()

    # tokenize + lowercase (Ex: "Pulmonary embolism's a tough condition...")
    tokens = [t.lower() for t in word_tokenize(text)]
    token_ct = len(tokens)

    # run through text in slices, adding recognized jargon to list
    terms = []

    # all of our terms are <=5 tokens long
    for idx in range(token_ct - 4):
        # look at phrases of length 1 - 5:
        for offset in range(1, 6):
            potential_term = " ".join(tokens[idx:idx+offset])
            # if the phrase is in our list, add it as "identified jargon":
            if potential_term in recognized_term_list:
                terms.append(potential_term)

    return get_term_indices(terms, text)


# # --------------------------------------------------------
# # Below are a few texts for DEBUGGING this file:
# # Example sentence:
# sent = "Test results returned positive for chronic emphesyma and an embolism. Testing soon for asthma and COPD."
# # Example doc:
# with open("example_doc.txt", 'r') as f:
#     text = f.read()

# # Run & print each kind of jardon ID'er:
# print(identify_jargon(sent))
# print(identify_jargon(text))

# print(identify_jargon_llm(sent))
# print(identify_jargon_llm(text))