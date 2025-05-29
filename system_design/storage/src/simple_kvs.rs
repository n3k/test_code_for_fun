//! Simple text Key-Value Storage
//! From Designing Data Intensive Applications (Chapter 3)
//! 
//! 

use std::collections::HashMap;
use std::fs::{File, OpenOptions};
use std::io::{self, BufRead, BufReader, Seek, SeekFrom, Write, ErrorKind};

struct SimpleKVS {
    filename: &'static str,
    fd      : File,
    /// An index of keys into the file
    index   : Option<HashMap<String, usize>>
}

impl SimpleKVS {

    /// Deletes an existent KVS db
    pub fn delete(filename: &'static str) -> Result<(), Box<dyn std::error::Error>> {
        std::fs::remove_file(filename)?;
        println!("db {} deleted successfully!", filename);
        Ok(())
    }

    /// Opens an existing KVS database or creates a new one
    pub fn open(filename: &'static str) -> Self {

        match OpenOptions::new()
            .read(true)
            .write(true)
            .append(true) 
            .create(false)
            .open(filename)
        {
            Ok(f) => {
                println!("KVS: {} opened successfully!\n", filename);                
                Self {
                    filename,
                    fd: f,
                    index: None
                }
            }
            Err(e) => {
                if e.kind() == ErrorKind::NotFound {
                    // Create a new file
                    match File::create_new(filename) {
                        Ok(f) => {
                            println!("KVS: {} created successfully!\n", filename);
                            Self {
                                filename,
                                fd: f,
                                index: None
                            }           
                        }
                        Err(e) => {
                            panic!("File::create_new error: {:?}", e);        
                        }
                    }
                } else {
                    panic!("File::open error: {:?}", e);
                }
            }
        }
    }

    /// Get a value from the database
    fn get(&mut self, key: &str) -> Option<String> {
        match self.fd.seek(SeekFrom::Start(0)) {
            Ok(_) => {                
                let mut value: Option<String> = None;
                let reader = BufReader::new(&mut self.fd);
                for line in reader.lines() {
                    match line {
                        Ok(line) => {
                            if let Some((k, v)) = line.split_once(',') {
                                if k == key {
                                    value = Some(v.to_string());
                                }
                            }
                        } 
                        Err(e) => {
                            println!("error reading file: {:?}", e);
                            return None;
                        }
                    }                    
                }
                return value;
            }
            Err(e) => {
                panic!("error seeking to the start of db: {:?}", e);
            }
        }        
    }

    /// Sets a value in the database
    fn set(&mut self, key: &str, value: &str) {
        match self.fd.seek(SeekFrom::End(0)) {
            Ok(_) => {
                let entry = format!("{},{}\n", key, value);
                if let Err(e) = self.fd.write(entry.as_bytes()) {
                    panic!("error writing entry to db: {:?}", e);
                }
            }
            Err(e) => {
                panic!("error seeking to end of db: {:?}", e);
            }
        }        
    }   

}


#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn kvs_test1() {
        
        let _ = SimpleKVS::delete("/tmp/foobar.kvs");
        let mut kvs = SimpleKVS::open("/tmp/foobar.kvs");
        kvs.set("123", "foobar");
        kvs.set("a", "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA");
        kvs.set("b", "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA");
        kvs.set("c", "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA");
        kvs.set("d", "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA");
        kvs.set("e", "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA");
        kvs.set("f", "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA");
        kvs.set("g", "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA");
        kvs.set("h", "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA");
        kvs.set("123", "newval");

        println!("GET(123) -> {:?}", kvs.get("123"));
    }
}
