@command
def cmd_echo(connection, channel, nick, s):
  connection.privmsg(channel, " ".join(s))
