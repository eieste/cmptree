#  Copyright (c) 2023. Stefan Eiermann
#  Licenced under AGPL see /LICENSE

import sys
from cmptree.part import Part
import cmptree.characteristic as char
from cmptree.characteristic.electric import ElectricSignal as ES

default_electric_step_down_5 = {
    "maximal_in_voltage": 30,
    "maximal_in_current": 3,
    "nominal_out_voltage": 5,
    "nominal_out_current": 3,
}

default_electric_step_down_7 = {
    "maximal_in_voltage": 30,
    "maximal_in_current": 3,
    "nominal_out_voltage": 7.5,
    "nominal_out_current": 3,
}

default_electric_drive_motor = {
    "nominal_voltage": 7.5,
    "nominal_current": 3,
    "maximal_current": 3,
}

default_dimension_step = {"weight": 60, "length": 43, "width": 14, "height": 45}

world = Part(name="world")
char.ElectricCharacteristic(world)
char.DimensionCharacteristic(world)

chassie = Part(name="chassie")
char.ElectricCharacteristic(chassie)
char.DimensionCharacteristic(chassie).set_parent(world)


supply_level = Part(name="Supply Level")
char.DimensionCharacteristic(supply_level).set_parent(chassie)

control_level = Part(name="Control Level")
char.DimensionCharacteristic(control_level).set_parent(chassie)

sensor_level = Part(name="Sensor Level")
char.DimensionCharacteristic(sensor_level).set_parent(chassie)

battery = Part(name="Battery")
char.DimensionCharacteristic(
    battery, weight=1400, length=134, width=67, height=60
).set_parent(supply_level)
char.ElectricSupplyCharacteristic(battery, capacity=3.3, nominal_voltage=12, c_value=1)

power_switch = Part(name="Power Switch", todo=True)
char.DimensionCharacteristic(
    power_switch, weight=5, length=20, width=15, height=15
).set_parent(supply_level)
char.ElectricCharacteristic(
    power_switch, nominal_voltage=12, nominal_current=1
).set_parent(battery, ES.POWER_IN)

relais = Part(name="Relaise")
char.ElectricCharacteristic(relais, nominal_voltage=12, nominal_current=3).set_parent(
    power_switch, ES.POWER_IN
)
char.DimensionCharacteristic(
    relais, weight=100, length=30, width=30, height=30
).set_parent(supply_level)

main_power_distribution = Part(name="Main Power Distribution")
char.ElectricDistributionCharacteristic(
    main_power_distribution,
    distribution_voltage=12,
    signal_name=ES.POWER_IN,
    maximal_current=3,
).set_parent(relais, ES.POWER_IN)

step_down_5v_1 = Part(name="Step Down Converter 5V - 1")
char.ElectricConvertCharacteristic(
    step_down_5v_1, **default_electric_step_down_5
).set_parent(main_power_distribution, ES.POWER_IN)
char.DimensionCharacteristic(step_down_5v_1, **default_dimension_step).set_parent(
    supply_level
)

step_down_5v_2 = Part(name="Step Down Converter 5V - 2")
char.ElectricConvertCharacteristic(
    step_down_5v_2, **default_electric_step_down_5
).set_parent(main_power_distribution, ES.POWER_IN)
char.DimensionCharacteristic(step_down_5v_2, **default_dimension_step).set_parent(
    supply_level
)

step_down_7v_3 = Part(name="Step Down Converter 7.5 -3")
char.ElectricConvertCharacteristic(
    step_down_7v_3, **default_electric_step_down_7
).set_parent(main_power_distribution, ES.POWER_IN)
char.DimensionCharacteristic(step_down_7v_3, **default_dimension_step).set_parent(
    supply_level
)

step_down_7v_4 = Part(name="Step Down Converter 7.5 - 4")
char.ElectricConvertCharacteristic(
    step_down_7v_4, **default_electric_step_down_7
).set_parent(main_power_distribution, ES.POWER_IN)
char.DimensionCharacteristic(step_down_7v_4, **default_dimension_step).set_parent(
    supply_level
)

step_down_5v_5 = Part(name="Step Down Converter 5 - 5")
char.ElectricConvertCharacteristic(
    step_down_5v_5, **default_electric_step_down_5
).set_parent(main_power_distribution, ES.POWER_IN)
char.DimensionCharacteristic(step_down_5v_5, **default_dimension_step).set_parent(
    supply_level
)

step_down_5v_6 = Part(name="Step Down Converter 5 - 6")
char.ElectricConvertCharacteristic(
    step_down_5v_6, **default_electric_step_down_5
).set_parent(main_power_distribution, ES.POWER_IN)
char.DimensionCharacteristic(step_down_5v_6, **default_dimension_step).set_parent(
    supply_level
)

step_down_5v_7 = Part(name="Step Down Converter 5 - 7")
char.ElectricConvertCharacteristic(
    step_down_5v_7, **default_electric_step_down_5
).set_parent(main_power_distribution, ES.POWER_IN)
char.DimensionCharacteristic(step_down_5v_7, **default_dimension_step).set_parent(
    supply_level
)

step_down_5v_8 = Part(name="Step Down Converter 5 - 8")
char.ElectricConvertCharacteristic(
    step_down_5v_8, **default_electric_step_down_5
).set_parent(main_power_distribution, ES.POWER_IN)
char.DimensionCharacteristic(step_down_5v_8, **default_dimension_step).set_parent(
    supply_level
)

