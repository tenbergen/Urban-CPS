from datetime import time

import numpy as np
from beamngpy import BeamNGpy, Scenario, Vehicle, set_up_simple_logging
from beamngpy.sensors import ultrasonic

SIZE = 1024

def main():
    set_up_simple_logging()

    beamng = BeamNGpy('localhost', 64256, 'C:/Users/ayusa/OneDrive/Desktop/BeamNG.tech.v0.27.1.0/BeamNG.tech.v0.27.1.0')
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
            #  Calculate the position as a sine curve that makes the vehicle
            #  drive from left to right. The z-coordinate is not calculated in
            #  any way because `ai_set_script` by default makes the polyline to
            #  follow cling to the ground, meaning the z-coordinate will be
            #  filled in automatically.
            'x': 4 * np.sin(np.radians(i)) + orig[0],
            'y': i * 0.2 + orig[1],
            'z': orig[2],
            #  Calculate timestamps for each node such that the speed between
            #  points has a sinusoidal variance to it.
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

    scenario.add_vehicle(vehicle, pos=(-769.1, 400.8, 142.8), rot_quat=(0, 0, 1, 0))
    scenario.add_vehicle(vehicle1, pos=(-769.1, 395.8, 142.8), rot_quat=(0, 0, 1, 0))
    scenario.add_vehicle(vehicle2, pos=(-769.1, 390.8, 142.8), rot_quat=(0, 0, 1, 0))
    scenario.add_vehicle(vehicle3, pos=(-769.1, 385.8, 142.8), rot_quat=(0, 0, 1, 0))
    scenario.add_vehicle(vehicle4, pos=(-769.1, 380.8, 142.8), rot_quat=(0, 0, 1, 0))
    scenario.add_vehicle(vehicle5, pos=(-769.1, 375.8, 142.8), rot_quat=(0, 0, 1, 0))

    scenario.make(beamng)

    beamng.settings.set_deterministic(60)

    try:
        beamng.scenario.load(scenario)
        vehicle.attach_sensor("ultrasonic", ultrasonic)
        vehicle1.attach_sensor("ultrasonic", ultrasonic)
        vehicle2.attach_sensor("ultrasonic", ultrasonic)
        vehicle3.attach_sensor("ultrasonic", ultrasonic)
        vehicle4.attach_sensor("ultrasonic", ultrasonic)
        vehicle5.attach_sensor("ultrasonic", ultrasonic)

        beamng.scenario.start()
        beamng.debug.add_spheres(sphere_coordinates, sphere_radii, sphere_colors, cling=True, offset=0.1)
        beamng.debug.add_polyline(points, point_color, cling=True, offset=0.1)
        vehicle.ai.set_script(script)
        vehicle1.ai.set_script(script)
        vehicle2.ai.set_script(script)
        vehicle3.ai.set_script(script)
        vehicle4.ai.set_script(script)
        vehicle5.ai.set_script(script)

        distance_threshold = 5.0  # meters
        stop_time = 1.0  # seconds

        while True:
            distance1 = vehicle1.get_sensor("ultrasonic")["distance"]
            distance2 = vehicle2.get_sensor("ultrasonic")["distance"]
            distance3 = vehicle3.get_sensor("ultrasonic")["distance"]
            distance4 = vehicle4.get_sensor("ultrasonic")["distance"]
            distance5 = vehicle5.get_sensor("ultrasonic")["distance"]

            if distance1 < distance_threshold:
                vehicle1.ai.stop()
                time.sleep(stop_time)
                vehicle1.ai.resume()
            if distance2 < distance_threshold:
                vehicle2.ai.stop()
                time.sleep(stop_time)
                vehicle2.ai.resume()
            if distance3 < distance_threshold:
                vehicle3.ai.stop()
                time.sleep(stop_time)
                vehicle3.ai.resume()
            if distance4 < distance_threshold:
                vehicle4.ai.stop()
                time.sleep(stop_time)
                vehicle4.ai.resume()
            if distance5 < distance_threshold:
                vehicle5.ai.stop()
                time.sleep(stop_time)
                vehicle5.ai.resume()

            beamng.control.step(60)
    finally:
        beamng.close()



if __name__ == '__main__':
    main()
