from hashlib import sha256
from random import randint
from decimal import Decimal #处理非常大的数字，并且不受Python整数范围的限制。
from sympy import Integer
import hashlib
import sys
# import gmpy2 
# from sympy import FiniteField #处理访问索引超出范围，因该库提供了有限域的定义和操作，确保在进行运算时索引不会超出范围。
# from pyfinite import genericmatrix
# from pyfinite import genericgf
# from pyfinite import exceptions
# 使用pyfinite库  来定义了一个有限域，该有限域采用了一个随机选择的质数作为模数，

from .genericgf import GenericGF

'''#曲线和其生成元，这是比特币和以太坊等加密货币使用的曲线，
定义有限域和椭圆曲线上的加法和乘法操作。这些操作是用于加密和解密数据的基本操作。

 비트코인 및 이더리움 등의 암호화폐에서 사용되는 곡선과 그 생성원은 유한체와 타원곡선 상의 덧셈 및 곱셈 연산을 정의합니다. 
이러한 연산은 데이터를 암호화하고 복호화하기 위한 기본적인 작업에 사용됩니다.'''


def init():
    ''' 随机选择的质数，作为有限域的模数
    유한체의 모듈로 선택된 임의의 소수를 정의한다
    '''
    """
        prime：是一个素数，用于定义有限域GF(2^31)的模数
        GenericGF：是一个特定的多项式 且次数为256，用于定义扩展有限域GF(2^256)的参数

        ZKSNARKs算法中，我们可以使用有限域GF(2^31)来表示底层的二进制数值，
        并使用扩展有限域GF(2^256)来进行算法的加密和解密操作



        和155行的 GenericGF(2**256, int(prime), 0)   两者可以同时使用，区别在于
        前者一个是使用一个素数作为模数，后者则是使用一个特定的多项式作为模数。
  

     """
    # prime = mod() # 163行
    # prime = 2 ** 16-1  #65535
    # prime=2**3-1 #genericgf.py中 第 29行引用到
    # prime=2**256 - 2**32 - 977
    
    prime = 2 ** 5-1     #5-8都是可用的 
    max_int = sys.maxsize


    # F = FiniteField(int(prime))
    # F = FiniteField(64,prime,1)
    F = FiniteField(prime)
    print(f"F : {F}")

    ''' 定义两个非零元素         
        두 개의 비 영 원소를 정의한다'''
    a = F(8)
    print(f"a: {a}")
    b = F(15)
    print(f"b: {b}")
    '''
         定义两个非零元素的积         
        두 개의 비 영 원소의 곱을 정의한다'''
    c = a * b

    print(f"c : {c}")
    ''' 
        #증명하고자 하는 명제는 다음과 같습니다: x와 y 두 개의 숫자를 알고 있을 때, 
        그들의 곱이 z = x * y와 같다는 것을 증명한다'''
    x = F(20)
    print(f"x : {x}")
    y = F(17)
    print(f"y : {y}")

    z = x * y    #要证明的断言
    print(f"z : {z}")
    '''要证明的断言是：已知两个数字x和y，使得它们的积等于z = x * y，为了证明这个断言 算法使用了一个随机的s和t，
        使得他们积等于z 然后生成2个哈希值h1和h2，并将它们作为证明的一部分。
        '''

    '''
         我们需要找到一个随机的 s 和 t，使得 s 和 t 的积等于 z，这样我们就可以将断言转换为 s 和 t 的相等关系
        #우리는 s와 t의 곱이 z와 같아지도록 임의의 s와 t를 찾아야 한다 
        #이렇게하면 명제를 s와 t의 동일성 관계로 변환할 수 있다
        '''
    # maxint=2**30-1
    s = F(randint(1, prime-1))   #  s一旦可以实行 t也就可以
    print(f"s : {s}")
    t = F(z/s)
    print(f"t : {t}")

    print(f"prime: {prime}")

    ''' 我们还需要定义一个随机的密钥 k，它将用于计算证明,并计算出ks 和kt的哈希值h1和h2

        우리는 또한 증명을 계산하는 데 사용될 임의의 키 k를 정의해야한다'''
    # k  = F(randint(1, prime-1))  # random K 생성한다
    k  = F(randint(1, prime-1)) % 3+1
    print(f"k : {k}")
    print(f"k*s:{k*s}")
    print(f"k*t:{k*t}")





    data = b'This is the data to be hashed'

    hash_object = hashlib.sha1()
    hash_object.update(data)
    sha1_hash = hash_object.digest()

    print("SHA-1 hash:", sha1_hash)
        

    hash_object = hashlib.sha256()
    hash_object.update(data)
    sha256_hash = hash_object.digest()

    print("SHA-256 hash:", sha256_hash)
        





    return {
        'k': k,
        's': s,
        't': t,
        'z': z,
        'prime': prime
    }




