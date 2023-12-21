#  Copyright (c) 2023. Stefan Eiermann
#  Licenced under AGPL see /LICENSE
from cmptree.characteristic.base import BaseCharacteristic


class ThermalCharacteristic(BaseCharacteristic):
    characteristic_name = "thermal"

    def __init__(self, *args, btu=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.btu = btu
        self.units = {"btu": "btu"}
