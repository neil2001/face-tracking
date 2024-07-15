#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  main.py
#  
#  Copyright 2024  <neilxu@raspberrypi2>

import sys
from tracker_context import FaceTracker

def main(args):

    face_tracker = FaceTracker()

    # while True:
    for i in range(10):
        face_tracker.execute()
    return

if __name__ == '__main__':
    sys.exit(main(sys.argv))
