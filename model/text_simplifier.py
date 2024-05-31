from transformers import T5Tokenizer, T5ForConditionalGeneration
from transformers import BartForConditionalGeneration, BartTokenizer
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
from datasets import load_metric
from nltk.tokenize import word_tokenize

import re
import csv

def csv_loader(filepath: str):
    """
    Load a CSV file into a gold standard and input dictionary for use in the text simplifier model

    Arguments:
    filepath
        The string path indicating where the .csv file is stored

    Returns:
    ref_dict
        A dictionary with row ids as keys and the gold standard simplified sentences as values.
        To be used as the gold standard for evaluation of model performance
    input_dict
        A dictionary with row ids as keys and the original length sentences as values. To be
        used as input for the text simplification model
    """
    
    with open(filepath, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)

    # Initialize dictionary to store gold references, and input sentences
    ref_dict = {}
    input_dict = {}

    # Add the file data into dictionaries based on placement in the csv
    for row in data[1:50]:
        id = row[0]
        sentence = row[1]
        simple_sentence = row[2]
        ref_dict[id] = simple_sentence
        input_dict[id] = sentence
    
    return ref_dict, input_dict


class TextSimplifier:
    """
    A class used to simplify sentences with three options for pre-trained models and tokenizers

    Attributes:
    ----------
    model_type : str
        Specifies the pre-trained model that is used for simplification 
        The supported models are 'T5', 'Pegasus', and 'BART'.

    Methods:
    -------
    setup_model():
        Initializes the appropriate model and tokenizer based on the specified model_type.
        
    clean_definition(sentence: str) -> str:
        Cleans the model output by removing any artifacts from the 'simplify:' prompt.

    simplify_sentence(sentence: str) -> str:
        Simplifies the input sentence using the initialized model and tokenizer.

    simplify_sentences(sentences: dict, write_output: bool, output_file: str = None) -> Optional[dict]:
        Simplifies a dictionary of sentences and optionally writes the output to a file.
        
    evaluate(gold_std: dict, write_output: bool, output_file: str = None) -> dict:
        Evaluates the simplified sentences against a gold standard using ROUGE and METEOR metrics and optionally writes the results to a file.
    """

    def __init__(self, model_type):
        
        self.model_type = model_type


    def setup_model(self):
        """
        Initialize the model and tokenizer depending on the model_type specified for the TextSimplifier Class.
        """

        if self.model_type == 'T5':
            # Initialize T5 model and tokenizer
            model = T5ForConditionalGeneration.from_pretrained('t5-base')
            tokenizer = T5Tokenizer.from_pretrained('t5-base')
        
        elif self.model_type == 'Pegasus':
            # Initialize Pegasus model and tokenizer
            model = PegasusForConditionalGeneration.from_pretrained('google/pegasus-xsum')
            tokenizer = PegasusTokenizer.from_pretrained('google/pegasus-xsum')

        elif self.model_type == 'BART':
            # Initialize BART model and tokenizer
            model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')
            tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')

        # Save model and tokenizer
        self.model = model
        self.tokenizer = tokenizer


    def clean_definition(self, sentence: str):
        """
        Removes whitespace and colons from the left-hand side of the sentence string

        Arguments:
        sentence
            The sentence to be cleaned

        Returns:
        sentence
            The cleaned version of the input sentence
        """
        # remove initial prompt if still present
        sentence = re.sub(r'to simplify', '', sentence)

        # remove any leading colons and whitespace if they're present in the sentence
        sentence = re.sub(r'^[:\s]*', '', sentence)

        return sentence
    

    def simplify_sentence(self, sentence: str):
        """
        Use the established encoder-decoder model to simplify a given sentence and return the output.

        Arguments:
        sentence
            The sentence to be simplified using the model.
        
        Returns:
        simplified_sentence
            The simplified version of the input sentence provided.
        """

        if self.model_type == 'T5':
            # Run the T5 Encoder-Decoder model on the given sentence
            inputs = self.tokenizer.encode("simplify: " + sentence, return_tensors="pt", max_length=512, truncation=True)
            outputs = self.model.generate(inputs, max_length=512, num_beams=4, early_stopping=True)
            simplified_sentence = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        elif self.model_type == 'Pegasus':
            # Run the Pegasus Encoder-Decoder model on the given sentence
            inputs = self.tokenizer.encode("simplify: " + sentence, return_tensors="pt", max_length=512, truncation=True)
            outputs = self.model.generate(inputs, max_length=512, num_beams=4, early_stopping=True)
            simplified_sentence = self.tokenizer.decode(outputs[0], skip_special_tokens=True)           

        elif self.model_type == 'BART':
            # Run the BART Encoder-Decoder model on the given sentence
            inputs = self.tokenizer.encode("simplify: " + sentence, return_tensors="pt", max_length=1024, truncation=True)
            outputs = self.model.generate(inputs, max_length=1024, num_beams=4, early_stopping=True)
            simplified_sentence = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        return simplified_sentence


    def simplify_sentences(self, sentences: dict, write_output: bool, output_file: str = None ):
        """
        Takes a dictionary of words and their definitions, and provides simplified sentences

        Arguments:
        sentences
            A dictionary with words as keys and their definitions as values
        write_output
            A boolean that tells the system whether to write the output to a file
        output_file
            A string to be used as the output file path for writing the simplified sentences

        Returns:
        out_dict (Optional)
            If write_output is True, return a dictionary with words as keys, and values as a dictionary 
            with keys as 'original' and 'simple' as keys, and the original and simplified sentences as values
        """
        
        # Write output file and return a dictionary with simplified sentences
        if write_output == True:
            out_dict = {}
            if output_file is not None:
                with open(output_file, "w") as f:
                    for key, value in sentences.items():
                        simplified_sentence = self.simplify_sentence(value)
                        simplified_sentence = self.clean_definition(simplified_sentence)
                        f.write(key + "\n")
                        f.write("Original sentence:" + '\n' + str(value) + '\n')
                        f.write("Simplified sentence:" + '\n' + str(simplified_sentence) + '\n\n')
                        out_dict[key] = {}
                        out_dict[key]['original'] = value
                        out_dict[key]['simple'] = simplified_sentence
            else:
                raise Exception("Please specify an output path if you want to write the output to a file")
            
            self.simple_dict = out_dict
            return out_dict

        # Do not write output file, but return a dictionary with simplified sentences
        elif write_output == False:
            for key, value in sentences.items():
                simplified_sentence = self.simplify_sentence(value)
                simplified_sentence = self.clean_definition(simplified_sentence)
                out_dict[key] = {}
                out_dict[key]['original'] = value
                out_dict[key]['simple'] = simplified_sentence
            
            self.simple_dict = out_dict
            return out_dict

    def simplify_medical_definitions(self, sentences: dict):
        """
        Takes a dictionary of words and their definitions, and provides simplified sentences

        Arguments:
        sentences
            A dictionary with words as keys and their definitions as values

        Returns:
        out_dict
            A dictionary with words as keys, and values as a nested dictionary with database names and their definitions
        """
        out_dict = {}

        # go through all definitions that need simplification, create new dictionary with simplified definitions
        for term in sentences.keys():
            for database in sentences[term].keys():
                definition = sentences[term][database]

                simplified_definition = self.simplify_sentence(definition)
                simplified_definition = self.clean_definition(simplified_definition)

                out_dict[term] = {}
                out_dict[term][database] = simplified_definition

        return out_dict


    def evaluate(self, gold_std: dict, write_output: bool, output_file: str = None):
        """
        Given an evaluation metric, the function splits its dictionary into reference and prediction sentences,
        then evaluates the data on that metric and returns it.

        Arguments:
        gold_std
            Dictionary with the gold standard simplifications to compare against in evaluation
        write_output
            Boolean argument specifying whether to write the output to a file or not
        output_file (Optional)
            String specifying the path to the output file that is written

        Returns:
        results
            The results of the evaluation on the system
        """
        results = {}
        references = []
        predictions = []

        # Retrieve list of references
        for key in gold_std:
            references.append(gold_std[key])

        # Retrieve list of predictions
        for key in self.simple_dict:
            predictions.append(self.simple_dict[key]['simple'])

        eval_metrics = ['rouge', 'meteor']
        for eval_metric in eval_metrics:

            # Instantiate evaluation based on current eval_metric
            metric = load_metric(eval_metric)
            result = metric.compute(predictions=predictions, references=references)
            results[eval_metric] = result

        # Return and write the evaluation to output depending on the input for write_output
        # If writing output file
        if write_output == True and output_file is not None:
            with open(output_file, "w") as f:
                for metric_name, result in results.items():
                    if metric_name == "rouge":
                        f.write(f"ROUGE1 score: {result['rouge1']}\n")
                        f.write(f"ROUGE2 score: {result['rouge2']}\n")
                    elif metric_name == "meteor":
                        f.write(f"METEOR score: {result['meteor']}\n")
            
            return results

        # If writing output file but no output_file specified
        elif write_output == True and output_file is None:
            raise Exception("Please specify an output path if you want to write the output to a file")
        
        # If not writing output file
        else:
            return results
        