raspberry_pi = Part(name="Raspberry PI")
char.ElectricCharacteristic(
    raspberry_pi, required_current=2.0, required_voltage=5.0, maximal_current=3.0
).set_parent(step_down_5v_1, ES.POWER_LVL_5)
char.DimensionCharacteristic(
    raspberry_pi, weight=46, length=85, width=58, height=19
).set_parent(control_level)

raspberry_pi_fan = Part(name="Raspberry PI Fan")
char.ElectricCharacteristic(
    raspberry_pi_fan, nominal_voltage=5.0, nominal_current=0.2
).set_parent(step_down_5v_1, ES.POWER_LVL_5).set_parent(raspberry_pi, ES.PWMCTL)
char.DimensionCharacteristic(
    raspberry_pi_fan, weight=20, length=30, width=30, height=7
).set_parent(control_level)

teensy = Part(name="Teensy", todo=True)
char.ElectricCharacteristic(
    teensy, required_voltage=5.0, required_current=1.0, maximal_current=1.0
).set_parent(step_down_5v_2, ES.POWER_LVL_5).set_parent(raspberry_pi, ES.SERIAL)
char.DimensionCharacteristic(
    teensy, weight=10, length=60, width=18, height=2
).set_parent(control_level)

motor_front_left = Part(name="Motor Front Left", todo=True)
char.ElectricCharacteristic(
    motor_front_left, **default_electric_drive_motor
).set_parent(step_down_7v_3, ES.POWER_LVL_7).set_parent(teensy, ES.PWMCTL).set_parent(
    teensy, ES.PWMFEED
)
char.DimensionCharacteristic(motor_front_left).set_parent(supply_level)

motor_front_right = Part(name="Motor Front Right", todo=True)
char.ElectricCharacteristic(
    motor_front_right, **default_electric_drive_motor
).set_parent(step_down_7v_3, ES.POWER_LVL_7).set_parent(teensy, ES.PWMCTL).set_parent(
    teensy, ES.PWMFEED
)
char.DimensionCharacteristic(motor_front_right).set_parent(supply_level)

motor_back_left = Part(name="Motor Back Left", todo=True)
char.ElectricCharacteristic(motor_back_left, **default_electric_drive_motor).set_parent(
    step_down_7v_4, ES.POWER_LVL_7
).set_parent(teensy, ES.PWMCTL).set_parent(teensy, ES.PWMFEED)
char.DimensionCharacteristic(motor_back_left).set_parent(supply_level)

motor_back_right = Part(name="Motor Back Right", todo=True)
char.ElectricCharacteristic(
    motor_back_right, **default_electric_drive_motor
).set_parent(step_down_7v_4, ES.POWER_LVL_7).set_parent(teensy, ES.PWMCTL).set_parent(
    teensy, ES.PWMFEED
)
char.DimensionCharacteristic(motor_back_right).set_parent(supply_level)

lidar = Part(name="LiDAR", todo=True)
char.DimensionCharacteristic(lidar).set_parent(sensor_level)
char.ElectricCharacteristic(lidar).set_parent(step_down_5v_7, ES.POWER_LVL_5)

gyroscope = Part(name="Gyroscope Sensor", todo=True)
char.DimensionCharacteristic(gyroscope).set_parent(sensor_level)
char.ElectricCharacteristic(gyroscope).set_parent(
    step_down_5v_5, ES.POWER_LVL_5
).set_parent(raspberry_pi, ES.I2C)

compass = Part(name="Compass", todo=True)
char.DimensionCharacteristic(compass).set_parent(sensor_level)
char.ElectricCharacteristic(compass).set_parent(
    step_down_5v_5, ES.POWER_LVL_5
).set_parent(raspberry_pi, ES.I2C)

cam_tower_yaw = Part(name="Cam Tower Yaw", todo=True)
char.DimensionCharacteristic(cam_tower_yaw).set_parent(sensor_level)
char.ElectricCharacteristic(cam_tower_yaw).set_parent(
    step_down_5v_6, ES.POWER_LVL_5
).set_parent(raspberry_pi, ES.PWMCTL)

cam_tower_pitch = Part(name="Cam Tower Pitch", todo=True)
char.DimensionCharacteristic(cam_tower_pitch).set_parent(sensor_level)
char.ElectricCharacteristic(cam_tower_pitch).set_parent(
    step_down_5v_6, ES.POWER_LVL_5
).set_parent(raspberry_pi, ES.PWMCTL)

cam_nightvision = Part(name="Night Vision", todo=True)
char.DimensionCharacteristic(cam_nightvision).set_parent(sensor_level)
char.ElectricCharacteristic(cam_nightvision).set_parent(
    step_down_5v_6, ES.POWER_LVL_5
).set_parent(raspberry_pi, ES.PICAM)

cam_tower_us_yaw = Part(name="Cam Tower UltraSonic Yaw", todo=True)
char.DimensionCharacteristic(cam_tower_us_yaw).set_parent(sensor_level)
char.ElectricCharacteristic(cam_tower_us_yaw).set_parent(
    step_down_5v_6, ES.POWER_LVL_5
).set_parent(raspberry_pi, ES.PWMCTL)

depth_cam = Part(name="DepthCamera", todo=True)
char.DimensionCharacteristic(depth_cam).set_parent(control_level)
char.ElectricCharacteristic(depth_cam).set_parent(
    step_down_5v_1, ES.POWER_LVL_5
).set_parent(raspberry_pi, ES.USB)
