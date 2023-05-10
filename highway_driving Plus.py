"""Sample Webots controller for highway driving benchmark."""

from vehicle import Driver

# name of the available distance sensors
sensorsNames = [
    'front',
    'front right 0',
    'front right 1',
    'front right 2',
    'front left 0',
    'front left 1',
    'front left 2',
    'rear',
    'rear left',
    'rear right',
    'right',
    'left']
sensors = {}

max_speed = 100
driver = Driver()
driver.setSteeringAngle(0.0)  # go straight



# get and enable the distance sensors
for name in sensorsNames:
    sensors[name] = driver.getDistanceSensor('distance sensor ' + name)
    sensors[name].enable(10)

# get and enable the GPS
gps = driver.getGPS('gps')
gps.enable(10)

# get the camera
camera = driver.getCamera('camera')
# uncomment those lines to enable the camera
camera.enable(50)
camera.recognitionEnable(50)
destination =0
prevpos = -2
counter=0
rightb=5.8
leftb =2
average = 0
destination = 2
changelane=0
minx=1000
miny=1000
next_car = 0
destinationy = 800
lim = 7250
lim2 = 7550
lim3 = 7890
lim4 = 7980
lim5 = 8161
lim6 = 8350
lim7 = 8518
lim8 = 8800
while driver.step() != -1:
    # adjust the speed according to the value returned by the front distance sensor
    print(counter)
    x=gps.getValues()
    counter += 1
    if((counter > 7045)):#and(counter<8200)):
        
        front_distance = sensors['front'].getValue() 
        extent = sensors['front'].getMaxValue()
        speed = max_speed * front_distance / extent
        driver.setCruisingSpeed(speed)
        chnage_in_speed = driver.getCurrentSpeed() - speed
        max_speed= 200
        pos = x[0]
        if(counter < lim):
            driver.setSteeringAngle(  (1.2)*0.01) 
            #max_speed= 100
        if(counter >= lim):
            
            driver.setSteeringAngle(  (-0.9)*0.01) 
            max_speed= 120
            #max_speed= 50
            #if(counter > 7990):
            #    driver.setSteeringAngle(  (-1)*0.01)   
            #    max_speed = 120
        if(counter >= lim2):          
            driver.setSteeringAngle(  (-1.4)*0.01) 
            max_speed= 100
            #max_speed= 50
            
        if(counter >= lim3):   
            max_speed= 80       
            driver.setSteeringAngle(  (-3)*0.01) 
        prevpos = pos
        if(counter >= lim4):
           driver.setSteeringAngle(  (2.6)*0.01) 
        if(counter >= lim5):
           max_speed= 100
           driver.setSteeringAngle(  (-0.8)*0.01) 
        if(counter >= lim6):
           max_speed= 90
           driver.setSteeringAngle(  (-0.89)*0.01)
          
        if(counter >= lim7):
           max_speed= 90
           driver.setSteeringAngle(  (3.35)*0.01)
        if(counter >= lim8):
           max_speed= 90
           driver.setSteeringAngle(  (-1.5)*0.01)
        if ((chnage_in_speed > 0)):
            driver.setBrakeIntensity(0.5)
        else:
            driver.setBrakeIntensity(0)
        
    elif((counter>6700)):
        
        if(counter > 8200):
            max_speed = 50
        
        if(counter == 4800):
            max_speed= 200
        front_distance = min(sensors['front'].getValue() ,sensors['front left 0'].getValue() , sensors['front right 0'].getValue() )
        extent = sensors['front'].getMaxValue()
        speed = max_speed * front_distance / extent
        driver.setCruisingSpeed(speed)
        # brake if we need to reduce the speed
        chnage_in_speed = driver.getCurrentSpeed() - speed
        
        max_speed = 100
        pos = -x[0] 
        objects=camera.getRecognitionObjects()
        if(next_car == 0):
            #print("Normal Mode Following")
            for obj in objects:
                if(obj.get_id()>2000):
                    obj_pos=obj.get_position()
                    destination = obj_pos[0] 
                    if((abs(destination)<0.5)):
                        break
                      
            driver.setSteeringAngle(1*(prevpos - pos)*0.02 + (destination)*0.02)
        else:
            for obj in objects:
                if(obj.get_id()==id):
                    #print(obj.get_id())
                    obj_pos=obj.get_position()
                    destination = obj_pos[0] 
                    destinationy =obj_pos[2]  
                    break
            driver.setSteeringAngle(10*(prevpos - pos)*0.04 + (destination/10)*0.04)    
            #print(destination)          
        if ((chnage_in_speed > 0)):
            driver.setBrakeIntensity(1)
        if ((chnage_in_speed > 0)and(next_car == 0)):
            driver.setBrakeIntensity(1) 
            if((abs(destination)<0.1)):
                if (sensors['left'].getValue()>3)and(sensors['front left 2'].getValue()>8):
                    for obj in objects:
                        if(obj.get_id()>2000):
                            obj_pos=obj.get_position()
                            destinationx = obj_pos[0]
                            if destinationx>0:
                                continue 
                            destinationy = abs(obj_pos[2])
                            if((destinationy < miny)and(abs(destinationx) > 0.5)and(abs(destinationx) < 9)):
                                miny = destinationy
                                destination = destinationx
                                next_car = -1
                                id=obj.get_id()
                                #print("New car found:at x_axis: %f, y_axis: %f",destinationx,destinationy)
                elif((sensors['right'].getValue()>3)and(sensors['front right 2'].getValue()>8)and(not(sensors['right'].getValue()<7))): #you can turn right
                    for obj in objects:
                        if(obj.get_id()>2000):
                            obj_pos=obj.get_position()
                            destinationx = obj_pos[0]
                            if destinationx<0:
                                continue 
                            destinationy = abs(obj_pos[2])
                            if((destinationy < miny)and(abs(destinationx) > 0.5)and(abs(destinationx) < 9)):
                                miny = destinationy
                                destination = destinationx 
                                next_car = 1 
                                id=obj.get_id()
                                #print(id) 
                                #print("New car found:at x_axis: %f, y_axis: %f",destinationx,destinationy)     
        else:
            driver.setBrakeIntensity(0)     
        if(abs(destinationy) < 13):
            next_car = 0
            miny = 1000
        #prevpos = destination
        prevpos = -x[0]    
    else:
        front_distance = sensors['front'].getValue() 
        extent = sensors['front'].getMaxValue()
        speed = max_speed * front_distance / extent
        driver.setCruisingSpeed(speed)
        chnage_in_speed = driver.getCurrentSpeed() - speed
        if(counter > 6040): 
            destination = 1
        if(destination == 2):#1.3
            #if(x[0]<1.3): #then turn left
            driver.setSteeringAngle(60*(x[0] - prevpos)*0.05 + (x[0]-1.3)*0.04) #TUNNING!!
            #if(x[0]>1.3): #then turn right
            #    driver.setSteeringAngle(1*0.1)
    
            #continue
        if(destination == 1):# 5.2
           #if(x[0]<1.3): #then turn left
           driver.setSteeringAngle(60*(x[0] - prevpos)*0.05 + (x[0]-5.2)*0.04)
           #if(x[0]>1.3): #then turn right
           #    driver.setSteeringAngle(1*0.1)
     
           #continue   
        if(destination == 3):# -2
           #if(x[0]<1.3): #then turn left
           driver.setSteeringAngle(60*(x[0] - prevpos)*0.05 + (x[0]+2)*0.04)
           #if(x[0]>1.3): #then turn right
           #    driver.setSteeringAngle(1*0.1)
           prevpos = x[0]
           #continue    
        prevpos = x[0] 
        counter=counter +1
        if ((chnage_in_speed > 0)):
            #print(counter)
            if((sensors['right'].getValue()>3)and(sensors['front right 2'].getValue()>8)and(not(sensors['right'].getValue()<7))): #you can turn right
                 #print("trying right")
                 if((x[0]<5.25)and(x[0]>5.15)): #means you are left, go middle
                     destination = 2 #middle
                 if((x[0]<1.5)and(x[0]>1)):  #1.3, you are middle,go right
                     destination = 3 #right
            elif((sensors['left'].getValue()>3)and(sensors['front left 2'].getValue()>8)and(sensors['front left 1'].getValue()>14)): #You can steer left  
                #driver.setSteeringAngle(-chnage_in_speed*0.1)
                #print("trying left")
                if((x[0]<-1.5)and(x[0]>-2.5)): #-2, you are in the right row, go left
                    destination = 2 #middle
                if((x[0]<1.5)and(x[0]>1)):  #1.3, you are middle,go left
                    destination = 1 #left
            else:    
                driver.setBrakeIntensity(1)
        else:
            driver.setBrakeIntensity(0)
            max_speed = 120    