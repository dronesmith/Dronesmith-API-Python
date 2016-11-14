import SocketServer
import SimpleHTTPServer
import json
import threading
import time

from dronesmith import *

USER_EMAIL = 'test@test.com'
USER_API_KEY = 'a1204f04-c2a9-477b-ae20-a8bba455da09'

PORT = 8080
SQUARE_SIZE = 10

# Authenticate with Dronesmith
dss = Dronesmith(USER_EMAIL, USER_API_KEY)

# Create or grab the drone node
mydrone = dss.drone('cranky_fermi')

print mydrone.info().online

# class CustomHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
#
#     def getLiveData(self):
#         global mydrone
#         pos = mydrone.Position()
#         return pos
#
#
#     def do_GET(self):
#         if self.path == '/gps':
#             self.send_response(200)
#             self.send_header('Content-type','text/json')
#             self.send_header("Access-Control-Allow-Origin", "*")
#             self.end_headers()
#
#             data = self.getLiveData()
#
#             r = {
#              'lat': data.latitude,
#              'lon': data.longitude,
#             #  'intensity': data['PAYLOAD']['rads']
#             }
#
#             self.wfile.write(json.dumps(r))
#             return
#         else:
#             SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
#
#
# def constrainSync(target, typeVal, threshold, timeout):
#     global mydrone
#     attempts = timeout
#     while True:
#         pos = mydrone.Position()
#         attempts -= 1
#         if typeVal == 'alt':
#             print abs(pos.altitude - target)
#             if abs(pos.altitude - target) < threshold:
#                 return True
#         elif typeVal == 'loc':
#             targetLat = target[0]
#             targetLon = target[1]
#             if abs(pos.latitude - targetLat) < threshold \
#             and abs(pos.longitude - targetLon) < threshold:
#                 return True
#         if attempts <= 0:
#             return False
#         time.sleep(1)
#
# def droneWorker():
#     global mydrone
#
#     targetSqr = SQUARE_SIZE / 1e4
#
#     # Start the node if not started.
#     if not mydrone.Running():
#         mydrone.Run()
#
#     if not mydrone.Takeoff():
#         mydrone.Abort()
#         return
#
#     if not constrainSync(10, 'alt', .5, 60):
#         print 'Could not takeoff'
#         return
#
#     # give some buffering time
#     time.sleep(5)
#
#     if not mydrone.Goto(targetSqr, 0.0):
#         mydrone.Abort()
#         return
#
#     startPos = mydrone.Position()
#     if not constrainSync((startPos.latitude + targetSqr, startPos.longitude), 'loc', .00005, 60):
#         print 'Could not goto'
#         return
#
#     # give some buffering time
#     time.sleep(5)
#
#     if not mydrone.Goto(0.0000, targetSqr):
#         mydrone.Abort()
#         return
#
#     startPos = mydrone.Position()
#     if not constrainSync((startPos.latitude, startPos.longitude + targetSqr), 'loc', .00005, 60):
#         print 'Could not goto'
#         return
#
#     # give some buffering time
#     time.sleep(5)
#
#     if not mydrone.Goto(-targetSqr, 0):
#         mydrone.Abort()
#         return
#
#     startPos = mydrone.Position()
#     if not constrainSync((startPos.latitude - targetSqr, startPos.longitude), 'loc', .00005, 60):
#         print 'Could not goto'
#         return
#
#     # give some buffering time
#     time.sleep(5)
#
#     if not mydrone.Goto(0, -targetSqr):
#         mydrone.Abort()
#         return
#
#     startPos = mydrone.Position()
#     if not constrainSync((startPos.latitude, startPos.longitude - targetSqr), 'loc', .00005, 60):
#         print 'Could not goto'
#         return
#
#     mydrone.Land()
#
# worker = threading.Thread(target=droneWorker)
# worker.start()
#
# httpd = SocketServer.ThreadingTCPServer(('localhost', PORT), CustomHandler)
#
# print 'Listening on', PORT
# httpd.serve_forever()
