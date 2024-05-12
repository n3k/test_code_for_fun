mod sha1;


#[cfg(test)]
mod tests {
    use self::sha1::Sha1;

    use super::*;

    #[test]
    fn it_works() {
        assert_eq!(4, 4);
    }

    #[test]
    fn test_sha1_a() {
        let mut sha1 = Sha1::new();
        sha1.update(b"abcd");
        assert_eq!("81fe8bfe87576c3ecb22426f8e57847382917acf", sha1.hexdigest());
    }

    #[test]
    fn test_sha1_b() {
        let mut sha1 = Sha1::new();
        let x = &std::iter::repeat(0x41).take(512).collect::<Vec<u8>>();
        
        sha1.update(x);

        assert_eq!("10106f85d6ff9e833817fea16ae015fd9f81795c", sha1.hexdigest());
    }

    #[test]
    fn test_sha1_c() {
        let mut sha1 = Sha1::new();
        sha1.update(b"abcd");
        sha1.update(b"XXXX");
        assert_eq!("1aebef8daf612dce818fcb45e22bbf29c85654cf", sha1.hexdigest());
    }

    #[test]
    fn test_sha1_d() {
        let mut sha1 = Sha1::new();
        sha1.update(&std::iter::repeat(0x41).take(64).collect::<Vec<u8>>());
        sha1.update(&std::iter::repeat(0x42).take(64).collect::<Vec<u8>>());
        sha1.update(&std::iter::repeat(0x43).take(32).collect::<Vec<u8>>());
        sha1.update(&std::iter::repeat(0x44).take(32).collect::<Vec<u8>>());        
        assert_eq!("f13f852bee209d37616014a5732c382e167447a0", sha1.hexdigest());
    }

    #[test]
    fn test_sha1_e() {
        let mut sha1 = Sha1::new();
        sha1.update(&std::iter::repeat(0x41).take(64).collect::<Vec<u8>>());
        sha1.update(&std::iter::repeat(0x42).take(64).collect::<Vec<u8>>());
        sha1.update(&std::iter::repeat(0x43).take(27).collect::<Vec<u8>>());
        sha1.update(&std::iter::repeat(0x44).take(32).collect::<Vec<u8>>());        
        assert_eq!("f13f852bee209d37616014a5732c382e167447a0", sha1.hexdigest());
    }



    #[test]
    fn test_transmute() {
        let v1 = &mut [0u8; 32];        
        let v2: &mut [u32; 8]  = unsafe {
            std::mem::transmute(v1)
        };
        v2[0] = 0x41414141;
        v2[1] = 0x42424242;

        let v1: &mut [u8; 32]  = unsafe {
            std::mem::transmute(v2)
        };
        
        for x in v1 {
            println!("{:02x}", *x);
        }

    }
}
