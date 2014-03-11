@command
def restart(con, chan, args):
  con.close()
  python = sys.executable
  os.execl(python, python, * sys.argv)
