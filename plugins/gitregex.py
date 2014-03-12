@regex
def gh_issues(con, chan, nick, msg):
  for arg in msg:
    match = re.match(r"#?(\d+)$", arg)
    #match = re.match("(\d+)", arg)
    if match:
      print match.group(1)
      issue = github_issue(match.group(1))
      if issue:
        irc.privmsg(channel,issue)
      return True
  return False
