#!/usr/bin/env python
#
# UDP Hole Punching Server
# Two client connect to a server and connect to each other.
#
#
 
import socket
import struct
import sys
 
def addr2bytes( addr ):
    """Convert an address pair to a hash."""
    host, port = addr
    try:
        host = socket.gethostbyname( host )
    except (socket.gaierror, socket.error):
        raise (ValueError, "invalid host")
    try:
        port = int(port)
    except ValueError:
        raise (ValueError, "invalid port")
    bytes  = socket.inet_aton( host )
    bytes += struct.pack( "H", port )
    return bytes
 
def main():
    port = 8888
    try:
        port = int(sys.argv[1])
    except (IndexError, ValueError):
        pass
 
    sockfd = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
    sockfd.bind( ("", port) )
    print "listening on *:%d (udp)" % port
 
    poolqueue = {}
    while True:
	print "listening"
        data, addr = sockfd.recvfrom(32)
        print "connection from %s:%d" % addr
 
        pool = data.strip()
        sockfd.sendto( "ok "+pool, addr )
	print "send ok packet"
        data, addr = sockfd.recvfrom(2)
        if data != "ok":
            continue
 
        print "request received for pool:", pool
 
        try:
            a, b = poolqueue[pool], addr
	    print "have 2 client"
            sockfd.sendto( addr2bytes(a), b )
            sockfd.sendto( addr2bytes(b), a )
            print "linked", pool
            del poolqueue[pool]
	    print "sending info"
        except KeyError:
            poolqueue[pool] = addr
	    a, b = poolqueue[pool], addr
	    print a
	    print b
	    print "add client 1", addr
 
if __name__ == "__main__":
    main()
