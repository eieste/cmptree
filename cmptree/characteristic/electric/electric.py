#  Copyright (c) 2023. Stefan Eiermann
#  Licenced under AGPL see /LICENSE
from cmptree.characteristic.base import BaseCharacteristic


class BaseElectricCharacteristic(BaseCharacteristic):
    name = "electric"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.units = {}


class ElectricSupplyCharacteristic(BaseElectricCharacteristic):
    def __init__(
        self, *args, capacity=None, c_value=None, nominal_voltage=None, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.capacity = capacity
        self.c_value = c_value
        self.nominal_voltage = nominal_voltage
        self.units = {"capacity": "A/h", "c_value": "c", "nominal_voltage": "V"}


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


class ElectricDistributionCharacteristic(BaseElectricCharacteristic):
    def __init__(
        self,
        *args,
        bus=None,
        distribution_voltage=None,
        signal_name=None,
        maximal_current=None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.distribution_voltage = distribution_voltage
        self.maximal_current = maximal_current
        self.bus = bus
        self.units = {"distribution_voltage": "V", "maximal_current": "A"}


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
