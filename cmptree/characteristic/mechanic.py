#  Copyright (c) 2023. Stefan Eiermann
#  Licenced under AGPL see /LICENSE

from cmptree.characteristic.base import BaseCharacteristic


class MechanicCharacteristic(BaseCharacteristic):
    characteristic_name = "mechanic"

    def __init__(self, *args, torque=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.torque = torque
        self.units = {"torque": "Nm"}
