@command
def pull(con, chan, nick, msg):
  os.system("cd bookie && pwd && git pull")
