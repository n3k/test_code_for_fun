use std::{cell::RefCell, collections::{BTreeMap, HashMap}, fmt, ops::DerefMut, rc::Rc};

use bitvec::vec::BitVec;

#[repr(transparent)]
#[derive(Debug, Copy, Clone, Hash, PartialEq, Eq)]
pub struct Symbol(u8);

#[derive(Debug, Copy, Clone, PartialEq)]
pub enum HuffmanNode {
    // A byte - These are leaves in the tree
    Symbol(Symbol),
    // Frequency node - a mini-root 
    Frequency(u32),
}

impl HuffmanNode {
    pub fn new_symbol(symbol: Symbol) -> Self {
        HuffmanNode::Symbol(symbol)
    }

    pub fn new_frequency(frequency: u32) -> Self {
        HuffmanNode::Frequency(frequency)
    }
}

/// A huffman frequency tree 
#[derive(Debug, Clone, PartialEq)]
pub struct HuffmanTree {
    //node:   Rc<RefCell<HuffmanNode>>,
    node:   HuffmanNode,
    // children
    left:   Option<Rc<RefCell<HuffmanTree>>>,
    right:  Option<Rc<RefCell<HuffmanTree>>>  
}

impl fmt::Display for HuffmanTree {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "Node: {:?} - L: {:?} - R: {:?}", self.node, self.left, self.right)
    }
}

impl HuffmanTree {

    pub fn new_node(node: HuffmanNode) -> Self {
        Self {
            //node    : Rc::new(RefCell::new(node)),
            node    : node,
            left    : None,
            right   : None
        }
    }

    pub fn dfs_walk(root: Rc<RefCell<HuffmanTree>>) {        

        let mut stack = Vec::<Rc<RefCell<HuffmanTree>>>::new();
        stack.push(root);
        
        while let Some(tree) = stack.pop() {            
            println!("{:?}", &tree.borrow().node);
            if let Some(right) = tree.borrow().right.clone() {
                stack.push(right);
            }
            if let Some(left) = tree.borrow().left.clone() {
                stack.push(left);
            }
        }
    }
    
    
    pub fn create_tree(training_data: &[u8]) -> Result<Self, Box<dyn std::error::Error>> {

        assert!(training_data.len() > 0);

        // Each byte holds the frequency
        let mut frequency_array = [0u32; 256];

        // Compute frequencies O(n)
        for b in training_data {
            frequency_array[*b as usize] += 1;
        }

        // 256 buckets with vectors inside
        // O (log n)
        let mut buckets = BTreeMap::<u32, Vec::<u8>>::new();
        
        for (jj, freq) in frequency_array.iter().enumerate() {
            if *freq > 0 {
                if let Some(bucket) = buckets.get_mut(&(*freq - 1)) {
                    bucket.push(jj as u8)
                } else {
                    buckets.insert(*freq - 1, vec![jj as u8]);
                }                                 
            }
        }
        
        // Iterate over the buckets (ascending frequency order)
        let mut iter = buckets.iter_mut().rev();
        let mut stack = Vec::<(u32, HuffmanNode)>::new();
        'next_freq: loop {            
            if let Some((freq, symbols)) = iter.next() {
                'next_symbol: loop {
                    if let Some(sym) = symbols.pop() {                        
                        stack.push((*freq + 1, HuffmanNode::new_symbol(Symbol(sym))));
                    } else {
                        break 'next_symbol;
                    }
                }
            } else {
                // No more frequencies.. end of buckets
                break 'next_freq;
            }
        }            
        

        let mut total_freq = 0;
        // Finally create the tree with the nodes
        let (freq, node) = stack.pop()
            .expect("at least 1 node is expected at this point");

        total_freq += freq;

        let mut current_root = HuffmanTree::new_node(node);
        
        while let Some((freq, node)) = stack.pop() {
            let new_node = HuffmanTree::new_node(node);
            total_freq += freq;

            // Auxiliar freq node
            let mut freq_node = HuffmanTree::new_node(HuffmanNode::new_frequency(total_freq));
            freq_node.left  = Some(Rc::new(RefCell::new(current_root)));
            freq_node.right = Some(Rc::new(RefCell::new(new_node)));
            // Change root
            current_root = freq_node;
        }
        
        Ok(current_root)
    }
        
}

pub struct HuffmanCode {

    /// root of the Huffman Tree
    tree: Option<HuffmanTree>,

    /// Code map computed from the tree
    code_map: HashMap<Symbol, BitVec>,
}

impl HuffmanCode {

