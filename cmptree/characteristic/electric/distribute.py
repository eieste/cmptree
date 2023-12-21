#  Copyright (c) 2023. Stefan Eiermann
#  Licenced under AGPL see /LICENSE

from cmptree.characteristic.electric.base import BaseElectricCharacteristic


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
