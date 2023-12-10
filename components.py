#  Copyright (c) 2023. Stefan Eiermann
#  Licenced under AGPL see /LICENSE

import sys
from basecomponents import *

ES = ElectricSignal

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

world = Component(name="world")
ElectricComponent(world)
DimensionComponent(world)

chassie = Component(name="chassie")
ElectricComponent(chassie)
DimensionComponent(chassie).set_parent(world)


supply_level = Component(name="Supply Level")
DimensionComponent(supply_level).set_parent(chassie)

control_level = Component(name="Control Level")
DimensionComponent(control_level).set_parent(chassie)

sensor_level = Component(name="Sensor Level")
DimensionComponent(sensor_level).set_parent(chassie)

battery = Component(name="Battery")
DimensionComponent(battery, weight=1400, length=134, width=67, height=60).set_parent(
    supply_level
)
ElectricSupplyComponent(battery, capacity=3.3, nominal_voltage=12, c_value=1)

power_switch = Component(name="Power Switch", todo=True)
DimensionComponent(power_switch, weight=5, length=20, width=15, height=15).set_parent(
    supply_level
)
ElectricComponent(power_switch, nominal_voltage=12, nominal_current=1).set_parent(
    battery, ES.POWER_IN
)

relais = Component(name="Relaise")
ElectricComponent(relais, nominal_voltage=12, nominal_current=3).set_parent(
    power_switch, ES.POWER_IN
)
DimensionComponent(relais, weight=100, length=30, width=30, height=30).set_parent(
    supply_level
)

main_power_distribution = Component(name="Main Power Distribution")
ElectricDistributorComponent(
    main_power_distribution,
    distribution_voltage=12,
    signal_name=ElectricSignal.POWER_IN,
    maximal_current=3,
).set_parent(relais, ElectricSignal.POWER_IN)

step_down_5v_1 = Component(name="Step Down Converter 5V - 1")
ElectricConvertComponent(step_down_5v_1, **default_electric_step_down_5).set_parent(
    main_power_distribution, ElectricSignal.POWER_IN
)
DimensionComponent(step_down_5v_1, **default_dimension_step).set_parent(supply_level)

step_down_5v_2 = Component(name="Step Down Converter 5V - 2")
ElectricConvertComponent(step_down_5v_2, **default_electric_step_down_5).set_parent(
    main_power_distribution, ES.POWER_IN
)
DimensionComponent(step_down_5v_2, **default_dimension_step).set_parent(supply_level)

step_down_7v_3 = Component(name="Step Down Converter 7.5 -3")
ElectricConvertComponent(step_down_7v_3, **default_electric_step_down_7).set_parent(
    main_power_distribution, ES.POWER_IN
)
DimensionComponent(step_down_7v_3, **default_dimension_step).set_parent(supply_level)

step_down_7v_4 = Component(name="Step Down Converter 7.5 - 4")
ElectricConvertComponent(step_down_7v_4, **default_electric_step_down_7).set_parent(
    main_power_distribution, ES.POWER_IN
)
DimensionComponent(step_down_7v_4, **default_dimension_step).set_parent(supply_level)

step_down_5v_5 = Component(name="Step Down Converter 5 - 5")
ElectricConvertComponent(step_down_5v_5, **default_electric_step_down_5).set_parent(
    main_power_distribution, ES.POWER_IN
)
DimensionComponent(step_down_5v_5, **default_dimension_step).set_parent(supply_level)

step_down_5v_6 = Component(name="Step Down Converter 5 - 6")
ElectricConvertComponent(step_down_5v_6, **default_electric_step_down_5).set_parent(
    main_power_distribution, ES.POWER_IN
)
DimensionComponent(step_down_5v_6, **default_dimension_step).set_parent(supply_level)

step_down_5v_7 = Component(name="Step Down Converter 5 - 7")
ElectricConvertComponent(step_down_5v_7, **default_electric_step_down_5).set_parent(
    main_power_distribution, ES.POWER_IN
)
DimensionComponent(step_down_5v_7, **default_dimension_step).set_parent(supply_level)

step_down_5v_8 = Component(name="Step Down Converter 5 - 8")
ElectricConvertComponent(step_down_5v_8, **default_electric_step_down_5).set_parent(
    main_power_distribution, ES.POWER_IN
)
DimensionComponent(step_down_5v_8, **default_dimension_step).set_parent(supply_level)

raspberry_pi = Component(name="Raspberry PI")
ElectricComponent(
    raspberry_pi, required_current=2.0, required_voltage=5.0, maximal_current=3.0
).set_parent(step_down_5v_1, ES.POWER_LVL_5)
DimensionComponent(raspberry_pi, weight=46, length=85, width=58, height=19).set_parent(
    control_level
)

