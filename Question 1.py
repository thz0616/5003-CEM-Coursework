import random


class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(size)]

    def insert(self, key):
        index = hash_function(key, self.size)
        self.table[index].append(key)
        return len(self.table[index]) > 1  # Return True if collision occurred


def hash_function(ic_number, table_size):
    # convert IC number to string
    ic_str = str(ic_number)

    # make sure the IC number is 12 digits
    if len(ic_str) != 12:
        # extend the ic with zeros if too short or too long
        ic_str = ic_str.zfill(12)[:12]

    # divide into chunks of 4 digits
    chunks = [int(ic_str[i:i + 4]) for i in range(0, len(ic_str), 4)]

    # sum of the chunks
    hash_value = sum(chunks)

    # hash value
    return hash_value % table_size


def generate_random_ic():
    """Generate a random 12-digit Malaysian IC Number"""
    # Simplified approach - generate a fixed-format 12-digit number
    # Format: YYMMDDSTNNNG where ST is state code and NNNG is a 4-digit number

    # Birth date portion (6 digits)
    year = random.randint(0, 99)
    month = random.randint(1, 12)
    day = random.randint(1, 31)

    # BP code - state code (01-16 or other valid codes)
    state_codes = [
        "01", "02", "03", "04", "05", "06", "07", "08", "09", "10",
        "11", "12", "13", "14", "15", "16", "21", "22", "23", "24",
        "25", "26", "27", "28", "29", "30", "31", "32", "33", "34",
        "35", "36", "37", "38", "39", "40", "41", "42", "43", "44",
        "45", "46", "47", "48", "49", "50", "51", "52", "53", "54",
        "55", "56", "57", "58", "59"
    ]
    bp_code = random.choice(state_codes)

    # Last 4 digits
    last_digits = random.randint(0, 9999)

    # Combine into a 12-digit string
    ic_str = f"{year:02d}{month:02d}{day:02d}{bp_code}{last_digits:04d}"

    # Safety check
    if len(ic_str) != 12:
        # Force it to be 12 digits
        ic_str = ic_str.zfill(12)[:12]

    return int(ic_str)


def run_code():
    # Create two hash tables with different sizes
    first_table = HashTable(1009)
    second_table = HashTable(2003)

    # Statistics variables
    first_table_collisions = [0] * 10
    second_table_collisions = [0] * 10

    # Run 10 rounds
    for round_num in range(10):
        # Reset tables for each round
        first_table = HashTable(1009)
        second_table = HashTable(2003)

        # Insert 1000 random IC numbers
        for _ in range(1000):
            ic = generate_random_ic()
            if first_table.insert(ic):
                first_table_collisions[round_num] += 1
            if second_table.insert(ic):
                second_table_collisions[round_num] += 1

    # Calculate statistics
    total_first_collisions = sum(first_table_collisions)
    total_second_collisions = sum(second_table_collisions)
    avg_first_collisions = total_first_collisions / 10
    avg_second_collisions = total_second_collisions / 10

    first_collision_rate = (avg_first_collisions / 1000) * 100
    second_collision_rate = (avg_second_collisions / 1000) * 100

    # Display statistics
    print("\nTotal Number of Collisions for the First Hash Table:", total_first_collisions)
    print("Total Number of Collisions for the Second Hash Table:", total_second_collisions)
    print("Collision Rate for the First Hash Table: {:.2f} %".format(first_collision_rate))
    print("Collision Rate for the Second Hash Table: {:.2f} %".format(second_collision_rate))


if __name__ == "__main__":
    run_code()
