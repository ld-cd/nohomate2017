#!/usr/bin/python3
import websocket
import json

ws = websocket.WebSocket()
ws.connect("ws://10.0.0.15:8000")

while True:
    command = raw_input("enter command>> ")
    args = command.split()

    if args[0] == "set":
        ws.send("{ \"op\" : \"" + args[0] + "\", \"arg1\" : \"" + args[1] + "\", \"arg2\" : \"" + args[2] + "\"}")
        print("{ 'op' : '" + args[0] + "', 'arg1' : '" + args[1] + "', 'arg2' : '" + args[2] + "'}")
    else:
        ws.send("{ \"op\" : \"" + args[0] + "\", \"arg1\" : \"" + args[1] + "\"}")
        print("{ 'op' : '" + args[0] + "', 'arg1' : '" + args[1] + "'}")
