from math import inf

from src.LEACH_create_sensors import *


def start(Sensors: list[Sensor], my_model, dead_num: list[Sensor], round_number):
    for sensor in Sensors:
        print(f"\nresetting {sensor.id}")

        # if sensor is dead
        if sensor.E <= 0 and sensor not in dead_num:
            sensor.df = 1
            dead_num.append(sensor)
            print(f'{sensor.id} is dead, \ndeadnum=')
            for _ in dead_num:
                print(_.id, end=' ')
            print()

        # allow to sensor to become cluster-head. LEACH Algorithm
        AroundClear = 1 / my_model.p  # After every "AroundClear" rounds, let every sensor be CH again
        if round_number % AroundClear == 0:
            sensor.G = 0

        sensor.MCH = my_model.n  # MCH = member of CH, initially all will have sink as their CH
        sensor.type = 'N'
        sensor.dis2ch = inf

    return dead_num
