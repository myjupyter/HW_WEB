from blog.models import *
import random

questions = Questions.objects.all()
users = MyUser.objects.all()
for q in questions:
    for u in random.choices(users,k=random.choice(range(500))):
        q.set_like(u, random.choice([True,True,True,False]))
