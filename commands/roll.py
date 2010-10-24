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
    
    d = text_Dicey()
    
    text = event.arguments()[0]
    text = d.replaceDieStrings(text)

    parent.describe("Roll was made by " + source + ": " + text)

    parent.say(source, text, target)
    

    
    

    
    
    
class text_Dicey(Dice.Dicey):
    def replaceDieRoll(self, m):
        """Replaces die rolls with text and the result of the roll."""
        die = Dice.Die(int(m.group('die')), m.group('rolls'), m.group('op'), m.group('val'), m.group('rolltype'), m.group('seltype'), m.group('nrofresults'))
        die.roll()
        
        text = str(die.dieroll) + ": " + str(die.result)
        text += " " + str(die.list)
        
        return text


if __name__ == '__main__':
    string = "asdf 4d6h3 qwer d20+100 asdfasf d12-100 asdf OpenD20 D8 d3 Ob3T6 d4 t10 d100 d12"
    print "Original string: " + string
    d = text_Dicey()
    newstring = d.replaceDieStrings(string)
    print "Result string: " + newstring