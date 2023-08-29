Urban-Cyber Physical System

**Introduction:**
BeamNG.tech is a simulation platform for the development of autonomous driving systems and driver’s training applications. BeamNG.tech expands the capabilities of BeamNG.drive by supporting automated data generation,providing various sensor models that are commonly used in the autonomous driving sector and allowing more parametrization of the overall software.

BeamNG.py is the python interface to control and automate the usage of BeamNG.tech. It is an indispensable tool in developing autonomous systems with BeamNG.tech.It’s responsible for sensor management, simulation control, and vehicle control. 

**Dependencies:**
Python IDE 
Python 3.11
40GB Hard Drive Storage 
8GM RAM

**Installation:**
Register for a research license and you will be provided with a download link

Download the build of BeamNG.tech and extract it.
Place the “tech.key” file in installation directory for it to be detected 
For example, if you extract "BeamNG.tech.v0.23.5.1.zip" to "D:/BeamNG/" such
that this folder contains the EULA at "D:/BeamNG/EULA.pdf", then the "tech.key"
needs to be placed in "D:/BeamNG/tech.key". When a valid license file is found,
the logo of the game will clearly indicate that it is the BeamNG.tech version.

To install BeamNG.py on your Python IDE
pip install beamngpy

**NOTE: While running the simulation, the graphics should be set to the lowest so that it runs smoothly on the PC.**

**Useful Github links:
BeamNG.py feature overview -https://github.com/BeamNG/BeamNGpy/blob/master/examples/feature_overview.ipynb
Example Lidar -https://github.com/BeamNG/BeamNGpy/blob/master/examples/lidar_tour.py 
Example AI- follow line https://github.com/BeamNG/BeamNGpy/blob/master/examples/ai_line.py**

How does the Simulation Work:
The simulation is divided into three phases to simulate Collaborative Adaptive Cruise Control behavior. 

**Phase 1
Initiate**
The simulator has the following built-in AI for spawned vehicles 
Possible values are:

 * ``disabled``: Turn the AI off (default state)
 * ``random``: Drive from random points to random points on the map
 * ``span``: Drive along the entire road network of the map
 * ``manual``: Drive to a specific waypoint, target set separately
 * ``chase``: Chase a target vehicle, target set separately
 * ``flee``: Flee from a vehicle, target set separately
 * ``stopping``: Make the vehicle come to a halt (AI disables itself once the vehicle stopped.)

The script creates a scenario in ‘West Coast USA’ where ten vehicles are spawned , one being the lead car and other being the follow. The AI set for lead car and follow car is set to “span” which leads to driving at random points with the drive_in_lane feature always active. Once the following car comes in contact with the lead car, the AI set to “chase” wherein the car will follow the target car. 

The lead car would have “span” in its entirety and the rest of the cars would have “span” initially and would switch to “chase” after coming in contact with the lead car. A safe distance from objects is declared form the start 

**Phase 2
Sensing and Control**
The simulator also has options to mount the spawned vehicles with sensors,which capture the simulation and vehicle state data. There are currently two classes of sensor, which have slightly different APIs.

The first class of sensors are our Automated Sensors. These sensors are created with parameters to allow them to update automatically in the simulator at a given time, and with a given priority. This management is needed when we wish to run the simulation with many sensors. These sensors can also be set to not update automatically, if desired. We can poll these sensors in two ways: 
i) by getting the latest readings which were polled at the set update time for the sensor
ii) by sending ad-hoc requests for data, which can be used if we only want occasional reading on-the-fly.

Camera (providing color images, class annotation images, semantic annotation images, and depth images)
LiDAR (providing point cloud and/or annotation color data)
Ultrasonic Sensor (eg can be used as a parking sensor)
Accelerometer (a tri-axial accelerometer, providing a vehicles acceleration in a local coordinate system)

The second class of sensors are not automated currently, and use the older API. These are polled in an ad-hoc fashion.
IMU (Inertial Measurement Unit)
Electrics
Vehicle state

The cars are mounted with a camera and ultrasonic sensors to monitor the distance between each car which will continuously poll data.The sensor data is continuously polled after the AI is set to chase, which is used for the cars to adjust their speed based on the distance from the car in front.

**Phase 3
Negotiation**
The negotiation phase occurs when the speed of the convoy is homogeneous

The negotiation phase follows the following steps
Proposal - Each vehicle proposes a random speed within a predefined range.

The predefined range is determined by 
a.Polling sensor data to get current speed of all vehicles 
b.Compute Mean and Standard Deviation c.Lower Bound Range is = Mean - Standard Deviation, Upper Bound Range is = Mean + Standard Deviation

Consensus - The average of all proposed speeds is computed 
Adoption - Each vehicle adopts the average speed computed

Sequence Diagram:
![mermaid-diagram-2023-08-23-164256](https://github.com/asigdel29/Urban-CPS/assets/64096825/e21338be-bae0-40c2-a402-7bc3d09d087f)
