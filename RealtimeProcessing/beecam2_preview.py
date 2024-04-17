#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  9 10:24:01 2023

@author: master
"""

import io
import os
import picamera2 as pc2
from libcamera import controls
import cv2
import numpy as np
from apriltag import apriltag
import time
import threading
from gpiozero import CPUTemperature

width = 800
height = 320
fps = 24
camera_height_inches = 1.5

#function to put apriltag detection into string
def getDataString(detection):
    corners = detection["lb-rb-rt-lt"]
    ID = str(detection['id'])
    center = detection['center']
    x = int(center[0])
    y = int(center[1])
    
    lb = corners[0]
    rb = corners[1]
    rt = corners[2]
    lt = corners[3]
    
    #calculate angle of tag
    A = rt[0] - rb[0]
    B = rb[1] - rt[1]
    C = np.rad2deg(np.arccos(A/(np.sqrt(A**2+B**2))))
    
    if (lb[0] < rb[0]):
        theta = C
    else:
        theta = 360 - C
    cpu = CPUTemperature()
    temp = str(cpu.temperature)
    Time = time.ctime()
    data = [Time, ' ID: ', ID, " Center: ", str(center), " Angle: ", str(theta), "CPU Temp: ", str(temp) ]
    return data

#function to visualize apriltag detection
def outlineDetection(detection, image):
    corners = detection['lb-rb-rt-lt']
    lb = (int(corners[0,0]), int(corners[0,1]))
    rb = (int(corners[1,0]), int(corners[1,1]))
    rt = (int(corners[2,0]), int(corners[2,1]))
    lt = (int(corners[3,0]), int(corners[3,1]))
    
    pts = np.array(corners, np.int32)
    pts = pts.reshape((-1,1,2))
    
    ID = str(detection['id'])
    center = detection['center']
    center_coords = (int(center[0]), int(center[1]))
    text_coords = (int(center[0]-5*len(ID)), int(center[1]-5))
    front_coords = (int((rt[0]+lt[0])/2), int((rt[1]+lt[1])/2))

    
    color = (0,0,255)
    color2 = (0,255,0)
    color3 = (255,100,0)
    font = cv2.FONT_HERSHEY_PLAIN
    fontscale = 0.75
    isClosed = True
    
    cpu = CPUTemperature()
    temp = str(cpu.temperature)
        
    image = cv2.polylines(image, [pts], isClosed, color3, thickness=2)
    image = cv2.line(image, center_coords, front_coords , color2, thickness=1)
    image = cv2.putText(image, ID, text_coords, font, fontscale, color, thickness=1)   
    return image

class ApriltagDetector(threading.Thread):
    def __init__(self, owner, detector):
        super(ApriltagDetector, self).__init__()
        self.stream = io.BytesIO()
        self.event = threading.Event()
        self.terminated = False
        self.owner = owner
        self.detector = detector
        self.daemon = True
        self.start()
        
    def run(self):
        while not self.terminated:
            if self.event.wait(1):
                #print(self.getName(), str('starting'))
                #self.start = time.time()
                try:
                    self.stream.seek(0)
                    self.capture = self.stream.read()
                    self.byte_array = np.array(bytearray(self.capture), dtype='uint8')
                    self.frame = self.byte_array.reshape((height, width, 3)) #cv2 compatible image
                    self.image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
                    
                    #dilation to emphasize white pixels
                    self.B = np.ones((2,2), np.uint8)
                    self.image = cv2.dilate(self.image, self.B, iterations=1)
                
                    
                    try:
                        self.detections = self.detector.detect(self.image)
                        self.detection_number = len(self.detections)
                    except RuntimeError:
                        self.detection_number = 0
                    finally:
                        self.cpu = CPUTemperature()
                        self.temp = "CPU Temp: " + str(self.cpu.temperature) + " deg C"
                        self.frame = cv2.putText(self.frame, self.temp,
                                                 (10,30), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,255),thickness=1)
                        self.frame = cv2.putText(self.frame, time.strftime("%Y-%m-%d %H:%M:%S"),
                                                 (10,10), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,255), thickness=1)
                        if self.detection_number > 0:
                            #detections are outlined in preview frame
                            for detection in self.detections:
                                self.frame = outlineDetection(detection, self.frame)
                                self.data = getDataString(detection)
                                #write data to .txt file
                                with self.owner.lock:
                                    self.data_path = '/home/master/Documents/Data/%s_data.txt'%str(os.uname()[1])
                                    with open(self.data_path, 'a') as t:
                                        t.writelines(self.data)
                                        t.write('\n')
                        #display preview frame
                        with self.owner.lock:
                            if not self.owner.done:
                                cv2.imshow("Preview", self.frame)
                                if cv2.waitKey(int(1/fps*1000)) == 27:
                                    self.owner.done = True
                             
                #close and add thread back to main pool
                finally:
                    self.stream.seek(0)
                    self.stream.truncate()
                    self.event.clear()
                    with self.owner.lock:
                        ##print(self.getName(), 'ending after ' + str(round(time.time()-self.start, 2)) + 's')
                        self.owner.pool.append(self)
  
                        

#This object receives frames from the camera and distributes them to detection threads
class ProcessOutput(object):
    def __init__(self, detector):
        self.done = False
        #Construct a pool of image processors with lock
        self.lock = threading.Lock()
        self.pool = [ApriltagDetector(self,detector) for i in range(4)]
        self.processor = None
        
    def write(self, buf):
        #When a frame is written to this output, pull a thread from the pool
        # and write the frame to its stream. Then, start this thread when the
        # write function is called again.
        if self.processor:
            self.processor.event.set()
        with self.lock:
            if self.pool:
                self.processor = self.pool.pop()
            else:
                #No processors available
                self.processor = None
                    
        if self.processor:
            self.processor.stream.write(buf)
            
    def close(self):
        #close all threads
        while True:
            with self.lock:
                #append idle thread to pool
                if self.processor:
                    self.pool.append(self.processor)
                    self.processor = None
                #close all threads in pool
                try:
                    proc = self.pool.pop()
                except IndexError:
                    #pool is empty
                    break
                else:
                    print('closing ' + proc.getName())
                    proc.terminated = True
                    proc.join()


#create apriltag detector
detector = apriltag("tagCircle44h12", 
                    threads=2,
                    ) 
output = ProcessOutput(detector)

def PullFrame(request):
    with pc2.MappedArray(request, 'main') as m:
        copy = np.array(m.array)
        output.write(copy)        

try:            
    with pc2.Picamera2() as camera:
        
        modes = camera.sensor_modes
        mode = modes[0]
        config = camera.create_preview_configuration(main={"size": (width, height), "format": "RGB888"},
                                                     #lores={"size": (800,320)},
                                                     #display = "lores"
                                                     buffer_count=2,
                                                     #queue=False,
                                                     #sensor={'output_size': mode['size'], 'bit_depth':mode['bit_depth']},
                                                     #raw={'format': 'SRGGB10', 'size': (2304,1296)}
                                                     )

        camera.configure(config)
        
        #Optional: horizontally crop the frame
        h = 0 #horizontal crop in pixels
        crop = camera.camera_controls['ScalerCrop'] #(768, 432, 3072, 1728) is the sensor limit
        crop_ar = crop[2]
        manual_crop = (crop_ar[0]+h, crop_ar[1], crop_ar[2]-h, crop_ar[3])
        
        camera.set_controls({#'AeEnable': False,
                             'ExposureTime': 1000, 
                             #'AnalogueGain': 1.0,
                             'FrameRate': fps,
                             'AfMode': controls.AfModeEnum.Manual,
                             'LensPosition': (39.37/camera_height_inches),
                             'ScalerCrop': manual_crop,
                             })
        
        
        camera.pre_callback = PullFrame
        camera.start(show_preview=False)
        
        #wait for white balance and analogue gain to be set
        time.sleep(2)
        
        #fix analogue gain and white balance
        metadata = camera.capture_metadata()
        controls = {c: metadata[c] for c in ["AnalogueGain","ColourGains"]}
        print(controls)
        camera.set_controls(controls)
                
        while not output.done:
            time.sleep(1)
            
finally:
    time.sleep(1)
    output.close()
    cv2.destroyAllWindows()
    camera.close()
