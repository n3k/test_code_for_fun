//! A SHA1 Implementation
//! 
//! SHA1 combines Merkle–Damgard hash function with a Davies–Meyer compression function with
//! a block cipher called SHACAL
//! 
//! Merkle-Damgard constructions split the message M in blocks of n bits and mixes the blocks
//! with an internal state using the compression function.
//! 
//! If the message cannot be evenly divided with the block size, then the last block is padded.
//! Padding adds a single '1' bit and completes with '0' bits for the block size.
//! The last bits of the padded block however encodes the size of the original message
//! 
//! Compression functions are based on block ciphers. Given the message block M(i), and the previous
//! chaining value H(i - 1), the Davies-Meyer compression function yields the next chaining value
//! as follows:
//!             Hi = E(Mi, Hi − 1) ⊕ Hi − 1
//!    Where E is the block cipher, M(i) serves as the Key and H(i - 1) as the plaintext for E.
//! 
//! Without the XOR with the previous chaining value, Davies-Meyer would be 
//! insecure because you could inver it, going from the new chaining value to 
//! the previous one using the block cipher's decryption function.
//! 
//! 
//! SHA1 defines blocks of 512 bits and iterates over the message doing:
//!             H = E(M, H) + H 
//! 
//! 

use std::fmt::Write;

/// Initial SHA1 state
const H0: u32 = 0x67452301;
const H1: u32 = 0xEFCDAB89;
const H2: u32 = 0x98BADCFE;
const H3: u32 = 0x10325476;
const H4: u32 = 0xC3D2E1F0;

/// Block size
const BLOCK_SIZE_BITS: usize  = 512;
const BLOCK_SIZE_BYTES: usize = 64;

pub struct Sha1 { 
    /// These hold the state
    h0: u32,
    h1: u32,
    h2: u32,
    h3: u32,
    h4: u32,

    /// length in bits of currently processed data
    data_length: usize,

    /// Holds the last data that did not get to a whole block
    last_block: [u8; BLOCK_SIZE_BYTES],
    /// Defines how many bytes of last_block are in use
    last_block_size: usize,
}

impl Sha1 {

    pub fn new() -> Self {
        Sha1 { 
            h0:H0, h1:H1, h2:H2, h3:H3, h4:H4,
            data_length: 0,
            last_block: [0u8; BLOCK_SIZE_BYTES],
            last_block_size: 0
        }
    }

    /// returns the current digest
    pub fn digest(&mut self) -> [u8; 20] {

        if self.last_block_size > 0 {
            let mut data_block = [0u8; 64];
            // Clone the relevant bytes from the last_block
            data_block[0..self.last_block_size]
                .copy_from_slice(&self.last_block[0..self.last_block_size]);

            // Set 1 bit and 0 bits and encoded length
            let byte_bit = (self.data_length & 0x1FF) >> 3;
            let bit_bit = (self.data_length & 0x1FF) & 0b11;

            data_block[byte_bit] ^= 1 << (7 - bit_bit); // big endian

            unsafe {
                let p = &data_block[56..64] as *const [u8] as *const u64 as *mut u64;
                p.write(p.read() ^ (self.data_length as u64).to_be());
            }

            self.sha1_compress(&data_block);

        } else {
            // even blocks of data, still requires a final block of padding and encoded length
            let mut data_block = [0u8; 64];
            data_block[0] = 0x80; // 1 bit added
            unsafe {
                let p = &data_block[56..64] as *const [u8] as *const u64 as *mut u64;
                p.write(p.read() ^ (self.data_length as u64).to_be());
            }

            self.sha1_compress(&data_block);
        }

        let mut v = [0u32; 5];
        v[0] = self.h0.to_be();
        v[1] = self.h1.to_be();
        v[2] = self.h2.to_be();
        v[3] = self.h3.to_be();
        v[4] = self.h4.to_be();

        return unsafe { std::mem::transmute(v) };
    }

    pub fn hexdigest(&mut self) -> String {
        let mut s = String::new();
        for &byte in &self.digest() {            
            write!(&mut s, "{:02x}", byte).expect("Unable to write");
        }

        s
    }

