name = "!help"
description = "Shows the help text"
available = ('private', 'public')
restricted = False

def index(parent, connection, event):
    source = event.source().split("!")[0]
    target = source
    
    t = []
    t.append(parent.decoline)
    t.append("  Command help for Dreamer:")
    
    for module in parent.priv_commands:
        ava = parent.priv_commands[module].available
        if isinstance(ava, tuple):
            ava = "/".join(ava)
        
        r = "[all]"
        if parent.priv_commands[module].restricted:
            r = " [" + parent.priv_commands[module].restricted + "]"
            
        t.append(parent.priv_commands[module].name + " -::- " + \
                 parent.priv_commands[module].description + \
                 "[" + ava + "]" + r)
        


    for l in t:
        parent.say(target, l, target)