from pox.lib.addresses import EthAddr
from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()
countDictionary = {}
flag = 0 
foo = []

class MyCtrl (object):
  """
  A Tutorial object is created for each switch that connects.
  A Connection object for that switch is passed to the __init__ function.
  """
  
  def __init__ (self, connection):
    # Keep track of the connection to the switch so that we can
    # send it messages!
    self.connection = connection
 
    # This binds our PacketIn event listener
    connection.addListeners(self)
 
    # This empty list stores our MAC addresses and the corresponding
    # port on the switch where the host is connected
    self.macStore = {}

  def _handle_PacketIn (self, event):
    global foo
    """
    Handles packet in messages from the switch.
    """
 
    packet = event.parsed # This is the parsed packet data.
    
    log.debug("here")
    #self.check_migration()
    log.debug(packet)
    log.debug(packet.__dict__)
    log.debug("there") 
    if(foo==[] or foo[0] == '\n'):
        foo = filter(None,open("/home/mininet/migrationVaribles","r").read().split(' '))
        
    log.debug("there2")
    log.debug(foo)
    log.debug("there1")
    

    srcaddr = EthAddr(packet.src)
    dstaddr = EthAddr(packet.dst)
    if countDictionary.has_key(srcaddr.toStr()):
        countDictionary[srcaddr] = countDictionary[srcaddr] + 1
    else:
        countDictionary[srcaddr] = 0
     
    if countDictionary.has_key(dstaddr.toStr()):
        countDictionary[dstaddr] = countDictionary[dstaddr] + 1
    else:
        countDictionary[dstaddr] = 0
    
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return
 
    packet_in = event.ofp # The actual ofp_packet_in message.
    

 
    if(foo!=[]):
        if(foo[0]!='\n'):
            log.debug("yaha aayaa ")
            if srcaddr.toStr() == foo[0]:
                log.debug("yaha 1")
                self.update(foo[1], packet, packet_in)
            elif dstaddr.toStr() == foo[0]:
                log.debug("yaha 2")

                self.update(foo[1], packet, packet_in)
            if dstaddr.toStr() == foo[0]:
                log.debug("yaha 3")

                self.update(foo[1], packet, packet_in)
            elif srcaddr.toStr() == foo[1]:
                log.debug("yaha 1")

                self.update(foo[0], packet, packet_in)

    # This line calls the function act_like_lswitch and passes
    # the parsed package and the openflow packet message to our
    # learning switch
    self.act_like_lswitch(packet, packet_in)

  def update(self, new_mac, packet, packet_in):
    srcaddr = EthAddr(packet.src)
    dstaddr = EthAddr(packet.dst)
    
    
    log.debug("---------------------------------")
    log.debug(srcaddr)
    log.debug(dstaddr)
    log.debug("MAC Address Store")
    log.debug(self.macStore)
    log.debug("Done")
    log.debug("---------------------------------")
    fm = of.ofp_flow_mod(command=of.OFPFC_MODIFY)
    fm.match = of.ofp_match.from_packet(packet)
    #fm.match.in_port = packet_in.in_port
    #fm.match.dl_dst = new_mac
    fm.actions.append(of.ofp_action_output(port = self.macStore[new_mac]))
    print "dicic"
    print dir(fm)
      #fm.idle_timeout = 10
      #fm.hard_timeout = 30
    log.debug("UPDATING FLOWTABLE ENTRY")
    self.connection.send(fm)
 
      # We wont loose this package, so we forward it
      # to its destination
    self.send_packet(packet_in.buffer_id, packet_in.data, self.macStore[new_mac], packet_in.in_port)
    self.send_packet(packet_in.buffer_id, packet_in.data, self.macStore[new_mac], packet_in.in_port)
    log.debug("-------------Package <"+str(packet_in.buffer_id)+"> forwarded by controller over Port "+str(self.macStore[new_mac]))

  def check_migration(self):
    foo = filter(None,open("/home/mininet/migrationVaribles").read().split(' '))
    log.debug("there2")
    log.debug(foo)
    log.debug("there1")

  def send_packet (self, buffer_id, raw_data, out_port, in_port):
    #Sends a packet out of the specified switch port.
    msg = of.ofp_packet_out()
    msg.in_port = in_port
    msg.data = raw_data
    # Add an action to send to the specified port
    action = of.ofp_action_output(port = out_port)
    msg.actions.append(action)
    # Send message to switch
    self.connection.send(msg)


  def act_like_hub (self, packet, packet_in):
    #flood packet on all ports
    self.send_packet(packet_in.buffer_id, packet_in.data,
                     of.OFPP_FLOOD, packet_in.in_port)

  def act_like_lswitch (self, packet, packet_in):
    """
    Implement switch-like behavior.
    """
 
    # Learn the port for the source MAC if necessary
    srcaddr = EthAddr(packet.src)
    if not self.macStore.has_key(srcaddr.toStr()):
      self.macStore[srcaddr.toStr()] = packet_in.in_port
      log.debug("New Host detected with MAC %s on Port %s" % (srcaddr.toStr(), packet_in.in_port))
 
    # Check if we have the destination in our store
    dstaddr = EthAddr(packet.dst)
    if self.macStore.has_key(dstaddr.toStr()):
      # Yes, it might bee a good idea to install a flowtable entry,
      # otherwise we have to ask the controller every time
      fm = of.ofp_flow_mod()
      fm.match.in_port = packet_in.in_port
      fm.match.dl_dst = dstaddr
      fm.actions.append(of.ofp_action_output(port = self.macStore[dstaddr.toStr()]))
      #fm.idle_timeout = 10
      #fm.hard_timeout = 30
      log.debug("Installing FlowTable entry")
      self.connection.send(fm)
 
      # We wont loose this package, so we forward it
      # to its destination
      self.send_packet(packet_in.buffer_id, packet_in.data, self.macStore[dstaddr.toStr()], packet_in.in_port)
      log.debug("Package <"+str(packet_in.buffer_id)+"> forwarded by controller over Port "+str(self.macStore[dstaddr.toStr()]))
 
    else:
      # Flood the packet out everything but the input port.
      # We are here, because we just put the source MAC and port
      # in our store and don't no the destination Port, 
      # thus the Flood is the only thing we can do.
      self.act_like_hub(packet, packet_in)
      log.debug("Package <"+str(packet_in.buffer_id)+"> flooded by controller")
  

def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    MyCtrl(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)
