import random
from blog.models import *

answers = list()
for i in range(1,5):
    f = open('./data/answer' + str(i))
    answers.append(' '.join([line.strip() for line in f]))
    f.close()

users = MyUser.objects.all()
questions = Question.objects.all()

for i in range(100):
    j = random.choice(range(10))
    for k in range(j):
        user = random.choice(users)
        question = random.choice(questions)
        if user.username == question.author.username:
            continue
        Answer.objects.create_answer(user, question, random.choice(answers))

