#!/usr/bin/python3


import random
import string
import shutil
import os
import fnmatch
import docker
import socket
from colorama import Style, Fore


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

if sim_type == 'hp':

    # Generate random serial number
    serial = str(''.join(random.choices(string.ascii_uppercase + string.digits, k=10)))

    # Generate hostname
    hostname = "ILO"+serial

    # Generate server_name
    server_name = serial+".cisco.lab"

    # Generate random IP address
    ip = "10."+(".".join(str(random.randint(0, 255)) for _ in range(3)))

    print(Style.BRIGHT+Fore.GREEN+"Creating simulated redfish server as a container with the following randomly generated attributes...")
    print(Style.BRIGHT+Fore.WHITE+"  --> Serial Number: "+Style.RESET_ALL+serial)
    print(Style.BRIGHT+Fore.WHITE+"  --> ILO Hostname: "+Style.RESET_ALL+hostname)
    print(Style.BRIGHT+Fore.WHITE+"  --> Server Name: "+Style.RESET_ALL+server_name)
    print(Style.BRIGHT+Fore.WHITE+"  --> IP Address: "+Style.RESET_ALL+ip)

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
container = client.containers.run('michzimm/redfish_sim:1.0', command=None, volumes=['/root/redfish_simgen/instances/'+instance_name+':/usr/src/app/instance'], ports={'8000/tcp': None}, detach=True)

print("      "+u'\U0001F44D'+" Done.")

container.reload()

print(Style.BRIGHT+Fore.GREEN+"When claiming this instance as a \"Redfish Server Target\" in Intersight, use the following information..."+Style.RESET_ALL)

print(Style.BRIGHT+Fore.WHITE+"Intersight Assist: "+Style.RESET_ALL+"Select your local Intersight Assist.")

print(Style.BRIGHT+Fore.WHITE+"Hostname/IPAddress: "+Style.RESET_ALL+socket.gethostbyname(socket.gethostname()))

print(Style.BRIGHT+Fore.WHITE+"Port: "+Style.RESET_ALL+container.ports['8000/tcp'][0]['HostPort'])

print(Style.BRIGHT+Fore.WHITE+"Username: "+Style.RESET_ALL+"administrator")

print(Style.BRIGHT+Fore.WHITE+"Password: "+Style.RESET_ALL+"password")

print(Style.BRIGHT+Fore.WHITE+"Secure: "+Style.RESET_ALL+"enabled")
