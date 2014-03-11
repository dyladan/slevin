from bot.irc.connection import Connection
from bot.util.parse import parsemsg
from glob import glob
import re
import os

chanlist = ["#slevintest","#slevin"]
nick = "slevin"
server = "irc.freenode.net"
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

    if message[0] == '.func':
      os.chdir("bookie/bookie")
      os.system("git pull")
      functions = find_func(message[1])
      os.chdir("../../")
      out = [item for sublist in functions for item in sublist]
      if len(out) > 5:
        irc.privmsg(channel, "More than 5 matches. Please refine your search")
      else:
        for s in out:
          irc.privmsg(channel,s)

    #match github issues
    for arg in message:
      match = re.match(r"#?(\d+)$", arg)
      if match:
        issue = github_issue(match.group(1))
        irc.privmsg(channel,issue)
      #irc.privmsg(channel,github_issue(message[1]))
