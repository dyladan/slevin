from bot.util.find import find_func
from bot.util.github import github
import bot.irc.connection as connection
import bot.util.parse as parse
import re
import os

chanlist = ["#slevintest","#slevin"]
nick = "slevin"
server = "irc.freenode.net"

#os.chdir("/home/user/bookie/bookie")


os.chdir("bookie/bookie")

irc = connection.Connection(server=server,nick=nick)
for chan in chanlist:
  irc.join(chan)
while True:
  raw = irc.listen()
  print raw
  out = parse.parsemsg(raw)
  prefix  = out[0]
  command = out[1]
  args    = out[2]
  if command == 'PRIVMSG':
    if args[0] == irc.nick:
      channel = prefix.split('!')[0]
    else:
      channel = args[0]
    message = args[1].rstrip()
    if re.match(".func \w+", message):
      os.system("git pull")
      l = find_func(message[6:].rstrip())
      out = [item for sublist in l for item in sublist]
      if len(out) > 5:
        irc.privmsg(channel,"More than 5 results. Please refine your search.")
      else:
        for s in out[:5]:
          irc.privmsg(channel,s)
      continue

    issue = github(message)
    if issue:
      irc.privmsg(channel,issue)

