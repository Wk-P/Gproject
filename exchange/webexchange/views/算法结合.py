# 导入必要的库
# from merkle import MerkleTree
# from zk_snarks import generate_proof, verify_proof
from . import *

         # def 
# 准备输入数据
data = [b'block1', b'block2', b'block3', b'block4']
input_data = {
    'merkle_data': data,
    'zk_data': {
        'secret': 'my_secret_key',
        'public': 'my_public_key'
    }
}

# 调用 Merkle Tree 函数
tree = MerkleTree(data)
merkle_root_hash = tree.get_root_hash().hex()

# 调用 ZK-SNARKs 函数
proof, signal = generate_proof(input_data['zk_data']['secret'], input_data['zk_data']['public'])
verification_result = verify_proof(proof, signal, input_data['zk_data']['public'])

# 存储输出数据
output_data = {
    'merkle_root_hash': merkle_root_hash,
    'zk_proof': proof,
    'zk_verification_result': verification_result
}

# 调用 verifytest.py
run_test(input_data, output_data)
