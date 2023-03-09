from hashlib import sha256
from random import randint
from pyfinite import *
from pyfinite import genericmatrix
from pyfinite import genericgf
from pyfinite import exceptions
'''#曲线和其生成元，这是比特币和以太坊等加密货币使用的曲线，
定义有限域和椭圆曲线上的加法和乘法操作。这些操作是用于加密和解密数据的基本操作。

 비트코인 및 이더리움 등의 암호화폐에서 사용되는 곡선과 그 생성원은 유한체와 타원곡선 상의 덧셈 및 곱셈 연산을 정의합니다. 
이러한 연산은 데이터를 암호화하고 복호화하기 위한 기본적인 작업에 사용됩니다.'''


'''使用pyfinite库来定义有限域 & 定义 FiniteField类的定义和实现
pyfinite 라이브러리를 사용하여 유한체를 정의하고 FiniteField 클래스를 구현한다
'''

class FiniteField:
    def __init__(self, prime):
        self.field = genericgf.GenericGF(2 ** 256, int(prime), 0)

    def __call__(self, value):
        return self.field(int(value))

''' 随机选择的质数，作为有限域的模数
 #유한체의 모듈로 선택된 임의의 소수를 정의한다'''
prime = 2 ** 256 - 2 ** 32 - 977


'''# 定义有限域元素的类型
# #유한체 원소의 유형을 정의한다'''
F = FiniteField(prime)

'''# 定义两个非零元素         
 #두 개의 비 영 원소를 정의한다'''
a = F(7)
b = F(13)


'''
# 定义两个非零元素的积         
#두 개의 비 영 원소의 곱을 정의한다'''
c = a * b

'''# 要证明的断言是：知道两个数字 x 和 y，使得它们的积等于 z = x * y
#증명하고자 하는 명제는 다음과 같습니다: x와 y 두 개의 숫자를 알고 있을 때, 
그들의 곱이 z = x * y와 같다는 것을 증명한다'''
x = F(42)
y = F(17)
z = x * y


'''
# 我们需要找到一个随机的 s 和 t，使得 s 和 t 的积等于 z，这样我们就可以将断言转换为 s 和 t 的相等关系
#우리는 s와 t의 곱이 z와 같아지도록 임의의 s와 t를 찾아야 한다 
이렇게하면 명제를 s와 t의 동일성 관계로 변환할 수 있다
'''
s = F(randint(1, prime-1))
t = F(z/s)


'''# 我们还需要定义一个随机的密钥 k，它将用于计算证明
#우리는 또한 증명을 계산하는 데 사용될 임의의 키 k를 정의해야한다'''
k = F(randint(1, prime-1))    #random K 생성한다

'''# 计算两个哈希值 h1 和 h2，它们将被用作证明的一部分
#증명의 일부로 사용될 두 개의 해시 값 h1과 h2를 계산한다'''
h1 = int(sha256(str(k*s).encode()).hexdigest(), 16)
h2 = int(sha256(str(k*t).encode()).hexdigest(), 16)


'''# 最终证明将包含 s 和 t 的值以及哈希值 h1 和 h2
#최종 증명에는 s와 t의 값 및 해시 값 h1과 h2가 포함된다'''
proof = (s, t, h1, h2)


'''# 定义一个函数，它将接受证明和断言作为输入，并返回一个布尔值，指示断言是否被证明
#증명과 명제를 입력으로 받아들이고, 명제가 증명되었는지 여부를 나타내는 부울 값이 반환되는 함수를 정의한다
'''
def verify(proof, z):
    s, t, h1, h2 = proof


'''    # 检查 h1 和 h2 是否与证明中的 s 和 t 对应的哈希值匹配
    #"h1"과 "h2"가 증명에서의 "s"와 "t"에 해당하는 해시 값과 일치하는지 확인한다
    '''
    if h1 != int(sha256(str(k*s).encode()).hexdigest(), 16):
        return False
    if h2 != int(sha256(str(k*t).encode()).hexdigest(), 16):
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

'''#验证证明是否正确
#증명이 올바른지 확인한다'''

assert verify(proof, z)




