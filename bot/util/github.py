import re
import requests

def github_issue( issue, user="bookieio", repo="bookie" ):
  r = requests.get("https://api.github.com/repos/%s/%s/issues/%s" % (user,repo,issue))
  if r.status_code == 200:
    json = r.json()
    url = json['html_url']
    title = json['title']
    state = json['state']
    return state + " - " + url + " - " + title
  else:
    return None

def github(s):
  match = re.search(r"(?:^|\s)#?(\d+)\b",s)
  if match:
      number = match.group(1)
      return github_issue(number)
  else:
      return None
