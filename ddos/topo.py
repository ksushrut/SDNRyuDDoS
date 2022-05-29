#!/usr/bin/python
import os
from functools import partial

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch, OVSSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

def myNetwork():

    OVSSwitch13 = partial(OVSSwitch, protocols='OpenFlow13')

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8')

    info( '*** Adding remote Ryu controller\n' )
    c0 = net.addController(
        name = 'c0',
        controller = RemoteController,
        ip = '127.0.0.1',
        protocol = 'tcp',
        port = 6633
    )

    # info( '*** Adding default controller\n' )
    # c0=net.addController(name='c0',
    #                   controller=Controller,
    #                   protocol='tcp',
    #                   port=6633)

    info( '*** Add switches\n')

    s4 = net.addSwitch('s4', cls=OVSKernelSwitch)
    s6 = net.addSwitch('s6', cls=OVSKernelSwitch)
    s5 = net.addSwitch('s5', cls=OVSKernelSwitch)
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch)
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)

    info( '*** Add hosts\n')
    h8 = net.addHost('h8', cls=Host, ip='10.0.0.8', defaultRoute=None,mac='0A:0A:00:00:00:08')
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.1', defaultRoute=None,mac='0A:0A:00:00:00:01')
    h2 = net.addHost('h2', cls=Host, ip='10.0.0.2', defaultRoute=None,mac='0A:0A:00:00:00:02')
    h6 = net.addHost('h6', cls=Host, ip='10.0.0.6', defaultRoute=None,mac='0A:0A:00:00:00:06')
    h4 = net.addHost('h4', cls=Host, ip='10.0.0.4', defaultRoute=None,mac='0A:0A:00:00:00:04')
    h3 = net.addHost('h3', cls=Host, ip='10.0.0.3', defaultRoute=None,mac='0A:0A:00:00:00:03')
    h9 = net.addHost('h9', cls=Host, ip='10.0.0.9', defaultRoute=None,mac='0A:0A:00:00:00:09')
    h5 = net.addHost('h5', cls=Host, ip='10.0.0.5', defaultRoute=None,mac='0A:0A:00:00:00:05')
    h7 = net.addHost('h7', cls=Host, ip='10.0.0.7', defaultRoute=None,mac='0A:0A:00:00:00:07')

    info( '*** Add links\n')
    net.addLink(h6, s4)
    net.addLink(h7, s4)
    net.addLink(h8, s5)
    net.addLink(h9, s5)
    net.addLink(h1, s6)
    net.addLink(s1, s6)
    net.addLink(s1, s2)
    net.addLink(s1, s3)
    net.addLink(s1, s4)
    net.addLink(s1, s5)
    net.addLink(h2, s2)
    net.addLink(h3, s2)
    net.addLink(h4, s3)
    net.addLink(h5, s3)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s4').start([c0])
    net.get('s6').start([c0])
    net.get('s5').start([c0])
    net.get('s3').start([c0])
    net.get('s2').start([c0])
    net.get('s1').start([c0])

    info( '*** Post configure switches and hosts\n')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    # Open new gnome-terminal for running Ryu controller.
    # os.system('gnome-terminal --command="ryu-manager ryu.app.simple_switch_13 ryu.app.ofctl_rest"')
    
    # Start Custom topo
    setLogLevel( 'info' )
    myNetwork()

# Ryu controller
# ryu-manager ryu.app.simple_switch_13 ryu.app.ofctl_rest
