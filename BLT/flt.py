"""
Copyright (c) 2019 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
               https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.

Filename: flt.py
Version: Python 3.7.2
Authors: Aaron Warner (aawarner@cisco.com)
Description: This program is designed to automate the licensing of Cisco Catalyst
Switches and Cisco Integrated Services Routers. This tool relies on the Cisco Federal
Licensing Tool to function.
"""
import sys
import os
from datetime import datetime
import csv
from multiprocessing.dummy import Pool as ThreadPool
import subprocess
import netmiko



def getLoginInfo(csvFile):
    """
    Function to create list of dictionaries from CSV file.
    """
    with open(csvFile, "r") as swfile:
        reader = csv.DictReader(swfile)
        data = []
        for line in reader:
            data.append(line)
    return data


def convertLoginDict(data):
    """
    Converts list of dictionaries to list of lists
    """
    try:
        swlist = [[row["ipaddr"], row["username"], row["password"]] for row in data]
        return swlist
    except KeyError:
        print(
            "\nInvalid header in CSV file. Please modify to the format below: "
            "\nipaddr,username,password"
            "\n10.10.10.10,admin,cisco"
            "\n10.10.10.11,admin,cisco\n"
        )
        sys.exit()


def checkVersion(conn):
    version = conn.send_command("show version | i Cisco IOS XE Software")
    version = version.split()
    release = version[-1]
    release_major = int(release[:2])
    if release_major == 16:
        num = float(release[3::])
        print(num)
        if num == 09.04:
            return True
        if num > 12.01:
            return True
        print("FLT is not supported with this version of IOS-XE")
        return False
    if release_major == 17:
        return True

    print("FLT is not supported with this version of IOS-XE")
    return False


def licenseSwitch(ip, user, pwd):
    """
    Function logs in to Cisco IOS-XE device and licenses it with the FLT
    """

    session = {
        "device_type": "cisco_ios",
        "ip": ip,
        "username": user,
        "password": pwd,
        "verbose": False,
    }
    try:
        print("Connecting to device {switch}".format(switch=ip))
        conn = netmiko.ConnectHandler(**session)
        if checkVersion(conn) is True:
            checklic = conn.send_command("show run | i license smart reservation")
            if checklic == "license smart reservation":
                pass
            else:
                print(
                    "Device {switch} is missing the 'license smart reservation' "
                    "command...enabling now".format(
                        switch=ip
                    )
                )
                plr = ["license smart reservation"]
                conn.send_config_set(plr)
            conn.enable()
            reqcode = conn.send_command("license smart reservation request local")
            reqcode = reqcode.split()
            reqcode = reqcode[-1]

            print(
                "Request Code collection successful from device {switch}".format(
                    switch=ip
                )
            )
            print("Request code is {reqcode}".format(reqcode=reqcode))
            try:
                if os.path.exists(
                        "C:\\Program Files\\Cisco Federal Licensing Tool\\fltool.exe"
                ):
                    authcode = subprocess.check_output(
                        'C:\\"Program Files"\\"Cisco Federal Licensing Tool"\\fltool.exe'
                        ' -u {code}'.format(
                            code=reqcode
                        ),
                        shell=True,
                        universal_newlines=True,
                        stderr=subprocess.DEVNULL,
                    )
                    authcode = authcode.split()
                    authcode = authcode[-1]

                    print("Authorization code is {authcode}".format(authcode=authcode))

                    conn.send_command(
                        "license smart reservation install {authcode}".format(
                            authcode=authcode
                        )
                    )
                else:
                    print("FLT not installed on the system")
            except subprocess.CalledProcessError:
                print(
                    "fltool.exe is missing. Ensure the FLT is installed in the "
                    "'C:\Program Files\Cisco Federal Licensing Tool' directory."
                )
                sys.exit()

            reg = conn.send_command("show license summary")

            reg = reg.split()

            if reg[10] == "REGISTERED":
                print("Device {switch} licensed successfully".format(switch=ip))
            else:
                print("Device {switch} license process failed".format(switch=ip))
        else:
            print("Cisco IOS-XE software version is not compatible with FLT")
    except (
            netmiko.NetMikoTimeoutException,
            netmiko.NetMikoAuthenticationException,
    ) as e:
        print(e)


def main(args):
    """Main code function"""
    try:
        # Define start time
        start_time = datetime.now()

        # Define the number of threads
        num_threads = int(sys.argv[2])
        pool = ThreadPool(num_threads)

        # Import CSV file and generate list of dictionaries
        csvFile = sys.argv[1]
        data = getLoginInfo(csvFile)

        # Convert list of dictionaries to list of lists
        swlist = convertLoginDict(data)

        # Start threads
        pool.starmap(licenseSwitch, swlist)
        pool.close()
        pool.join()

        print("\nElapsed time: " + str(datetime.now() - start_time))

    except ValueError:
        print("Invalid entry for number of threads. Please enter an integer.")


if __name__ == "__main__":
    if len(sys.argv) == 3:
        main(sys.argv)
    else:
        print(
            "\nThis program is designed to automate the licensing of\n"
            "Cisco Catalyst switches and Cisco ISR Routers. This program \n"
            "relies on the Cisco Federal Licensing Tool in order to function.\n"
            "This program should be executed in the same directory as fltool.exe\n"
            "\nThe program accepts two arguments. The name of a CSV file and the "
            "number of desired threads.\n "
            "\nThe CSV should be in the format below:\n"
            "\nipaddr,username,password"
            "\n10.10.10.10,admin,cisco"
            "\n10.10.10.11,admin,cisco\n"
            "\nUsage: python get_info.py DeviceDetails.csv X\n"
            "\nThe 'X' represents the number of threads to execute"
        )
        sys.exit()