    pub fn new(training_data: &[u8]) -> Self {
        let tree = HuffmanTree::create_tree(training_data).unwrap();
        let mut code_map = HashMap::new();
        
        let rc_tree = Rc::new(RefCell::new(tree));
        
        // Use a stack for iterative DFS traversal
        let mut stack = Vec::new();
        stack.push((rc_tree.clone(), BitVec::new()));

        while let Some((node_rc, mut code)) = stack.pop() {
            let node = node_rc.borrow();
            
            match node.node {
                HuffmanNode::Symbol(symbol) => {
                    code_map.insert(symbol, code);
                }
                HuffmanNode::Frequency(_) => {
                    if let Some(right) = &node.right {
                        let mut right_code = code.clone();
                        right_code.push(true);
                        stack.push((right.clone(), right_code));
                    }
                    if let Some(left) = &node.left {
                        code.push(false);
                        stack.push((left.clone(), code));
                    }
                }
            }
        }

        let tree = unsafe {
            let refcell = Rc::into_raw(rc_tree);
            let refcell = std::ptr::read(refcell);  
            refcell.into_inner()  // extract T from RefCell
        };

        Self { tree: Some(tree), code_map }
    }

    pub fn encode(&self, data: &[u8]) -> BitVec {
        let mut encoded = BitVec::new();

        for &byte in data {
            let symbol = Symbol(byte);
            if let Some(code) = self.code_map.get(&symbol) {
                encoded.extend_from_bitslice(code);
            }
        }

        encoded
    }

    pub fn decode(&mut self, encoded: &BitVec) -> Vec<u8> {
        let mut decoded = Vec::new();

        // Take the tree out of self
        let tree = self.tree.take().expect("tree not initialized? cannot decode");
        let rc_tree = Rc::new(RefCell::new(tree)); // Root node
        let mut current_node = rc_tree.clone();    // Current position in the tree

        let mut bitstream = encoded.iter();

        
        'decode_loop: loop {
            if let Some(bit) = bitstream.next() {
                println!("Current bit: {:b}", *bit as u8);
                let mut next_node = None;
                {
                    let node_ref = current_node.borrow();
                    if let HuffmanNode::Frequency(..) = &node_ref.node {
                        next_node = if *bit {
                            println!("going right");
                            node_ref.right.as_ref().map(|r| r.clone())
                        } else {
                            println!("going left");
                            node_ref.left.as_ref().map(|l| l.clone())
                        };
                    }
                }

                if let Some(node) = &next_node {
                    current_node = node.clone();
                    let mut do_reset = false;
                    {
                        let node_ref = current_node.borrow();
                        if let HuffmanNode::Symbol(symbol) = &node_ref.node {
                            // If we're at a leaf, push the symbol
                            println!("pushing symbol");
                            decoded.push(symbol.0);                            
                            do_reset = true;
                        } 
                    }
                    if do_reset {
                        println!("---- reset!");
                        current_node = rc_tree.clone();
                    }
                } else {
                    // next_node is not set, meaning the value must have been a symbol
                    {
                        let node_ref = current_node.borrow();
                        if let HuffmanNode::Symbol(symbol) = &node_ref.node {
                            // If we're at a leaf, push the symbol
                            panic!("pushing symbol");
                            decoded.push(symbol.0);                            
                        } else {
                            panic!("undefined condition?");
                        }
                    }
                    // reset to root
                    current_node = rc_tree.clone();
                    println!("---- reset!");
                }
            } else {
                break 'decode_loop;
            }            
        }
        
        // Safely extract the tree and put it back into self
        let tree = unsafe {
            let refcell = Rc::into_raw(rc_tree);
            let refcell = std::ptr::read(refcell);  
            refcell.into_inner()  // extract T from RefCell
        };
        self.tree = Some(tree);

        decoded
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_works() {
        
        let tree = HuffmanTree::create_tree(
            &[41, 41, 42, 43, 42, 41, 44]
        ).unwrap();

        println!("tree: {}", tree);
        /*
        Node: Frequency(7) - 
                L: Some(RefCell { value: HuffmanTree { node: Frequency(4), 
                    left: Some(RefCell { value: HuffmanTree { node: Frequency(2), 
                        left: Some(RefCell { value: HuffmanTree { node: Symbol(43), left: None, right: None } })
                        right: Some(RefCell { value: HuffmanTree { node: Symbol(44), left: None, right: None } })
                        } })
                    right: Some(RefCell { value: HuffmanTree { node: Symbol(42), left: None, right: None } }) } })
                R: Some(RefCell { value: HuffmanTree { node: Symbol(41), left: None, right: None }})
         */

         HuffmanTree::dfs_walk(Rc::new(RefCell::new(tree)));
    }

    #[test]
    fn it_huffmans_1() {
        
        let mut huffman = HuffmanCode::new(
            &[41, 41, 42, 43, 42, 41, 44]
        );

        println!("code_map: {:?}\n\n", huffman.code_map);

        let encoded_data = huffman.encode(&[41, 41, 42, 43, 42, 41, 44, 45]);
        println!("encoded: {:?}", encoded_data);

        let decoded_data = huffman.decode(&encoded_data);
        println!("decoded: {:?}", decoded_data);
        // [1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1]
        // 41  41   42     43     42   41    44 
    }
}
