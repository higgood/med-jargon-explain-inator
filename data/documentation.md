# Data documentation
This file describes the various data artifacts we created in this project in Sp'24.

## Data artifacts

### Structured data
* cui_to_def.json: A recent, processed snapshot of UMLS focusing on medical terms. CUI is an machine-readable identifier for UMLS terms.
* semantic_groups.txt: the categories used to filter out non-medical terms (as part of the processing for cui_to_def.json).
* cui_to_def_final.json: This file is a derivative of process_json.py (described below).
* cui_to_def_simplified.json: This is similar to cui_to_def_final.json but it replaces complex definitions with their simplified versions. We define complex definitions as ones with a reading difficulty score >= 45. Simplified definitions are produced by T5, using `model/simplifier_pipeline.py`.
* jargon.txt: This is the non-UMLS terms (with definitions), which are combined with UMLS data before merging into cui_to_def_final.json. More details about how they were curated can be found herein.
* term_to_cui.json: This file maps (potentially ambiguous) term strings from UMLS to one or more CUIs. This is already filtered according to semantic_groups.txt.
* term_to_cui_final.json: This file is a derivative of process_json.py (described below).

### Unstructured data
* aligned_data.csv: A parallel general-domain corpus for English Wikipedia vs. Simple English Wikipedia. It was useful for training/evaluating models for simplifying medical definitions.

### Scripts
process_json.py: A script that combines UMLS and non-UMLS medical terms into the same format, in order to increase coverage and customize the medical ontology used as a data backbone for this system.

## How we curated non-UMLS data 

Processing Steps Documentation

Abbreviations:
1. Located abbreviations in file
2. Examined nearby terms for unabbreviated terms, as abbreviations are located near their full forms
3. Cross-referenced Harrison's Principles of Internal Medicine, Volumes 1 and 2, 20th ed, and the National Cancer Institute's Dictionaries as necessary
4. Remove abbreviations from data file and copied to abbreviations json file with appropriate full form


Non-Medical Jargon:
1. Examined terms in the file
2. Cross-referenced Harrison's Principles of Internal Medicine, Volumes 1 and 2, 20th ed, Robbins and Cotran Pathologic Basis of Disease 9th ed, Robbins and Cotran Atlas of Pathology 3rd ed, and Schaechter's Mechanisms of Microbial Disease 5th ed, as necessary to determine if term is medical jargon
3. Remove non-medical jargon from document



References for Medical Jargon and Abbreviations: 

Engleberg, N. C., DiRita, V. J., & Dermody, T. S. (2013). Schaechter’s Mechanisms of Microbial Disease (5th ed.). Lippincott, Williams & Wilkins. 

Jameson, J. L., Kasper, D. L., Longo, D. L., Fauci, A. S., Hauser, S. L., & Loscalzo, J. (2018). Harrison’s Principles of Internal Medicine (20th ed., Vol. 1). McGraw Hill Education. 

Jameson, J. L., Kasper, D. L., Longo, D. L., Fauci, A. S., Hauser, S. L., & Loscalzo, J. (2018). Harrison’s Principles of Internal Medicine (20th ed., Vol. 2). McGraw Hill Education.

Klatt, E. C. (2015). Robbins and Cotran Atlas of Pathology (3rd ed.). Elsevier Saunders. 

Kumar, V., Abbas, A. K., & Aster, J. C. (2015). Robbins and Cotran Pathologic Basis of Disease (9th ed.). Elsevier Saunders. 

NCI Dictionaries: https://www.cancer.gov/publications/dictionaries


 

Data Sources for Definitions:

Medline Plus: https://medlineplus.gov/xml/mplus_topics_2024-05-03.xml

MedJ Sample File: https://github.com/MozziTasteBitter/MedJEx/tree/main/data

MedJ Citation:

@inproceedings{kwon-etal-2022-medjex,
title = "{M}ed{JE}x: A Medical Jargon Extraction Model with {W}iki{'}s Hyperlink Span and Contextualized Masked Language Model Score",
author = "Kwon, Sunjae  and
  Yao, Zonghai  and
  Jordan, Harmon  and
  Levy, David  and
  Corner, Brian  and
  Yu, Hong",
booktitle = "Proceedings of the 2022 Conference on Empirical Methods in Natural Language Processing",
month = dec,
year = "2022",
address = "Abu Dhabi, United Arab Emirates",
publisher = "Association for Computational Linguistics",
url = "https://aclanthology.org/2022.emnlp-main.805",
pages = "11733--11751"}
