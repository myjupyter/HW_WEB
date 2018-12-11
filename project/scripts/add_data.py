from blog.models import *
import random


names = list(open('./data/names'))
emails = list(open('./data/emails'))
lastname = list(open('./data/lastname'))

user = 'user'
i = 0

for e in list(emails):
    MyUser.objects.create_a_user(username=user+str(i),
                                 first_name=random.choice(names).rstrip(),
                                 last_name=random.choice(lastname).rstrip(),
                                 email=e.rstrip(),
                                 password=random.choice(names).rstrip())
    i+=1

f = open('./data/qtitle')
title = ' '.join([line.strip() for line in f])
f.close()
f = open('./data/tags')
tags = [line.strip() for line in f]
f.close()
f = open('./data/qtext')
text = ' '.join([line.strip() for line in f])
f.close()

users = MyUser.objects.all()

for i in range(100):
    Question.objects.create_a_question(random.choice(users),
                                       title=title, text=text,
                                       tags = random.choices(tags,k=random.choice(range(len(tags)))))

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

questions = Question.objects.all()
users = MyUser.objects.all()
for q in questions:
    for u in random.choices(users,k=random.choice(range(500))):
        q.set_like(u, random.choice([True,True,True,False]))

