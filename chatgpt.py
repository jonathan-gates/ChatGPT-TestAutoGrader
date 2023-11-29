import time
from openai import OpenAI
from dotenv import load_dotenv
import os
from readdata import getData, getQuestion, getSections
import random

score_type = 'ave'
# score_type = 'me'
# score_type = 'other'

# section = '1.1'

directory = 'outcomes/'

train_percentage = 0.2

# trains on 20% of the data and tests on the other 80%
def run_section(section, score_type):

    data = getData(section, score_type)
    # separate the data randomly into train and test sets, 80% train and 20% test
    train_correct = []
    train_incorrect = []
    correct_messages = ["Some example correct solutions are: \n"]
    incorrect_messages = ["\nSome example incorrect solutions are: \n"]
    test = []
    expected = []
    test_messages = ["Suppose a student submitted: \n"]
    for key in data:
        if random.random() <= train_percentage:
            # separate train into correct and incorrect
            if data[key] == 'correct':
                train_correct.append((key, 'correct'))
                correct_messages.append(key + '\n')
            else:
                train_incorrect.append((key, 'incorrect'))
                incorrect_messages.append(key + '\n')
            
        else:
            test.append((key, data[key]))
            # add to test messages
            test_messages.append(key + '\n')
            # add the expected answer
            expected.append(data[key])
            
    test_messages.append('\nHow would you grade this? Please simply respond with the word "correct" or "incorrect" for each.')
    question = getQuestion(section)

    prompt = f"I need you to pretend to be an instructor for a Data Structures course. The students have been assigned to answer the question: {question}\n" + "".join(correct_messages) + "".join(incorrect_messages) + "".join(test_messages)

    load_dotenv()

    api_key_env = os.getenv("API_KEY")
    org_id = os.getenv("ORG_ID")

    client = OpenAI(
        api_key=api_key_env,
        organization=org_id,
    )

    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-4",
    )

    content = response.choices[0].message.content

    current_time = int(round(time.time() * 1000))
    with open(directory + section + '_' + score_type + '_' + str(train_percentage) + "_gpt_" + str(round(current_time)), 'w') as file:
        file.write('GPT Answered: \n')
        file.write(str(content))
        file.write('\n\n')
        file.write('Expected: \n')
        file.write(str(expected))

        
section_names = getSections()

# for section in section_names:
#     run_section(section, score_type) # call for ChatGPT

# run_section('1.1', score_type) # run just one section