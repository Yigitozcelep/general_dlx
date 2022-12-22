class Node:
    def __init__(self, id, parent, answer): self.up, self.right, self.down, self.left, self.parent, self.name, self.id, self.answer = None, None, None, None, parent, "n", id, answer

class Header:
    def __init__(self, id): self.up, self.right, self.down, self.left, self.total_1, self.name, self.id, self.parent = None, None, None, None, 0, "h", id, self

def create_nodes(ids, header_list, copy_list, answer):
    parents = [header_list[id] for id in ids]
    nodes = [Node(id, header_list[id], answer) for id in ids]
    us = [copy_list[id] for id in ids]
    for parent in parents: parent.total_1 += 1
    before = initial = nodes[0]
    for node in nodes[1:]:
        node.left = before
        before.right = node
        before = node
    initial.left = nodes[-1]
    nodes[-1].right = initial
    
    for i, u in enumerate(us):
        u.down = nodes[i]
        nodes[i].up = u
    
    for i, parent in enumerate(parents):
        parent.up = nodes[i]
        nodes[i].down = parent

    for i, id in enumerate(ids): copy_list[id] = nodes[i]

    
def get_min_col(initial):
    before = min_node = initial.right
    while before.right != initial:
        before = before.right
        if before.total_1 < min_node.total_1: min_node = before

    return min_node



    
def cover(node):
    before = col = node.parent
    col.left.right = col.right
    col.right.left = col.left
    while before.down.name != "h":
        current = before = before.down
        while current.right != before:
            current = current.right
            current.up.down = current.down
            current.down.up = current.up
            current.parent.total_1 += -1


def uncover(node):
    before = col = node.parent
    while before.up.name != "h":
        current = before = before.up
        while current.left != before:
            current = current.left
            current.up.down = current
            current.down.up = current
            current.parent.total_1 += 1
    
    col.left.right = col
    col.right.left = col

        
def DLX(solution, initial):
    if initial.right == initial: return True
    node = col = get_min_col(initial)
    cover(col)
    while node.down.name != "h": 
        current = node = node.down
        solution.add(node)
        while current.right != node:
            current = current.right
            cover(current)
        
        if DLX(solution, initial): return True
        current = node
        solution.remove(node)
        while current.left != node:
            current = current.left
            uncover(current)
    
    uncover(col)
