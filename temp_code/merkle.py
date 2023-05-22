from hashlib import sha256     
from typing import List
# Defines the Merkle Tree node class.
class MerkleNode:
    def __init__(self, data: bytes):
        self.data = data
        self.hash = self._calculate_hash()
        self.left = None
        self.right = None

    def _calculate_hash(self): #Call the library sha256 to calculate the node's hash value
        return sha256(self.data).digest()
#     Merkle Tree 클래스를 정의한다.
class MerkleTree:
    def __init__(self, data: List[bytes]):
        self.root = self._build_tree(data)

    def _build_tree(self, data: List[bytes]) -> MerkleNode:
        if len(data) == 1:  #If there is only one data block, then directly return a leaf node
            return MerkleNode(data[0])
#Otherwise, divide the data block into left and right parts, and recursively build the left and right word counts
        elif len(data) % 2 == 1:
            data.append(data[-1])
        mid = len(data) // 2
        left = self._build_tree(data[:mid])
        right = self._build_tree(data[mid:])
        node = MerkleNode(left.hash + right.hash)
#When constructing the parent node, the hash values ​​of the left and right nodes are concatenated,
#  and then the hash value of the node is calculated
        node.left = left
        node.right = right
        return node

    def get_root_hash(self) -> bytes:#Used to get the hash value of the root node of the Merkle tree
        return self.root.hash
if __name__ == '__main__':
    #Define data blocks
    data = [b'block1', b'block2', b'block3', b'block4']
    # Build a Merkle tree
    tree = MerkleTree(data)
    # output root hash
    print(tree.get_root_hash().hex()) #16진수 문자법 output
