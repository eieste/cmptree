#  Copyright (c) 2023. Stefan Eiermann
#  Licenced under AGPL see /LICENSE

from cmptree.characteristic.electric.base import BaseElectricCharacteristic


class ElectricSupplyCharacteristic(BaseElectricCharacteristic):
    def __init__(
        self, *args, capacity=None, c_value=None, nominal_voltage=None, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.capacity = capacity
        self.c_value = c_value
        self.nominal_voltage = nominal_voltage
        self.units = {"capacity": "A/h", "c_value": "c", "nominal_voltage": "V"}
