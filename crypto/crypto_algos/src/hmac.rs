use crate::hash::HashFunction;
use std::fmt::Write;


pub struct Hmac<H: HashFunction> {
    hash_function: H,
    inner_pad: Vec<u8>,
    outer_pad: Vec<u8>,
}


impl<H> Hmac<H> where  H: HashFunction + Clone {

    pub fn new(key: &[u8]) -> Self {
        let hash_function = H::new();
        let block_size = hash_function.block_size();
        let mut inner_pad = vec![0x36; block_size];
        let mut outer_pad = vec![0x5c; block_size];

        // XOR key with inner and outer pads
        for (pad_byte, key_byte) in inner_pad.iter_mut().zip(key) {
            *pad_byte ^= *key_byte;
        }
        for (pad_byte, key_byte) in outer_pad.iter_mut().zip(key) {
            *pad_byte ^= *key_byte;
        }

        Self {
            hash_function,
            inner_pad,
            outer_pad,
        }
    }

    pub fn digest(&mut self, message: &[u8]) -> Vec<u8> {
        let mut inner_hasher = self.hash_function.clone();
        let mut outer_hasher = self.hash_function.clone();

        // Hash inner padding concatenated with the message
        inner_hasher.update(&self.inner_pad);
        inner_hasher.update(message);
        let inner_digest = inner_hasher.digest();

        // Hash outer padding concatenated with the inner hash
        outer_hasher.update(&self.outer_pad);
        outer_hasher.update(&inner_digest);
        outer_hasher.digest()
    }

    pub fn hexdigest(&mut self, message: &[u8]) -> String {
        let digest = self.digest(message);
        let mut hex_string = String::with_capacity(digest.len() * 2);
        for byte in digest {
            write!(&mut hex_string, "{:02x}", byte).expect("Failed to write hex");
        }
        hex_string
    }
}