import os
import re

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

#function = "get_by_url"
#print rgrep('.', '\s*def\s.*%s.*:' % function)
