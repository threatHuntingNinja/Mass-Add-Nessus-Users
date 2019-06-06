This script automates creating Nessus users on remote SSH hosts.

In order for this script to run correctly, you will need to have a hosts.csv in the following format:

IP,UserID,Password,UserID to be added,Password for new UserID,y or n for sysadmin rights,Path to nessuscli binary

Example:
If you wanted to add a Nessus user account on host 10.10.10.10 using root account, you will need
root password
name of user that you want to add to Nessus - Ryan
password for Ryan - Ryanpass1
Should Ryan have Sys admin rights? y
What is the path to nessuscli /opt/nessus/sbin/nessuscli

With this information, you would create the following line in hosts.csv
10.10.10.10,root,Password1,Ryan,Ryanpass1,y,/opt/nessus/sbin/nessuscli

Add additional lines for each system 

When hosts.csv is complete, simply run
python mass_add_nessus_users.py 

Logging will be printed to STDOUT


