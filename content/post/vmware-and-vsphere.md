---
author: ["Olivia Snowden"]
title: "vSPHERE INTRODUCTION"
date: "2020-07-01"
tags: ["home-lab", "vms"]
ShowToc: true
TocOpen: true
---




Practicing installing/updating/building machines is much more fun when you aren't running the risk of ruining an entire computer. To give myself a safe environment to work in, I have been using VMware's vSphere in our home lab for many of my computer projects. vSphere is a suite of virtualization products that allow you to create and manage VMs. This allows me to work on VMs that can run any OS I like, and if I something goes wrong I can just delete the VM and begin again.







In our lab we have two ESXi hosts that share a common storage device- a Synology NAS DS420j (Diskstation). We made the two hosts into a cluster, which means they act as one device and balance the load of the VMs between each other. Below you can see the two ESXi hosts sitting on top of the Diskstation in the lab. 







![](/vmware-1.jpeg)







vSphere provides a variety of components to manage your VMs. Within the lab I created a VM to run vCenter, which allows you manage your server on a single console and create a virtual infrastructure. The vSphere Client is an interface that allows you to connect to the vCenter server from anywhere using the IP address of the VM running vCenter. On this page you can view your clusters, VMs, virtual networks, storage devices and manage all your resources.  














Once you have a VM created, you can make a template of it to "copy and paste" an OS and avoid having to do an install for each VM you want. You'll need to wipe out any unique information (IP, MAC address, etc.) in a VM before clicking "make a template" on vSphere, so that you don't end up with multiple identical machines. Fortunately instructions for making a template of almost any OS can easily be found online. 







You also have the option to contain VMs in a virtual network that allows the VMs to talk to each other but prevents them from accessing any outside network. A virtual network could be useful for a cybersecurity project or simulating a quarantined network. 







Cloud computing and containers are new solutions to avoid having to create and manage VMs yourself, but working with VMware has been a good learning experience. I've previously used VMware Horizon Client and VMware Fusion in my IT classes but using my VMs as a sandbox for my projects has been a useful way to implement VMware on our home lab. 



