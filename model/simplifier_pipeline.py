from text_simplifier import TextSimplifier
from reading_ease_evaluation.reading import ReadingDifficultyCalculator
import json


class SimplifierPipeline:
    """
    Class that loads medical jargon terms and their definitions from json files, scores each
    definition to get a reading difficulty score, and then simplifies definitions whose scores
    are higher than the cutoff score.
    """
	
    def __init__(self, term2cui, cui2def, reading_diff, model, new_cui2def_path):
        """
        Initializes the model, establishes paths for the two json files. 
        Identifies the cutoff reading difficulty score for a definition to be simplified
        """
        self.term2cui = term2cui
        self.cui2def = cui2def
        self.reading_diff = reading_diff
        self.model = model
        self.new_cui2def_path = new_cui2def_path


    def load_files(self):
        """
        Reads in two json files, connects terms with their definitions based on shared cui values.
        Stores dictionary in class.
        """

        # Load term2cui
        with open(self.term2cui, 'r') as f:
            t2c = json.load(f)
            self.t2c = t2c
        
        # Load cui2def
        with open(self.cui2def, "r") as g:
            c2d = json.load(g)
            self.c2d = c2d

        # Create term to definition dictionary
        termdict = {}
        for term in t2c.keys():

            # Connect term to definitions through cui
            cui = t2c[term]

            # If cui is a list, iterate over each cui
            if isinstance(cui, list):
                for c in cui:
                    if c in c2d:
                        definitions = c2d[c]
                        if term not in termdict:
                            termdict[term] = {}
                        for database in definitions.keys():
                            termdict[term][database] = definitions[database]
            else:
                if cui in c2d:
                    definitions = c2d[cui]
                    if term not in termdict:
                        termdict[term] = {}
                    for database in definitions.keys():
                        termdict[term][database] = definitions[database]
        
        # Save dictionary for future use
        self.termdict = termdict

    
    def check_reading_scores(self):
        """
        Calculates the reading difficulty of each definition, creates new dictionary of definitions that must be simplified
        """

        defs2simplify = {}
        for term in self.termdict.keys():
            for database in self.termdict[term]:
                definition = self.termdict[term][database]

                # Calculate reading difficulty of the definition
                calculator = ReadingDifficultyCalculator(definition)
                difficulty = calculator.calculate_reading_difficulty()

                # Adds definition to new dictionary if difficulty score is higher than the cutoff value
                if difficulty > self.reading_diff:
                    defs2simplify[term] = {}
                    defs2simplify[term][database] = definition

        # Save dictionary for future use
        self.defs2simplify = defs2simplify


    def get_simplified_sentences(self):
        """
        Simplifies a set of sentences, integrates them back into the term dictionary
        """
        # Initialize TextSimplifier class model
        simplifier = TextSimplifier(model_type=self.model)

        # Set up the class model
        simplifier.setup_model()

        # Simplify the sentences in the dictionary above
        simplified_definitions = simplifier.simplify_medical_definitions(sentences=self.defs2simplify)

        # Add simplified sentences back into term definitions dictionary
        for term in simplified_definitions.keys():
            for database in simplified_definitions[term].keys():
                simple_definition = simplified_definitions[term][database]

                # Replace termdict definition with simplified replacement
                self.termdict[term][database] = simple_definition
            
        
    def convert_to_json(self):
        """
        Converts termdict content into a new cui_to_def file including the simplified sentences.
        term_to_cui should remain unchanged, since no new terms or cui values are generated
        """
        new_cui2dict = {}

        for term in self.termdict.keys():
            
            # Get cui value for pair
            cui = self.t2c[term][0]
            new_cui2dict[cui] = {}

            # Add all definitions into dictionary based on their database of origin
            for database in self.termdict[term].keys():
                definition = self.termdict[term][database]
                new_cui2dict[cui][database] = definition

        with open(self.new_cui2def_path, "w") as json_file:
            json.dump(new_cui2dict, json_file, indent=4)
        


if __name__ == '__main__':

    # Identify file paths
    term2cui = "data/term_to_cui_final.json"
    cui2def = "data/cui_to_def_final.json"
    new_cui2def_path = "data/cui_to_def_simplified.json"
    # Establish the reading difficulty cut-off score
    reading_diff = 45
    # Initialize TextSimplifier class specifying model as either 'T5', 'Pegasus', or 'BART'
    model = "T5"

    # Initialize the model
    simplifier = SimplifierPipeline(term2cui=term2cui, 
                                    cui2def=cui2def, 
                                    reading_diff=reading_diff,
                                    model = model,
                                    new_cui2def_path = new_cui2def_path)

    # Load the definitions into a dictionary
    simplifier.load_files()

    # Get reading scores for all definitions
    simplifier.check_reading_scores()

    # Produce simplified definitions for subset of data
    simplifier.get_simplified_sentences()

    # Add new sentences into json file and save
    simplifier.convert_to_json()

