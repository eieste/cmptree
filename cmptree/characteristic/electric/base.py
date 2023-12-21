#  Copyright (c) 2023. Stefan Eiermann
#  Licenced under AGPL see /LICENSE
from cmptree.characteristic.base import BaseCharacteristic


class BaseElectricCharacteristic(BaseCharacteristic):
    characteristic_name = "electric"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.units = {}


class ElectricCharacteristic(BaseElectricCharacteristic):
    def __init__(
        self,
        *args,
        required_voltage=None,
        required_current=None,
        maximal_current=None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.nominal_voltage = required_voltage
        self.nominal_current = required_current
        self.maximal_current = maximal_current
        self.units = {
            "nominal_voltage": "V",
            "nominal_current": "A",
            "maximal_current": "A",
        }
