#!/usr/bin/python

import os
import re

db = 'db.sqlite3'
file_list = os.listdir('./')
if db in file_list:
    os.remove('./' + db)

path = './blog/migrations/'
file_list = os.listdir(path)
for f in file_list:
    if(re.match(r'\d\d\d\d_auto_*', f)):
        os.remove(path + f)

if((os.system('python3 ./manage.py makemigrations'))):
    raise RuntimeError('Error makemigrations')

if((os.system('python3 ./manage.py migrate'))):
    raise RuntimeError('Error migrate')
