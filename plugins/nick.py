@command
def setnick(con, chan, args):
  con.setnick(args[0])
