#!/usr/bin/env python

import os
import time
import subprocess
import sys

# python 2 and 3 compatibility
try:
    from urllib.request import urlopen
except ImportError:
    from urllib import urlopen
import multiprocessing


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# Make sure Tool is run via sudo or by root
if not os.geteuid() == 0:
    sys.exit(bcolors.FAIL + "\nOnly root can run this script\nTry with $ sudo kalel" + bcolors.ENDC)


# Check if setup is complete
def dosetup():
    if not os.path.isfile("/opt/KalEl/src/setupOK"):
        print("You must run setup.py first\n")
        ans1 = raw_input("Would you like to run setup now?\n y/n: ")
        if ans1 == "y":
            os.system('setup.py install')
        else:
            exit(1)


def check_os():
    if os.name == "nt":
        operating_system = "windows"
    if os.name == "posix":
        operating_system = "posix"
    return operating_system


kaldir = '/opt/KalEl/.kal'


# Get the version number:
def get_version():
    define_version = open("src/kalel.version", "r").read().rstrip()
    # define_version = '1.1.1'
    return define_version


define_version = get_version()


def pullupdate(define_version):
    cv = get_version()

    # pull version
    try:
        def pull_version():
            if not os.path.isfile(kaldir + "/version.lock"):
                try:
                    url = (
                        'https://raw.githubusercontent.com/noobscode/kalel/master/src/kalel.version')
                    version = urlopen(url).read().rstrip().decode('utf-8')
                    filewrite = open(kaldir + "/version.lock", "w")
                    filewrite.write(version)
                    filewrite.close()

                except KeyboardInterrupt:
                    version = "keyboard interrupt"
            else:
                version = open(kaldir + "/version.lock", "r").read()

            if cv != version:
                print("There is a new update available!")
            else:
                print("KalEl is up to date!")

        # Pull the version from out git repo
        p = multiprocessing.Process(target=pull_version)
        p.start()

        # Wait for 5 seconds or until process finishes
        p.join(8)

        # If thread is still active
        if p.is_alive():
            print(
                bcolors.FAIL + " Unable to check for new version are you connected to the internet?\n" + bcolors.ENDC)
            # terminate the process
            p.terminate()
            p.join()

    except Exception as err:
        print(err)
        pass


# Pull the TOR IP/Status Section
def getip():
    torip = open("module/tor/tor.ip", "r").read().rstrip()
    return torip


torip = getip()


def logo():
    print(bcolors.OKBLUE + """
    __  ___      ___       __          _______  __
   |  |/  /     /   \     |  |        |   ____||  |
   |  '  /     /  ^  \    |  |        |  |__   |  |
   |    <     /  /_\  \   |  |        |   __|  |  |
   |  .  \   /  _____  \  |  `----.   |  |____ |  `----.
   |__|\__\ /__/     \__\ |_______|   |_______||_______|

    - Kal El Network Penetration Testing (""" + bcolors.WARNING + """KalEl NPT""" + bcolors.OKBLUE + """)
    - Created by:""" + bcolors.FAIL + """ NoobsCode """ + bcolors.OKBLUE + """ """ + bcolors.WARNING + """ """ + bcolors.OKBLUE + """
    - Version: """ + bcolors.OKGREEN + """%s""" % (define_version) + bcolors.WARNING + """ """), pullupdate(define_version)
    print('    - Tor IP: %s' % (torip))
    print("""    - Github: """ + bcolors.OKGREEN + """https://www.Github.com/NoobsCode/KalEl""" + bcolors.OKBLUE + """ """)


# initial user menu
def agreement():
    if not os.path.isfile("/opt/KalEl/src/agreement"):
        with open("LICENSE") as fileopen:
            for line in fileopen:
                print((line.rstrip()))
                print('\n')

            print("{0}Kal El is designed purely"
                  " for good and not evil. If you are planning on "
                  "using this tool for malicious purposes that are "
                  "not authorized by the company you are performing "
                  "assessments for, you are violating the terms of "
                  "service and license of this toolset. By hitting "
                  "yes (only one time), you agree to the terms of "
                  "service and that you will only use this tool for "
                  "lawful purposes only.{1}".format(bcolors.FAIL, bcolors.ENDC))
            print(bcolors.OKGREEN)
            choice = raw_input("\nDo you agree to the terms of service [y/n]: ")
            if choice == "y":
                with open("/opt/KalEl/src/agreement", "w") as filewrite:
                    filewrite.write("user accepted")
                    print(bcolors.ENDC)
            else:
                print(bcolors.ENDC + "[!] Exiting Kal El, have a nice day." + bcolors.ENDC)
                sys.exit()


def goon():
    raw_input(bcolors.OKGREEN + 'Press [ENTER] to continue...' + bcolors.ENDC)


# Header information Intro text
def intro():
    print(bcolors.HEADER + bcolors.BOLD + "\n Kal El is a neat tool for Network Stress Testing and Penetration Testing")
    print(" This toolkit is still a work in progress and is a very early build." + bcolors.ENDC)


