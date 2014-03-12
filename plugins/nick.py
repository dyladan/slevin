@command
def setnick(con, chan, nick, args):
  con.setnick(args[0])
