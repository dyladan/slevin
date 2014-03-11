"""Manage connections with irc server

Simple usage:
>> import bot.irc.connection as connection
>> irc = connection.Connection(server="irc.freenode.net", nick="bookiebot")
>> irc.join(#channel)
>> irc.listen()

functions:
__init__
"""
import socket
import sys

class Connection:
  "Create a connection to an irc channel"
  _p = sys.stdout.write
  def __init__(self, server="irc.freenode.net", nick="bookiebot", name="Alan Turing", port=6667):
    self.nick = nick
    self.name = name
    self.s = socket.socket()
    self.connect(server, port, nick, name)

  def connect(self, server, port=6667, nick="bookiebot", name="Alan Turing"):
    "Connect and return a socket"
    self.s.connect((server,port))
    self.s.recv(4096)
    self.setnick(nick)
    self.setuser(name)

  def close(self, reason="GOOD BYE"):
    data = "QUIT :Bye\r\n"
    print ">", data.rstrip()
    self.s.send(bytearray(data, "utf-8"))
    self.s.close()

  def privmsg(self, chan,message):
    data = 'PRIVMSG %s :%s\r\n' % (chan, message)
    self.s.send(data)
    self._p("> %s" % data)

  def setnick(self, nick):
    data = 'NICK %s\r\n' % nick
    self.s.send(data)
    self._p("> %s" % data)
    self.nick = nick

  def setuser(self, name):
    data = 'USER %s 0 * :%s\r\n' % (self.nick, name)
    self.s.send(data)
    self._p("> %s" % data)
    self.name = name

  def join(self, chan):
    data = 'JOIN %s\r\n' % chan
    self.s.send(data)
    self._p("> %s" % data)

  def listen(self):
    while True: #While Connection is Active
      data = self.s.recv (4096) #Make Data the Receive Buffer
      if data[:4] == "PING":
        pong = 'PONG %s' % data[6:]
        self.s.send(pong) #Send back a PONG
      else:
        return data
