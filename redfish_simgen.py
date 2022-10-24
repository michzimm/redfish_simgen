#!/usr/bin/python3


import random
import string
import shutil
import os
import fnmatch
import docker


# Functions
def findReplace(directory, find, replace, filePattern):
    for path, dirs, files in os.walk(os.path.abspath(directory)):
        for filename in fnmatch.filter(files, filePattern):
            filepath = os.path.join(path, filename)
            with open(filepath) as f:
                s = f.read()
            s = s.replace(find, replace)
            with open(filepath, "w") as f:
                f.write(s)

#Get inputs
sim_type = input("Please select simulator type [hp, dell]: ")
port_num = input("Please enter a port number to run the simulator on between 30000-30999: ")

if sim_type == 'hp':

    # Generate random serial number
    serial = str(''.join(random.choices(string.ascii_uppercase + string.digits, k=10)))

    # Generate hostname
    hostname = "ILO"+serial

    # Generate server_name
    server_name = serial+".cisco.lab"

    # Generate random IP address
    ip = "10."+(".".join(str(random.randint(0, 255)) for _ in range(3)))

    print("Serial Number: "+serial)
    print ("ILO Hostname: "+hostname)
    print ("Server Name: "+server_name)
    print ("IP Address: "+ip)

    # Generate instance name
    instance_name = "hp_server."+serial

    # Create new directory tree for server, copy from template
    source_dir = "./hp_server.template"
    dest_dir = "./instances/"+instance_name
    shutil.copytree(source_dir, dest_dir)

    # Replace unique identifiers (serial, hostname, server_name, ip) in server directory tree
    findReplace("./hp_server_test", "{{SERIAL_NUMBER}}", serial, "*")
    findReplace("./hp_server_test", "{{ILO_HOSTNAME}}", hostname, "*")
    findReplace("./hp_server_test", "{{SERVER_NAME}}", server_name, "*")
    findReplace("./hp_server_test", "{{IP_ADDRESS}}", ip, "*")

client = docker.from_env()
container = client.containers.run('michzimm/redfish_sim', volumes=['/root/redfish_simgen/instances/'+instance_name])