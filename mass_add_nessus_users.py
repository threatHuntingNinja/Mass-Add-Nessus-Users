# -*- coding: utf-8 -*-


import SSH_lib
import pdb
import argparse
import csv

def main():

    with open('hosts.csv', newline='') as csvfile:
        host_particulars = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in host_particulars:
            try:
                host = row[0]
                user = row[1]
                passwd = row[2]
                user_to_add = row[3]
                passwd_to_add = row[4]
                is_admin = row[5]
                path_to_nessuscli = row[6]
                continue_on = True
            except:
                print("*) something wrong with row {}. Not processing".format(row))
                continue_on = False
             
            if continue_on:
                CREDS = {} 
                CREDS['host'] = host
                CREDS['user'] = user
                CREDS['passwd'] = passwd
                CREDS['port'] = 22

            #initialize client object
            ssh = SSH_lib.SSH(CREDS)
            client_obj = ssh.connect_to_ssh()
            if client_obj:
                print("*) Successfully connected to {}".format(CREDS['host']))
            else:
                print("*) Error! Failed to connect to {}".format(CREDS['host']))
                continue_on = False 

            # rm any old scripts
            if continue_on:
                cmd = "rm ./nessuscli_adduser.expect"
                cmd_output = ssh.ssh_exec_cmd(cmd)

            #upload the expect script
            if continue_on:
                local_file = "./nessuscli_adduser.expect"
                remote_file = "./nessuscli_adduser.expect"
                output = ssh.sftp_put_file(local_file, remote_file)
                if (output):
                    print("*) Uploaded {} to {}".format(local_file, CREDS['host']))
                else:
                    print("*) Error! Failed to upload {} to {}".format(local_file, CREDS['host']))
                    continue_on = False

            # chmod 700 script
            if continue_on:
                cmd = "chmod 700 ./nessuscli_adduser.expect"
                cmd_output = ssh.ssh_exec_cmd(cmd)

            # Add the user
            if continue_on:
                cmd = "./nessuscli_adduser.expect {} '{}' '{}' {}".format(path_to_nessuscli, user_to_add, passwd_to_add, is_admin)
                cmd_output = str(ssh.ssh_exec_cmd(cmd))
                if "User added" in cmd_output:
                    print("*) Added Nessus user {} to {}".format(user_to_add, CREDS['host']))
                else:
                    print("*) ERROR! Failed to add Nessus user {} to {}".format(user_to_add, CREDS['host']))
                    continue_on = False

            # rm the expect script
            if continue_on:
                cmd = "rm ./nessuscli_adduser.expect"
                cmd_output = ssh.ssh_exec_cmd(cmd)
                print("*) Deleted script")


            # log out of ssh server
            ssh.close()    
            print("*) connection to {} closed".format(CREDS['host']))



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Mass add Nessus users by logging in over SSH and executing nessuscli')
    args = parser.parse_args()

    print('*) Executing Script: {}'.format(__file__))
    main()

