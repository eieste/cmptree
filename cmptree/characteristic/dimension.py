#  Copyright (c) 2023. Stefan Eiermann
#  Licenced under AGPL see /LICENSE

from cmptree.characteristic.base import BaseCharacteristic


class DimensionCharacteristic(BaseCharacteristic):
    characteristic_name = "dimension"

    def __init__(
        self, *args, weight=None, height=None, width=None, length=None, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.weight = weight
        self.height = height
        self.width = width
        self.length = length
        self.units = {"weight": "g", "height": "mm", "width": "mm", "length": "mm"}
