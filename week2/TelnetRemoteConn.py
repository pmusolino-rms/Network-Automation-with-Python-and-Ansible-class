#!/usr/bin/env phython
from telnetlib import Telnet
import socket
import sys
import argparse
import time

class TelnetRemoteConn(object):

  def __init__(self,ip,port,timeout):
    self.ip_addr = ip
    self.port = port
    self.timeout = timeout
    self.telnet_session = None
    self.log = ""
    self.prompt = ""

  def open_session(self):
    try:
      self.telnet_session = Telnet(self.ip_addr,self.port,self.timeout)
      self.log += "Session to %s:%s opened" % (self.ip_addr,self.port)
    except socket.timeout:
      self.log += "Failed to open connection to %s" % self.ip_addr

  def login(self,username,password):
    prompts = [">","$","#"]
    if (self.telnet_session):
      self.log += self.telnet_session.read_until("sername",self.timeout)
      self.telnet_session.write(username + '\n')
      self.log += self.telnet_session.read_until("ssword",self.timeout)
      self.telnet_session.write(password + '\n')
      self.prompt = self.telnet_session.expect(prompts,self.timeout)[2]
      self.log += self.prompt
    else:
      self.log += "Unable to Login: No Connection"

  def logout(self):
    self.telnet_session.write("exit" + '\n')
    self.telnet_session.close()

  def send_command(self,command):
    if (self.telnet_session):
      self.telnet_session.write(command + '\n')
      time.sleep(1)
      output = self.telnet_session.read_very_eager()
      self.log += output
      output_list = output.split('\n')
      output_list = output_list[1:-1]
      output = '\n'.join(output_list)
      return output 
    else:
      self.log += "Unable to send command:  No connection"

