class NotAnElement(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"{self.value} is not an element of this field"


class NotInvertible(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"{self.value} is not invertible in this field"


class PolynomialError(Exception):
    pass
