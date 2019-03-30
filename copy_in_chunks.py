import os
import sys 

g_step = 1024*1024
source_file = sys.argv[1]
source_size = os.path.getsize(source_file)
target_file = sys.argv[2]
skip = int(sys.argv[3])
bytes_remaining = source_size - skip
print("Source Size: %.02f" % (source_size / float(g_step)))

with open(target_file, "ab") as dst:
    dst.seek(skip)
    with open(source_file, "rb") as src:
        src.seek(skip)
        while bytes_remaining > 0:
            if bytes_remaining < g_step:
                dst.write(src.read(bytes_remaining))
                skip += bytes_remaining
                bytes_remaining = 0             
            else:                
                dst.write(src.read(g_step))
                skip += g_step
                bytes_remaining = bytes_remaining - g_step
            print("bytes copied: %d" % skip)

print("Done!")