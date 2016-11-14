"""
    Dronesmith API
    Python Bindings

    Author: Geoff Gardner <geoff@dronesmith.io>
    Copyright 2016 Dronesmith Technologies
"""

__title__ = 'dronesmith'
__version__ = '1.0.01'
#__build__ = 0x000000
__author__ = 'Geoff Gardner'
#__license__ = ''
__copyright__ = 'Copyright 2016 Dronesmith Technologies'

import requests
import json
import math
import time

class APIError(Exception):
	def __init__(self, sstr):
		self.val = sstr

	def __str__(self):
		print ':', self.val

class Dronesmith(object):
    """docstring for Dronesmith."""
    def __init__(self, email, key):
        super(Dronesmith, self).__init__()
        self._link = Link(email, key)
        if self.__auth() is False:
            raise APIError("Error authenticating")

    def drone(self, name=""):
        return DroneNode(self._link, name)

    def drones(self):
        pass

    def changeName(self, name):
        pass
        # self._link.Request()

    def deleteDrone(self, name):
        pass

    def __auth(self):
        code, data = self._link.Request()
        return bool(code == 204)

class Link(object):
    """docstring for Link."""
    def __init__(self, email, key):
        super(Link, self).__init__()
        self._userEmail = email
        self._userKey = key
        self._API = 'api.dronesmith.io/api/'

    def __createHeader(self):
        return {
            'user-email': self._userEmail,
            'user-key': self._userKey,
            'Content-Type': 'application/json'
        }

    def __createUrl(self, sub=""):
        return 'http://' + self._API + sub

    def Request(self, method="GET", path="", body=None):
        url = self.__createUrl(path)
        print url
        if method == 'GET':
            response = requests.get(url, headers=self.__createHeader())
            try:
                jsonText = json.loads(response.text)
            except:
                return response.status_code, None
            else:
                return response.status_code, jsonText
        elif method == 'POST':
            compiled = {}

            if body != None:
                try:
                    compiled = json.dumps(body)
                except:
                    compiled = {}

            response = requests.post(url, data=compiled, headers=self.__createHeader())
            print response.text
            try:
                jsonText = json.loads(response.text)
            except:
                return response.status_code, None
            else:
                return response.status_code, jsonText
        else:
            return None


class DroneNode(object):
    """docstring for DroneNode."""
    def __init__(self, link, name=""):
        super(DroneNode, self).__init__()
        self._link = link
        self._name = name
        # self.missions = {}

        code, obj = self._link.Request('GET', self.__getDroneUrl())
        if code == 200:
            self.__updateMeta(obj)
        else:
            code, obj = self._link.Request('POST', self.__getDroneUrl())
            if code == 200:
                self.__updateMeta(obj)
            else:
                raise APIError("Could not create drone: " + str(code))

    #
    # Drone Object
    #
    def __updateMeta(self, droneObj):
        self.name = droneObj["name"]
        self.created = droneObj["created"]
        self.online = droneObj["online"]
        self.type = droneObj["type"]
        self.hardwareId = droneObj["firmwareId"]

    #
    # Telemetry calls
    #
    def position(self):
        obj = self.__telem('position')
        if obj != None:
            self._position = Position(obj)
        return self._position

    def attitude(self):
        obj = self.__telem('attitude')
        if obj != None:
            self._attitude = Attitude(obj)
        return self._attitude

    def takeoff(self, altitude=10):
        code, obj = self._link.Request('POST', self.__getDroneUrl('takeoff'), {
            "altitude": altitude
        })

        if code == 200 and obj["Command"] == 22 \
        and obj["StatusCode"] == 0:
            return True
        else:
            return False

    def goto(self, latitude, longitude, altitude=None):
        obj = {}
        obj["lat"] = latitude
        obj["lon"] = longitude
        if altitude != None:
            obj["altitude"] = altitude

        code, obj = self._link.Request('POST', self.__getDroneUrl('goto'), obj)
        if code == 200 and obj["Command"] == 192 \
        and obj["Status"] == "Command accepted.":
            return True
        else:
            return False

    def land(self):
        code, obj = self._link.Request('POST', self.__getDroneUrl('land'), {})
        if code == 200 and obj["Command"] == 21 \
        and obj["StatusCode"] == 0:
            return True
        else:
            return False

    def running(self):
        code, obj = self._link.Request('GET', self.__getDroneUrl('status'))
        if code != 200:
            return False
        else:
            if obj != None and \
            "Online" in obj:
                return bool(obj["Online"]) == True
            else:
                return False

    def info(self):
        code, obj = self._link.Request('GET', self.__getDroneUrl())
        if code == 200:
            self.__updateMeta(obj)
        return self

    def run(self):
        code, obj = self._link.Request('POST', self.__getDroneUrl('start'))
        if code == 200:
            attempts = 60
            while not self.Running():
                attempts -= 1
                if attempts <= 0:
                    return False
                time.sleep(1)
            return True
        else:
            return False

    def pause(self):
        code, obj = self._link.Request('POST', self.__getDroneUrl('stop'))
        if code == 200:
            return True
        else:
            return False

    def abort(self):
        code, obj = self._link.Request('POST', self.__getDroneUrl('mode'), {
            'mode': 'RTL'
        })

    def __telem(self, name):
        code, obj = self._link.Request('GET', self.__getDroneUrl(name))

        if code == 200:
            return obj
        else:
            return None

    def __getDroneUrl(self, endpoint=""):
        return 'drone/' + self._name + '/' + endpoint


class Position(object):
    """docstring for Position."""
    def __init__(self, obj):
        super(Position, self).__init__()
        self.x = obj['X']
        self.y = obj['Y']
        self.z = obj['Z']
        self.latitude = obj['Latitude']
        self.longitude = obj['Longitude']
        self.altitude = obj['Altitude']

class Attitude(object):
    """docstring for Attitude."""
    def __init__(self, obj):
        super(Attitude, self).__init__()
        self.roll = obj['Roll']
        self.pitch = obj['Pitch']
        self.yaw = obj['Yaw']
