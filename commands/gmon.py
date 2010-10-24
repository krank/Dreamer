name = "!gmon"
description = "Adds you or [nick] to the list of GM's"
available = ('private')
restricted = False


def index(parent, connection, event):
    source = event.source().split("!")[0]
    target = source
    
    if len(event.arguments()[0].split()) > 1:
        target = event.arguments()[0].split()[1]
    
    parent.gmon(source, target)