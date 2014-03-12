@command
def reflect(connection, channel, nick, s):
  connection.privmsg(channel, " ".join(s))