# Create the main menu
def mainmenu():
    os.system('clear')
    agreement()
    os.system('clear')
    ans = True
    while ans:
        logo()
        intro()
        print ("""
        1.Traffic Spoof Attack # Force Redirect Network Traffic (DNS SPOOF)
        2.The Harvester        # Harvest Email, Vhosts, Subdomain names (more)
        3.Spoof Emails         # Send Fake Emails To And From Anyone
        4.Traffic Generator    # Generate Fake Visitor Stats on a webpage
        5.Activate Tor(VPN)    # Activate VPN For Anonymity To Hide Yourself
        9.Update KalEl         # Update The KalEl Toolkit
        10.Help/Tutorial
        99.Exit/Quit
        """)
        ans = raw_input("Choose Attack Vector: ")
        if ans == "1":
            os.system('clear')
            logo()
            os.system('module/ettercap/spoof.py')
        elif ans == "2":
            os.system('clear')
            logo()
            os.system('module/harvester/prep.py')
        elif ans == "3":
            os.system('clear')
            logo()
            os.system('module/spoofmail/spoofmail.py')
        elif ans == "4":
            os.system('clear')
            logo()
            os.system('module/trafficgen/getheader.py')
        elif ans == "5":
            submenu_tor()
        elif ans == "9":
            print('Updating')
            update_kalel()
        elif ans == "10":
            print("Visit our github at: https://github.com/noobscode/kalel")
            goon()
        elif ans == "99":
            print("\n Goodbye")
            sys.exit(1)
        elif ans != "":
            print("\n Not Valid Choice Try again")


# Create the submenu
def submenu_tor():
    os.system('clear')
    ans = True
    while ans:
        logo()
        intro()
        print ("""
        1.Start TOR VPN        # Start TOR VPN
        2.Stop TOR VPN         # Stop TOR VPN
        3.Switch IP (Renew)    # Request new IP address

        4.Back to main menu
        """)
        ans = raw_input("Choose Attack Vector: ")
        if ans == "1":
            os.system('module/tor/tor.py start')
        elif ans == "2":
            os.system('module/tor/tor.py stop')
        elif ans == "3":
            os.system('module/tor/tor.py switch')
        elif ans == "4":
            mainmenu()
        elif ans != "":
            print("\n Not Valid Choice Try again")


# Check if we are running Kali Linux
def check_kali():
    if os.path.isfile("/etc/apt/sources.list"):
        kali = open("/etc/apt/sources.list", "r")
        kalidata = kali.read()
        if "kali" in kalidata:
            return "Kali"
        # if we aren't running kali
        else:
            return "Non-Kali"
    else:
        print("[!] Not running a Debian variant..")
        return "Non-Kali"


# KalEl Update
def update_kalel():
    if os.getcwd() == '/opt/KalEl':
        pass
    else:
        print(bcolors.FAIL + '\nYou are not in KalEl Directory!\n' + bcolors.ENDC)
        print(bcolors.WARNING + 'Please run KalEl from /opt/KalEl/\n' + bcolors.ENDC)
        time.sleep(2)
        mainmenu()

    print("Performing Update Please Wait")
    print("Cleaning up...")
    subprocess.Popen("git clean -fd", shell=True).wait()
    print("Updating, please wait...")
    subprocess.Popen("git fetch origin master", shell=True).wait()
    subprocess.Popen("git reset --hard FETCH_HEAD", shell=True).wait()
    subprocess.Popen("mkdir /opt/KalEl/.kal", shell=True).wait()

    # Fix permissions
    subprocess.Popen(['chmod', '+x', '/opt/KalEl/run.py'])
    subprocess.Popen(['chmod', '+x', '/opt/KalEl/module/tor/tor.py'])
    subprocess.Popen(['chmod', '+x', '/opt/KalEl/module/ettercap/spoof.py'])
    subprocess.Popen(['chmod', '+x', '/opt/KalEl/module/harvester/prep.py'])
    subprocess.Popen(['chmod', '+x', '/opt/KalEl/module/harvester/engine.py'])
    subprocess.Popen(['chmod', '+x', '/opt/KalEl/module/spoofmail/spoofmail.py'])
    cleanup()

    # Create a symbolic link for launching the toolkit via usr/bin
    subprocess.Popen("ln -s /opt/KalEl/run.py /opt/KalEl/kalel", shell=True).wait()

    print("Update finished, returning to main menu.")
    goon()
    os.system('kalel')
    time.sleep(2)


def cleanup():
    #if os.path.isfile(kaldir + '/version.lock'):
        #os.remove(kaldir + '/version.lock')
    if torip != 'VPN Disabled':
        print('NB: Tor is still running!')
        print('You can shut it down manually by typing\n$ sudo kalelvpn stop')


# Run the program
try:
    dosetup()
    mainmenu()
except KeyboardInterrupt:
    print("\n\nDon't forget your cat!\n")
# End
