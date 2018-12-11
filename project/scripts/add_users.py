from blog.models import MyUser
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