    /// Receives the message and updates the internal state
    pub fn update(&mut self, m: &[u8])  {
        
        // length in bits
        let mut msg_len_bits = m.len() * 8;
        
        // update tracked data_length
        self.data_length += msg_len_bits;

        // Offset in the message for the data that goes into a 
        // a new block (and not in the last_available block)        
        let mut start_offset = 0usize;

        // calculate how many blocks we need for the new data
        if self.last_block_size > 0 {
            // This means we have space from a previous update
            let available_space = BLOCK_SIZE_BYTES - self.last_block_size;
            let bytes_to_copy = std::cmp::min(available_space, m.len());
            
            // Fill last block
            self.last_block[self.last_block_size..self.last_block_size + bytes_to_copy]
                    .copy_from_slice(m);                

        
            if m.len() <= available_space {                                

                // Special case when the complete block is filled
                if m.len() == available_space {
                    // compress the block
                    self.sha1_compress(&self.last_block.clone());                    
                    // `clear` the last_block
                    self.last_block_size = 0;   
                    // end here
                    return;                 
                }
                
                self.last_block_size += m.len();

                // end here
                return;

            } else {
                // Update start offset (skip the portion copied into the last_block)
                start_offset += bytes_to_copy;
                // Decrease msg_len_bits in bytes_to_copy amount
                msg_len_bits -= bytes_to_copy * 8;
                
                // Compress the filled block
                self.sha1_compress(&self.last_block.clone());                    
                // `clear` the last_block
                self.last_block_size = 0;
                // continue
            }
        }

        let block_nums = msg_len_bits >> 9;

        let mut padding_len = 0;        
        
        if (msg_len_bits & 0x1FF) != 0 {
            padding_len = BLOCK_SIZE_BITS - (msg_len_bits & 0x1FF);
        }

        // shadow m to start_offset slice
        let m = &m[start_offset..];
     
        // process blocks
        for block in 0..block_nums {
            let offset = block * BLOCK_SIZE_BYTES;
            let data_block = &m[offset..offset+BLOCK_SIZE_BYTES];
            self.sha1_compress(data_block);
        }

        // process the last block
        if padding_len > 0 {
            let offset = block_nums;

            // Copy content into last_block 
            // and update last_block size
            let src_slice = &m[offset..];
            self.last_block[0..src_slice.len()].copy_from_slice(src_slice);            
            self.last_block_size = src_slice.len();

        } 
    }

    fn sha1_compress(&mut self, m_block: &[u8]) {        
        let (a, b, c, d, e) = self.sha1_block_cipher(m_block);
        self.h0 = self.h0.wrapping_add(a);
        self.h1 = self.h1.wrapping_add(b);
        self.h2 = self.h2.wrapping_add(c);
        self.h3 = self.h3.wrapping_add(d);
        self.h4 = self.h4.wrapping_add(e);        
    }

    #[inline]
    fn sha1_block_cipher(&self, m_block: &[u8]) -> (u32, u32, u32 ,u32 ,u32) {
        let mut a = self.h0;
        let mut b = self.h1;
        let mut c = self.h2;
        let mut d = self.h3;
        let mut e = self.h4;

        let W: [u32; 80] = Sha1::expand(m_block);
        // 80 rounds
        let mut k;
        let mut f;

        for i in 0..80 {
            if i < 20 {
                f = (b & c) | (!b & d);
                k = 0x5A827999;
            }
            else if i < 40 {
                f = b ^ c ^ d;
                k = 0x6ED9EBA1;
            }
            else if i < 60 {
                f = (b & c) | (b & d) | (c & d);
                k = 0x8F1BBCDC;
            }
            else if i < 80 {
                f = b ^ c ^ d;
                k = 0xCA62C1D6;
            } else {
                unreachable!("bad iteration");
            }

            let new = a.rotate_left(5)
                            .wrapping_add(f)
                            .wrapping_add(e)
                            .wrapping_add(k)
                            .wrapping_add(W[i]);

            
            e = d;
            d = c;
            c = b.rotate_right(2);
            b = a;            
            a = new;
            println!("{} {} {} {} {}", a, b, c, d, e);
        }

        return (a, b, c, d, e)
    }

    /// Expands the block of 512 bits to an array of 80 32-bit words
    #[inline]
    fn expand(m_block: &[u8]) -> [u32; 80] {
        let mut W = [0u32; 80];  
        // Assert the block is 64 bytes (512 bits)
        assert_eq!(m_block.len(), 64);
        unsafe {
            let p32: &[u32] = std::mem::transmute(m_block);
            // Ensure the block is 16 32-bit words (512 bits)
            // assert_eq!(p32.len(), 16); // This is not happening    
            // panic!("m_block len: {:02x} - p32_len: {:02x}", m_block.len(), p32.len());
            for i in 0..16 {
                W[i] = p32[i].to_be();
            }
        }      
        println!("{:?}", W);
        for i in 16..80 {
            W[i] = (W[i - 3] ^ W[i - 8] ^ W[i - 14] ^ W[i - 16]).rotate_left(1);
        }
        W
    }
}

