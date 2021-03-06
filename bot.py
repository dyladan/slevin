from bot.irc.connection import Connection
from glob import glob
import os
import sys
import thread

chanlist = ["#ubuntu-us-mi", "#bookie", "#slevin"]
nick = "bookiebot"
server = "irc.freenode.net"
cmds = dict()
securecmds = dict()
rehooks = dict()

def command(func):
  cmds[func.__name__] = func
def secure(func):
  securecmds[func.__name__] = func
def regex(func):
  rehooks[func.__name__] = func

modules = set(glob(os.path.join('plugins', '*.py')))

for mod in modules:
  with open(mod) as f:
    f = open(mod)
    code = f.read()
    f.close()
    obj = compile(code,mod, 'exec')
    exec(obj)

irc = Connection(server=server,nick=nick)

for chan in chanlist:
  irc.join(chan)


def privmsg(nick, channel, command, message):
    cmd = "cmd_"+re.compile(r"^\.").sub('', message[0])

    if cmd in cmds:
      cmds[cmd](irc, channel, nick, message[1:])
      return

    for hook in rehooks:
      if rehooks[hook](irc, channel, nick, message):
        return



while True:
  out = irc.listen()
  prefix  = out[0]
  command = out[1]
  args    = out[2]
  print("prefix: %s\r\ncommand: %s\r\nargs: %s" % (prefix, command, args))
  if command == 'PRIVMSG':
    nick = prefix.split('!')[0]
    if args[0] == irc.nick:
      channel = nick
    else:
      channel = args[0]

    message = args[1].rstrip().split(" ")

    irc.log(channel, nick, " ".join(message))

    thread.start_new_thread(privmsg, (nick, channel, command, message))

  elif command == 'KICK':
    if args[1] == irc.nick:
      irc.join(args[0])
      irc.privmsg(args[0], "HEY")
