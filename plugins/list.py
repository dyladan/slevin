@command
def list(con, chan, args):
  s = []
  for i in cmds.iterkeys():
    s.append(i)
  s.sort()
  out = " ".join(s)
  con.privmsg(chan, out)