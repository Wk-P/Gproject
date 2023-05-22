from hashlib import sha256
from random import randint
# from decimal import Decimal #处理非常大的数字，并且不受Python整数范围的限制。
# from sympy import Integer
# import hashlib
# import sys
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
    # prime=2**256 - 2**32 - 977
    prime = 2 ** 5-1    
    print(f"prime:{prime}")
    
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
    # s = F(randint(1, prime-1))%3+1
    s = F(randint(1, prime-1))   #  s一旦可以实行 t也就可以
    print(f"s : {s}")
    t = F(z/s)
    print(f"t : {t}")

    print(f"prime: {prime}")

    ''' 我们还需要定义一个随机的密钥 k，它将用于计算证明,并计算出ks 和kt的哈希值h1和h2

        우리는 또한 증명을 계산하는 데 사용될 임의의 키 k를 정의해야한다'''
    # k  = F(randint(1, prime-1))  # random K 생성한다
    k  = F(randint(1, prime-1))
    print(f"k : {k}")
    print(f"k*s:{k*s}")
    print(f"k*t:{k*t}")
        

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
    params = init()
    k = params['k']
    print(f"test k:{k}")
    s = secret
    t = public
    # s = params['s']
    # t = params['t']
    z = params['z']
    prime = params['prime']
    ''' 计算两个哈希值 h1 和 h2，它们将被用作证明的一部分
    #증명의 일부로 사용될 두 개의 해시 값 h1과 h2를 계산한다'''

    print(f"prime:{prime}")
    print(f"k:{k}")

    truncated_hash_s = s[:2]
    print(f"truncated_hash_s:{truncated_hash_s}")

    truncated_hash_s_value=int(truncated_hash_s,16)
    k_s=k*truncated_hash_s_value
    print(f"k_s1:{k_s}")

    hash256_s=sha256()
    hash256_s.update(str(k_s).encode('utf-8'))
    hash_s = hash256_s.hexdigest()      
    
    print(f"hash_s:{hash_s}")

    
    # h1 = (int(Decimal(sha256(str(int(k * s)).encode()).hexdigest(), 16)))
    #使用int()函数时，传递的字符串参数无法解析为整数
    #sha256字符串 长度超过了int()函数可以处理的范围。
   

    truncated_hash_t = t[:2]
    print(f"truncated_hash_t:{truncated_hash_t}")
    print(f"k:{k}")

    truncated_hash_t_value=int(truncated_hash_t,16)
    k_t=k*truncated_hash_t_value
    print(f"Integer(k * truncated_hash_t):{k_t}")
    # print(f"str(Integer(k * truncated_hash_t))).encode():{(str(int(k_t))).encode()}")
    
    # hash_t = sha256(str(k_t).encode()).hexdigest()
    # print(f"hash_t:{hash_t}")
    #     # Convert the truncated hash to an integer
    # h2 = int(hash_t,16)
    # print(f"h2:{h2}")

    hash256_t=sha256()
    hash256_t.update(str(k_t).encode('utf-8'))
    hash_t = hash256_t.hexdigest()      
   
    print(f"hash_t:{hash_t}")


    ''' s 和 t 的值以及哈希值 hash_s 和 hash_t
    #최종 증명에는 s와 t의 값 및 해시 값 h1과 h2가 포함된다'''
    proof = (s, t, hash_s, hash_t)  #返回了一个包含这四个的元组
    print(f"proof:{proof}")
    print(f"prime:{prime}")
    
    # print(f"z:{z}")
    # print(f"prime:{prime}")
    return (proof, z, prime,k)
    '''
        最终的证明将包含k_s和k_t的值和哈希值的h1和h2，
    定义了一个函数verify来接受证明和断言作为输入，
    并返回一个布尔值，指示断言是否被证明。verify函数检查hash_s和hash_t是否与证明中的
    k_s和k_t对应的哈希值(hash_s_proof,hash_t_proof)匹配，
    如果匹配，则返回True，否则返回False。
    '''

