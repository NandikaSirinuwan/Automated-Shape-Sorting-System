# Automated-Shape-Sorting-System
Automated Shape Sorting System based on image processing and Arduino controlling

<b>Introduction</b>

In briefly, this system can identify any polygons. It uses a computer vision system for that purpose. This identification is done while moving the polygon on the conveyor. Lot of industrial systems is used conveyor for moving their raw materials or productivity. So, this system can be used in many places in industrial environment.
This computer vision software can be configured for identify a special polygon. So, this system can be used to sort each polygon shapes separately. 

<b>Basic Function of the System</b>

While moving a polygon on the conveyor camera gets the real time images and process it using computer vision software. To get a clear and stable images, conveyor need to stop under the camera. This is done by using laser beam. If laser beam is cut, external Arduino is identify it as object is present at the under of the camera. Arduino sends a signal to computer vision software over serial communication between Arduino and PC that run the computer vision software. Computer vision program identify the polygon and it sends a commant to Arduino to perform sorting system.
Sorting system has rotatable plate. After Arduino sends the appropriate command to the sorting system, sorting plate is rotated and placed in front of the conveyor by a stepper motor to the exact place of pre-defined relevant polygon.

<b>Video</b>

https://youtu.be/F_4-iwNcRfU