''' 定义一个函数，它将接受证明和断言作为输入，并返回一个布尔值，指示断言是否被证明
#증명과 명제를 입력으로 받아들이고, 명제가 증명되었는지 여부를 나타내는 부울 값이 반환되는 함수를 정의한다

'''
def generate_proof(secret,public):
    print(f"secret:{secret}")
    print(f"public:{public}")
    global params 
    # max_int = sys.maxsize
    params = init()
    k = params['k']
    print(f"testk:{k}")
    s = secret
    t = public
    # s = params['s']
    # t = params['t']
    z = params['z']
    prime = params['prime']
    ''' 计算两个哈希值 h1 和 h2，它们将被用作证明的一部分
    #증명의 일부로 사용될 두 개의 해시 값 h1과 h2를 계산한다'''

    # modulus=2**4-1
    # try:
    #     h1 = int(sha256(str(int(k * s)).encode()).hexdigest(), 16)
    #     h1 = h1 % modulus
    #     print(f"h1:{h1}")
    # except ValueError:
    #     print("h1 is not a valid integer")
    #     h1 = None

    # return h1
   

    # max_int = sys.maxsize
    
    # try:
    #     # Compute the full hash value
    #     full_hash = sha256(str(int(k * s)).encode()).hexdigest()

    #     # Truncate the hash value to the first 32 characters
    #     truncated_hash = full_hash[:32]

    #     # Convert the truncated hash to an integer
    #     h1 = int(Decimal(truncated_hash, 16))

    #     if h1 > max_int:
    #         print("h1 exceeds the maximum integer value")
    #         h1 = None
    # except ValueError:
    #     print("h1 is not a valid integer")
    #     h1 = None

    # return h1

    print(f"prime:{prime}")
    truncated_hash_s = s[:2]
    print(f"truncated_hash_s:{truncated_hash_s}")
    print(f"k:{k}")
    print(f"Integer(k * truncated_hash_s):{Integer(k * truncated_hash_s)}")
    print(f"str(Integer(k * truncated_hash_s))).encode().hexdigest():{(str(Integer(k * truncated_hash_s))).encode()}")
    # hash_s = sha256(str(Integer(k * truncated_hash_s))).encode().hexdigest()
    hash_s = sha256(str(Integer(k * truncated_hash_s)).encode()).hexdigest()
    print(f"hash_s:{hash_s}")
        # Truncate the hash value to the first 32 characters
    # truncated_hash_s = full_hash_s[:5]

        # Convert the truncated hash to an integer
    h1 = int(hash_s,16)



    # try:
    #     h1 = int(Decimal(sha256(str(int(k * s)).encode()).hexdigest(), 16))
    #     if h1 > max_int:
    #         print("h1 exceeds the maximum integer value")
    #         h1 = None
    # except ValueError:
    #     # 处理无法转换为整数的情况
    #     print("h1 is not a valid integer")
    #     h1 = None

    # return h1


    
    # h1 = (int(Decimal(sha256(str(int(k * s)).encode()).hexdigest(), 16)))
    #使用int()函数时，传递的字符串参数无法解析为整数
    #sha256字符串 长度超过了int()函数可以处理的范围。
   
    

    truncated_hash_t = t[:2]
    print(f"truncated_hash_t:{truncated_hash_t}")
    print(f"k:{k}")
    print(f"Integer(k * truncated_hash_t):{Integer(k * truncated_hash_t)}")
    print(f"str(Integer(k * truncated_hash_t))).encode().hexdigest():{(str(Integer(k * truncated_hash_t))).encode()}")
    
    hash_t = sha256(str(Integer(k * truncated_hash_t)).encode()).hexdigest()
    print(f"hash_t:{hash_t}")
        # Truncate the hash value to the first 32 characters
    # truncated_hash_s = full_hash_s[:5]

        # Convert the truncated hash to an integer
    h2 = int(Decimal(hash_t, 16))
    # h2 = (int(Decimal(sha256(str(int(k * t)).encode()).hexdigest(), 16)))
    
    
    
    
    # h1 = int(sha256(str(int(k * s)).encode()).hexdigest(),16)
    # h2 = int(sha256(str(int(k * t)).encode()).hexdigest(),16)

    # print(f"k*s:{k*s}")
    # print(f"k*t:{k*t}")


    ''' s 和 t 的值以及哈希值 h1 和 h2
    #최종 증명에는 s와 t의 값 및 해시 값 h1과 h2가 포함된다'''
    proof = (s, t, h1, h2)  #返回了一个包含这四个的元组

    return (proof, verify_proof(proof, z, k, prime))
    '''
        最终的证明将包含s和t的值和哈希值的h1和h2，
    定义了一个函数verify来接受证明和断言作为输入，
    并返回一个布尔值，指示断言是否被证明。verify函数检查h1和h2是否与证明中的s和t对应的哈希值匹配，
    如果匹配，则返回True，否则返回False。
    '''

