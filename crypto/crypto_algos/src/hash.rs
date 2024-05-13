
pub trait HashFunction {

    fn new() -> Self;

    /// Appends to the message m
    fn update(&mut self, m: &[u8]);    

    /// calculates the digest for the current message
    /// T is defined by the specific function
    fn digest(&mut self) -> Vec<u8>;

    /// hex representation of the digest
    fn hexdigest(&mut self) -> String;

    /// Gives the block size of the hash function
    fn block_size(&self) -> usize;
}