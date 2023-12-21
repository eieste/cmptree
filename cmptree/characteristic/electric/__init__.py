#  Copyright (c) 2023. Stefan Eiermann
#  Licenced under AGPL see /LICENSE
import enum

from cmptree.characteristic.electric.base import (
    BaseCharacteristic,
    ElectricCharacteristic,
)
from cmptree.characteristic.electric.supply import ElectricSupplyCharacteristic
from cmptree.characteristic.electric.convert import ElectricConvertCharacteristic
from cmptree.characteristic.electric.distribute import (
    ElectricDistributionCharacteristic,
)


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


__all__ = [
    "BaseCharacteristic",
    "ElectricCharacteristic",
    "ElectricSupplyCharacteristic",
    "ElectricConvertCharacteristic",
    "ElectricDistributionCharacteristic",
    "ElectricSignal",
]
