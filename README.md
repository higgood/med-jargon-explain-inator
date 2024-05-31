# med-jargon-explain-inator

BEHOLD! THE MED-JARGON-EXPLAIN-INATOR! With this I will get rid of all pedantic and overly indulgent usage of jargon in the TRI-STATE AREA, thereby increasing MEDICAL LITERACY for all!! 🎉

## 📆 Schedule 📆
4/25
- Low-fidelity design for UX using figma and/or swagger.
- Create a UX design questionnaire based on the design.

5/2
- Fill out the questionnaire x 3 times with user hat on.
- Create a 1-page report to summarize the results and make recommendations for a more inclusive UX design.

## Setup
TBD, but you'll need at least Python 3.6. Install by using `pip <package name>`. Python packages needed are listed here:
- `nltk`
- `fastapi`
- `"uvicorn[standard]"`

## Structure
The explain-inator is built using a traditional [Model-View-Controller](https://www.geeksforgeeks.org/mvc-framework-introduction/) framework. See the READMEs inside each folder to see more details about how this all works together.

## Running the app
Run `uvicorn main:app --reload` in your terminal. Then navigate to `http://127.0.0.1:8000` and you should see the Hello World! message.
Navigating to `127.0.0.1:8000/docs` will give you the OpenAPI documentation for all the REST routes we currently have.

## Running the simplification model
The text simplification model is stored under model/text_simplifier.py. It can be run using the shell script ~./run_simplifier.sh located in the med_jargon_explain_inator directory. This model has a "model" parameter that should be specified on line 249, as well as various function parameters that can be changed to alter where the sentences and evaluations are output (write new files to the directory, or just return printed dictionaries). There are three model options: BERT, Pegasus, and T5, with T5 currently getting the best evaluation results on our three evaluation metrics (METEOR, Rouge1, Rouge2).

The setup folder includes a requirements.yml folder, and two shell scripts used to create a virtual environment and to update the virtual environment. These play a key role in running the entire system, and text_simplifier.py needs to be run on the virtual environment to ensure the user has all the correct packages and versions installed.