if __name__ == '__main__':

    # Read csv file for evaluating model
    ref_dict, input_dict = csv_loader("data/aligned_data.csv")
    
    # Specify the model name as either 'T5', 'Pegasus', or 'BART'
    model = 'BART'
    # Name files accordingly for output
    definitions_path = 'outputs/sentences' + model + '_sentences.txt'
    evaluations_path = 'outputs/evaluations' + model + '_evaluations.txt'

    # Example usage of simplifying sentences
    definitions = {"adhesion": "A band of scar tissue that joins normally separated internal body structures, most often after surgery, inflammation, or injury in the area.",
                    "arthroscopy": "A minimally invasive diagnostic and treatment procedure used for conditions of a joint. This procedure uses a small, lighted, optic tube (arthroscope) which is inserted into the joint through a small incision in the joint. Images of the inside of the joint are projected onto a screen; used to evaluate any degenerative and/or arthritic changes in the joint; to detect bone diseases and tumors; to determine the cause of bone pain and inflammation.",
                    "carpal tunnel": "Passageway in the wrist through which nerves and the flexor muscles of the hands pass.",
                    "CT scan": "Computed Tomography (CT) is a non-invasive, diagnostic procedure that uses a series of x-rays to show a cross-sectional view of the inside of the body.",
                    "fusion": "Correction of an unstable part of the spine by joining two or more vertebrae. Usually done surgically, but sometimes done by traction or immobilization.",
                    "gastroenterostomy": "Surgical creation of an opening between the stomach wall and the small intestines; performed when the normal opening has been eliminated.",
                    "meniscus": "Crescent-shaped cartilage between the upper end of the tibia (shin bone) and the femur (thigh bone).",
                    "pelvic floor": "Muscles and connective tissue providing support for pelvic organs; e.g. bladder, lower intestines, uterus (in females); also aids in continence as part of the urinary and anal sphincters.",
                    "pleurisy": "Inflammation of the pleura that is characterized by sudden onset, painful and difficult respiration and exudation of fluid or fibrinous material into the pleural cavity." 
                }
    
    # Initialize TextSimplifier class specifying model as eiter 'T5', 'Pegasus', or 'BART'
    simplifier = TextSimplifier(model_type=model)

    # Set up the class model
    simplifier.setup_model()

    # Simplify the sentences in the dictionary above
    simplified_definitions = simplifier.simplify_sentences(sentences=input_dict,
                                                           write_output=True,
                                                           output_file=definitions_path)
    
    print(simplified_definitions)
    
    # Evaluate the simplifier model's performance using two metrics: 'rouge' and 'meteor'
    evaluations = simplifier.evaluate(gold_std= ref_dict,
                                      write_output=True, 
                                      output_file=evaluations_path)
    
    print(evaluations)

    
