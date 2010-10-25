name = "!name"
description = "Renames the bot"
available = ('private')
restricted = "gm"

def index(parent, connection, event):
    source = event.source().split("!")[0]
    nick = parent.nickname
    
    if len(event.arguments()[0].split()) > 1:
        nick = event.arguments()[0].split()[1]
    
    parent.changename(source, nick)