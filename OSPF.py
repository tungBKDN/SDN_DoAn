"""This file contains a simple OSPF topology"""

import argparse
import json
import os
from mininet.log import LEVELS, lg
import ipmininet
from ipmininet.cli import IPCLI
from ipmininet.ipnet import IPNet
from ipmininet.router.config.zebra import Zebra
from ipmininet.iptopo import IPTopo
from ipmininet.router.config import RouterConfig

HOSTS_PER_ROUTER = 2


class MyTopology(IPTopo):
    """This simple network has multiple areas, as well as some passive
    interfaces in a management network"""

    def build(self, *args, **kwargs):
        # Build backbone
        r1, r2, r3 = self.addRouters('r1', 'r2', 'r3', use_v4=True,
                                     use_v6=False)

        # Connect routers
        self.addLink(r1, r2, igp_metric=10)
        self.addLink(r1, r3, igp_metric=5)
        self.addLink(r2, r3, igp_metric=15)

        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')

        # Add links to switches
        self.addLink(r1, s1, params1={'ip': '10.0.1.1/24'})
        self.addLink(r2, s2, params1={'ip': '10.0.2.1/24'})
        self.addLink(r3, s3, params1={'ip': '10.0.3.1/24'})

        # Add hosts to switches
        for i in range(HOSTS_PER_ROUTER):
            h1 = self.addHost(f'h{i}r1', ip=f'10.0.1.{i+11}/24')
            h2 = self.addHost(f'h{i}r2', ip=f'10.0.2.{i+11}/24')
            h3 = self.addHost(f'h{i}r3', ip=f'10.0.3.{i+11}/24')
            self.addLink(h1, s1)
            self.addLink(h2, s2)
            self.addLink(h3, s3)

        # OSPF configuration
        self.addOSPFArea(routers=(r1, r2), area='1.1.1.1')


        # Area 2.2.2.2
        r4, r5, r6 = self.addRouters('r4', 'r5', 'r6', use_v4=True, use_v6=False)
        s4 = self.addSwitch('s4')
        s5 = self.addSwitch('s5')
        s6 = self.addSwitch('s6')
        self.addLink(r4, r5, igp_metric=10)
        self.addLink(r4, r6, igp_metric=5)
        self.addLink(r3, r4, igp_metric=15)
        self.addLink(r4, s4, igp_area='2.2.2.2', params1={'ip': '10.0.4.1/24'})
        self.addLink(r5, s5, igp_area='2.2.2.2', params1={'ip': '10.0.5.1/24'})
        self.addLink(r6, s6, igp_area='2.2.2.2', params1={'ip': '10.0.6.1/24'})
        for i in range(HOSTS_PER_ROUTER):
            h4 = self.addHost(f'h{i}r4', ip=f'10.0.4.{i+11}/24')
            h5 = self.addHost(f'h{i}r5', ip=f'10.0.5.{i+11}/24')
            h6 = self.addHost(f'h{i}r6', ip=f'10.0.6.{i+11}/24')
            self.addLink(h4, s4)
            self.addLink(h5, s5)
            self.addLink(h6, s6)
        self.addOSPFArea(routers=(r4, r5, r6), area='2.2.2.2')


        super().build(*args, **kwargs)

ipmininet.DEBUG_FLAG = True
os.environ["PATH"] += os.pathsep + "/home/vagrant/quagga/bin" + os.pathsep + "/home/vagrant/quagga/sbin"
# Start network
net = IPNet(topo=MyTopology(), use_v4=True, use_v6=False, allocate_IPs=True)
net.start()
IPCLI(net)
net.stop()
