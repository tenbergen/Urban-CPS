import numpy as np
import random
import numba
from time import sleep
from beamngpy import BeamNGpy, Scenario, Vehicle, set_up_simple_logging
from beamngpy.sensors import Lidar, Ultrasonic
import threading

SIZE = 1024

@numba.jit
def update_vehicles(beamng, vehicles, script):
    for i in range(0, 3600, 10):
        node = script[i]
        t = node['t']
        for vehicle in vehicles:
            vehicle.ai_set_drive_power(t)
            vehicle.update_vehicle()
        beamng.step(1)

def main():
    set_up_simple_logging()

    beamng = BeamNGpy('localhost', 64256 , 'C:/Users/ayusa/OneDrive/Desktop/BeamNG.tech.v0.27.1.0/BeamNG.tech.v0.27.1.0')
    beamng.open(launch=True)

    orig = (-769.1, 400.8, 142.8)

    script = []
    points = []
    point_color = [0, 0, 0, 0.1]
    sphere_coordinates = []
    sphere_radii = []
    sphere_colors = []

    for i in range(3600):
        node = {
            'x': 4 * np.sin(np.radians(i)) + orig[0],
            'y': i * 0.2 + orig[1],
            'z': orig[2],
            't': (2 * i + (np.abs(np.sin(np.radians(i)))) * 64) / 64,
        }
        script.append(node)
        points.append((node['x'], node['y'], node['z']))

        if i % 10 == 0:
            sphere_coordinates.append((node['x'], node['y'], node['z']))
            sphere_radii.append(np.abs(np.sin(np.radians(i))) * 0.25)
            sphere_colors.append((np.sin(np.radians(i)), 0, 0, 0.8))

    scenario = Scenario('west_coast_usa', 'ai_test')

    vehicle = Vehicle('ego_vehicle', model='etk800', license='AI')
    vehicle1 = Vehicle('ego_vehicle1', model='etk800', license='AI')
    vehicle2 = Vehicle('ego_vehicle2', model='etk800', license='AI')
    vehicle3 = Vehicle('ego_vehicle3', model='etk800', license='AI')
    vehicle4 = Vehicle('ego_vehicle4', model='etk800', license='AI')
    vehicle5 = Vehicle('ego_vehicle5', model='etk800', license='AI')

    scenario.add_vehicle(vehicle, pos=(-717.121, 500.8, 142.8), rot_quat=(0, 0, 1, 0))
    scenario.add_vehicle(vehicle1, pos=(-717.121, 495.8, 142.8), rot_quat=(0, 0, 1, 0))
    scenario.add_vehicle(vehicle2, pos=(-717.121, 490.8, 142.8), rot_quat=(0, 0, 1, 0))
    scenario.add_vehicle(vehicle3, pos=(-717.121, 485.8, 142.8), rot_quat=(0, 0, 1, 0))
    scenario.add_vehicle(vehicle4, pos=(-717.121, 480.8, 142.8), rot_quat=(0, 0, 1, 0))
    scenario.add_vehicle(vehicle5, pos=(-717.121, 475.8, 142.8), rot_quat=(0, 0, 1, 0))

    scenario.make(beamng)
    
    vehicle.ai.set_mode('span')
    vehicle1.ai.set_mode('chase')
    vehicle2.ai.set_mode('chase')
    vehicle3.ai.set_mode('chase')
    vehicle4.ai.set_mode('chase')
    vehicle5.ai.set_mode('chase')

    vehicle.ai.drive_in_lane(True)
    vehicle1.ai.drive_in_lane(True)
    vehicle2.ai.drive_in_lane(True)
    vehicle3.ai.drive_in_lane(True)
    vehicle4.ai.drive_in_lane(True)
    vehicle5.ai.drive_in_lane(True)

beamng.settings.set_deterministic(60)

try:
    beamng.scenario.load(scenario)
    beamng.scenario.start()
    beamng.debug.add_spheres(sphere_coordinates, sphere_radii, sphere_colors, cling=True, offset=0.1)
    beamng.debug.add_polyline(points, point_color, cling=True, offset=0.1)

    vehicles = [vehicle, vehicle1, vehicle2, vehicle3, vehicle4, vehicle5]

    lidar = Lidar('lidar', beamng, vehicle, SIZE)
    ultrasonic = Ultrasonic('ultrasonic', beamng, vehicle, SIZE)

    t1 = threading.Thread(target=update_vehicles, args=(beamng, vehicles, script))
    t1.start()

    while True:
        d_lidar, _ = lidar.get_lidar()
        d_ultrasonic, _ = ultrasonic.get_ultrasonic()

        print(d_lidar)
        print(d_ultrasonic)
        sleep(1)

except KeyboardInterrupt:
    pass
finally:
    beamng.close()
