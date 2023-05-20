class GenericGF:
    def __init__(self, modulus, size, primitive):
        # prime=2**256-2**32-977
        self.modulus = modulus
        self.size = size
        self.primitive = primitive
        self.exp_table = [0] * (size+1) 
        self.log_table = [0] * (size+1)      
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
        print(self.log_table[a])  #output 255
        print(len(self.exp_table))  #output 257
        return self.exp_table[self.modulus - self.log_table[a] - 1]

    # def inverse(self, a):
    #     if a < 0 or a >= self.size:
    #        print("Input value is out of range.")
    #     if self.log_table[a] == 0:
    #        print("Cannot calculate inverse for zero.")
    #     return self.exp_table[self.modulus - self.log_table[a] - 1]

    

    def calculate_tables(self):
        x = 1
        for i in range(0, self.size):
            print(self.exp_table)
            print(self.log_table)
            print(x)
            self.exp_table[i] = x
            x = (x << 1) ^ ((x >> 7) * self.primitive)  # 乘法运算

            x %= self.size
            self.log_table[self.exp_table[i]] = i
        self.log_table[0] = -1













    # def calculate_tables(self):  #实现有限域GF(2^m)的元素乘法表和对数表的计算
        
    #     x = 1
    #     for i in range(self.size+1):
    #         print(self.exp_table)
    #         print(self.log_table)
    #         print(x)
    #         self.exp_table[i] = x
    #         x <<= 1  #== x=x*2
    #         if x >= self.size:
    #             x ^= self.primitive #相当于在有限域中执行模运算,
    #             print(x)
    #             print(self.size)
    #             #目的是确保有限域中的元素在执行乘法时仍然保持在有限域内，而不会出现超出有限域的情况。
    #         # self.log_table[self.exp_table[i]] = i
    #         self.log_table[x] = i
    #     self.log_table[0] = -1 #表示在有限域中，0 没有对应的对数。
        
