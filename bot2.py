from bot.irc.connection import Connection
from bot.util.parse import parsemsg
from glob import glob
import re
import os

chanlist = ["#slevintest","#slevin"]
nick = "slevin"
server = "irc.freenode.net"
cmds = dict()

def command(func):
  cmds["." + func.__name__] = func

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
while True:
  raw = irc.listen()
  print raw
  out = parsemsg(raw)
  prefix  = out[0]
  command = out[1]
  args    = out[2]
  if command == 'PRIVMSG':
    if args[0] == irc.nick:
      channel = prefix.split('!')[0]
    else:
      channel = args[0]
    message = args[1].rstrip().split(" ")

    if message[0] in cmds:
      cmds[message[0]](irc, channel, message[1:])

    if message[0] == '.listfunc':
      irc.privmsg(channel, cmds)
      continue

    #match github issues
    for arg in message:
      match = re.match(r"#?(\d+)$", arg)
      if match:
        issue = github_issue(match.group(1))
        if issue:
          irc.privmsg(channel,issue)
