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
import bot.util
from bot.util import parsemsg
import sqlite3
import re
import datetime

class Connection:
  "Create a connection to an irc channel"
  _p = sys.stdout.write
  def __init__(self, server="irc.freenode.net", nick="bookiebot", name="Alan Turing", port=6667):
    self.nick = nick
    self.name = name
    self.s = socket.socket()
    self.connect(server, port, nick, name)
    self.logdb = "log.db"
    self.table_name = re.sub(r"[\W]+", "", server)
    conn = sqlite3.connect(self.logdb)
    sql = "create table if not exists " + self.table_name + " (utc timestamp, chan text, nick text, msg text)"
    print sql
    conn.execute(sql)
    conn.commit()

  def connect(self, server, port=6667, nick="bookiebot", name="Alan Turing"):
    "Connect and return a socket"
    self.s.connect((server,port))
    self.s.recv(4096)
    self.setnick(nick)
    self.setuser(name)

  def log(self, chan, nick, msg):
    sql = "insert into %s VALUES (?, ?, ?, ?)" % self.table_name
    conn = sqlite3.connect(self.logdb)
    conn.execute(sql, (datetime.datetime.now(), chan, nick, msg))
    conn.commit()


  def close(self, reason="GOOD BYE"):
    data = "QUIT :Bye\r\n"
    print ">", data.rstrip()
    self.s.send(bytearray(data, "utf-8"))
    self.s.recv(4096)
    self.s.close()

  def privmsg(self, chan,message):
    data = 'PRIVMSG %s :%s\r\n' % (chan, message)
    self.s.send(bytearray(data, "utf-8"))
    self.log(chan, self.nick, message)
    self._p("> %s" % bytearray(data, "utf-8"))

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
      raw = self.s.recv (4096) #Make Data the Receive Buffer
      data = bot.util.decode(raw)
      if data[:4] == "PING":
        pong = 'PONG %s' % data[6:]
        self.s.send(pong) #Send back a PONG
      else:
        out = parsemsg(data)
        return out
