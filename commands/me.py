name = "!me message"
description = "Alias for /me, makes the bot convey the message in first person. Example: !me is hungry"
available = ('private')
restricted = "gm"


def index(parent, connection, event):
    source = event.source().split("!")[0]
    
    if len(event.arguments()[0].split()) > 1:
        message = "/me " + event.arguments()[0]
        parent.say(source, message)