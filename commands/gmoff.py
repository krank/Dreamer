name = "!gmoff [nick]"
description = "Removes you or [nick] from the list of GM's"
available = ('private')
restricted = False


def index(parent, connection, event):
    source = event.source().split("!")[0]
    target = source
    
    if len(event.arguments()[0].split()) > 1:
        target = event.arguments()[0].split()[1]
    
    parent.gmoff(source, target)