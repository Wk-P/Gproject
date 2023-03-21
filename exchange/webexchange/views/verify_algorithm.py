# 导入必要的库
# from merkle import MerkleTree
# from zk_snarks import generate_proof, verify_proof
from . import *


def combin_data(user_data):
    with open('output_data.json', 'a') as f:
        try:
            # 准备输入数据
            data = [asset["wallet_ID"] + asset["asset_type"] + asset["asset_amount"].encode() for asset in user_data["assets"]]
            input_data = {
                'merkle_data': data,
                'zk_data': {
                    'secret': user_data['user_name'] + user_data['user_ID'],
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
                'user_name': user_data['user_name'],
                'user_ID': user_data['user_ID'],
                'merkle_root_hash': merkle_root_hash,
                'zk_proof': proof,
                'zk_verification_result': verification_result,
                'assets':[]
            }
            for asset in user_data['assets']:
                output_asset={
                    'wallet_ID':asset['wallet_ID'],
                    'asset_type':asset['asset_type'],
                    'asset_amount':asset['asset_amount']
                }
                output_data['aaset'].append(output_asset)

            json.dump(output_data, f)
        except Exception as e:
            write_exception_log(e)