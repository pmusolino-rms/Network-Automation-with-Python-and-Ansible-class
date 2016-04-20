#!/usr/bin/env python
from TelnetRemoteConn import TelnetRemoteConn

def main():
  ip_addr = "50.76.53.27"
  TELNET_PORT = 23
  TELNET_TIMEOUT = 6

  remote_conn = TelnetRemoteConn(ip_addr,TELNET_PORT,TELNET_TIMEOUT)
  remote_conn.open_session()
  remote_conn.login("pyclass","88newclass")
  output = remote_conn.send_command("show ip int bri")
  remote_conn.logout()
  print output
if __name__ == "__main__":
  main()


