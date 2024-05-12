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

const DEBUG: bool = false;

/// Initial SHA1 state
const H0: u32 = 0x67452301;
const H1: u32 = 0xEFCDAB89;
const H2: u32 = 0x98BADCFE;
const H3: u32 = 0x10325476;
const H4: u32 = 0xC3D2E1F0;

/// Block size
const BLOCK_SIZE_BYTES: usize = 64; // 512 bits

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

    fn get_state(&self) -> [u8; 20] {
        let mut v = [0u32; 5];
        v[0] = self.h0.to_be();
        v[1] = self.h1.to_be();
        v[2] = self.h2.to_be();
        v[3] = self.h3.to_be();
        v[4] = self.h4.to_be();

        return unsafe { std::mem::transmute(v) };
    }

    pub fn get_hexstate(&self) -> String {
        let mut s = String::new();
        for &byte in &self.get_state() {            
            write!(&mut s, "{:02x}", byte).expect("Unable to write");
        }

        s
    }

    /// returns the current digest in bytes
    pub fn digest(&mut self) -> [u8; 20] {        

        let (a, b, c, d, e) =
        if self.last_block_size > 0 {
            let mut data_block = [0u8; BLOCK_SIZE_BYTES];
            // Clone the relevant bytes from the last_block
            data_block[0..self.last_block_size]
                .copy_from_slice(&self.last_block[0..self.last_block_size]);

            // Set 1 bit and 0 bits and encoded length
            let byte_bit = (self.data_length & 0x1FF) >> 3;
            let bit_bit = (self.data_length & 0x1FF) & 0b11;

            data_block[byte_bit] ^= 1 << (7 - bit_bit); // big endian

            if self.last_block_size < (BLOCK_SIZE_BYTES - 8) {
                if DEBUG {
                    println!("last_block_size has enough space for the encoded length")
                }

                unsafe {
                    let p = &data_block[56..64] as *const [u8] as *const u64 as *mut u64;
                    p.write(p.read() ^ (self.data_length as u64).to_be());
                }              
        
                Sha1::sha1_compress(self.h0, self.h1, self.h2, self.h3, self.h4, &data_block)
            } else {
                // In this case, we still need to add another block because 
                // the data len needs to be congruent with 56 mod 64
                if DEBUG {
                    println!("last_block_size does not have space for the encoded length");
                    println!("compress the current data and send a empty block as well");
                }
                let (a, b, c, d, e) = 
                    Sha1::sha1_compress(self.h0, self.h1, self.h2, self.h3, self.h4, &data_block);

                let h0 = self.h0.wrapping_add(a);
                let h1 = self.h1.wrapping_add(b);
                let h2 = self.h2.wrapping_add(c);
                let h3 = self.h3.wrapping_add(d);
                let h4 = self.h4.wrapping_add(e); 

                unsafe {
                    let data_ptr = data_block.as_mut_ptr();
                    // Zero out the array
                    std::ptr::write_bytes(data_ptr, 0, BLOCK_SIZE_BYTES);
                    // Write current data length bits
                    let p: *mut u64 = &data_block[56..64] as *const [u8] as *const u64 as *mut u64;
                    p.write((self.data_length as u64).to_be());
                };

                let (h0x, h1x, h2x, h3x, h4x) = 
                    Sha1::sha1_compress(h0, h1, h2, h3, h4, &data_block);

                let h0 = h0.wrapping_add(h0x);
                let h1 = h1.wrapping_add(h1x);
                let h2 = h2.wrapping_add(h2x);
                let h3 = h3.wrapping_add(h3x);
                let h4 = h4.wrapping_add(h4x); 

                let mut v = [0u32; 5];
                v[0] = h0.to_be();
                v[1] = h1.to_be();
                v[2] = h2.to_be();
                v[3] = h3.to_be();
                v[4] = h4.to_be();

                return unsafe { std::mem::transmute(v) };
            }
            

        } else {
            // even blocks of data, still requires a final block of padding and encoded length
            let mut data_block = [0u8; BLOCK_SIZE_BYTES];
            data_block[0] = 0x80; // 1 bit added
            unsafe {
                let p = &data_block[56..64] as *const [u8] as *const u64 as *mut u64;
                p.write(p.read() ^ (self.data_length as u64).to_be());
            }

            Sha1::sha1_compress(self.h0, self.h1, self.h2, self.h3, self.h4, &data_block)
        };

        let h0 = self.h0.wrapping_add(a);
        let h1 = self.h1.wrapping_add(b);
        let h2 = self.h2.wrapping_add(c);
        let h3 = self.h3.wrapping_add(d);
        let h4 = self.h4.wrapping_add(e); 

        let mut v = [0u32; 5];
        v[0] = h0.to_be();
        v[1] = h1.to_be();
        v[2] = h2.to_be();
        v[3] = h3.to_be();
        v[4] = h4.to_be();

        return unsafe { std::mem::transmute(v) };
    }

    /// returns a hex string with the digest
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

        if DEBUG {
            println!("update:: with message len: {} bytes ({} bits)", m.len(), msg_len_bits);
        }
        
        // update tracked data_length
        self.data_length += msg_len_bits;

        if DEBUG {
            println!("data_length: {} bits", self.data_length);
        }

        // Offset in the message for the data that goes into a 
        // a new block (and not in the last_available block)        
        let mut start_offset = 0usize;

        // calculate how many blocks we need for the new data
        if self.last_block_size > 0 {
            // This means we have space from a previous update
            let available_space = BLOCK_SIZE_BYTES - self.last_block_size;
            let bytes_to_copy = std::cmp::min(available_space, m.len());

            if DEBUG {
                println!("Adding to previous block");
                println!("  -> available_space: {} bytes", available_space);
                println!("  -> bytes_to_copy:   {} bytes", bytes_to_copy);
            }
            
            // Fill last block
            self.last_block[self.last_block_size..self.last_block_size + bytes_to_copy]
                    .copy_from_slice(&m[0..bytes_to_copy]);                

        
            if m.len() <= available_space {                                
                if DEBUG {
                    println!("new msg_len is less or equal to the available space");
                }          

                // Special case when the complete block is filled
                if m.len() == available_space {
                    if DEBUG {
                        println!("completed a previous block evenly");
                        println!(" -> (new msg_len matches the previous block available space)");
                        println!(" -> compressing and setting last_block_size to 0");
                    }
                    // compress the block and update state
                    let (a, b, c, d, e) = 
                        Sha1::sha1_compress(self.h0, self.h1, self.h2, self.h3, self.h4, 
                            &self.last_block.clone());
                    self.update_state(a, b, c, d, e);

                    // `clear` the last_block
                    self.last_block_size = 0;   
                    // end here
                    return;                 
                }
                
                if DEBUG {
                    println!("last_block_size before: {}", self.last_block_size);
                }
                self.last_block_size += m.len();

                if DEBUG {
                    println!("setting last_block_size to {}", self.last_block_size);
                    println!("last msg_len: {}", msg_len_bits >> 3);
                }

                // end here
                return;

            } else {
                if DEBUG {
                    println!("msg_len is larger than the last_block available space");
                }

                // Update start offset (skip the portion copied into the last_block)
                start_offset += bytes_to_copy;
                // Decrease msg_len_bits in bytes_to_copy amount
                msg_len_bits -= bytes_to_copy * 8;
                
                // Compress the filled block and update state
                let (a, b, c, d, e) = 
                    Sha1::sha1_compress(self.h0, self.h1, self.h2, self.h3, self.h4, 
                    &self.last_block.clone());
                self.update_state(a, b, c, d, e);            

                // `clear` the last_block
                self.last_block_size = 0;
                // continue
                if DEBUG {
                    println!(" -> start_offset is now at {}", start_offset);
                    println!(" -> msg_len_bits is now {} bits", msg_len_bits);
                    println!(" -> last_block_size = 0");
                }
            }
        }

        let block_nums = msg_len_bits >> 9;

        let mut requires_last_block = false;        
        
        if (msg_len_bits & 0x1FF) != 0 {
            requires_last_block = true;
        }

        if DEBUG {
            println!("block_nums: {} - requires_last_block: {}", 
                block_nums, requires_last_block);
        }

        // shadow m to start_offset slice
        if DEBUG {
            println!("slicing at start_offset: {}", start_offset);        
        }
        let m = &m[start_offset..];
        assert_eq!(m.len(), msg_len_bits >> 3);
     
        // process blocks
        for block in 0..block_nums {
            let offset = block * BLOCK_SIZE_BYTES;
            let data_block = &m[offset..offset+BLOCK_SIZE_BYTES];
            let (a, b, c, d, e) = 
                Sha1::sha1_compress(self.h0, self.h1, self.h2, self.h3, self.h4, data_block);
            self.update_state(a, b, c, d, e);
        }

        // process the last block
        if requires_last_block {
            let offset = block_nums * BLOCK_SIZE_BYTES;

            // Copy content into last_block 
            // and update last_block size
            let src_slice = &m[offset..];
            println!("{} block_nums: {}", src_slice.len(), block_nums);
            println!("m_len: {}", m.len());
            self.last_block[0..src_slice.len()].copy_from_slice(src_slice);            
            self.last_block_size = src_slice.len();

        } 
    }

    #[inline]
    fn sha1_compress(h0: u32, h1: u32, h2: u32, h3: u32, h4: u32, m_block: &[u8]) 
        -> (u32, u32 ,u32 ,u32, u32) 
    {        
        let mut a = h0;
        let mut b = h1;
        let mut c = h2;
        let mut d = h3;
        let mut e = h4;

        if DEBUG {
            println!("Entering sha_compress with: {} {} {} {} {}", a, b, c, d, e);
        }

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
            
            if DEBUG {
                println!("{} {} {} {} {}", a, b, c, d, e);
            }
        }

        return (a, b, c, d, e)     
    }

    #[inline]
    fn update_state(&mut self, a: u32, b: u32, c: u32, d: u32, e: u32) {
        self.h0 = self.h0.wrapping_add(a);
        self.h1 = self.h1.wrapping_add(b);
        self.h2 = self.h2.wrapping_add(c);
        self.h3 = self.h3.wrapping_add(d);
        self.h4 = self.h4.wrapping_add(e); 

        if DEBUG {
            println!(" -> state: [{}]", self.get_hexstate());
        } 
    }

    /// Expands the block of 512 bits to an array of 80 32-bit words
    #[inline]
    fn expand(m_block: &[u8]) -> [u32; 80] {
        let mut W = [0u32; 80];  
        // Assert the block is 64 bytes (512 bits)
        assert_eq!(m_block.len(), BLOCK_SIZE_BYTES);
        unsafe {
            let p32: &[u32] = std::mem::transmute(m_block);
            // Ensure the block is 16 32-bit words (512 bits)
            // assert_eq!(p32.len(), 16); // This is not happening    
            // panic!("m_block len: {:02x} - p32_len: {:02x}", m_block.len(), p32.len());
            for i in 0..16 {
                W[i] = p32[i].to_be();
            }
        }      
        // println!("{:?}", W);
        for i in 16..80 {
            W[i] = (W[i - 3] ^ W[i - 8] ^ W[i - 14] ^ W[i - 16]).rotate_left(1);
        }
        W
    }
}

