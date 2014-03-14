@command
def cmd_pull(con, chan, nick, msg):
  os.system("cd bookie && pwd && git pull")
