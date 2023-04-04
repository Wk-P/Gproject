from .exceptions import NotAnElement, NotInvertible, PolynomialError

class GenericGF:
    def __init__(self, modulus, size, primitive):
        self.modulus = modulus
        self.size = size
        self.primitive = primitive
        self.exp_table = [0] * size
        self.log_table = [0] * size
        self.calculate_tables()

    def multiply(self, a, b):
        if a == 0 or b == 0:
            return 0
        log_sum = self.log_table[a] + self.log_table[b]
        return self.exp_table[(log_sum % self.modulus) + self.modulus]

    def divide(self, a, b):
        if a == 0:
            return 0
        if b == 0:
            raise ZeroDivisionError()
        log_diff = self.log_table[a] - self.log_table[b]
        return self.exp_table[(log_diff % self.modulus) + self.modulus]

    def inverse(self, a):
        return self.exp_table[self.modulus - self.log_table[a] - 1]

    def calculate_tables(self):
        x = 1
        for i in range(self.size):
            self.exp_table[i] = x
            x <<= 1
            if x >= self.size:
                x ^= self.primitive
            self.log_table[self.exp_table[i]] = i
        self.log_table[0] = -1
