import math
from collections import deque

class CacheBlock:
    def __init__(self, tag, data, valid=True):
        self.tag = tag
        self.data = data
        self.valid = valid
        self.lru_counter = 0  # usado para política LRU en 2-way

class Cache:
    def __init__(self, size=64, block_size=4, associativity=1):
        self.block_size = block_size
        self.associativity = associativity
        self.num_blocks = size // block_size
        self.num_sets = self.num_blocks // self.associativity
        self.sets = [[] for _ in range(self.num_sets)]

        # Stats
        self.accesses = 0
        self.hits = 0

    def _get_index_and_tag(self, address):
        block_address = address // self.block_size
        index = block_address % self.num_sets
        tag = block_address // self.num_sets
        return index, tag

    def read(self, address, memory):
        self.accesses += 1
        index, tag = self._get_index_and_tag(address)
        cache_set = self.sets[index]

        # Buscar hit
        for block in cache_set:
            if block.valid and block.tag == tag:
                self.hits += 1
                # LRU: actualizar contador
                for b in cache_set:
                    b.lru_counter += 1
                block.lru_counter = 0
                return block.data

        # Miss: traer de memoria y cargar en caché
        data = memory[address]
        self._replace_block(index, tag, data)
        return data

    def write(self, address, value, memory):
        index, tag = self._get_index_and_tag(address)
        cache_set = self.sets[index]

        # Verificar si está en caché
        for block in cache_set:
            if block.valid and block.tag == tag:
                block.data = value
                memory[address] = value  # Write-through
                return

        # Miss: write-allocate
        memory[address] = value
        self._replace_block(index, tag, value)

    def _replace_block(self, index, tag, data):
        cache_set = self.sets[index]

        if len(cache_set) < self.associativity:
            # Hay espacio
            cache_set.append(CacheBlock(tag, data))
        else:
            # Reemplazo por LRU
            lru_block = max(cache_set, key=lambda b: b.lru_counter)
            lru_block.tag = tag
            lru_block.data = data
            lru_block.lru_counter = 0
            lru_block.valid = True
            for b in cache_set:
                b.lru_counter += 1

    def get_stats(self):
        hit_rate = self.hits / self.accesses if self.accesses else 0
        return {
            "accesses": self.accesses,
            "hits": self.hits,
            "misses": self.accesses - self.hits,
            "hit_rate": round(hit_rate * 100, 2)
        }
