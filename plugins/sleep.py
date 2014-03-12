@command
def sleep(con, chan, msg):
  import time
  time.sleep(10)
  con.privmsg(chan, "slept ten seconds")
