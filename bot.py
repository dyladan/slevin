import bot.irc.connection as connection
import bot.util.parse as parse
import re
import requests

chan = ""
nick = ""
server = ""

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

irc = connection.Connection(server=server,nick=nick)
irc.join(chan)
while True:
  out = parse.parsemsg(irc.listen())
  prefix  = out[0]
  command = out[1]
  args    = out[2]
  if command == 'PRIVMSG':
    if args[0] == irc.nick:
      channel = prefix.split('!')[0]
    else:
      channel = args[0]
    message = args[1].rstrip()
    ##irc.privmsg(channel,message)
    issue = github(message)
    if issue:
      irc.privmsg(channel,issue)

