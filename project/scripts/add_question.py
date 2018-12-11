from blog.models import *
import random

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
                                       random.choices(tags,k=random.choice(range(len(tags)))))



