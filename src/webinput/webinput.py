#!/usr/bin/env python

# WS server that sends messages at random intervals

import asyncio
import websockets

import math
import time
import json
import pyserial


def server(freq: float):
    """Returns a websocket handler.

    Input: freq
    Output: websocket handler
    """

    async def handler(websocket, path):
        while True:
            x = math.sin(time.time())
            package = dict(I=dict(x=x))

            await websocket.send(json.dumps(package))
            await asyncio.sleep(1./freq)
    return handler

if __name__=='__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--freq', default=60, type=float)
    args = parser.parse_args()

    start_server = websockets.serve(server(args.freq), "localhost", 8765)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
