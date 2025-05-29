//! TODO: implement deletion, get, get_mut, contains
//! -> https://www.youtube.com/watch?v=TlfQOdeFy0Y
//! 
//! Red-Black Tree Implementation
//! 
//! 1. Each node is either red or black
//! 2. The root is always black
//! 3. Every NIL leaf is black
//! 4. If a node is red, its children must be black
//! 5. Every path from a node to its descendants NIL nodes, 
//!    must have the same number of black nodes
//! 

use core::fmt;
use std::{cell::RefCell, collections::VecDeque, rc::Rc};

#[derive(Debug, Copy, Clone, PartialEq, Eq)]
enum Color {    
    Red,
    Black
}

#[derive(Debug, Clone, PartialEq, Eq)]
struct RbNode<K, V> 
    where K: Eq + PartialEq + Ord + PartialOrd + std::fmt::Debug + Copy + Clone, V: PartialEq
{
    key     : K,
    data    : Option<V>,
    color   : Color,
    parent  : Option<Rc<RefCell<RbNode<K, V>>>>,
    left    : Option<Rc<RefCell<RbNode<K, V>>>>,
    right   : Option<Rc<RefCell<RbNode<K, V>>>>,
}

impl <K: Eq + PartialEq + Ord + PartialOrd + std::fmt::Debug + Copy + Clone, 
    V: PartialEq> fmt::Display for RbNode<K, V> {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let parent = if let Some(parent) = self.parent.clone() {
            Some(parent.borrow().key)
        } else {
            None
        };

        let left = if let Some(left) = self.left.clone() {
            Some(left.borrow().key)
        } else {
            None
        };

        let right = if let Some(right) = self.right.clone() {
            Some(right.borrow().key)
        } else {
            None
        };

        write!(f, 
            "Node: [Key: {:?}, color: {:?}, parent: {:?}, left: {:?}, right: {:?}",
            self.key,
            self.color,
            parent,
            left,
            right
        )
    }
}

impl <K: Eq + PartialEq + Ord + PartialOrd + std::fmt::Debug + Copy + Clone, 
    V: PartialEq> RbNode<K, V> {
    pub fn new_red(k: K, v: Option<V>) -> Self {
        Self {
            key     : k,
            data    : v,
            color   : Color::Red,
            parent  : None,
            left    : None,
            right   : None
        }
    }

    pub fn new_black(k: K, v: Option<V>) -> Self {
        Self {
            key     : k,
            data    : v,
            color   : Color::Black,
            parent  : None,
            left    : None,
            right   : None
        }
    }
}

#[derive(Debug, Clone)]
struct RbTree<K, V> 
    where K: Eq + PartialEq + Ord + PartialOrd + std::fmt::Debug + Copy + Clone, 
    V: PartialEq
{
    /// The root of the tree
    root: Option<Rc<RefCell<RbNode<K, V>>>>,

    /// Number of nodes in the tree
    nodes:  usize,


}

