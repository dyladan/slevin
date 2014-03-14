import requests
import re

@regex
def gh_issues(con, chan, nick, msg):
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
  for arg in msg:
    match = re.match(r"#(\d+)$", arg)
    #match = re.match("(\d+)", arg)
    if match:
      print match.group(1)
      issue = github_issue(match.group(1))
      if issue:
        irc.privmsg(channel,issue)
      return True
  return False
