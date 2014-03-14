import os
import re
#import string
@command
def cmd_func(connection, channel, nick, s):
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
  regex = s[0]
  regex = re.compile(r'\.\*').sub('*',regex)
  regex = re.compile(r'[^A-Za-z0-9_*^\\.+]+').sub('',regex)
  regex = re.compile(r'\*').sub('.*', regex)
  regex = re.compile(r'\^').sub(r'\\b', regex)
  print regex
  functions = find_func(regex)
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
