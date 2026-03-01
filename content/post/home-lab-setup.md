---
author: ["Olivia Snowden"]
title: "HOME-LAB SETUP"
date: "2020-06-12"
tags: ["home-lab"]
ShowToc: true
TocOpen: true
---
For the home-lab, we used the following devices: 







  * Ubiquiti EdgeRouter X
  * Ubiquiti UniFi 24 port switch 
  * 2 VMware ESXi Hosts
  * A Synology NAS DS420j (Diskstation) 






Building the home lab also required quite a few patch cables to connect devices, and I made most of them myself. This required UTP cable, plastic clips for the ends, a cable crimping tool, and a lot of patience. The arrangement of the wires, or the pinout, had to be in a specific order. 







![Patch Cable](/home-cable.png)








The first step in building the home-lab was finding a way to connect our home network to the garage. The lab needed to be in it's own subnet so that anything done in the lab (or anything that goes _wrong_ in the lab) doesn't bleed over into the home network. To extend the home network to the garage, we used two Ubiquiti UniFi access points. One was connected to the home network and then placed on top of the house. The other was put on the garage, and the two access points were aligned. 







The AP on the garage was plugged into port 4 on the Ubiquiti EdgeRouter X, where a new 192.168.100.x/24 network was set. The router connected to the switch, which in turn connected to the two ESXi hosts and the Diskstation storage device.





![](/home-topology.png)





The Edge Router X doubles as a DHCP server, and once it gave the ESXi hosts and the Diskstation their own IP address the home-lab was ready for new projects. 