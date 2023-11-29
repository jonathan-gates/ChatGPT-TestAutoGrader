# Dependencies
```python
pip install openai
```

# Data
The data can be found at https://web.eecs.umich.edu/~mihalcea/downloads.html labeled "Data for Automatic Short Answer Grading"

It can also be downloaded directly at this [link](https://web.eecs.umich.edu/~mihalcea/downloads.html#saga)

# Code
### ```chatgpt*.py```
To run the chatgpt files you will need to make a ```.env``` file and place add your API_KEY and ORG_ID. Create an empty `outcomes/` directory or change the directory name at the top of the file. As well as uncommenting one of the ```run_section``` at the bottom of the python file.

### ```test_accuracy.py```
This looks through the outcomes files to get the data for the Correct and Incorrect Guesses as well as the how many were marked incorrectly and in which ways. It uses the old way for when it was using openai 0.28. 

### ```readdata.py```
This is used to get the question and the data based on the section and who scored the data.

### ```outcome folders```
These are past runs that can use the ```test_accuracy.py``` to view their stats.

obo -> One by One - meaning chatgpt was given each answer individually

old -> old output for version 0.28 of openai library

20 -> 20% trained

80 -> 80% trained

4.5 -> Greater than 4 counts as correct, instead of just 5's

3 -> only 3 correct and 3 incorrect answers to train on