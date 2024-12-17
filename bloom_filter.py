import math
import hashlib

class BloomFilter:
    def __init__(self, size, hash_count):
        self.size = size
        self.hash_count = hash_count
        self.bit_array = [0] * size
        self.count = 0
        self.capacity = 0

    def insert(self, element):
        indices = self.hash_element(element)
        for index in indices:
            self.bit_array[index] = 1
        self.count += 1

    def is_full(self):
        return self.count >= self.capacity

    def query(self, element):
        indices = self.hash_element(element)
        return all(self.bit_array[index] for index in indices)

    def hash_element(self, element):
        hashes = []
        for i in range(self.hash_count):
            result = hashlib.sha256(f"{element}_{i}".encode()).hexdigest()
            hashes.append(int(result, 16) % self.size)
        return hashes


class ExtensibleBloomFilter:
    def __init__(self, initial_size, hash_count, false_positive_rate):
        self.initial_size = initial_size
        self.hash_count = hash_count
        self.false_positive_rate = false_positive_rate
        self.vectors = []
        self.active_index = -1
        self.init_first_vector()

    def init_first_vector(self):
        capacity = int(self.initial_size * (-math.log(self.false_positive_rate) / (math.log(2) ** 2)))
        bf = BloomFilter(self.initial_size, self.hash_count)
        bf.capacity = capacity
        self.vectors.append(bf)
        self.active_index = 0

    def add(self, element):
        active_vector = self.vectors[self.active_index]
        if active_vector.is_full():
            self.extend_ebf()
        self.vectors[self.active_index].insert(element)

    def extend_ebf(self):
        new_size = self.vectors[-1].size * 2
        new_capacity = self.vectors[-1].capacity * 2
        bf = BloomFilter(new_size, self.hash_count)
        bf.capacity = new_capacity
        self.vectors.append(bf)
        self.active_index += 1

    def query(self, element):
        for vector in self.vectors:
            if vector.query(element):
                return True
        return False
