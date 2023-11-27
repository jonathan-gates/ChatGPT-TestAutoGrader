# Dependencies
OpenAI version 0.28.0
```python
pip install openai==0.28
```

# Data
The data can be found at https://web.eecs.umich.edu/~mihalcea/downloads.html labeled "Data for Automatic Short Answer Grading"

It can also be downloaded directly at this [link](https://web.eecs.umich.edu/~mihalcea/downloads.html#saga)

# Code
### ```chatgpt.py```
To run this file you will need to make a ```.env``` file and place add your API_KEY and ORG_ID. As well as uncommenting one of the ```run_sections``` at the bottom.

### ```test_accuracy.py```
This looks through the outcomes files to get the data for the Correct and Incorrect Guesses as well as the how many were marked incorrectly and in which ways.

### ```readdata.py```
This is used to get the question and the data based on the section and who scored the data.