def verify_proof(proof, z, k, prime):  # 最终的证明将包含s和t的值和哈希值的h1和h2，
    s, t, h1, h2 = proof
    max_int = sys.maxsize

    '''    # 检查 h1 和 h2 是否与证明中的 s 和 t 对应的哈希值匹配
    #"h1"과 "h2"가 증명에서의 "s"와 "t"에 해당하는 해시 값과 일치하는지 확인한다
    '''
    if h1 != (int(Integer(sha256(str(int(k * s)).encode()).hexdigest(), 16))):
        return False
    if h2 != (int(Integer(sha256(str(int(k * t)).encode()).hexdigest(), 16))):

        return False

   

    

    '''    # 检查 s 和 t 是否是有限域中的非零元素
    #"s"와 "t"가 유한체에서의 비영원 원소인지 확인한다
    '''
    if not (0 < s < prime and 0 < t < prime):
        return False

    '''    # 检查 s 和 t 的积是否等于 z
    #"s"와 "t"의 곱이 "z"와 같은지 확인한다
    s，t value 확인 안 된다'''

    if s*t != z:
        return False

    return True

# params = {}



class FiniteField:
    def __init__(self, prime):
        """
        当使用一个很大的数作为模数时，
        会导致在计算加法、乘法和求逆元素等操作时产生很大的中间结果，
        从而导致栈溢出。这是因为Python默认的递归深度限制为1000，
        当递归深度超过这个限制时就会引发RecursionError。

        为了避免这种情况，可以使用非递归的算法或者优化递归算法的实现，
        或者使用特殊的数据结构（如多项式）来存储中间结果，从而减小内存使用量。
        此外，也可以通过增加Python的递归深度限制来解决该问题，但这可能会导致其他问题，
        例如性能下降或内存消耗增加。因此，需要根据具体情况来选择最适合的解决方案。
        """
        
        self.field = GenericGF(prime,256,primitive=3)  #创建一个列表或数组，而访问的索引超出了范围。
            # self.field.append(primitive=2)
    def __call__(self, value):
        print(value) #output
        # return self.field.inverse(int(str(value)))
        return self.field.inverse(int(value))
    #value参数可以是任意整数值，表示要计算其逆元素的值







# class mod:
#     def add_mod(x, y, prime):
    
#     # 计算模数为 prime 的两个数 x 和 y 的和，使用位运算避免溢出。
    
#         return (x + y) & (prime - 1)

#     def sub_mod(x, y, prime):
        
#         # 计算模数为 prime 的两个数 x 和 y 的差，使用位运算避免溢出。
        
#         return (x - y) & (prime - 1)

#     def mul_mod(x, y, prime):
        
#         # 计算模数为 prime 的两个数 x 和 y 的积，使用位运算避免溢出。
        
#         return (x * y) & (prime - 1)

#     def pow_mod(x, n, prime):
        
#         # 计算模数为 prime 的数 x 的 n 次幂，使用快速幂算法优化。
    
#         result = 1
#         while n > 0:
#             if n % 2 == 1:
#                 result = mul_mod(result, x, prime)  #mul_mod 210行
#             x = mul_mod(x, x, prime)
#             n //= 2
#         return result

#     def inv_mod(x, prime):
        
#         # 计算模数为 prime 的数 x 的逆元素，使用扩展欧几里得算法优化。
        
#         a, b, u = x, prime, 1
#         v, t = 0, 0
#         while b != 0:
#             q = a // b
#             a, b = b, a - q * b
#             u, v = v, u - q * v
#             t, s = s, t - q * s
#         if u < 0:
#             u += prime
#         return u


# class mul_mod:
#      def mul_mod(a, b, m):
#     # 将 a 和 b 转换为二进制字符串
#         a_bin = bin(a)[2:]
#         b_bin = bin(b)[2:]

#     # 用 0 填充较短的二进制字符串，使两个字符串长度相等
#         max_len = max(len(a_bin), len(b_bin))
#         a_bin = a_bin.zfill(max_len)
#         b_bin = b_bin.zfill(max_len)

#         # 初始化结果为 0
#         result = 0

#         # 从低位到高位遍历二进制字符串
#         for i in range(max_len):
#             # 如果当前位是 1，则将对应的乘积加到结果中
#             if a_bin[-i-1] == '1':
#                 result += b << i

#             # 对结果取模
#             result %= m

#         return result

