from hashlib import sha256
from random import randint
from .genericgf import GenericGF

'''
 비트코인 및 이더리움 등의 암호화폐에서 사용되는 곡선과 그 생성원은 유한체와 타원곡선 상의 덧셈 및 곱셈 연산을 정의합니다. 
이러한 연산은 데이터를 암호화하고 복호화하기 위한 기본적인 작업에 사용됩니다.'''
def init():
    # Define a random prime number chosen as a modulo of a finite field
        #  define two non-zero elements

    prime = 2 ** 5-1    
 
    
    F = FiniteField(prime)
    print(f"F : {F}")
    a = F(8)
    b = F(15)    
        # Defines the product of two nonzero elements
    c = a * b
    '''The proposition we want to prove is: Given two numbers x and y,
        Prove that their product is equal to z = x * y '''
    x = F(20)
    y = F(17)
    z = x * y    #assertion to prove
    '''The assertion to be proved is: Two numbers x and y are known such that their product is equal to z = x * y. 
    To prove this assertion, the algorithm uses a random s and t,
    Make their product equal to z Then generate 2 hash values ​​h1 and h2, and use them as part of the proof.
        '''

    '''
    We need to find a random s and t such that the product of s and t is equal to z, 
    so we can convert the assertion into an equality relation of s and t
        '''
    # s = F(randint(1, prime-1))%3+1
    s = F(randint(1, prime-1))  
    t = F(z/s)
    '''We also need to define a random key k, which will be used to calculate the proof, 
    and calculate the hash values ​​​​h1 and h2 of ks and kt '''
    # k  = F(randint(1, prime-1))  # random K 생성한다
    k  = F(randint(1, prime-1))
    return {
        'k': k,
        's': s,
        't': t,
        'z': z,
        'prime': prime
    }

''' Define a function that will take a proof 
and an assertion as input and return a boolean indicating whether the assertion is proven
'''
def generate_proof(secret,public):
    global params
    params = init()
    k = params['k']
    s = secret
    t = public
    z = params['z']
    prime = params['prime']
    ''' Compute two hash values ​​h1 and h2 which will be used as part of the proof'''
    truncated_hash_s = s[:2]
    truncated_hash_s_value=int(truncated_hash_s,16)
    k_s=k*truncated_hash_s_value
    hash256_s=sha256()
    hash256_s.update(str(k_s).encode('utf-8'))
    hash_s = hash256_s.hexdigest()      
   
    truncated_hash_t = t[:2]
    truncated_hash_t_value=int(truncated_hash_t,16)
    k_t=k*truncated_hash_t_value
    hash256_t=sha256()
    hash256_t.update(str(k_t).encode('utf-8'))
    hash_t = hash256_t.hexdigest()      
    #  Values ​​of s and t and hash values ​​hash_s and hash_t
    proof = (s, t, hash_s, hash_t)  #returns a tuple containing the four
    return (proof, z, prime,k)
    '''
        The final proof will contain the values ​​of k_s and k_t and h1 and h2 of the hash values,
    A function verify is defined to accept proofs and assertions as input,
    and returns a boolean indicating whether the assertion was proven. 
    The verify function checks whether hash_s and hash_t are the same as those in the proof
    The hash values ​​(hash_s_proof, hash_t_proof) corresponding to k_s and k_t match,
    Returns True if it matches, otherwise returns False.
    '''

def verify_proof(proof, z,prime,k):  # The final proof will contain the values ​​of s and t and the hash values ​​h1 and h2,
    s, t, hash_s, hash_t = proof
# Check that hash_s and hash_t match the hash values ​​corresponding to s and t in the proof
    
    truncated_hash_s = s[:2]
    truncated_hash_s_value=int(truncated_hash_s,16)
    k_s_proof=int(k*truncated_hash_s_value)
    hash256_s_proof=sha256()
    hash256_s_proof.update(str(k_s_proof).encode('utf-8'))
    hash_s_proof = hash256_s_proof.hexdigest()      
    
    
    truncated_hash_t = t[:2]
    truncated_hash_t_value=int(truncated_hash_t,16)
    k_t_proof=int(k*truncated_hash_t_value)
    hash256_t_proof=sha256()
    hash256_t_proof.update(str(k_t_proof).encode('utf-8'))
    hash_t_proof = hash256_t_proof.hexdigest()   

    # F=FiniteField(prime)
    # z_proof=int(F(k_s*k_t),16)
    z_proof=(k*truncated_hash_s_value)*(k*truncated_hash_t_value)

    if hash_s==hash_s_proof:
        print(f"hash_s = hash_s_proof is ok:{hash_s==hash_s_proof}")
    else:
        return False
    
    if hash_t == hash_t_proof:
        print(f"hash_t = hash_t_proof is ok:{hash_t == hash_t_proof}")
    else:

        return False
#checks whether k_s and k_t are nonzero elements in the finite field
    """The modulo operation can limit a number within a specific range, 
    ensuring that its value will not exceed this range,
    limited to the range 0 to prime-1
    """
    if(0 <k_s_proof %prime< prime and 0 < k_t_proof%prime< prime):
        print(f"0 < k_s_proof < prime_proof&0 < k_t_proof < prime_proof is ok : {0 < k_s_proof%prime < prime and 0 < k_t_proof%prime < prime}")
     
    else:
        return False

    #Check if the product of k_s_proof and k_t_proof is equal to z_proof
    if k_s_proof*k_t_proof == z_proof:
        print(f"k_s_proof * k_t_proof == z_proof:{k_s_proof*k_t_proof == z_proof}")
    else:
        return False

    return True

class FiniteField:
    def __init__(self, prime):
        # A list or array was created and an index accessed was out of bounds.
        self.field = GenericGF(prime,256,primitive=3)  
    def __call__(self, value):
        return self.field.inverse(int(value))  
    #The value parameter can be any integer value,
    #  indicating the value of its inverse element to be calculated
