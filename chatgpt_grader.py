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


by_percent = True
one_by_one = False
train_percentage = 0.2

directory = 'outcomes/'

# test each one by one and only trains on 3 correct and 3 incorrect answers
def run_section(section, score_type):

    data = getData(section, score_type)
    # separate the data randomly into train and test sets, 80% train and 20% test
    train_correct = []
    train_incorrect = []
    correct_messages = ["Some example correct solutions are: \n"]
    incorrect_messages = ["\nSome example incorrect solutions are: \n"]
    test = []
    expected = []
    test_messages = ["\nSuppose a student submitted: \n"]

    if not by_percent:
        # check if there are more than 3 correct and incorrect answers if there are randomly grab 3 of each to be added to the messages
        for key in data:
            if data[key] == 'correct':
                train_correct.append((key, 'correct'))
            else:
                train_incorrect.append((key, 'incorrect'))

        if len(train_correct) > 3 and len(train_incorrect) > 3:
            train_correct = random.sample(train_correct, 3)
            train_incorrect = random.sample(train_incorrect, 3)
        else:
            return # not an interesting enough dataset
        
        # add the correct and incorrect messages to the messages
        for correct in train_correct:
            correct_messages.append(correct[0] + '\n')
        for incorrect in train_incorrect:
            incorrect_messages.append(incorrect[0] + '\n')

        # add the test messages
        for key in data:
            # check if the key is in the correct or incorrect lists
            if (key, 'correct') in train_correct or (key, 'incorrect') in train_incorrect:
                continue
            test.append((key, data[key]))
            test_messages.append(key + '\n')
            expected.append(data[key])

    elif by_percent:
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
            
    # test_messages.append('\nHow would you grade this? Please simply respond with the word "correct" or "incorrect" for each.')
    question = getQuestion(section)

    c_m = "".join(correct_messages) if len(correct_messages) > 1 else ""
    i_m = "".join(incorrect_messages) if len(incorrect_messages) > 1 else ""

    prompt = f"The students have been assigned to answer the question: {question}\n" + c_m + i_m # + "".join(test_messages)

    load_dotenv()

    api_key_env = os.getenv("API_KEY")
    org_id = os.getenv("ORG_ID")

    client = OpenAI(
        api_key=api_key_env,
        organization=org_id,
    )

    contents = []
    if one_by_one:
        for test_message in test_messages[1:]:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an instructor for a Data Structures course grading assignments. You only respond to the to the students answers with the word 'correct' or 'incorrect'.",
                    },
                    {
                        "role": "user",
                        "content": (prompt + test_messages[0] + test_message + '\nHow would you grade this? Please simply respond with only the word "correct" or "incorrect".'),
                    }
                ]
            )

            content = response.choices[0].message.content
            
            print(test_messages.index(test_message), '/', len(test_messages) - 1) # progress to know it's still running

            # if content does not end with a \n, add one
            if content[-1] != '\n':
                content += '\n'

            contents.append(content)
    else:
        response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an instructor for a Data Structures course grading assignments. You only respond to the to the students answers with the word 'correct' or 'incorrect'.",
                    },
                    {
                        "role": "user",
                        "content": (prompt + test_messages + '\nHow would you grade these? Please simply respond with only the word "correct" or "incorrect".'),
                    }
                ]
            )
        
        content = response.choices[0].message.content
        
        print(test_messages.index(test_message), '/', len(test_messages) - 1) # progress to know it's still running

        # if content does not end with a \n, add one
        if content[-1] != '\n':
            content += '\n'

        contents.append(content)

    current_time = int(round(time.time() * 1000))
    with open(directory + section + '_' + score_type + '_3_random_gpt_' + str(round(current_time)), 'w') as file:
        file.write('GPT Answered: \n')
        file.write(str(contents))
        file.write('\n\n')
        file.write('Expected: \n')
        file.write(str(expected))

        
section_names = getSections()

# for section in section_names:
#     run_section(section, score_type) # call for ChatGPT

# run_section('1.1', score_type) # run just one section