def verify_proof(proof, z,prime,k):  # 最终的证明将包含s和t的值和哈希值的h1和h2，
    s, t, hash_s, hash_t = proof
    print(f"s:{s}")
    print(f"z:{z}")
    print(f"t:{t}")
    print(f"k:{k}")
    print(f"prime:{prime}")
    print(f"hash_s:{hash_s}")
    print(f"hash_t:{hash_t}")
    '''    # 检查 hash_s 和 hash_t 是否与证明中的 s 和 t 对应的哈希值匹配
    #"h1"과 "h2"가 증명에서의 "s"와 "t"에 해당하는 해시 값과 일치하는지 확인한다
    '''
    truncated_hash_s = s[:2]
    truncated_hash_s_value=int(truncated_hash_s,16)
    print(f"truncated_hash_s_value:{truncated_hash_s_value}")
    k_s_proof=int(k*truncated_hash_s_value)
    # print(f"k_s2:{k_s}")

    hash256_s_proof=sha256()
    hash256_s_proof.update(str(k_s_proof).encode('utf-8'))
    hash_s_proof = hash256_s_proof.hexdigest()      
    print(f"hash_s_proof:{hash_s_proof}")


    truncated_hash_t = t[:2]
    truncated_hash_t_value=int(truncated_hash_t,16)
    print(f"truncated_hash_t_value:{truncated_hash_t_value}")
    k_t_proof=int(k*truncated_hash_t_value)
    # print(f"k_t3:{k_t}")

    hash256_t_proof=sha256()
    hash256_t_proof.update(str(k_t_proof).encode('utf-8'))
    hash_t_proof = hash256_t_proof.hexdigest()      
    print(f"hash_t_proof:{hash_t_proof}")

    # F=FiniteField(prime)
    # z_proof=int(F(k_s*k_t),16)
    z_proof=(k*truncated_hash_s_value)*(k*truncated_hash_t_value)
    print(f"z_proof:{z_proof}")

    prime_proof=(prime)
    print(f"prime_proof:{prime_proof}") 



    print(f"hash_s:{hash_s}")
    print(f"hash_t:{hash_t}")
    print(f"hash_s_proof:{hash_s_proof}")
    print(f"hash_t_proof:{hash_t_proof}")

    if hash_s==hash_s_proof:
        print(f"hash_s = hash_s_proof is ok:{hash_s==hash_s_proof}")
    else:
        return False
    
    if hash_t == hash_t_proof:
        print(f"hash_t = hash_t_proof is ok:{hash_t == hash_t_proof}")
    else:

        return False

   
    

    '''    # 检查 k_s 和 k_t 是否是有限域中的非零元素
    #"s"와 "t"가 유한체에서의 비영원 원소인지 확인한다
    '''
    print(f"k_s_proof:{k_s_proof}")
    print(f"k_t_proof:{k_t_proof}")
    print(f"prime:{prime}")
    

    """取模运算可以将一个数限制在一个特定的范围内，确保其值不会超过该范围,
    限制在0到prime-1的范围内
    """
    if(0 <k_s_proof %prime< prime and 0 < k_t_proof%prime< prime):
        print(f"k_s_proof%prime:{k_s_proof%prime}")
        print(f"k_t_proof%prime:{k_t_proof%prime}")
        print(f"0 < k_s_proof < prime_proof&0 < k_t_proof < prime_proof is ok : {0 < k_s_proof%prime < prime and 0 < k_t_proof%prime < prime}")
     
    else:
        return False

    '''    # 检查 k_s_proof 和 k_t_proof 的积是否等于 z_proof
    #"k_s_proof"와 "k_t_proof"의 곱이 "z_proof"와 같은지 확인한다
    k_s_proof，k_t_proof value 확인 안 된다'''



    if k_s_proof*k_t_proof == z_proof:
        print(f"k_s_proof * k_t_proof == z_proof:{k_s_proof*k_t_proof == z_proof}")
    else:
        return False

    return True



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
        return self.field.inverse(int(value))  #8
    #value参数可以是任意整数值，表示要计算其逆元素的值
