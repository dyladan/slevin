@command
def list(con, chan, nick, args):
  s = []
  for i in cmds.iterkeys():
    s.append(i)
  s.sort()
  out = " ".join(s)
  con.privmsg(chan, out)

@command
def relist(con, chan, nick, args):
  s = []
  for i in rehooks.iterkeys():
    s.append(i)
  s.sort()
  out = " ".join(s)
  con.privmsg(chan, out)
