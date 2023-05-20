from hashlib import sha256     
from typing import List
#类型提醒
#从当前模块的相对路径中导入所有模块成员

# 定义默克尔树节点类  Merkle Tree 노드 클래스를 정의한다.
# MerkleNode 表示 Merkle Tree 中的节点，每个节点包含一个数据块、其哈希值以及左右子节点。
class MerkleNode:
    def __init__(self, data: bytes):
        self.data = data
        self.hash = self._calculate_hash()
        self.left = None
        self.right = None

    def _calculate_hash(self): #通过调用库 sha256 来计算该节点的哈希值
        return sha256(self.data).digest()


# 定义默克尔树类    Merkle Tree 클래스를 정의한다.
# MerkleTree 表示整个 Merkle Tree，可以通过构建 MerkleTree 对象来创建 Merkle Tree 并获取其根节点的哈希值。
class MerkleTree:
    def __init__(self, data: List[bytes]):
        self.root = self._build_tree(data)

    def _build_tree(self, data: List[bytes]) -> MerkleNode:
        if len(data) == 1:  #如果只有一个数据块 则直接返回一个叶子结点
            return MerkleNode(data[0])
        elif len(data) % 2 == 1:#否则 将 数据块分为左右两部分，并递归地构建左右字数，
            data.append(data[-1])
        mid = len(data) // 2
        left = self._build_tree(data[:mid])
        right = self._build_tree(data[mid:])
        node = MerkleNode(left.hash + right.hash)#构建父节点时，将左右字节点的哈希值拼接起来，然后在计算该节点的哈希值
        node.left = left
        node.right = right
        return node

    def get_root_hash(self) -> bytes:#用于获取默克尔树的根节点的哈希值
        return self.root.hash


# 定义主程序 메인 프로그램을 정의한다
if __name__ == '__main__':
    # 定义数据块            데이터 블록을 정의한다
    data = [b'block1', b'block2', b'block3', b'block4']
    # 构建默克尔树            Merkle Tree를 구축한다
    tree = MerkleTree(data)
    # 输出根哈希值          루트 해시 값을 출력한다
    print(tree.get_root_hash().hex()) #16진수 문자법 output
