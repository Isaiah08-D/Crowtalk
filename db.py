from manage import INIT

userDB = INIT.userDB
postsDB = INIT.postsDB
modActivity = INIT.modActivity

"""
DB FORMATING:

postsDB[<index>] = {'title': '<title>', 'author': <username>', 'content': '<content>', 'comments': [['example-user', 'nice!'], ['example-user2', 'i like it!']]}

postsDBdict['title'] = {'title': '<title>', 'author': <username>', 'content': '<content>', 'comments': [['example-user', 'nice!'], ['example-user2', 'i like it!']]}

userDB['<username>'] = {'password':'<password>', posts':[postsDb['<title>']], 'caws': <caws>, status:'<date till unban> OR normal', 'position':'user OR admin', 'comments': [['example-user', 'nice!'], ['example-user2', 'i like it!']]}

modActivity = ['example-mod banned example-user until 8/14/2021', 'example-mod became a mod',]

"""