impl<K: Eq + PartialEq + Ord + PartialOrd + std::fmt::Debug + Copy + Clone, 
    V: PartialEq> RbTree<K, V> 
{

    pub fn new() -> Self {
        Self { root: None, nodes: 0 }
    }

    /// Height of the tree
    pub fn height(&self) -> usize {
        // h <= 2 * log(n + 1)
        0
    }

    /// Number of nodes in the tree
    pub fn len(&self) -> usize {
        self.nodes
    }


    /// Performs a left rotation for the specified node
    /// The current node becomes a left child of its previous right child
    fn rotate_left(&mut self, node: Rc<RefCell<RbNode<K, V>>>) {
        let node_y = node.borrow_mut().right.take();
        if node_y.is_none() {
            panic!("invalid left-rotation operation: right child of node is None");
        }

        let node_y = node_y.unwrap();

        let left_child = node_y.borrow_mut().left.take();
        // Take node y's left child and set it as right child of current node
        if let Some(left_child) = left_child {
            // Update the parent of left_child to node
            left_child.borrow_mut().parent = Some(node.clone());
            node.borrow_mut().right = Some(left_child);
        } else {
            // There was no left child for Y, so right child of node is None
            node.borrow_mut().right = None;
        }

        // Grab the current node parent and sets it as node-y parent
        let parent = node.borrow_mut().parent.take();
        if let Some(parent) = parent {
            node_y.borrow_mut().parent  = Some(parent.clone());
            // We also need to update the parent's child link
            let mut parent_link_set = false;
            let parent_left  = parent.borrow_mut().left.clone();            
            if let Some(parent_left) = parent_left {
                if parent_left == node {
                    parent.borrow_mut().left = Some(node_y.clone());
                    parent_link_set = true;
                }
            }
            if !parent_link_set {
                let parent_right = parent.borrow_mut().right.clone();
                if let Some(parent_right) = parent_right {
                    if parent_right == node {
                        parent.borrow_mut().right = Some(node_y.clone());
                        parent_link_set = true;
                    }
                }
            }

            // At this point, the parent link must have been set
            assert!(parent_link_set == true);
                        
        } else {
            // If the parent of Node was None, it means it was the root
            let root_node = self.root.take().unwrap();
            assert!(root_node == node);

            self.root = Some(node_y.clone());
            node_y.borrow_mut().parent  = None;
        }

        // Set the original node as the left of node-y
        node_y.borrow_mut().left    = Some(node.clone());

        // Sets node-y as the parent of the current node
        node.borrow_mut().parent    = Some(node_y);        
    }

    /// Performs a right rotation for the specified node
    /// The current node becomes a right child of its previous left child
    fn rotate_right(&mut self, node: Rc<RefCell<RbNode<K, V>>>) {
        let node_y = node.borrow_mut().left.take();
        if node_y.is_none() {
            panic!("invalid right-rotation operation: left child of node is None");
        }

        let node_y = node_y.unwrap();

        let right_child = node_y.borrow_mut().right.take();
        // Take node y's right child and set it as right child of current node
        if let Some(right_child) = right_child {
            // Update the parent of right_child to node
            right_child.borrow_mut().parent = Some(node.clone());
            node.borrow_mut().left = Some(right_child);
        } else {
            // There was no right child for Y, so left child of node is None
            node.borrow_mut().left = None;
        }

        // Grab the current node parent and sets it as node-y parent
        let parent = node.borrow_mut().parent.take();
        if let Some(parent) = parent {
            node_y.borrow_mut().parent  = Some(parent.clone());
            // We also need to update the parent's child link
            let mut parent_link_set = false;
            let parent_left  = parent.borrow_mut().left.clone();            
            if let Some(parent_left) = parent_left {
                if parent_left == node {
                    parent.borrow_mut().left = Some(node_y.clone());
                    parent_link_set = true;
                } else {
                    // re-set the original child
                    parent.borrow_mut().left = Some(parent_left);
                }
            }
            if !parent_link_set {
                let parent_right = parent.borrow_mut().right.clone();
                if let Some(parent_right) = parent_right {
                    if parent_right == node {
                        parent.borrow_mut().right = Some(node_y.clone());
                        parent_link_set = true;
                    } else {
                        // Reaching here means the none of the children of Parent correspond with 
                        // the `node` we're working with.
                        unreachable!("this is an impossible case");
                    }
                }
            }

            // At this point, the parent link must have been set
            assert!(parent_link_set == true);
                        
        } else {
            // If the parent of Node was None, it means it was the root
            let root_node = self.root.take().unwrap();
            assert!(root_node == node);

            self.root = Some(node_y.clone());
            node_y.borrow_mut().parent  = None;
        }

        // Set the original node as the right of node-y
        node_y.borrow_mut().right    = Some(node.clone());

        // Sets node-y as the parent of the current node
        node.borrow_mut().parent    = Some(node_y);        
    }

    /// This function makes sure the properties of Red-Black trees is kept
    /// when a new node gets inserted
    fn fix_insert(&mut self, new_node: Rc<RefCell<RbNode<K, V>>>) {
        
        if new_node == self.root.clone().unwrap() {
            return;
        }
        
        let parent_node = new_node.borrow_mut().parent.clone().unwrap();
        let parent_color = parent_node.borrow().color;       
        // Check color of the parent
        match parent_color {
            Color::Black => {
                // if the parent is black, then no properties are violated 
                // (the tree remains balanced)                
            }
            Color::Red => {
                // If parent is red, we need to adjust
                // If the parent of the new node is the left child of the grandparent
                let grand_parent_node = 
                    parent_node.borrow_mut().parent.clone();
                if let Some(grand_parent_node) = grand_parent_node.clone() {
                    
                    let grand_parent_node_left_child = 
                        grand_parent_node.borrow_mut().left.clone();
                    
                    let grand_parent_node_right_child = 
                        grand_parent_node.borrow_mut().right.clone();

                    let mut grand_parent_link_handled: bool = false;

                    // if the parent of the inserted node is the left child of grand parent
                    if let Some(grand_parent_node_left_child) = grand_parent_node_left_child.clone() {
                        if grand_parent_node_left_child == parent_node {  
                            grand_parent_link_handled = true;
                            if grand_parent_node_right_child
                                    .clone()
                                    .is_none_or(|uncle| {
                                        let uncle_color = uncle.borrow().color;
                                        uncle_color == Color::Black
                                    }) 
                            {
                                // Handle situation when uncle node is black

                                let parent_right_child = 
                                            parent_node.borrow_mut().right.clone();
                                        
                                let mut parent_rotated = false;        
                                if let Some(parent_right_child) = parent_right_child {
                                    if parent_right_child == new_node {
                                        self.rotate_left(parent_node.clone());
                                        parent_rotated = true;
                                    }
                                }

                                if parent_rotated {
                                    // parent was rotated, meaning the new-node becomes the parent
                                    new_node.borrow_mut().color     = Color::Black;
                                } else {
                                    // Recolor original parent to black
                                    parent_node.borrow_mut().color  = Color::Black;
                                }

                                // Recolor grandparent to red
                                grand_parent_node.borrow_mut().color = Color::Red;

                                // Restore balance
                                self.rotate_right(grand_parent_node.clone());

                            } else {
                                // Handle situation when uncle node is Red
                                
                                // Recolor both parent and uncle to black
                                parent_node.borrow_mut().color  = Color::Black;
                                grand_parent_node_right_child.clone().unwrap().borrow_mut().color  = Color::Black;

                                // Recolor grandparent to red
                                grand_parent_node.borrow_mut().color = Color::Red;

                                // Move upwards to the grandparent and check for adjustments
                                self.fix_insert(grand_parent_node.clone());
                            }                            
                        }
                    }

                    if !grand_parent_link_handled {                        
                        if let Some(grand_parent_node_right_child) = grand_parent_node_right_child {
                            if grand_parent_node_right_child == parent_node {
                                grand_parent_link_handled = true;                                
                            }

                            if grand_parent_node_left_child
                                    .clone()
                                    .is_none_or(|uncle| {
                                        let uncle_color = uncle.borrow().color;
                                        uncle_color == Color::Black
                                    }) 
                            {
                                // Handle situation when uncle node is black

                                let parent_left_child = 
                                            parent_node.borrow_mut().left.clone();
                                
                                let mut parent_rotated = false;
                                if let Some(parent_left_child) = parent_left_child {
                                    if parent_left_child == new_node {
                                        self.rotate_right(parent_node.clone());
                                        parent_rotated = true;
                                    }
                                }

                                if parent_rotated {
                                    // parent was rotated, meaning the new-node becomes the parent
                                    new_node.borrow_mut().color     = Color::Black;
                                } else {
                                    // Recolor original parent to black
                                    parent_node.borrow_mut().color  = Color::Black;
                                }
                                
                                // Recolor grandparent to red
                                grand_parent_node.borrow_mut().color = Color::Red;

                                // Restore balance                                
                                self.rotate_left(grand_parent_node);

                            } else {
                                // Handle situation when uncle node is Red
                                
                                // Recolor both parent and uncle to black
                                parent_node.borrow_mut().color  = Color::Black;
                                grand_parent_node_left_child.clone().unwrap().borrow_mut().color  = Color::Black;

                                // Recolor grandparent to red
                                grand_parent_node.borrow_mut().color = Color::Red;

                                // Move upwards to the grandparent and check for adjustments                                
                                self.fix_insert(grand_parent_node);
                            }

                        }
                    }
                    
                    // The grandparent-parent relationship must have been handled by now
                    assert!(grand_parent_link_handled == true);

                } else {
                    panic!("grand parent is None.. what now?");
                }

                // Always set the color of the root to black
                self.root.clone().unwrap().borrow_mut().color = Color::Black;
            }
        }
        
    }

    /// Inserts key-data pair into the Tree
    /// If the key exists, it performs an update over the value
    /// If an update occurs, the existent value is returned, otherwise None
    pub fn insert(&mut self, key: K, data: Option<V>) -> Option<V> {     

        // If this is the first insertion, the root is None
        if self.root.is_none() {
            // Create a new black node and set the root
            self.root   = Some(Rc::new(RefCell::new(RbNode::new_black(key, data))));
            self.nodes  = 1;
            return None
        }   
    
        enum InsertLocation {
            Left,
            Right,
            Update,
        }

        let location;

        let mut parent_ref = Some(self.root.as_ref().unwrap().clone());

        'binary_search: loop {
            let parent_node = parent_ref.unwrap();
            let parent_node_ref  = parent_node.borrow();
            if key == parent_node_ref.key {
                // Key already exists in the Tree, process update                
                location = InsertLocation::Update;
                drop(parent_node_ref);
                parent_ref = Some(parent_node);
                break 'binary_search;
            } else if key < parent_node_ref.key {
                if let Some(left) = parent_node_ref.left.as_ref() {
                    parent_ref = Some(left.clone());
                    continue 'binary_search;
                } else {
                    // break the look with the current parent_ref
                    location = InsertLocation::Left;
                    drop(parent_node_ref);
                    parent_ref = Some(parent_node);
                    break 'binary_search;
                }                
            } else {
                // key > parent_node.key
                if let Some(right) = parent_node_ref.right.as_ref() {
                    parent_ref = Some(right.clone());
                    continue 'binary_search;
                } else {
                    // break the look with the current parent_ref
                    location = InsertLocation::Right;
                    drop(parent_node_ref);
                    parent_ref = Some(parent_node);
                    break 'binary_search;
                }
            }
        }

        let result = match location {
            InsertLocation::Update => {
                // This is easy because the tree does not require re-coloring or re-balancing
                //  -> only the data is modified
                let parent_node = parent_ref.unwrap();
                let prev_data = parent_node.borrow_mut().data.take();
                parent_node.borrow_mut().data = data;
                prev_data
            }
            InsertLocation::Left => {
                let parent_node = parent_ref.unwrap();
                let new_node    = Rc::new(RefCell::new(RbNode::new_red(key, data)));
                new_node.borrow_mut().parent    = Some(parent_node.clone());
                parent_node.borrow_mut().left   = Some(new_node.clone());                              
                self.fix_insert(new_node);
                None
            }   
            InsertLocation::Right => {
                let parent_node = parent_ref.unwrap();
                let new_node    = Rc::new(RefCell::new(RbNode::new_red(key, data)));
                new_node.borrow_mut().parent    = Some(parent_node.clone());
                parent_node.borrow_mut().right  = Some(new_node.clone());
                self.fix_insert(new_node);
                None
            }
        };

        if result.is_none() {
            self.nodes += 1;
        }

        return result;
    }

    pub fn delete(&mut self, key: &K) -> Result<(), Box<dyn std::error::Error>> {
        Ok(())
    }

    pub fn contains(&self, key: &K) -> bool {
        false
    }

    pub fn get(&self, key: &K) -> Option<&RbNode<K, V>> {
        None
    }

    pub fn get_mut(&mut self, key: &K) -> Option<&mut RbNode<K, V>> {
        None
    }

    /// Walks the three doing bread-first-search and apply the callback to each node
    pub fn  walk_bfs<F>(&self, callback: F) where F: Fn(&RbNode<K,V>) {
        if self.root.is_none() {
            return;
        }
        
        let mut queue = VecDeque::<Rc::<RefCell::<RbNode<K, V>>>>::new();
        queue.push_back(self.root.clone().unwrap());

        'bfs: loop {
            if let Some(node) = queue.pop_front() {                
                callback(&node.borrow());

                if let Some(left) = &node.borrow().left {
                    queue.push_back(left.clone());
                }

                if let Some(right) = &node.borrow().right {
                    queue.push_back(right.clone());
                }

            } else {
                break 'bfs;
            }
        }
    }

    /// Walks the three doing depth-first-search and apply the callback to each node
    pub fn  walk_dfs<F>(&self, callback: F) where F: Fn(&RbNode<K,V>) {
         if self.root.is_none() {
            return;
        }
        
        let mut stack = Vec::<Rc::<RefCell::<RbNode<K, V>>>>::new();
        stack.push(self.root.clone().unwrap());

        'bfs: loop {
            if let Some(node) = stack.pop() {                
                callback(&node.borrow());

                if let Some(left) = &node.borrow().left {
                    stack.push(left.clone());
                }

                if let Some(right) = &node.borrow().right {
                    stack.push(right.clone());
                }

            } else {
                break 'bfs;
            }
        }
    }
}



