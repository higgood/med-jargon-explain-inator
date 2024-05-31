# API endpoints:

Implemented:

* define: it takes as input a term (str) and returns the corresnding list of definitions from `data/cui_to_def_final.json`.

WIP (in PRs, pending review):

* identify: uses string matching against text to find medical terms using the merged (but not simplified) data. The output is a list of dictionaries, each of which has the following fields: char_position_in_text, term_length.
* identify_llm: uses promptify to do NER for identifying medical terms (which may not be an exact string match). The output is a list of dictionaries, each of which has the following fields: char_position_in_text, term_length.

# Model (this is the NLP stuff)
The model is where data becomes useful information. This would normally talk to a database too but we're probably not doing one? Unclear so far. This is where we're gonna put all the NLP stuff like language models!
Try to keep it organized and use the [DRY principle](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself) to keep things readable.
