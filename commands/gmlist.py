name = "!gmlist"
description = "Displays a list of current GM's"
available = ('private', 'public')
restricted = False

def index(parent, connection, event):
    source = event.source().split("!")[0]
    
    if event.target()[0] == "#":
        parent.listgms(source,False)
    else:
        parent.listgms(source, source)