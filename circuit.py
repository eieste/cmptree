
class Circuit:

    all_circuits = []
    
    def __init__(self, signal_name, uuid, *args):
        self.signal_name = signal_name
        self.uuid = uuid
        self.members = args

    def is_member(self, component):
        for member in self.members:
            if component is member:
                return True

        return False
    
    @classmethod
    def search(cls, component, signal_name):
        for circuit in cls.all_circuits:
            if circuit.is_member(component) and self.signal_name is signal_name:
                return circuit
        return False