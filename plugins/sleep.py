@command
def cmd_sleep(con, chan, nick, msg):
  import time
  time.sleep(10)
  con.privmsg(chan, "slept ten seconds")
