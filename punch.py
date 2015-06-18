#!/usr/bin/env python
#
# UDP Hole Punching client
#
# This is the client.
#
# thank for Koen Bollen
#
 
import sys
import socket, time
from select import select
import struct
import os
import threading
from threading import Thread
 
def bytes2addr( bytes ):
    """Convert a hash to an address pair."""
    if len(bytes) != 6:
        raise (ValueError, "invalid bytes")
    host = socket.inet_ntoa( bytes[:4] )
    port, = struct.unpack( "H", bytes[-2:] )
    return host, port
def main():
    
    try:
        master = (sys.argv[1], int(sys.argv[2]))
        pool = sys.argv[3].strip()
    except (IndexError, ValueError):
        print (sys.stderr, "usage: %s <host> <port> <pool>" % sys.argv[0])
        sys.exit(65)
 
    sockfd = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
    sockfd.sendto( pool, master )
    print sockfd.getsockname()
    data, addr = sockfd.recvfrom( len(pool)+3 )
    if data != "ok "+pool:
        print (sys.stderr, "unable to request!")
        sys.exit(1)
    sockfd.sendto( "ok", master )
    print ("request sent, waiting for parkner in pool '%s'..." % pool)
    data, addr = sockfd.recvfrom( 6 )
 
    target = bytes2addr(data)
    print ("connecting to %s:%d" % target)
    #time.sleep(1)
    print "send ok"
    sockfd.sendto("ok", target )
    data, addr = sockfd.recvfrom( 1024 )
    print data, addr
    if data == "ok":
	print "connected to to %s:%d" % target
    while True:
	rfds,_,_ = select( [0, sockfd], [], [] )
        if 0 in rfds:
            data = sys.stdin.readline()
            if not data:
                break
            sockfd.sendto(data, target )
        elif sockfd in rfds:
            data, addr = sockfd.recvfrom( 1024 )
            sys.stdout.write( data )
    sockfd.close()
 
if __name__ == "__main__":
    main()
