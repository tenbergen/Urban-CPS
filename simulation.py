from beamngpy import BeamNGpy, Vehicle, Scenario
from beamngpy.sensors import Camera, Ultrasonic
import time

# Initialize BeamNGpy instance
beamng = BeamNGpy('localhost', 64256, 'C:/Users/sigde/OneDrive/Desktop/BeamNG.tech.v0.28.2.0/BeamNG.tech.v0.28.2.0')

# Define the scenario
scenario = Scenario('west_coast_usa', 'CACC', description='Collaborative Adaptive Cruise Control')

# Create and configure the lead vehicle
lead_vehicle = Vehicle('lead_vehicle', model='etk800', licence='LEAD', colour='Red')
camera_lead = Camera(beamng, 'camera_lead', pos=(0, 1, 1.5))
ultrasonic_lead = Ultrasonic(pos=(0, 2.5, 0.4))
lead_vehicle.attach_sensor('camera_lead', camera_lead)
lead_vehicle.attach_sensor('ultrasonic_lead', ultrasonic_lead)

# Add the lead vehicle to the scenario
scenario.add_vehicle(lead_vehicle, pos=(0, 0, 0), rot=None, rot_quat=None)

# Create and configure the follow vehicles
for i in range(1, 11):
    follow_vehicle = Vehicle(f'follow_vehicle_{i}', model='etk800', licence=f'FOLLOW{i}', colour='Blue')
    follow_vehicle.ai_set_mode('span')
    camera_follow = Camera(beamng, f'camera_follow_{i}', pos=(0, 1, 1.5))
    ultrasonic_follow = Ultrasonic(pos=(0, 2.5, 0.4))
    follow_vehicle.attach_sensor(f'camera_follow_{i}', camera_follow)
    follow_vehicle.attach_sensor(f'ultrasonic_follow_{i}', ultrasonic_follow)
    scenario.add_vehicle(follow_vehicle, pos=(i*5, i*5, 0), rot=None, rot_quat=None)

# Compile the scenario
scenario.make(beamng)

# Start BeamNG and enter the created scenario
bng = beamng.open(launch=True)
try:
    bng.load_scenario(scenario)
    bng.start_scenario()

    # Set lead vehicle AI mode to 'span' (driving at random points)
    lead_vehicle.ai_set_mode('span')

    # Poll sensor data for a specified duration (e.g., 60 seconds)
    for _ in range(60):
        # Poll data from the lead vehicle's sensors
        sensors_lead = bng.poll_sensors(lead_vehicle)
        print('Lead vehicle camera data:', sensors_lead['camera_lead'])
        print('Lead vehicle ultrasonic data:', sensors_lead['ultrasonic_lead'])

        # Poll data from the follow vehicles' sensors and check for contact
        for i in range(1, 11):
            follow_vehicle = scenario.get_vehicle_by_name(f'follow_vehicle_{i}')
            sensors_follow = bng.poll_sensors(follow_vehicle)
            print(f'Follow vehicle {i} camera data:', sensors_follow[f'camera_follow_{i}'])
            print(f'Follow vehicle {i} ultrasonic data:', sensors_follow[f'ultrasonic_follow_{i}'])

            # Check for contact with the lead vehicle using the ultrasonic sensor
            if sensors_follow[f'ultrasonic_follow_{i}']['distance'] < 1.5:
                # If contact detected, set AI mode to 'chase' to follow the target car
                follow_vehicle.ai_set_target(lead_vehicle.vid)
                follow_vehicle.ai_set_mode('chase')

        # Wait for a second before polling data again
        time.sleep(1)

finally:
    bng.close()
