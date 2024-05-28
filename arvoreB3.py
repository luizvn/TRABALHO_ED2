import json

class BTreeNode:
    def __init__(self, t, leaf=False):
        self.t = t
        self.leaf = leaf
        self.keys = []
        self.children = []

    def insert_non_full(self, k):
        i = len(self.keys) - 1
        if self.leaf:
            self.keys.append(None)
            while i >= 0 and k < self.keys[i]:
                self.keys[i + 1] = self.keys[i]
                i -= 1
            self.keys[i + 1] = k
        else:
            while i >= 0 and k < self.keys[i]:
                i -= 1
            i += 1
            if len(self.children[i].keys) == 2 * self.t - 1:
                self.split_child(i, self.children[i])
                if k > self.keys[i]:
                    i += 1
            self.children[i].insert_non_full(k)

    def split_child(self, i, y):
        t = self.t
        z = BTreeNode(t, y.leaf)
        self.children.insert(i + 1, z)
        self.keys.insert(i, y.keys[t - 1])
        z.keys = y.keys[t:(2 * t - 1)]
        y.keys = y.keys[0:(t - 1)]
        if not y.leaf:
            z.children = y.children[t:(2 * t)]
            y.children = y.children[0:t]

    def traverse(self, data):
        i = 0
        while i < len(self.keys) and 7 > self.keys[i]:
            print(self.leaf, self.keys[i])
            i += 1
        if i < len(self.keys) and 7 == self.keys[i]:
            print(self.leaf, self.keys[i])
            return self.keys[i]
        if self.leaf:
            return None
        return self.children[i].search(7)
        '''i = 0
        for i in range(len(self.keys)):
            if not self.leaf:
                print('1')
                self.children[i].traverse(data)
            print(self.leaf, self.keys[i], " - ", data[str(self.keys[i])])
        if not self.leaf:
            self.children[i].traverse(data)'''

    '''def traverse(self, data):
            i = 0
            for i in range(len(self.keys)):
                if not self.leaf:
                    self.children[i].traverse(data)
                print(self.keys[i], " - ", data[str(self.keys[i])])
            if not self.leaf:
                self.children[i].traverse(data)'''

    def search(self, k):
        i = 0
        while i < len(self.keys) and k > self.keys[i]:
            i += 1
        if i < len(self.keys) and k == self.keys[i]:
            return self.keys[i]
        if self.leaf:
            return None
        return self.children[i].search(k)
    
class BTree:
    def __init__(self, t):
        self.root = BTreeNode(t, True)
        self.t = t

    def insert(self, k):
        root = self.root
        if len(root.keys) == (2 * self.t) - 1:
            temp = BTreeNode(self.t)
            self.root = temp
            temp.children.insert(0, root)
            temp.leaf = False
            temp.split_child(0, root)
            temp.insert_non_full(k)
        else:
            root.insert_non_full(k)

    def traverse(self, data):
        if self.root:
            self.root.traverse(data)

    def search(self, k):
        if self.root:
            return self.root.search(k)
        else:
            return None

    def load_from_json(self, json_data):
        for key in json_data.keys():
            self.insert(int(key))

def main():
    # Carregar dados do arquivo JSON
    with open('catalogo.json', 'r') as file:
        data = json.load(file)
    
    # Criar a árvore B
    t = 2
    b = BTree(t)
    
    # Carregar dados do JSON na árvore B
    b.load_from_json(data)
    
    # Exemplo de travessia da árvore
    print("Travessia da árvore B:")
    b.traverse(data)
    
    # Exemplo de busca
    key_to_search = 7
    result = b.search(key_to_search)
    if result:
        print(f"Encontrado: {result} - {data[str(result)]}")
    else:
        print(f"Não encontrado: {key_to_search}")

if __name__ == '__main__':
    main()