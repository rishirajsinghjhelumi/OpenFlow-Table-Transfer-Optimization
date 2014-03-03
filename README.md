Optimize flow table transfer during the VM migration
====================================================

A Small Introduction of the project:
-----------------------------------
* Software Defined Networks is relatively new domain which decouples the data and control flow in network
* VM Migration is an important metric for evaluation network virtualization and cloud computing domain.
* We propose an algorithm which will figure out the order and priority of the rules to migrate from the flow tables of routers when migrating the Virtual Machines in a network using OpenFlow protocol.

Detailed Introduction(Abstract submitted for Unisys Cloud 20/20):
----------------------------------------------------------------
[Abstract Link] [1]






Mentors:    
--------
Dr. Vasudeva Varma(vv@iiit.ac.in)

Reddy Raja

Pulkit Goel


Team Members: 
-------------
Kumar Rishabh (shailrishabh@gmail.com)

Vishrut Mehta (vishrut.mehta009@gmail.com)

Rishi Raj Singh Jhelumi (rishiakhnoor@gmail.com)

Rajeev Kumar (rajeevkumarchail@gmail.com)




Usage:
------

* Select one of the network-generators from the network-generator folder
* All these require three files link, switches and switches as input argument sample of which can be found in testerFiles folder
* Also required is the traffic generator sample of which can be found in generator in testerFiles folder
* Select one the controller to listen in remote mode in controllers folder
* Generate the Network 



Current Metric used:
--------------------

* Random
* Most Recently Used
* Frequency Distribution


TODO (ROADMAP):
---------------

* Simulate a Real World Dataset(Network activity logs of a real world network)
* Take care of other factors in Network 
* Reduce Communication blockage frequeny
* Port to other network controllers ( Floodlight, RYU ?????? maybe)
* Better logging of the entire system


Interesting:
------------

We presented a poster for the same as part of our Cloud Computing Course :-)




[1]: https://dl.dropboxusercontent.com/u/37587724/abstract.pdf "Abstract Link" 
