#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
import time
import sys

h1 = None
h2 = None
h3 = None
h4 = None
s1 = None
s2 = None
s3 = None
linkList = []
hostList = []
switchList = []
Port=6634
noOfHosts = 0
noOfLinks = 0
noOfSwitches = 0
globalX=None
globalY=None




def emptyNet():

    "Create an empty network and add nodes to it."
    global h1,h2,h3,h4,s1,s2,s3,linkList,hostList,switchList,Port,noOfHosts,noOfLinks,noOfSwitches
    net = Mininet( topo=None,
                   build=False)

    net.addController( 'c0',
                       controller=RemoteController,
                       ip='127.0.0.1'  )
    for i in range(20):
        
        print "=",
    print
    print 
    print "Spawning the Hosts"  
    hostFile = open(sys.argv[1],"r").read().split('\n')
    noOfHosts = int(hostFile[0])
    hostFile.pop(0)
    print hostFile
    hostFile = filter(None,hostFile)
    for i in hostFile:
        i=i.split(' ')
       
        print i
        hostList.append(net.addHost(i[0]))        
    print
    print
    for i in range(20):
        
        print "=",
    print
    print 
    print "Spawning the Switches"  
    


    switchFile = open(sys.argv[2],"r").read().split('\n')
    noOfSwitches = int(switchFile[0])
    switchFile.pop(0)
    switchFile = filter(None,switchFile)
    print switchFile
    for i in switchFile:
        i=i.split(' ')
        
        print i
        switchList.append(net.addSwitch(i[0],cls=OVSSwitch) )
        switchList[-1].listenPort = Port
        Port+=1      
    print
    print
    for i in range(20):
        
        print "=",
    print
    print 
    print "Making Links"  
   



    linkFile = open(sys.argv[3],"r").read().split('\n')
    noOfLinks = int(linkFile[0])
    linkFile.pop(0)
    linkFile = filter(None,linkFile)
    print linkFile
    for i in linkFile:
        i = i.split(' ')
        print i
        x = net.get(i[0])
        y = net.get(i[1])
        linkList.append(net.addLink( x, y ))
        

    #h1 = net.addHost( 'h1')
    #print "here"
    #print h1.__dict__
    #print h1.intfIsUp()
    #print sys.argv[1]
    #file=open("config","r")
    #x=file.read().split('\n')
    #print x
    #print "there"
    #h2 = net.addHost( 'h2')
    #h3 = net.addHost( 'h3')
    #h4 = net.addHost( 'h4')

    #s1 = net.addSwitch( 's1', cls=OVSSwitch )
    #s1.listenPort = 6634
    
    #s2 = net.addSwitch( 's2', cls=OVSSwitch )
    #s2.listenPort = 6635
    
    #s3 = net.addSwitch( 's3', cls=OVSSwitch )
    #s3.listenPort = 6636
    
    #linkList.append(net.addLink( h1, s1 ))
    #linkList.append(net.addLink( h2, s1 ))
    #linkList.append(net.addLink( h3, s2 ))
    #linkList.append(net.addLink( h4, s2 ))
    #net.addLink( s1, s3 )
    #net.addLink( s2, s3 )
    print
    print
    print "Spawning Network"
    print
    for i in range(20):
        
        print "=",
   
    net.start()
    print 
    print
    print "Installing MAC Address"
    for i in hostFile:
        print i
        i = i.split(' ')
        x = net.get(i[0])
        x.setMAC(i[1])
    for i in switchFile:
        print i
        i = i.split(' ')
        x = net.get(i[0])
        x.setMAC(i[1])
    print
    print
    #print h1.intfIsUp()
    #h1.setMAC("00:00:00:00:00:01")
    #h2.setMAC("00:00:00:00:00:02")
    #h3.setMAC("00:00:00:00:00:03")
    #h4.setMAC("00:00:00:00:00:04")
    #s1.setMAC("00:00:00:00:00:11")
    #s2.setMAC("00:00:00:00:00:12")
    #s3.setMAC("00:00:00:00:00:13")







    #print h1.MAC()
    #print "checking there"
    return net




    
   #net.stop()

def simulatePing(net,x,y):
    global globalX,globalY
    
    print "Got Ping Command"
    #foo = open("migrationVaribles","w")
    print "globalvar"
    print globalX
    print globalY 
    print "done"
    print net,x,y
   
    x = net.get(x)
    y = net.get(y)
    if(x==globalX):
        net.ping([y,globalY])
    elif(y==globalX):
        net.ping([x,globalY])
    else:
        net.ping([x,y])
    print "Ping Done"
    print
    print

def migrate(net,x,y):
    global globalX,globalY
    print "Migration Flag Raised"
    num = map(lambda x:int(x),filter(None,x.split('h')))
    foo = open("migrationVaribles","w")
    #foo.write(x+" "+y+"\n")
    print num
    x = net.get(x)
    y = net.get(y)
    globalX = x
    globalY = y
    foo.write(x.MAC()+" "+y.MAC())
    print "List Before Migration"
    print linkList
    linkList[num[0]-1].delete()
    linkList.pop(num[0]-1) 
    print "List After Migration"
    print linkList
    print 
    print



def tester(net):
    print
    print "Test and Learning Phase"
    for i in range(20):
        
        print "=",
    print 
    #net.pingall() 
    net.ping([hostList[0],hostList[2]])
    switchList[0].cmd('ifconfig s1 inet 10.0.0.10')
    traffic = filter(None,open("generator","r").read().split('\n'))  
    #print traffic
    print
    print "Simulating Traffic"
    print "Enter the Simulation Phase"
    x = raw_input()
    if(x=='x'):
        for i in range(20):
        
            print "=",
        print 
    
        for i in traffic:
        
            i=i.split(' ')
            print i
            if(i[0]=='ping'):
                simulatePing(net,i[1],i[2])
            elif(i[0]=='migrate'):
                migrate(net,i[1],i[2]) 
    
        print "Simulation Done"
        print
     
    #print "here it is"
    #print hostList[0].intfIsUp()
    #print hostList[0].IP()
    #print linkList
    #print "there it is"
        CLI( net )
    #print "yaha bhi aaya"
    #x.do_link([h1,s1])
 






if __name__ == '__main__':
    setLogLevel( 'info' )
    net = emptyNet()
    #time.sleep(10)
    print "Entering Traffic Simulation Phase"
    print
    for i in range(20):
        
        print "=",
    print
    print "Enter x to start Testing "
    x = raw_input() 
    if(x=='x'):
        tester(net) 
