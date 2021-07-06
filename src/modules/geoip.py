# GEOIP.py BY ZLL (Zheng Lin Lei)
# 2021
# APACHE 2.0 LICENSE
# MORE IN LICENSE FILE


import requests
import json


class GeoIp:

    requestsURI = 'https://geolocation-db.com/json/'

    def __init__(self, ip):

        self.ip = ip

        return self.request()

    def __repr__(self):
        return f"<GeoIp(ip={self.ip})>"

    # MAKE REQUEST
    def request(self):
        data = json.loads(requests.get(f'{self.requestsURI}{self.ip}').content)

        self.country =    data['country_name']
        self.city =       data['city']
        self.state =      data['state']
        self.ip =         data['IPv4']



# SIMPLY GEOLOCATION API

