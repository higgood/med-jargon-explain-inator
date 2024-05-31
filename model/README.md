# API endpoints:

Implemented:

* define: it takes as input a term (str) and returns the corresnding list of definitions from `data/cui_to_def_final.json`.

WIP (in PRs, pending review):

* identify: uses string matching against text to find medical terms using the merged (but not simplified) data. The output is a list of dictionaries, each of which has the following fields: char_position_in_text, term_length.
* identify_llm: uses promptify to do NER for identifying medical terms (which may not be an exact string match). The output is a list of dictionaries, each of which has the following fields: char_position_in_text, term_length.

# model/jargon_identifier/ner.py
WIP: Without using the API endpoints, one can use the following two methods for identifying jargon in a document:

identify_jargon_llm() - Based on Vicky's code using the Promptify package. This sends the document to OpenAI's GPT-3.5 with an NER template tailored to medical jargon recognition.
Requires the API user to put an OpenAI API key in med-jargon-explain-inator/openai-api-key.txt
Promptify's ner.jinja template works extremely well, but it only works with OpenAI models. This is a bit of a data privacy concern, given the expected use-case of this API, so I implemented another method, described below.
Sometimes hangs (probably because it's generating bad JSONs).
identify_jargon() - Looks for exact matches between the text and our term list in term_to_cui_final.json. Uses pure python string processing and NLTK's tokenizer.
Not as effective. Our term list has a lot of stopwords and non-medical jargon.
If you compare each function's output on the example care instructions in model/jargon_identifier/example_doc.txt, you can see how our list affects the quality of identify_jargon's output.
BUT ! Doesn't send sensitive medical information to a third-party.
This new script model/jargon_identifier/ner.py uses similar file access as retrieval.py by locating the absolute path to the root from the current working directory, then finding the relevant file.

# model/vector_db/vector_db.py
WIP: To retrieve and store data (in our case, definitions), one can use these (recommended but not mandatory) methods:

[Chroma DB](https://www.trychroma.com/) - Chroma is a free Vector DB that handles storing and retriving vectors. Additionally, it allows for similarity search based on an arbitrary search string. 
Some embedding model - Chroma will save and retrieve embeddings but cannot create it on its own. Therefore, another vectorizing library is required. A small sample can be found in the [LangChain docs](https://python.langchain.com/v0.1/docs/integrations/text_embedding/)

Sample code is in the Pull Requests.

# Model (this is the NLP stuff)
The model is where data becomes useful information. This would normally talk to a database too but we're probably not doing one? Unclear so far. This is where we're gonna put all the NLP stuff like language models!
Try to keep it organized and use the [DRY principle](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself) to keep things readable.
