//! Simple text Key-Value Storage
//! From Designing Data Intensive Applications (Chapter 3)
//! 
//! 

use std::collections::HashMap;
use std::fs::{File, OpenOptions};
use std::io::{BufRead, BufReader, Seek, SeekFrom, Write, ErrorKind};

/// This is the minimum size of each segment
/// If a value has more than KVS_SEGMENT_MIN_SIZE bytes, then the segment gets extended
pub const KVS_SEGMENT_MIN_SIZE: usize = 128;


/// Each segment must be its own file 
/// For now we're representing it like this only
#[derive(Default, Debug)]
struct Segment {
    /// Offset where the segment starts within the db
    offset  : usize,
    /// Size of the segment
    size    : usize,

    /// Index structure within the segment
    index   :  HashMap<String, usize>
}

struct SegmentedKVS {
    filename: &'static str,
    fd      : File,

    /// Number of active segments in the KVS
    segments: Vec<Segment>,
}

impl SegmentedKVS {

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
            Ok(mut fd) => {
                println!("KVS: {} opened successfully!\n", filename);      

                // Read into segments and create indexes
                //
                //

                let mut segments = Vec::<Segment>::new();
    
                // absolute offset within the file
                let mut file_offset = 0usize;
                
                // current segment
                let mut current_segment = Segment::default();
                current_segment.offset = file_offset;

                let reader = BufReader::new(&mut fd);
                for line in reader.lines() {
                    match line {
                        Ok(line) => {
                                                       
                            // create index into segment
                            if let Some((k, _)) = line.split_once(',') {
                                current_segment.index.insert(k.into(), current_segment.size);
                            }

                            // add line length to current offset
                            file_offset += line.len();

                            // update current segmenet size
                            current_segment.size += line.len();

                            // Check if it is time for a new segment
                            if current_segment.size > KVS_SEGMENT_MIN_SIZE {
                                // Add current segment to segments vector 
                                segments.push(current_segment);

                                // Create new segment
                                current_segment = Segment {
                                    offset  : file_offset,
                                    size    : 0,
                                    index   : HashMap::new()
                                };
                            }
                        } 
                        Err(e) => {
                            panic!("error reading file: {:?}", e);                            
                        }
                    }
                }

                Self {
                    filename,
                    fd: fd,
                    segments: segments
                }
            }
            Err(e) => {
                if e.kind() == ErrorKind::NotFound {
                    // Create a new file
                    match File::create_new(filename) {
                        Ok(fd) => {
                            println!("KVS: {} created successfully!\n", filename);
                            Self {
                                filename,
                                fd: fd,
                                segments: vec![Segment::default()],
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
        // Query the indexes of the segments in reverse order
        let mut jj = self.segments.len() - 1;
        loop {
            let segment = self.segments.get(jj)
                                        .expect("invalid segment index?");
            if let Some(entry_offset) = segment.index.get(key) {
                let file_offset = segment.offset + entry_offset;
                
                match self.fd.seek(SeekFrom::Start(file_offset as u64)) {
                    Ok(_) => {                                        
                        let mut reader = BufReader::new(&mut self.fd);
                        let mut buf = String::new();
                        match reader.read_line(&mut buf) {
                            Ok(_) => {
                                if let Some((_, val)) = buf.split_once(',') {
                                    return Some(val.into());
                                } else {
                                    panic!("invalid key delimiter?");
                                }                                
                            }
                            Err(e) => {
                                panic!("error reading line: {:?}", e);
                            }
                        }
                    }
                    Err(e) => {
                        panic!("error seeking to the target segment within the db: {:?}", e);
                    }
                }     
            }

            if jj == 0 {
                break;
            } else {
                jj -= 1;
            }
        }
        
        None
    }

    /// Sets a value in the database
    fn set(&mut self, key: &str, value: &str) {

        // Grab the last segment and seek into the File to the end of it
        if let Some(last_segment) = self.segments.last_mut() {
            let offset = last_segment.offset + last_segment.size;
            match self.fd.seek(SeekFrom::Start(offset as u64)) {
                Ok(_) => {
                    let entry = format!("{},{}\n", key, value);
                    if let Err(e) = self.fd.write(entry.as_bytes()) {
                        panic!("error writing entry to db: {:?}", e);
                    }

                    // Update segment index
                    last_segment.index.insert(key.into(), last_segment.size);

                    last_segment.size += entry.len();

                    if last_segment.size > KVS_SEGMENT_MIN_SIZE {                        
                        // Create new segment
                        let new_segment = Segment {
                            offset  : offset + entry.len(),
                            size    : 0,
                            index   : HashMap::new()
                        };

                        self.segments.push(new_segment);
                    }
                }
                Err(e) => {
                    panic!("error seeking to end of db: {:?}", e);
                }
            }
        } else {
            panic!("no segments in KVS?");
        }
             
    }   

}


#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn segmented_kvs_test1() {
        
        let _ = SegmentedKVS::delete("/tmp/foobar.kvs");
        let mut kvs = SegmentedKVS::open("/tmp/foobar.kvs");
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

        for s in kvs.segments.iter() {
            println!("{:?}", s);
        }

        println!("GET(123) -> {:?}", kvs.get("123"));
    }
}
