class Node:
    def __init__(self, key):
        self.key = key
        self.prev= None
        self.next = None


class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.map = {}
        self.head = Node(-1)
        self.last = Node(-1)
        self.head.next = self.last
        self.last.prev = self.head


    def print(self):
        node = self.head.next
        while(node != self.last):
            print(str(node.key)+ '-->')
            node=node.next

        print('============')
        print(self.map)
        print('============')

        return

    def put(self,key, value):
        if self.map.get(key):
            self.reset(key, value)
        else:
            if len(self.map) < self.capacity:
                self.add(key, value)
            else:
                self.add(key, value)
                self.remove()

        self.print()

    def get(self,key):
        if self.map.get(key):
            self.reset(key, self.map.get(key))
            self.print()
            return self.map.get(key)
        self.print()
        return -1


    def reset(self, key, value):
        self.map[key] = value
        self.remove(key)
        self.add(key, value)
        self.print()


    def add(self,key, value):
        self.map[key] = value
        node = Node(key)
        prevNode = self.last.prev
        prevNode.next = node
        node.next = self.last
        node.prev = prevNode
        self.last.prev = node

    def remove(self, key=None):
        if key:
        #     find the key
            node = self.head
            self.map.pop(key)
            while(node.next):
                if node.key == key:
                    break
                node = node.next
            node.prev.next =node.next
            node.next.prev =node.prev
            node.prev = None
            node.next = None

        else:
            node = self.head.next
            self.map.pop(node.key)
            self.head.next = node.next
            node.next.prev = self.head
            node.prev = None
            node.next = None






if __name__ == '__main__':
    s =LRUCache(5)
    s.put(1,'abc')
    s.put(2, 'adad')
    s.put(3, 'asadad')
    print(s.get(1))
    s.put(4, 'asdcscdf')
    s.put(5, 'dadacxd')
    s.put(6, 'dasasxas')
    s.put(4, 'asdcs')
    print(s.get(4))
    print(s.get(1))
    print(s.get(5))
    s.put(1,'asdada')




