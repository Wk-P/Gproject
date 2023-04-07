def generate_proof(secret, public):
    # 假设这里使用了一个非常简单的算法来生成zk-SNARKs证明
    
    proof = secret + public
    signal = hash(proof)
    return proof, signal

def verify_proof(proof, signal, public):
    # 假设这里使用了一个非常简单的算法来验证zk-SNARKs证明
    
    expected_signal = hash(proof)
    return signal == expected_signal