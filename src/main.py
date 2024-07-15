#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  main.py
#  
#  Copyright 2024  <neilxu@raspberrypi2>

import sys
import signal
from FaceTracker.src.state.facetracker import FaceTracker

face_tracker = FaceTracker()

def cleanup_handler(sig, frame):
    face_tracker.cleanup()
    sys.exit(0)

signal.signal(signal.SIGINT, cleanup_handler)

def main(args):

    # while True:
    for i in range(10):
        face_tracker.execute()

if __name__ == '__main__':
    sys.exit(main(sys.argv))
