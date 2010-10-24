name = "!whisp nick message"
description = "Makes the bot whisper to nick."
available = ('private')
restricted = "gm"

def index(parent, connection, event):
    source = event.source().split("!")[0]
    
    if len(event.arguments()[0].split()) > 2:
        target = event.arguments()[0].split()[1]
        text = " ".join(event.arguments()[0].split(" ")[2:])
        parent.say(source, text, target)
    else:
        parent.say(source, "Message or target omitted", source)