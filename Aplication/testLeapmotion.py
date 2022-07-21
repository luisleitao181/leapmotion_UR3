from cmath import sqrt
import win_inet_pton
from pyModbusTCP.client import ModbusClient
import os, sys, inspect, time, thread, math

arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
src_dir = os.getcwd()

sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, "../lib")))

import Leap

import socket


HOST = "10.20.38.10"
ModBus = ModbusClient(host=HOST, port=502, auto_open=True)
PORT_SPEED = 30002
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT_SPEED))


class timeout:
    acttime=0

class state:
    state="IDLE"

class handf:
    maoref=[0,0,0]
    maodif=[0,0,0]
    rref=[9,328,172]
    rnp=[0,0,0]
    grip=0
    rpos=[0,0,0]
def twos_comp(val, bits):
    """compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val                         # return positive value as is

class SampleListener(Leap.Listener):
    
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']

    def on_init(self, controller):
        print ("Initialized")
        controller.set_policy(controller.POLICY_ALLOW_PAUSE_RESUME)
        aux =0
        while aux<2:
            #Loop to initialize Camera
            time.sleep(1)
            print ("Try Connect to LeapMotion")
            aux+=1

    def on_connect(self, controller):
        print ("Connected")
        #Disable "Orientacion automatica de rastreo"  
        controller.config.set("tracking_processing_auto_flip", False)
        #Enable the robust mode to improves the tracking and correct IR from environment.
        controller.config.set("robust_mode_enabled", True)
        controller.config.save()

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print ("Disconnected")
        #controller.set_paused(True)

    def on_exit(self, controller):
        print ("Exited")
        controller.set_paused(True)
    
    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()   
        # HANDS
        '''hands=frame.hands
        for hand in hands:           
            if hand.is_left and  hand.confidence == 1:
                print ("Frame id: %d, timestamp: %d, hands: %d, current fingers: %d") % ( frame.id, frame.timestamp, len(frame.hands), len(frame.pointables.extended()))
                print ("Left hand palm position: ")
                print(hand.palm_position)
                print("Confidence: %d")%(hand.confidence)
                #print "qtd of fingers on left hand: ", frame.fingers.) %(hand.palm_position, hand.confidence)
                #print "qtd of fingers on left hand: ", frame.fingers.
                #print "hand direction:  " hand.direction
            elif hand.confidence == 1:
                print ("Frame id: %d, timestamp: %d, hands: %d, current fingers: %d") % (frame.id, frame.timestamp, len(frame.hands), len(frame.pointables.extended()))
                print ("Left hand palm position: ")
                print(hand.palm_position)
                print("Confidence: %d")%(hand.confidence)
        if frame.hands.is_empty:
            time.sleep(2)
            print ("\n")'''

        #FINGERCOUNT(ACTIONS)

        #ModBus.write_single_register(129, 0)
        
        hands=frame.hands
        holdings=[0]
        if(hands[0].palm_position[1]<=700 and len(hands)>0):
            st=state
            count=0
            anfing=0
            for i in range(0,9999):
                if(hands[0].confidence==1):
                    anfing+=len(frame.pointables.extended())
                    count += 1
            if(count!=0):anfing/=count
            if(anfing==1 and st.state=="IDLE" and ModBus.read_holding_registers(129, 1)==holdings and 400<hands[0].palm_position[1]):
                print("Action 1")
                st.state="CONFIRMATION_1"
                timeout.acttime=time.time()
            elif(anfing==2 and st.state=="IDLE" and ModBus.read_holding_registers(129, 1)==holdings and 400<hands[0].palm_position[1]):
                print("Action 2")
                st.state="CONFIRMATION_2"
                timeout.acttime=time.time()
            '''elif(anfing==3 and st.state=="IDLE"):
                print("Action 3")
                st.state="CONFIRMATION_3"
                timeout.acttime=time.time()'''
            if(anfing==4 and st.state=="IDLE" and ModBus.read_holding_registers(129, 1)!=holdings and 400<hands[0].palm_position[1]):
                print("Action 4")
                st.state="CONFIRMATION_4"  
                timeout.acttime=time.time()
            if((anfing==0 or 5 or 4) and st.state=="IDLE"):
                print("\n")

            time.sleep(0.1)
            if(anfing==0 and st.state=="CONFIRMATION_1"):
                print("Action 1 confirmed")
                st.state="IDLE"
                ModBus.write_single_register(129, 1)
            elif(anfing==0 and st.state=="CONFIRMATION_2"):
                print("Action 2 confirmed")
                st.state="IDLE"
                handf.maoref=hands[0].palm_position
                s.send("wait:1"+"\n")
                ModBus.write_single_register(129, 2)
            elif(anfing==0 and st.state=="CONFIRMATION_3"):
                print("Action 3 confirmed")
                st.state="IDLE"
                ModBus.write_single_register(129, 3)
            elif(anfing==5 and st.state!="IDLE"):
                print("Action cancelled")
                st.state="IDLE"
            if(anfing==0 and st.state=="CONFIRMATION_4" and ModBus.read_holding_registers(129, 1)==[1]):
                print("returning to idle position")
                st.state="IDLE"
                time.sleep(0.05)
                s.send(("movep(j[0.212,-0.025,0.123,2.152,-2.288,0], a=0.01, v=0.035, r=0)"+"\n"))
                ModBus.write_single_register(129, 0)
            if(anfing==0 and st.state=="CONFIRMATION_4" and ModBus.read_holding_registers(129, 1)==[2]):
                print("returning to idle position")
                st.state="IDLE"
                ModBus.write_single_register(129, 0)
            
            if(st.state!="IDLE" and time.time()-timeout.acttime>3.00):
                print("confirmation cancelled")
                time.sleep(3)
                st.state="IDLE"

            maoat=[0,0,0]
            i=0
            apos=[0,0,0]
            for i in range(0,9999):
                if(hands[0].confidence==1):
                    apos[0]+=hands[0].palm_position[0]
                    apos[1]+=hands[0].palm_position[1]
                    apos[2]+=hands[0].palm_position[2]
                    i += 1
            if(i!=0):
                apos[0]/=i
                apos[1]/=i
                apos[2]/=i
            handf.maoat=apos

            if(ModBus.read_holding_registers(129, 1)==[2]):     
                handf.maodif[0]=-handf.maoref[0]+handf.maoat[0]
                handf.maodif[1]=-handf.maoref[1]+handf.maoat[1]#diferenca da mao
                handf.maodif[2]=-handf.maoref[2]+handf.maoat[2]
                handf.rnp[0]=handf.rref[0]+handf.maodif[2]
                handf.rnp[1]=handf.rref[1]+handf.maodif[0]
                handf.rnp[2]=handf.rref[2]+handf.maodif[1]           
                if(-226<handf.rnp[0]<300 and 0<handf.rnp[1]<450 and -47<handf.rnp[2]<330):
                    s.send(("movep(p["+str((handf.rnp[0])/1000)+","+str((handf.rnp[1])/1000)+","+str((handf.rnp[2])/1000)+",3.1416,0,0], a=0.01, v=0.035, r=0)"+"\n")) #pickandplacespeed recomended=0.035   /fun =0.5 
                
                if(anfing==1 and handf.grip==0):
                    handf.grip=1
                    #time.sleep(0.1)
                    s.send("set_digital_out(0,True)"+"\n")
                    print("iman ON")
                elif(anfing==2 and handf.grip==1):                    #parte do griper(ligar e desligar)
                    handf.grip=0
                    #time.sleep(0.1)
                    s.send("set_digital_out(0,False)"+"\n")
                    print("iman OFF")
            rposx = ModBus.read_input_registers(400) #pose x in base frame
            rposy = ModBus.read_input_registers(401) #pose y in base frame
            rposz = ModBus.read_input_registers(402) #pose z in base frame
            if( rposx is not None):
                X = twos_comp(rposx[0],16)/10.0
            if( rposy is not None):
                Y = twos_comp(rposy[0],16)/10.0
            if( rposz is not None):
                Z = twos_comp(rposz[0],16)/10.0
            dist=math.sqrt((X-(hands[0].palm_position[2]+160))**2+(Y-(hands[0].palm_position[0]-370))**2+(Z-hands[0].palm_position[1]-198)**2)
            #print("rX:",X,"   hX",  (hands[0].palm_position[2])+160)
            #print("rY:",Y,"   hY",  (hands[0].palm_position[0])-370)
            #print("rZ:",Z,"   hZ",  (hands[0].palm_position[1])-190)
            #print("distancia: ", dist)
            if(0<dist<1000):
                vel=0.00125*dist
                #vel=0.35*math.log(-300+dist,1)
                s.send("set speed "+str(vel)+"\n")
            else:
                s.send("set speed 1"+"\n")
        else:
            s.send("set speed 1"+"\n")
                
                
                


#s.close()


def main():
   
    time.sleep(5)
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
        '''if device.is_valid:
            print ("Range: %f -- HorizontalAngle(X): %f --  VerticalAngle(Z): %f ") %(device.range,device.horizontal_view_angle,device.vertical_view_angle)
        else:
            print (device.is_valid)'''
        
        controller.remove_listener(listener)


if __name__ == "__main__":
    main()