#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn rb_tree_insertion_test1() {
        
        let mut tree = RbTree::<u32, ()>::new();
        println!("Inserting 10\n");
        tree.insert(10, None);
        tree.walk_bfs(|x| {
            println!(" -> Node {}", x);
        });

        println!("Inserting 5\n");
        tree.insert(5, None);
        tree.walk_bfs(|x| {
            println!(" -> Node {}", x);
        });
        println!("Inserting 15\n");
        tree.insert(15, None);
        tree.walk_bfs(|x| {
            println!(" -> Node {}", x);
        });
        println!("Inserting 3\n");
        tree.insert(3, None);
        tree.walk_bfs(|x| {
            println!(" -> Node {}", x);
        });
        println!("Inserting 2\n");
        tree.insert(2, None);
        tree.walk_bfs(|x| {
            println!(" -> Node {}", x);
        });
        println!("Inserting 4\n");
        tree.insert(4, None);
        tree.walk_bfs(|x| {
            println!(" -> Node {}", x);
        });
        println!("Inserting 20\n");
        tree.insert(20, None);
        tree.walk_bfs(|x| {
            println!(" -> Node {}", x);
        });
        println!("Inserting 16\n");
        tree.insert(16, None);
        
        tree.walk_bfs(|x| {
            println!(" -> Node {}", x);
        });

    }
}