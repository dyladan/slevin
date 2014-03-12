@secure
def join(con, chan, nick, msg):
  if msg[0] != "daniel06":
    con.privmsg(chan, "not authorized")
  else:
    con.join(msg[1])
