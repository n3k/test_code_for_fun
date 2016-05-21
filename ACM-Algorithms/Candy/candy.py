import sys

class Vector_descriptor():
    def __init__(self, value, vector):
        self.value = value
        self.vector = vector
        
class Node():
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
 

class Tree():
    def __init__(self, root):        
        self.root = Node(root)
        self.paths = []

    def get_max_path(self):
        max_sum = 0
        for p in self.paths:
            if max_sum < sum(p):
                max_sum = sum(p)
        return max_sum
    
    def add_node(self,value):
        return Node(value)

    def insert(self,root,value, left):
        if(root == None):
            root = self.add_node(value)
        else:
            if left:
               root.left = self.insert(root.left,value, True)
            else:
                root.right = self.insert(root.right,value, False)
        return root
    
    def is_leaf(self, node):
        if node.right == None and node.left == None:
            return True
        return False

    def preorder_traversal(self, node, candy_path):    
        
        candy_path.append(node.value)      
        if node == None:
            return None
        
        if self.is_leaf(node):
            self.paths.append(candy_path[:])
            candy_path.pop()
            
        else:    

            #Generate Successors
            if node.left != None:
                self.preorder_traversal(node.left, candy_path)
            
                
            if node.right != None:
                self.preorder_traversal(node.right, candy_path)             
            else:
                candy_path.pop()

def fill_tree(position, vector, tree, root):
    if (position + 2) < len(vector):
        child = tree.insert(root, vector[position+2], True)
        fill_tree(position + 2, vector, tree, child)
    if (position + 3) < len(vector):
        child = tree.insert(root, vector[position+3], False)
        fill_tree(position + 3, vector, tree, child)
    return


def get_max_sum_vector(vector):   

    tree_a = Tree(vector[0])
    tree_b = Tree(vector[1])
    
    fill_tree(0,vector, tree_a, tree_a.root)
    fill_tree(1,vector, tree_b, tree_b.root)
    
    tree_a.preorder_traversal(tree_a.root,[])
    tree_b.preorder_traversal(tree_b.root,[])
    max_a = tree_a.get_max_path()
    max_b = tree_b.get_max_path()
    if max_a > max_b:
        return Vector_descriptor(max_a,vector)
    else:
        return Vector_descriptor(max_b,vector)
        

def get_max_vector_descriptor(v_descriptor_list):
    v_descriptor_values = []
    for i in range(len(v_descriptor_list)):       
        v_descriptor_values.append(v_descriptor_list[i].value)
    
    tree_a = Tree(v_descriptor_values[0])
    tree_b = Tree(v_descriptor_values[1])
    
    fill_tree(0,v_descriptor_values, tree_a, tree_a.root)
    fill_tree(1,v_descriptor_values, tree_b, tree_b.root)
    
    tree_a.preorder_traversal(tree_a.root,[])
    tree_b.preorder_traversal(tree_b.root,[])
    max_a = tree_a.get_max_path()
   
    max_b = tree_b.get_max_path()
    
    if max_a > max_b:
        return max_a
    else:
        return max_b       

def process_test_case(matrix):
    
    v_list = []

    for row in matrix:
        v_list.append(get_max_sum_vector(row))
        
    for vector in v_list:
        print str(vector.vector) + "  " + str(vector.value)    

    print get_max_vector_descriptor(v_list)
    

def main():
    
    if len(sys.argv) != 2:
        print "Usage: " + sys.argv[0] + " <input-file>"
        sys.exit(1)
    else:
        try:
            f = open(sys.argv[1], 'r')
        except IOError:
            print "Cannot open file"
        else:
            data = [map(int, line.split()) for line in f.readlines()]
            i = 0
            while data[i] != [0,0]:           
                if len(data[i]) == 2:
                    # I just care about rows
                    N = data[i][0]                   
                    matrix = []
                    j = i
                    while j < (i + N):
                        matrix.append(data[j+1])
                        j += 1
                        
                    process_test_case(matrix)
                i += 1
            f.close()      


if __name__ == "__main__":
    main()