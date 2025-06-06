import uos

def check_space(path):
    try:
        # Get file system stats
        stat = uos.statvfs(path)

        # Calculate available and total space
        block_size = stat[0]
        total_blocks = stat[2]
        free_blocks = stat[3]

        total_space = block_size * total_blocks  # In bytes
        free_space = block_size * free_blocks

        print(f"=== Storage info for '{path}' ===")
        print("Total space: {:.2f} MB".format(total_space / (1024 * 1024)))
        print("Free space: {:.2f} MB\n".format(free_space / (1024 * 1024)))
    except Exception as e:
        print("Could not access '{}': {}".format(path, e))

# Check internal flash
check_space("/")
