import numpy as np
import sys
from matplotlib import pyplot as plt

#make CNC draw rays out from your eyes
#Cayden

def writePath(path, f, color):
    cmd = "M3 S{}".format(color) #colour setter
    f.write(cmd + "\n") #turn on/off light
    
    for point in path:
        cmd = "G1 X{} Y{}\n\n\n".format(point[0], point[1])
        f.write(cmd + "\n")

def writeHeader(f):
    f.write("g55					(use g54 offset ref) \n" +
    "g20 \n" + 
    "g64 p0.0005				(set motion for 1/2 thou accuracy) \n" +
    "                                (fake spindle set, and spindle on) \n" +
    "g10 l2 p1 x0y0z0  			(set g54 offset home) \n" +
    "g1 f200 \n" +
    "g54 \n" +
    "g17	(sets XY curve plane) \n")

def plotRays(points):
    #grab x and y vals in one list to visualize our path
    x = list()
    y= list()
    for item in points[:][:]:
        for val in item[:,0]:
            x.append(val)
    for item in points[:][:]:
        for val in item[:,1]:
            y.append(val)
            
    #plot it    
    plt.plot(x,y)
    plt.show()

def getStop(p1, p2): #we wanted to change things to the eye starts at some negative x value. Since the plotter can't go -x, here is a function to calcuate the y position is should stop at when traversing the ray from eye to merchandise. All that to say, this return y-intercept
    x1, y1 = p1
    x2, y2 = p2
    a = (y2 - y1) / (x2 - x1)
    b = y1 - a * x1
    return b
        
#NOTE commented out all of the linspace command because we realized that putting in M call during a ray would slow down the machine. This is kept in here because if can get around that issue, we can use the np.linspace command to break ray down into arbitrary number of steps, so we control colour down the length of the array... Cayden

def main(cncHeight, cncWidth, numRays, raySteps, merchSteps, eyeDist, fileName="test.ngc", interestFile="test.npy"):
    #positions are [x, y]
    eyePos = [0, 0] #start at home
    merchPos = [cncWidth, 0]

    #holds our entire path:
    points = list()

    #file to save values
    gcodeFile = open("./output/{}".format(fileName), "w")
    writeHeader(gcodeFile)

    #array holding merchandise interest values
    interest = np.load(interestFile) #load in just red values, which represent interest
    interest = np.mean(interest.reshape(-1, (len(interest)//numRays)), axis=1) #shrink list down to number of ray values
    scaler = 255 / np.amax(interest)
    for i, item in enumerate(interest):
        interest[i] = scaler * item

    #home the cnc here?

    for i in range(numRays):
        oldMerchPos = np.copy(merchPos)
        merchPos[1] = (cncHeight / numRays) * i #set new y pos
        eyePos = [0, getStop([eyeDist, cncHeight/2],merchPos)] #this gets us the new x position to make it look like rays are originating from eye
        if (i % 2 == 0):
            start = eyePos
            end = merchPos
            writePath([eyePos], gcodeFile, 0)
        else:
            start = merchPos
            end = eyePos
            #turn off LED and move cnc to this merchPos BEFORE moving back to eyePos/start
            #path = np.linspace(oldMerchPos, merchPos, num=merchSteps)
            #writePath(path, gcodeFile, 0)
            writePath([merchPos], gcodeFile, 0)
            #points.append(path)
        
        #create series of steps for gcode to follow through (must seperate ray into any steps so we can interleave M calls for LED)
        #path = np.linspace(start, end, num=raySteps)
        #writePath(path, gcodeFile, interest[i])
        writePath([end], gcodeFile, interest[len(interest)-1-i])
        #points.append(path)
    gcodeFile.write("M2") #end gcode file
    gcodeFile.close()
       
if __name__ == "__main__":
    #configs/settings in inches for our CNC in dark rooom
    cncHeight = 19
    cncWidth = 22.5
    eyeDist = -4.25 #displacement of eye along x axis of plotter
    numRays = 100
    raySteps = 1
    merchSteps = 1
    
    main(cncHeight, cncWidth, numRays, raySteps, merchSteps, eyeDist)
