from micloud import MiCloud
from micloud.micloudexception import MiCloudAccessDenied
from getpass import getpass
from tabulate import tabulate
import logging

logging.basicConfig(level=logging.CRITICAL)

AVAILABLE_LOCALES = {
    "all": "All",
    "cn": "China",
    "de": "Germany",
    "i2": "i2",  # unknown
    "ru": "Russia",
    "sg": "Singapore",
    "us": "USA",
}


def main():
    username = input("Username(Email/phone): ")
    password = getpass("Password: ")
    mc = MiCloud(username, password)
    try:
        success = mc.login()
    except MiCloudAccessDenied:
        print("Username or password incorrect")
        exit(1)
    token = mc.get_token()  # to get your cloud service token.
    devices = []
    for country in AVAILABLE_LOCALES:
        try:
            device_list = mc.get_devices(
                country=country)  # get list of devices
            devices.extend(device_list)
        except Exception as e:
            pass

    rows = []
    for d in devices:
        name = d.get("name")
        token = d.get("token")
        ip = d.get("localip")
        mac = d.get("mac")
        rows.append([name, token, ip, mac])
    print(tabulate(rows, ["NAME", "TOKEN", "IP", "MAC"]))
