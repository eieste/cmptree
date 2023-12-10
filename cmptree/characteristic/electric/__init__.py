#  Copyright (c) 2023. Stefan Eiermann
#  Licenced under AGPL see /LICENSE
import enum


class ElectricSignal(enum.Enum):
    name = "electric"

    POWER_IN = "PWR_IN"
    POWER_LVL_5 = "PWR_LVL_5"
    POWER_LVL_7 = "PWR_LVL_7"
    I2C = "I2C"
    PWMCTL = "PWM-CTL"
    PWMFEED = "PWM-FEED"
    PICAM = "PICAM"
    PIDISPLAY = "PIDISPLAY"
    USB = "USB"
    SERIAL = "SERIAL"
    OTHER = "OTHER"
