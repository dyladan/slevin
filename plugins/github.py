import requests
import re

@regex
def bookie_issues(con, chan, nick, msg):
  def github_issue( issue, user="bookieio", repo="bookie" ):
    r = requests.get("https://api.github.com/repos/%s/%s/issues/%s" % (user,repo,issue))
    if r.status_code == 200:
      json = r.json()
      return json
    else:
      return None
  for arg in msg:
    match = re.match(r"#(\d+)$", arg)
    if match:
      issue = github_issue(match.group(1))
      out = " - ".join([issue['state'], issue['title'], issue['html_url']])
      if issue:
        irc.privmsg(channel,out)
      return True
    match_gh = re.match(r".*bookie/(?:issues|pull)/(\d+)", arg, flags=re.IGNORECASE)
    if match_gh:
      issue = github_issue(match_gh.group(1))
      out = " - ".join([issue['state'], issue['title']])
      if issue:
        irc.privmsg(channel, out)
      return True

  return False
