#  Copyright (c) 2023. Stefan Eiermann
#  Licenced under AGPL see /LICENSE

from cmptree.characteristic.electric.base import BaseElectricCharacteristic


class ElectricConvertCharacteristic(BaseElectricCharacteristic):
    def __init__(
        self,
        *args,
        maximal_in_voltage=None,
        maximal_in_current=None,
        nominal_out_voltage=None,
        nominal_out_current=None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.maximal_in_voltage = maximal_in_voltage
        self.maximal_in_current = maximal_in_current
        self.nominal_out_voltage = nominal_out_voltage
        self.nominal_out_current = nominal_out_current
        self.units = {
            "maximal_in_voltage": "V",
            "maximal_in_current": "A",
            "nominal_out_voltage": "V",
            "nominal_out_current": "A",
        }
