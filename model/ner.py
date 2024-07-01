# Recommended to test on Python 3.7+, openai 0.25+. Use `pip3 install promptify` before calling this script.
# A short script for recongizing name entities using the promptify pipeline and LLM.

from promptify import Prompter,OpenAI, Pipeline

# Input sentence for recognition
sentence     =  " "

model        = OpenAI(api_key) # can also use `HubModel()` for Huggingface-based inference or 'Azure'
prompter     = Prompter('ner.jinja') # select a template or provide custom template
pipe         = Pipeline(prompter , model)

result = pipe.fit(sentence, domain="medical", labels=None)
