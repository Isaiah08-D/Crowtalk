from manage import INIT

userDB = INIT.userDB
postsDB = INIT.postsDB
postsDBdict = INIT.postsDBdict
modActivity = INIT.modActivity

"""
DB FORMATING:

postsDB[<index>] = {'title': '<title>', 'author': <username>', 'content': '<content>', 'comments': [['example-user', 'nice!'], ['example-user2', 'i like it!']]}

postsDBdict['title'] = {'title': '<title>', 'author': <username>', 'content': '<content>', 'comments': [['example-user', 'nice!'], ['example-user2', 'i like it!']]}

userDB['<username>'] = {'password':'<password>', posts':[postsDb['<title>']], 'caws': <caws>, status:'<date till unban> OR normal', 'position':'user OR admin', 'comments': [['example-user', 'nice!'], ['example-user2', 'i like it!']]}

modActivity = ['example-mod banned example-user until 8/14/2021', 'example-mod became a mod',]

bans = ['example-banned-user', 'example-banned-user2']

clear:
db['postsDB'] = []
db['userDB'] = {}
db['postsDBdict']
db['modActivity'] = []
"""