#!/usr/bin/python
# -*- coding: utf-8 -*- 

#Dreamer IRC bot v2

#privat:
#-!gm = regga sig som spelledare
#-!listgm = lista spelledare
#-!whisp [user] [message] = viska meddelande till användare
#-!name [name] = byt namn på botten
#-!roll/!dice [diceregexp] = rulla tärning (med flood protect)
#-!help = visa hjälpen
#-Allt annat; säg i kanalen

#publikt:
#-!listgm
#-!roll
#-!help

import ircbot
import glob
import imp
import datetime
import time
import random
import sys

import irclib

import Dice

class IrcProfile:
    def __init__(self, title, servers, channels):
        self.title = title
        self.servers = servers
        self.channels = channels


#Settings
name = "Dreamer"
nick = "Dreamer"
reloadpasswd = "DR3@meR"

decoline = ".-__-__-__-__-__-__-__-_:*:_-__-__-__-__-__-__-__-."

#Profiles

profile = {}
profile["solveserver"] = IrcProfile('Solvebrings kanal', [('irc.quakenet.org', 6667)], '#bakerstreet')
profile["reptiden"] = IrcProfile('Reptiden', [('naman.yafas.net', 6667)], '#bottest')

priv_commands = {}
pub_commands = {}

#===Scanner for commands========================================================
def scan(target):
    
    print "Scanning for modules..."
    
    priv_commands = {}
    pub_commands = {}
    for moduleSource in glob.glob ( 'commands/*.py' ):
        name = moduleSource.replace ( '.py', '' ).replace ( '\\', '/' ).split ( '/' ) [ 1 ].upper()
        handle = open ( moduleSource )
        module = imp.load_module ( 'COMMAND_'+name, handle, ( 'commands/' + moduleSource ), ( '.py', 'r', imp.PY_SOURCE ) )
        
        try:
            if "public" in module.available:
                pub_commands[name] = module
                print " Adding module " + module.name + " to [public] module list"
            if "private" in module.available:
                priv_commands[name] = module
                print " Adding module " + module.name + " to [private] module list"
        except:
            pass
            

    target.priv_commands = priv_commands
    target.pub_commands = pub_commands


#===The DreamerBot class========================================================

class DreamerBot(ircbot.SingleServerIRCBot):
    """Dreamer IRC bot v2
    An IRC bot for roleplaying
    """

    #---Main -------------------------------------------------------------------
    
    def __init__(self, profile):
        self.p_servers = profile.servers
        self.p_channels = profile.channels
        self.p_name = profile.title
        
        self.nickname = name
        self.decoline = decoline
        
        self.gmlist = [] #Note for later: Save list of GM's?
        
        print self.decoline
        print "Connecting to " + str(self.p_servers) + "..."        
        
        ircbot.SingleServerIRCBot.__init__(self, self.p_servers, nick, name)
        
        scan(self)
        
        


    #---Generic methods---------------------------------------------------------
    
    def describe(self, text):
        moment = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        
        print moment + ": " + text #Note for later: Logging?
        
        
    #---Handlers----------------------------------------------------------------
        
    def on_nicknameinuse(self, connection, event):
        print "Nickname in use!"
        self.nickname = name + str(random.randint(1,1024))
        print "Changing to " + self.nickname
        connection.nick(self.nickname)

    
    def on_welcome(self, connection, event):
        print self.decoline
        print "Entering channel " + self.p_channels + "..."
        
        connection.join(self.p_channels)
        self.connection.mode(nick,"+B")
        
        self.connection.action(self.p_channels, "testar")
        
        print self.decoline


    def on_privmsg(self, connection, event):
        cmd = event.arguments()[0].split()[0]
        source = event.source().split("!")[0]        
        
        if cmd[0] == "!":
            cmd = cmd[1:].upper()
            if self.priv_commands.has_key(cmd):
                if not self.priv_commands[cmd].restricted or source in self.gmlist:
                    self.priv_commands[cmd].index(self, connection, event)
                else:
                    self.say(source, "Only a GM may do that!", source)
                    
        else:
            if source in self.gmlist:
                line = event.arguments()[0]
                self.say(source, line.strip("!/"))
            

            

    def on_ctcp ( self, connection, event ):
        if event.arguments() [ 0 ] == reloadpasswd.upper():
            scan(self)
    
    def on_pubmsg(self, connection, event):
        cmd = event.arguments()[0].split()[0]
        if cmd[0] == "!":
            cmd = cmd[1:].upper()
            if self.pub_commands.has_key(cmd):
                
                source = event.source().split("!")[0]
                
                if not self.pub_commands[cmd].restricted or source in self.gmlist:
                    self.pub_commands[cmd].index(self, connection, event)
                else:
                    self.say(source, "Only a GM may do that!", source)

    #---Action methods----------------------------------------------------------
    
    def changename(self, source, name):
        #Check so the intended name does not already exist
        if self.channels[self.p_channels].has_user(name):
            self.say(source, "Nick already in use")
            self.describe("Tried changing name to " + name + " but that nick was already in use")
        else:
            # Change nick
            self.connection.nick(name)
            self.describe("Changing name to " + name)

    # Built-in Gamemaster methods

    def gmon(self, source, target):
        if target not in self.gmlist:
            self.gmlist.append(target)
            self.say(source, target + " has been added to the GM list. Use !gmlist to list current GM's", source)
            self.describe("Making " + target + " a GM")
        else:
            self.describe("An attempt was made to make " + target + " a GM - but " + target + " was already a GM")
            self.say(target + " is already a GM", source)

    def gmoff(self, source, target):
        if target in self.gmlist:
            self.gmlist.remove(target)
            self.say(source, target + " was removed from the GM list", source)
            self.describe("Removed " + target + " from the GM list")
        else:
            self.say(source, target + " is not a GM!", source)


    def listgms(self, source, target):
        t = []
        t.append(self.decoline)
        t.append("List of the current GMs:")

        if len(self.gmlist):
            for gm in self.gmlist:
                t.append(" - " + gm)
        else:
            t.append(" - [None]")
        
        for l in t:
            self.say(source, l, target)

    # Built-in Say method
    
    def say(self, source, message, target=False, action=False):
        
        # If target is not defined, use current channel
        if not target:
            target = self.p_channels
            self.describe("Saying in channel " + target + ": " + message)
            self.connection.privmsg(target, message)
            
        else:
            # If target user exist, send the message to it
            
            if self.channels[self.p_channels].has_user(target):
                if action:
                    self.connection.action(target, message)
                else:
                    self.connection.privmsg(target, message)
                self.describe("Whispering to " + target + ": " + message)
                
            # Otherwise, throw an error
            else:
                if self.channels[self.p_channels].has_user(source):
                    self.say(source, "Target " + target + " does not exist")
                self.describe("Tried whispering to " + target + " but there is no user by that name in the channel")

#if there's no valid profile as argument, show menu

p = False
if len(sys.argv) > 1:
    if profile.has_key(sys.argv[1]):
        p = profile[sys.argv[1]]


if not p:
    choice = -1
    keys = profile.keys()
    while choice not in range(0,len(profile)) + ["q"]:
        print decoline
        print "Choose your profile"
        print
        i = 0
        for pl in keys:
            print str(i) + " -::- " + profile[pl].title
            i+=1
        
        choice = raw_input("Select a number or 'q': ")
        
        if choice.isdigit():
            choice = int(choice)
        
    
    if choice != "q":
        p = profile[keys[choice]]
        
if p:
    dreamer = DreamerBot(p)
    dreamer.start()
