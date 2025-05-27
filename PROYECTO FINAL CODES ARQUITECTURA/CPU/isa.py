class Instruction:
    def __init__(self, op, **kwargs):
        self.op = op
        for k, v in kwargs.items():
            setattr(self, k, v)
    def __repr__(self):
        return f"Instruction({self.op}, {self.__dict__})"