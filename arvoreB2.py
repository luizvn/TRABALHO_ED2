import json
import pandas as pd

class BTreeNode:
    def __init__(self, t, folha=False):
        self.t = t
        self.folha = folha
        self.chaves = []
        self.children = []

    def insert_non_full(self, key):
        i = len(self.chaves) - 1
        if self.folha:
            self.chaves.append((None, None))
            while i >= 0 and key[0] < self.chaves[i][0]:
                self.chaves[i + 1] = self.chaves[i]
                i -= 1
            self.chaves[i + 1] = key
        else:
            while i >= 0 and key[0] < self.chaves[i][0]:
                i -= 1
            i += 1
            if len(self.children[i].chaves) == 2 * self.t - 1:
                self.split_child(i, self.children[i])
                if key[0] > self.chaves[i][0]:
                    i += 1
            self.children[i].insert_non_full(key)

    def split_child(self, i, y):
        t = self.t
        z = BTreeNode(t, y.folha)
        self.children.insert(i + 1, z)
        self.chaves.insert(i, y.chaves[t - 1])
        z.chaves = y.chaves[t:(2 * t - 1)]
        y.chaves = y.chaves[0:(t - 1)]
        if not y.folha:
            z.children = y.children[t:(2 * t)]
            y.children = y.children[0:t]

    def traverse(self):
        i = 0
        for i in range(len(self.chaves)):
            if not self.folha:
                self.children[i].traverse()
            print(self.folha, self.chaves[i])
        if not self.folha:
            self.children[i].traverse()
        '''for i in range(len(self.chaves)):
            if not self.folha:
                self.children[i].traverse()
            print(self.t, " - ", self.chaves[i])
        if not self.folha:
            self.children[i].traverse()'''

    def search(self, key):
        i = 0
        while i < len(self.chaves) and key > self.chaves[i][0]:
            i += 1
        if i < len(self.chaves) and key == self.chaves[i][0]:
            return self.chaves[i]
        if self.folha:
            return None
        return self.children[i].search(key)

class BTree:
    def __init__(self, t):
        self.root = BTreeNode(t, True)
        self.t = t

    def insert(self, key):
        root = self.root
        if len(root.chaves) == (2 * self.t) - 1:
            temp = BTreeNode(self.t)
            self.root = temp
            temp.children.insert(0, root)
            temp.folha = False
            temp.split_child(0, root)
            temp.insert_non_full(key)
        else:
            root.insert_non_full(key)

    def traverse(self):
        if self.root:
            self.root.traverse()

    def search(self, key):
        if self.root:
            return self.root.search(key)
        else:
            return None

    def load_from_json(self, json_data):
        for key, value in json_data.items():
            self.insert((int(key), value))

    def to_dict(self):
        def node_to_dict(node):
            result = {}
            result['chaves'] = node.chaves
            if not node.folha:
                result['children'] = [node_to_dict(child) for child in node.children]
            return result
        return node_to_dict(self.root)

def main():
    # Carregar dados do arquivo JSON
    with open('catalogo.json', 'r') as file:
        data = json.load(file)
    
    # Criar a árvore B
    b_tree = BTree(t=7)
    
    # Carregar dados do JSON na árvore B
    b_tree.load_from_json(data)
    
    # Exemplo de travessia da árvore
    print("Travessia da árvore B:")
    b_tree.traverse()
    
    # Exemplo de busca
    key_to_search = 6
    result = b_tree.search(key_to_search)
    if result:
        print(f"Encontrado: {result}")
    else:
        print(f"Não encontrado: {key_to_search}")

if __name__ == '__main__':
    main()