@secure
def restart(con, chan, nick, args):
  con.close()
  python = sys.executable
  os.execl(python, python, * sys.argv)
