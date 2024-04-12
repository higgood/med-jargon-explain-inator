# med-jargon-explain-inator

BEHOLD! THE MED-JARGON-EXPLAIN-INATOR! With this I will get rid of all pedantic and overly indulgent usage of jargon in the TRI-STATE AREA, thereby increasing MEDICAL LITERACY for all!!

## Setup
TBD, but you'll need at least Python 3.6. Python packages needed are listed here:
- `nltk`
- `fastapi`
- `"uvicorn[standard]"`
Install by using `pip <package name>`

## Structure
The explain-inator is built using a traditional [Model-View-Controller](https://www.geeksforgeeks.org/mvc-framework-introduction/) framework. See the READMEs inside each folder to see more details about how this all works together.

## Running the app
Run `uvicorn main:app --reload` in your terminal. Then navigate to `http://127.0.0.1:8000` and you should see the Hello World! message.
Navigating to `127.0.0.1:8000/docs` will give you the OpenAPI documentation for all the REST routes we currently have.