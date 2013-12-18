"""Custom topology example

Two directly connected switches plus a host for each switch:

   host --- switch --- switch --- host

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.
"""

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import OVSSwitch, Controller, RemoteController


c0 = RemoteController( 'c0', ip='0.0.0.0',port=6633 )




from time import sleep
class MyTopo( Topo ):
    "Simple topology example."

    def __init__( self ):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

        # Add hosts and switches
        leftFirstHost = self.addHost( 'h1' )
        leftSecondHost = self.addHost( 'h2' )
        rightFirstHost = self.addHost( 'h3' )
        rightSecondHost = self.addHost( 'h4' )
        leftLOneSwitch = self.addSwitch( 's1' )
        rightLOneSwitch = self.addSwitch( 's2' )
        topSwitch = self.addSwitch( 's3' )
        

        # Add links
        self.addLink( leftFirstHost, leftLOneSwitch )
        self.addLink( leftSecondHost, leftLOneSwitch )
        self.addLink( rightFirstHost, rightLOneSwitch )
        self.addLink( rightSecondHost, rightLOneSwitch )



        self.addLink( leftLOneSwitch, topSwitch )
        self.addLink( rightLOneSwitch, topSwitch )



#x = Mytopo()
topos = { 'mytopo': ( lambda: MyTopo() ) }



net = Mininet(topo = MyTopo(),build=False)
net.build()
#net.addController(c0)
net.start()



#sleep(10)


#CLI(net)
    #print "Dumping host connections"
    #dumpNodeConnections(net.hosts)
    #print "Testing network connectivity"
#net.pingAll()

h1 = net.get('h1')
print h1
h4 = net.get('h4')
print h4

net.ping([h1,h4])



    #net.iperf((h1, h4))
    #h1 = net.get('h1')  
result = h1.cmd('ifconfig')
print result



print net.hosts



#net.ping(hosts=h1,h4)
    #net.stop()

