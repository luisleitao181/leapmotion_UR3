################################################################################
# Script to detect and Classify Hand Gesture                                   #
# Disable the config "Orientacion automatica de rastreo"                       #
################################################################################

#import os, sys, inspect, thread, time,csv
import os, sys, inspect, time,csv, thread
global testName
testName = "L4New.csv"


arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
src_dir = os.getcwd()

sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, "../lib")))

import Leap

class SampleListener(Leap.Listener):
    global testName
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']

    def on_init(self, controller):
        print ("Initialized")
        controller.set_policy(controller.POLICY_ALLOW_PAUSE_RESUME)
        #print controller.is_paused() 
        aux =0
        while aux<5:
            #Loop to initialize Camera
            controller.set_paused(False)
            aux = aux +1
            print ("Try Connect to LeapMotion")

    def on_connect(self, controller):
        print ("Connected")
        #Disable "Orientacion automatica de rastreo"  
        controller.config.set("tracking_processing_auto_flip", False);
        #Enable the robust mode to improves the tracking and correct IR from environment.
        controller.config.set("robust_mode_enabled", True);
        controller.config.save()

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print ("Disconnected")
        #controller.set_paused(True)

    def on_exit(self, controller):
        print ("Exited")
        controller.set_paused(True)

    def on_frame(self, controller):
        global testName
        # Get the most recent frame and report some basic information
        frame = controller.frame()

        
        # Get Gestures
        for hand in frame.hands:           
            if hand.is_left and  hand.confidence == 1:
                print ("Frame id: %d, timestamp: %d, hands: %d, current fingers: %d") % (
                frame.id, frame.timestamp, len(frame.hands), len(frame.pointables.extended()))
                print ("Left hand palm position:  "), hand.palm_position, " Confidence: ", hand.confidence
                #print "qtd of fingers on left hand: ", frame.fingers.
                #print "hand direction:  " hand.direction
                data = [len(frame.pointables.extended()),'Left',hand.palm_position, hand.direction]
                with open(testName, 'ab') as f:
                    writer = csv.writer(f)
                    writer.writerow(data)
                f.close()
            elif hand.confidence == 1:
                print ("Frame id: %d, timestamp: %d, hands: %d, current fingers: %d") % (
                frame.id, frame.timestamp, len(frame.hands), len(frame.pointables.extended()))
                #print "Right hand palm position:", hand.palm_position, " Confidence: ", hand.confidence
                data = [len(frame.pointables.extended()),'Right',hand.palm_position, hand.direction]
                with open(testName, 'ab') as f:
                    writer = csv.writer(f)
                    writer.writerow(data)
                f.close()

        if not frame.hands.is_empty:
            print ("")
        input_file = open(testName,"r+")
        reader_file = csv.reader(input_file)
        value = len(list(reader_file))
        print (value)
        if value > 2000:
            print ("atingido as 2000 amostras, por favor, encerrar o cod pressionando enter")
            
            #delay to finish the experiment
            time.sleep(5)
            #sys.exit()
            #quit()

def main():
    global testName
    #delay to start the experiment
    time.sleep(5)

    with open(testName, 'wb') as f:
        writer = csv.writer(f)
        header = ['Gestures','Hand', 'HandPalmPosition','HandPalmOrientation']
        writer.writerow(header)

    controller = Leap.Controller() 
    # Create a sample listener and controller
    listener = SampleListener()
    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print ("Press Enter to quit...")
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        device=controller.devices[0]
        controller.set_paused(True)
        if device.is_valid:
            print ("Range: %f -- HorizontalAngle(X): %f --  VerticalAngle(Z): %f  ") %(device.range,device.horizontal_view_angle,device.vertical_view_angle)
        else:
            print (device.is_valid)
        
        controller.remove_listener(listener)


if __name__ == "__main__":
    main()

