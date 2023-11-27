def getData(section, score_type):
    data = []
    with open('data/raw/' + section) as f:
        for line in f:
            # remove any '<br>' from the text
            line = line.replace('<br>', '')
            data.append(line[4:].strip())
    scores = []
    with open('data/scores/' + section + '/'+ score_type) as file:
        for line in file:
            scores.append(line.strip())

    final = dict(zip(data, scores))
    # change final scores to be correct or incorrect based on 5 for correct and everything else incorrect
    for key in final:
        if final[key] == '5':
            final[key] = 'correct'
        else:
            final[key] = 'incorrect'
    return final

def getQuestion(section):
    with open('data/sent/questions') as file:
        for line in file:
            if line.startswith(section):
                question = line.split(' ', 1)[1].strip()
                # remove ' <STOP>' at the end
                question = question[:-7]
                return question

