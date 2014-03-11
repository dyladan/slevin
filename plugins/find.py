import os
import re
@command
def func(connection, channel, s):
  def rgrep(path, regex):
      regObj = re.compile(regex)
      python = re.compile(r".*\.py$")
      res = []
      for root, dirs, fnames in os.walk(path):
          for fname in fnames:
              if python.match(fname):
                  match = search_file(os.path.join(root,fname), regObj)
                  if match:
                      res.append(match)
                      #res.append(os.path.join(root,fname))
      return res

  def search_file(path, regex):
      res = []
      with open(path) as f:
          lines = f.readlines()
      for num, line in enumerate(lines):
          if regex.match(line):
              res.append("%s:%d - %s" % (path, num, line.lstrip().rstrip()))
      if res == []:
          return None
      else:
          return res

  def find_func(s):
    try:
      return rgrep(".", "\s*def\s.*%s.*\(.*:" % s)
    except Exception:
      return []

  os.chdir("bookie/bookie")
  os.system("git pull")
  print s[0]
  functions = find_func(s[0])
  os.chdir("../../")
  out = [item for sublist in functions for item in sublist]
  if len(out) > 5:
    connection.privmsg(channel, "More than 5 matches.")
  elif len(out) == 0:
    connection.privmsg(channel, "No functions like that")
  else:
    for s in out:
      connection.privmsg(channel,s)

#function = "get_by_url"
#print rgrep('.', '\s*def\s.*%s.*:' % function)
