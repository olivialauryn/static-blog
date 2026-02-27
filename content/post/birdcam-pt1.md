---
author: osnowden
comments: true
date: 2020-05-18 17:38:06+00:00
layout: post
link: http://oliviasnowden.me/2020/05/18/birdcam-pt-1/
slug: birdcam-pt-1
title: BIRDCAM Pt. 1
wordpress_id: 118
tags: [code, docker, raspberrypi]
---






In this project I wanted to set up a camera to take pictures of pretty birds at a feeder, and then view those photos online.  To do so I used three Raspberry Pis, NFS, and Docker. 







One Raspberry pi served as the NFS server, while the other two were NFS clients. One of the clients was a Raspberry Pi zero w outfitted with a camera to take the pictures and store them on the NFS server. The other client hosted the docker container linuxserver/photoshow that accessed the NFS server to display the photos in a gallery.  









Since I wanted to take multiple photos a day, dedicating one Pi to storing the photos freed up the other Pis to do their respective jobs. This was done by making one Pi an NFS (Network File System) server. NFS allows client computers to access files over a network as if those files were stored locally. First, I configured one Pi as the NFS server. To do so, I first made sure all packages were updated on the Raspbian OS. 






    
    sudo apt-get update 
    sudo apt-get upgrade 







Then, I installed the nfs-kernel-server package that builds the protocol to handle the server side of NFS. 






    
    sudo apt-get install nfs-kernel-server -y







Next I gave the pi user/group ownership of the folder I want shared (the folder for the bird photos). I also used the **find** command to change the permissions of the directories and files in that folder. 






    
    sudo chown -R pi:pi <em>/path-to-folder</em>
    sudo find <em>/path-to-folder</em> -type d -exec chmod 755 {} \;
    sudo find <em>/path-to-folder</em> -type f -exec chmod 644 {} \;







To allow the NFS protocol to know what directories to share, we need to include that path in the /etc/exports file. In addition to the path,  I included a variety of options: 






    
    /<em>path-to-folder</em> *(rw,all_squash,insecure,async,no_subtree_check,anonuid=1000,anongid=1000)







  * *: allow all IPs to access this share, you can also include specific IPs
  * rw: allow reading/writing
  * all_squash: maps uids and gids to an anonymous user
  * insecure: allows clients that do not use a reserved NFS port
  * async: allows the NFS server to improve performance if the server crashes, even if that causes data to be corrupted
  * no_subtree_check: disables subtree checking, improving reliability of NFS
  * anonuid: this is the UID of the pi user 
  * anongid: this is the GID of the pi user  








Once the Pi with the NFS server was set up, I configured the other Raspberry Pis to be clients. On each Pi, I first installed NFS tools, and created a virtual folder to serve as a mount-point to the NFS share. The location of the folder doesn't matter-as long as you remember the path to it. 






    
    sudo apt-get install nfs-common -y
    sudo mkdir -p <em>/path-to-folder</em>







Like on the NFS server, I also changed the permissions of the mount point to the pi user and group (or the user's user/group name). 






    
    sudo chown -R pi:pi <em>/path-to-folder</em>







Next, mount the NFS share to the mount-point.  First, name the IP of the NFS server and then the path to the shared folder on the NFS server. Then name the path to the shared folder on the client.






    
    sudo mount <em>ip-of-NFS-server:path-on-server path-on-client</em>







Edit the /etc/fstab file to include the mount and permissions so that the NFS share will automatically mount when your machine boots. One done editing the fstab file, enter Ctrl+x, Y, Enter to save and exit. 






    
    sudo nano /etc/fstab
    <em>ip-of-NFS-server:path-on-server path-on-client</em> nfs rw 0 0 







Now, one Raspberry Pi is an NFS server and the other two are connected to it via a shared folder. This allows the Pi with the camera to store the photos it takes on the share, and the Pi running the photo gallery container to access those photos, all without taking up any storage on the other two Pis. 



