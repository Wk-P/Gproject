# 导入必要的库
from .merkle import MerkleTree
from .zk_snarks import generate_proof, verify_proof
from .utils import *

def combine_data(user_data, all_user_data):
    with open('output_data.json', 'a', encoding='utf-8') as f:
        try:
            # 准备输入数据
            print(user_data)
            print(all_user_data)
            data = []
            for item in all_user_data:
                # print(item)
                asset = item['assets'][0][0]
                # print(f"ASSET: {asset}")
                data.append(str(asset["asset_type"] + str(asset["asset_amount"])).encode('utf-8'))

            input_data = {
                'merkle_data': data,
                'zk_data': {
                    'secret': user_data['user_name'] + user_data['user_ID'],
                    'public': 'my_public_key'
                }
            }  

            # not run
            # run
            # print(input_data)

            # 调用 Merkle Tree 函数
            tree = MerkleTree(data)
            merkle_root_hash = tree.get_root_hash().hex()

            # not run
            # run
            # print(merkle_root_hash)


            # 调用 ZK-SNARKs 函数

            # run
            # print(input_data['zk_data']['secret'], input_data['zk_data']['public'])
            
            # generate_proof参数对不上
            proof, signal = generate_proof(input_data['zk_data']['secret'], input_data['zk_data']['public'])
            # not run
            print(f"PROOF: {proof}, SIGNAL: {signal}")

            # run
            verification_result = verify_proof(proof, signal, input_data['zk_data']['public'])

            # not run
            # run
            # print(f"VERIFY RESULT: {verification_result}")

            # 存储输出数据
            output_data = {
                'user_name': user_data['user_name'],
                'user_ID': user_data['user_ID'],
                'merkle_root_hash': merkle_root_hash,
                'zk_proof': proof,
                'zk_verification_result': verification_result,
                'assets': []
            }
            for asset in user_data['assets']:
                output_asset = {
                    'wallet_ID':asset['wallet_ID'],
                    'asset_type':asset['asset_type'],
                    'asset_amount':asset['asset_amount']
                }
                output_data['asset'].append(output_asset)
            # not run
            print(output_data)
            json.dump(output_data, f)
            return output_data
        except Exception as e:
            return None