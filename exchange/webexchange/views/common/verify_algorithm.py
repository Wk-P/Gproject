# 导入必要的库
from .merkle import MerkleTree
from .zk_snarks import generate_proof, verify_proof
from .utils import *

def combine_data(user_data, all_user_data):
    data = []
    with open('output_data.json', 'a', encoding='utf-8') as f:
        try:
            # 准备输入数据
            for i in range(len(all_user_data)):
                asset_string = " "
                for index in range(len(all_user_data[i]['assets'])):
                    asset_string += all_user_data[i]['assets'][index]['asset_type'] + str(all_user_data[i]['assets'][index]['asset_amount'])
                
                data.append(bytes(all_user_data[i]['user_ID'] + asset_string, encoding='utf8'))

            input_data = {
                'merkle_data': data,
                'zk_data': {
                    # 'secret': user_data['user_name'] + user_data['user_ID'],
                    'secret':  user_data['user_ID'],
                    'public': user_data['wallet_ID']
                }
            }
            print(f"data:{data}")
            # 调用 Merkle Tree 函数
            tree = MerkleTree(data)

            print(f"tree:{tree}") 
            merkle_root_hash = tree.get_root_hash().hex()
            print(f" merkle_root_hash: { merkle_root_hash}")
            # 调用 ZK-SNARKs 函数
            proof, signal = generate_proof(input_data['zk_data']['secret'], input_data['zk_data']['public'])
            verification_result = verify_proof(proof, signal, input_data['zk_data']['public'])
            # try:
            #     print(proof)
            #     print(signal)
            #     print(verification_result)
            # except Exception as e:
            #     print("ERROR",e)

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
                output_data['asset'].append(output_asset)

            json.dump(output_data, f)
        except Exception as e:
            print(e)
            