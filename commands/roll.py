name = "!roll"
description = "Roll a die"
available = ('private', 'public')
restricted = False

import Dice

def index(parent, connection, event):
    source = event.source().split("!")[0]
    target = source
    if event.target()[0] == "#":
        target = False
    
    d = Dice.Dicey()
    
    text = event.arguments()[0]
    text = d.replaceDieStrings(text)

    parent.describe("Roll was made by " + source + ": " + text)

    parent.say(source, text, target)


if __name__ == '__main__':
    string = "6d10>4 asdf 4d6h3 qwer d20+100 asdfasf d12-100 asdf OpenD20 D8 d3 Ob3T6 d4 t10 d100 d12"
    print "Original string: " + string
    d = Dice.Dicey()
    newstring = d.replaceDieStrings(string)
    print "Result string: " + newstring