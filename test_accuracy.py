import os


# loop through the files in outcomes
correct_guesses = 0
incorrect_guesses = 0
marked_incorrect_but_correct = 0
marked_correct_but_incorrect = 0
number_of_incorrect_responses = 0
files = os.listdir('outcomes')
for file in files:
    answers = []
    expected = ''
    with open('outcomes/' + file) as f:
        adding_answers = True
        for line in f:
            if line.startswith('GPT Answered:') or line == '\n':
                continue
            elif line.startswith('Expected:'):
                adding_answers = False
            elif adding_answers:
                answers.append(line.strip())
            elif not adding_answers:
                expected = line.strip()
    format_expected = expected.replace('[', '')
    format_expected = format_expected.replace(']', '')
    format_expected = format_expected.replace('\'', '')
    format_expected = format_expected.split(', ')
    if len(answers) == len(format_expected):
        for a, e in zip(answers, format_expected):
            if 'incorrect' in a.lower() and 'incorrect' in e.lower() or ('correct' in a.lower() and 'correct' in e.lower() and 'incorrect' not in a.lower() and 'incorrect' not in e.lower()):
                correct_guesses += 1
            else:
                incorrect_guesses += 1
                if 'correct' in a.lower() and 'incorrect' in e.lower():
                    marked_correct_but_incorrect += 1
                elif 'incorrect' in a.lower() and 'correct' in e.lower():
                    marked_incorrect_but_correct += 1
    else:
        number_of_incorrect_responses += 1

print('Correct Guesses: ', correct_guesses)
print('Incorrect Guesses: ', incorrect_guesses)
print('Incorrect but Correct: ', marked_incorrect_but_correct)
print('Correct but Incorrect: ', marked_correct_but_incorrect)
# percent of correct guesses and incorrect guesses
print('Percent Correct: ', correct_guesses/(correct_guesses + incorrect_guesses))
print('Percent Incorrect: ', incorrect_guesses/(correct_guesses + incorrect_guesses))
# percent of incorrect guesses that were incorrect but correct
print('Percent Marked Incorrect but Correct: ', marked_incorrect_but_correct/incorrect_guesses)
# percent of incorrect guesses that were correct but incorrect
print('Percent Marked Correct but Incorrect: ', marked_correct_but_incorrect/incorrect_guesses)
print('Number of Incorrect Responses: ', number_of_incorrect_responses)
print('Number of Files: ', len(files))