@command
def cmd_help(con, chan, nick, args):
  if len(args) == 0:
    s = []
    for i in cmds.iterkeys():
      s.append(i[4:])
    s.sort()
    out = " ".join(s)
    con.privmsg(chan, out)
  else:
    cmd = "cmd_"+args[0]
    if cmd in cmds:
      doc = cmds[cmd].__doc__
      if doc:
        con.privmsg(chan, doc)
      else:
        con.privmsg(chan, "no docs for command")
    else:
      con.privmsg(chan, "no such command")


