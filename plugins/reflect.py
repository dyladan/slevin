@command
def reflect(connection, channel, s):
  connection.privmsg(channel, " ".join(s))
