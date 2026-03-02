---
author: ["Olivia Snowden"]
title: "Birdcam Pt. 2"
date: "2020-05-20"
tags: ["Home-Lab", "Raspberry-Pi", "Docker"]
ShowToc: true
TocOpen: true
---






After setting up the NFS server, but before making any NFS clients, I configured another Raspberry Pi to take the photos for my Bird Cam project. For this I used a Raspberry Pi Zero W and the appropriate camera attachment. Instead of using a keyboard/monitor to configure the Zero, I created a headless setup to allow the Zero to connect to wifi automatically when plugged in. 







First, I put the Raspbian Lite OS on a mini SD card. Once the OS was finished downloading, I removed the card from my computer and inserted it again. On my computer's terminal I entered the SD card's boot directory (found with **df -h**) and created a new file to configure the wifi information for my home network. 






    
    cd <em>card's-boot-directory</em>
    vim wpa_supplicant.conf







In the file I added:






    
       country=US
       ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev 
       update_config=1
       network={
        ssid="<em>Network's-name</em>"
        psk="<em>Network's-password</em>"
        key_mgmt=WPA-PSK
       }







This allowed the Raspberry Pi Zero to automatically know my home network's wifi info and be able to connect without having to attach a keyboard and enter the information manually. 







The final step in creating a headless setup on the Zero is to enable ssh so that you are able to connect to the Pi through secure shell.  To do this, I created an empty file in the boot directory of the SD card named ssh. 






    
    cd <em>card's-boot-directory </em>
    touch ssh 







Then, after plugging in the Raspberry Pi Zero and finding it's IP on my network, I was able to ssh into it and set up the camera. 









To take photos with the Zero I used a Raspberry Pi camera and an adapter for the Zero's tiny camera port. Once the adapter was snapped into the camera on one end and the Zero on the other (with the circuitry facing the back of the Zero) I configured the camera and tested it. To do so I entered the configuration program for the Raspberry Pi:






    
    sudo raspi-config 







I then enabled the camera under "Interfacing Options". To test that the camera works, I ran the **raspistill **command:






    
    raspistill -v -o <em>name</em>.jpg 







Once the camera was attached and working, I created a directory to store the photos using **mkdir **(this should be the same directory used to mount the NFS share, so that the photos are mapped to the NFS server). 







I wanted to configure the camera to take photos every half hour from 8am-5pm. I did this by writing a simple bash script to use **raspistill** to take photos and give them a unique name of the date/time.






    
    vim <em>script</em>.sh
    #!/bin/bash
    DATE=$(date +"%Y-%m-%d_%H%M")
    raspistill -o /<em>path-to-photos</em>/$DATE.jpg







I then made that script executable:






    
    chmod +x <em>script</em>.sh 







Finally, I created two cron jobs, one to take a photo every hour and another to take a photo every half hour. **cronab -e** will place you in the cron editor. 






    
    crontab -e
    0 8,9,10,11,12,13,14,15,16,17 * * * ./<em>script</em>.sh
    30 8,9,10,11,12,13,14,15,16,17 * * * ./<em>script</em>.sh







Once I added the jobs I wanted to schedule I entered Ctrl+X, Y, Enter to exit. To double check the jobs, I viewed them with **crontab -l.** Now, the Raspberry Pi Zero W is able to take multiple photos a day, and store them on the NFS server through the shared folder. 



