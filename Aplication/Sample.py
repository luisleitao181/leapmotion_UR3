################################################################################
# Copyright (C) 2012-2016 Leap Motion, Inc. All rights reserved.               #
# Leap Motion proprietary and confidential. Not for distribution.              #
# Use subject to the terms of the Leap Motion SDK Agreement available at       #
# https://developer.leapmotion.com/sdk_agreement, or another agreement         #
# between Leap Motion and you, your company or other organization.             #
################################################################################

import os, sys, inspect, time, thread

arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
src_dir = os.getcwd()

sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, "../lib")))

import Leap

class SampleListener(Leap.Listener):

    def on_connect(self, controller):
        print ("Connected")


    def on_frame(self, controller):

        frame = controller.frame()

        #print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d" % (
        #      frame.id, frame.timestamp, len(frame.hands), len(frame.fingers))
        ibox = frame.interaction_box

        front_finger = frame.fingers.frontmost
        normalized_position = ibox.normalize_point( front_finger.tip_position)

        x = 500  * normalized_position.x
        y = 500 * (1 - normalized_position.y)
        draw_pointer(x,y)

def main():

    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)
    print ("Press Enter to quit...")
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