raspberry_pi_fan = Component(name="Raspberry PI Fan")
ElectricComponent(
    raspberry_pi_fan, nominal_voltage=5.0, nominal_current=0.2
).set_parent(step_down_5v_1, ES.POWER_LVL_5).set_parent(raspberry_pi, ES.PWMCTL)
DimensionComponent(
    raspberry_pi_fan, weight=20, length=30, width=30, height=7
).set_parent(control_level)

teensy = Component(name="Teensy", todo=True)
ElectricComponent(
    teensy, required_voltage=5.0, required_current=1.0, maximal_current=1.0
).set_parent(step_down_5v_2, ES.POWER_LVL_5).set_parent(raspberry_pi, ES.SERIAL)
DimensionComponent(teensy, weight=10, length=60, width=18, height=2).set_parent(
    control_level
)

motor_front_left = Component(name="Motor Front Left", todo=True)
ElectricComponent(motor_front_left, **default_electric_drive_motor).set_parent(
    step_down_7v_3, ES.POWER_LVL_7
).set_parent(teensy, ES.PWMCTL).set_parent(teensy, ES.PWMFEED)
DimensionComponent(motor_front_left).set_parent(supply_level)

motor_front_right = Component(name="Motor Front Right", todo=True)
ElectricComponent(motor_front_right, **default_electric_drive_motor).set_parent(
    step_down_7v_3, ES.POWER_LVL_7
).set_parent(teensy, ES.PWMCTL).set_parent(teensy, ES.PWMFEED)
DimensionComponent(motor_front_right).set_parent(supply_level)

motor_back_left = Component(name="Motor Back Left", todo=True)
ElectricComponent(motor_back_left, **default_electric_drive_motor).set_parent(
    step_down_7v_4, ES.POWER_LVL_7
).set_parent(teensy, ES.PWMCTL).set_parent(teensy, ES.PWMFEED)
DimensionComponent(motor_back_left).set_parent(supply_level)

motor_back_right = Component(name="Motor Back Right", todo=True)
ElectricComponent(motor_back_right, **default_electric_drive_motor).set_parent(
    step_down_7v_4, ES.POWER_LVL_7
).set_parent(teensy, ES.PWMCTL).set_parent(teensy, ES.PWMFEED)
DimensionComponent(motor_back_right).set_parent(supply_level)

lidar = Component(name="LiDAR", todo=True)
DimensionComponent(lidar).set_parent(sensor_level)
ElectricComponent(lidar).set_parent(step_down_5v_7, ES.POWER_LVL_5)

gyroscope = Component(name="Gyroscope Sensor", todo=True)
DimensionComponent(gyroscope).set_parent(sensor_level)
ElectricComponent(gyroscope).set_parent(step_down_5v_5, ES.POWER_LVL_5).set_parent(
    raspberry_pi, ES.I2C
)

compass = Component(name="Compass", todo=True)
DimensionComponent(compass).set_parent(sensor_level)
ElectricComponent(compass).set_parent(step_down_5v_5, ES.POWER_LVL_5).set_parent(
    raspberry_pi, ES.I2C
)

cam_tower_yaw = Component(name="Cam Tower Yaw", todo=True)
DimensionComponent(cam_tower_yaw).set_parent(sensor_level)
ElectricComponent(cam_tower_yaw).set_parent(step_down_5v_6, ES.POWER_LVL_5).set_parent(
    raspberry_pi, ES.PWMCTL
)

cam_tower_pitch = Component(name="Cam Tower Pitch", todo=True)
DimensionComponent(cam_tower_pitch).set_parent(sensor_level)
ElectricComponent(cam_tower_pitch).set_parent(
    step_down_5v_6, ES.POWER_LVL_5
).set_parent(raspberry_pi, ES.PWMCTL)

cam_nightvision = Component(name="Night Vision", todo=True)
DimensionComponent(cam_nightvision).set_parent(sensor_level)
ElectricComponent(cam_nightvision).set_parent(
    step_down_5v_6, ES.POWER_LVL_5
).set_parent(raspberry_pi, ES.PICAM)

cam_tower_us_yaw = Component(name="Cam Tower UltraSonic Yaw", todo=True)
DimensionComponent(cam_tower_us_yaw).set_parent(sensor_level)
ElectricComponent(cam_tower_us_yaw).set_parent(
    step_down_5v_6, ES.POWER_LVL_5
).set_parent(raspberry_pi, ES.PWMCTL)

depth_cam = Component(name="DepthCamera", todo=True)
DimensionComponent(depth_cam).set_parent(control_level)
ElectricComponent(depth_cam).set_parent(step_down_5v_1, ES.POWER_LVL_5).set_parent(
    raspberry_pi, ES.USB
)
