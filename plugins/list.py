@command
def cmd_list(con, chan, nick, args):
  s = []
  for i in cmds.iterkeys():
    s.append(i[4:])
  s.sort()
  out = " ".join(s)
  con.privmsg(chan, out)

@command
def cmd_relist(con, chan, nick, args):
  s = []
  for i in rehooks.iterkeys():
    s.append(i[4:])
  s.sort()
  out = " ".join(s)
  con.privmsg(chan, out)
