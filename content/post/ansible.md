---
author: ["Olivia Snowden"]
title: "INTRODUCTION TO ANSIBLE"
date: "2022-01-13"
tags: ["code", "raspberrypi", "home-lab", "automation"]
ShowToc: true
TocOpen: true
---
![](/ansible-logo.png)
**In this post:**

1. **What is Ansible** 

2. **Installing Ansible**

3. **Authentication**

4. **Inventories**

5. **Playbooks**

6. **Testing Ansible**

### What is Ansible?
Ansible is an open-source infrastructure as code tool provided by Red Hat. Instead of agents, Ansible relies on SSH to pass tasks defined in YAML to remote machines.  To get familiar with Ansible, I created a simple scenario where a bash script needed to be uploaded to a remote machine and ran periodically. 

In a previous [blog post](https://www.osnowden.com/raspberry-pi-kubernetes/) I've explained the process of building a Kubernetes cluster using 3 Rasperry Pis in my home computer lab. For this project I used my personal MacBook and one of the Pis from that cluster. Although it is possible to use Ansible with all 3 Pis, for the simplicity of this project I used only 1. 
![](/raspberry-1.jpeg)

### Installing Ansible
To install Ansible, the Ansible package just needs to be downloaded onto a machine running MacOS or Windows and with Python 3.8 (or a newer version of Python) installed. The machine with Ansible installed becomes the control node, and can then manage a fleet of machines or "managed nodes".  Ansible usually uses SSH to connect to managed nodes and transfers tasks using SFTP. That being said, if any of the nodes can't use SFTP you can switch to SCP in the Ansible config file ansible.cfg. 
I have a MacBook, and to install Ansible using pip I ran: `sudo python3 -m pip install ansible`
![](/ansible-install-ansible.png)
This installed Ansible my home directory under /Users

### Authentication
Since Ansible connects to managed nodes using SSH, I needed to create an SSH key pair. The *private* SSH key would remain on the control node, and the *public* SSH key would be placed on the managed node. This way, the connection between the nodes was secure for SSH. 

**Note: To avoid using SSH keys, the `--ask-pass` argument can be added to Ansible commands to prompt the user for the SSH password.**

To create an SSH key pair, I used the ssh-keygen command: `ssh-keygen -t rsa -f FILE_NAME`
![](/ansible-key.png)
The key pair is placed in the default SSH key directory, ~/.ssh 
The public keys have the `.pub` extension,  this is the key that needs to be placed on the managed node in the ~/.ssh/authorized_keys directory. 
![](/ansible-ssh-keys.png)
To place my "id_rsa.pub" public key on the managed node I used an SCP command with the syntax: `scp LOCAL_PATH_OF_KEY USER@IP_OF_CONTROL_NODE:~/.ssh/authorized_keys`

### Inventory
Once the control node and the managed node(s) have a secure connection, the managed nodes can be added to an inventory. Ansible inventories specify managed nodes that should be used by Ansible, and you can use an inventory to organize your managed nodes. The default location for Ansible's inventory is /etc/ansible/hosts. The `-i PATH_TO_HOSTS_FILE` argument can be added to Ansible commands to specify a different path for the inventory if you are working out of a different directory (which I did). 

The contents of an inventory can be as simple as the IP addresses of the managed nodes, which is what I used. However group names enclosed in brackets [] and assigning aliases to hosts with `ALIAS ansible_host=IP` can help organize the inventory. 
![](/ansible-hosts-file.png)
Once the managed hosts were defined, I tested the connection between the control and managed nodes using a ping command with the syntax:  `ansible all -i PATH_TO_HOSTS_FILE -u USERNAME_ON_MANAGED_NODE -m ping`
![](/ansible-ping.png)

### Playbooks
Next, the tasks to be passed along to the managed nodes defined in the inventory need to be specified in a playbook. Playbooks are YAML files that can include variables and tasks, and are executed from top to bottom. Tasks are named with the `-name` line, the value of which appears when Ansible executes the playbook so that you can keep track of when tasks run. Like Python, Ansible has a variety of modules that can be called to perform tasks. The list of Ansible modules can be found on their [site]( https://docs.ansible.com/ansible/2.9/modules/modules_by_category.html) and incorporated into the YAML of playbooks.

Similar to Terraform, Ansible can check whether anything needs to be changed on managed nodes to meet the desired configuration in the playbook. Therefore, if nothing needs to be changed Ansible won't do anything. 
For my playbook, I needed to upload a bash script to a managed node and have that script run on a schedule. For testing purposes, I created a simple bash script, "test-script.sh",  to place "Hello World" into a new file "output.sh" each time the script ran. In my playbook, playbook.yml, I created two tasks. The first task transferred test-script.sh from the control node to the home directory of the user "pi" on the managed node.  The second task used Ansible's "cron" module to create a cron job on the managed node. The details of the cron job set test-script.sh to run daily at 2 and 5. 

**Note: I used the cron module since the managed node was running Linux. If the managed node is a Windows machine, the Ansible module win_scheduled_task can be used to run tasks on a schedule.**

![](/ansible-playbook.png)
**Note: It is important to give scripts the appropriate permissions to run, hence "mode=0777"**

### Testing Ansible
To test the playbook, I ran the command ansible-playbook using the syntax: `-i PATH_TO_HOSTS_FILE playbook.yml` 
![](/ansible-run-playbook.png)
To confirm that Ansible worked, I SSHed into the managed node and checked that test-script.sh was on the machine, the output.sh file was created and contained "Hello World", and that the cronjob specified in the playbook existed using the command `crontab -l`. I then removed the cron job using `crontab -r` and deleted test-script.sh and output .sh using the `rm FILE_NAME` command. 
![](/ansible-result.png)