#!/usr/bin/python3


import random
import string
import shutil
import os
import fnmatch
import docker
import socket
from colorama import Style, Fore
from netifaces import interfaces, ifaddresses


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
print("\n")
while True:
    sim_type = input(Style.BRIGHT+Fore.CYAN+"Please select simulated server type "+Style.RESET_ALL+"[ hp , dell ]: ")
    if sim_type in ['hp','HP','Hp','dell','Dell','DELL']:
        sim_type = sim_type.lower()
        break
    else:
        print(Fore.RED+"Not a supported option, try again!"+Style.RESET_ALL)


print("\n")

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
    source_dir = "/opt/redfish_simgen/hp_server.template"
    dest_dir = "/opt/redfish_simgen/instances/"+instance_name
    shutil.copytree(source_dir, dest_dir)

    # Replace unique identifiers (serial, hostname, server_name, ip) in server directory tree
    findReplace(dest_dir, "{{SERIAL_NUMBER}}", serial, "*")
    findReplace(dest_dir, "{{ILO_HOSTNAME}}", hostname, "*")
    findReplace(dest_dir, "{{SERVER_NAME}}", server_name, "*")
    findReplace(dest_dir, "{{IP_ADDRESS}}", ip, "*")

elif sim_type == 'dell':
    
    # Generate random service tag
    service_tag = str(''.join(random.choices(string.ascii_uppercase + string.digits, k=7)))

    # Generate random serial number
    serial_num = str(''.join(random.choices(string.ascii_uppercase + string.digits, k=14)))

    # Generate random IP address
    ip = "10."+(".".join(str(random.randint(0, 255)) for _ in range(3)))

    print(Style.BRIGHT+Fore.GREEN+"Creating simulated redfish server as a container with the following randomly generated attributes...")
    print(Style.BRIGHT+Fore.WHITE+"  --> Serial Number: "+Style.RESET_ALL+serial_num)
    print(Style.BRIGHT+Fore.WHITE+"  --> Service Tag: "+Style.RESET_ALL+service_tag)
    print(Style.BRIGHT+Fore.WHITE+"  --> IP Address: "+Style.RESET_ALL+ip)

    # Generate instance name
    instance_name = "dell_server."+service_tag

    # Create new directory tree for server, copy from template
    source_dir = "/opt/redfish_simgen/dell_server.template"
    dest_dir = "/opt/redfish_simgen/instances/"+instance_name
    shutil.copytree(source_dir, dest_dir)

    # Replace unique identifiers (serial, hostname, server_name, ip) in server directory tree
    findReplace(dest_dir, "{{SERVICE_TAG}}", service_tag, "*")
    findReplace(dest_dir, "{{IP_ADDRESS}}", ip, "*")
    findReplace(dest_dir, "{{SERIAL_NUMBER}}", serial_num, "*")


client = docker.from_env()
container = client.containers.run('michzimm/redfish_sim:1.0', command=None, name=instance_name, volumes=['/opt/redfish_simgen/instances/'+instance_name+':/usr/src/app/instance'], ports={'8000/tcp': None}, detach=True)

print("      "+u'\U0001F44D'+" Done.")
print("\n")

container.reload()

for ifaceName in interfaces():
    if ifaceName == 'ens160':
        hostip = ifaddresses(ifaceName)[2][0]['addr']
        print(hostip)

print(Style.BRIGHT+Fore.GREEN+"When claiming this instance as a \"Redfish Server Target\" in Intersight, use the following information..."+Style.RESET_ALL)
print(Style.BRIGHT+Fore.WHITE+"  --> Intersight Assist: "+Style.RESET_ALL+"Select your local Intersight Assist.")
print(Style.BRIGHT+Fore.WHITE+"  --> Hostname/IPAddress: "+Style.RESET_ALL+hostip)
print(Style.BRIGHT+Fore.WHITE+"  --> Port: "+Style.RESET_ALL+container.ports['8000/tcp'][0]['HostPort'])
print(Style.BRIGHT+Fore.WHITE+"  --> Username: "+Style.RESET_ALL+"administrator")
print(Style.BRIGHT+Fore.WHITE+"  --> Password: "+Style.RESET_ALL+"password")
print(Style.BRIGHT+Fore.WHITE+"  --> Secure: "+Style.RESET_ALL+"enabled")
print("      "+u'\U0001F44D'+" Done.")
print("\n")
