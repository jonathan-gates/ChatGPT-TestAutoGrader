import time
import openai
from dotenv import load_dotenv
import os
# from icecream import ic
from readdata import getData, getQuestion
import random

score_type = 'ave'
# score_type = 'me'
# score_type = 'other'

# section = '1.1'

def run_section(section, score_type):

    train_percentage = 0.8

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
        if random.random() < train_percentage:
            # separate train into correct and incorrect
            if data[key] == 'correct':
                train_correct.append((key, 'correct'))
            else:
                train_incorrect.append((key, 'incorrect'))
            if data[key] == 'correct':
                correct_messages.append(key + '\n')
            else:
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

    openai.api_key = api_key_env
    openai.organization = org_id

    def ask_gpt():
        response = openai.ChatCompletion.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-4",
        )
        return response

    response = ask_gpt()
    content = response['choices'][0]['message']['content']

    # ic(response)
    # ic(content)
    # ic(expected)
    # ic(test)
    # ic(test_messages)
    # ic(correct_messages)
    # ic(incorrect_messages)
    # ic(prompt)

    current_time = int(round(time.time() * 1000))
    with open('outcomes/' + section + '_' + score_type + '_' + str(train_percentage) + "_gpt_" + str(round(current_time)), 'w') as file:
        file.write('GPT Answered: \n')
        file.write(str(content))
        file.write('\n\n')
        file.write('Expected: \n')
        file.write(str(expected))

        
file_names = os.listdir('data/raw')
file_names.sort()
file_names = file_names[:-3] # remove the last 3 files (all, answers, questions)
file_names.sort(key=lambda x: float(x.split('.')[0]) + float(x.split('.')[1])/10) # sort by section number
for section in file_names:
    # run_section(section, score_type) # call for ChatGPT
    # time.sleep(1)

# run_section('1.1', score_type) # run just one section