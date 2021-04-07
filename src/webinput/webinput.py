#!/usr/bin/env python
import asyncio
import websockets
import sys

import math
import time
import json
import serial

def server(freq: float, device):
    """Returns a websocket handler.

    Input: freq
    Output: websocket handler
    """

    async def handler(websocket, path):
        while True:
            if device is not None:
                x = device.grabData()[1]
            else:
                x = time.time() % 100 - 50
            package = dict(I=dict(x=x))

            await websocket.send(json.dumps(package))
            await asyncio.sleep(1./freq)
    return handler

def setup(port):
    from slider import sliderUSB as slider
    try:
        device = slider(port=port)
    except:
        print('No device detected at port: {}'.format(port))
        sys.exit(0)

    device.startArduino()

    return device


if __name__=='__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=None, type=str)
    parser.add_argument('--freq', default=60, type=float)
    args = parser.parse_args()

    device = None
    if args.port is not None:
        device = setup(args.port)

    start_server = websockets.serve(server(args.freq, device), "localhost", 8765)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

