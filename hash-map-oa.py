# Description: Contains a Hash map ADT that uses a dynamic array and Hash entry class as the underlying data structures.
#              Implements Open Addressing with Quadratic Probing for collision resolution inside that dynamic array.

from underlying-data-structures import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        """
        return self._capacity

    def put(self, key: str, value: object) -> None:
        """
        Updates the key/value pair in the hash map.

        :param key: string that defines key
        :param value: object for value

        :return: none
        """
        # Doubles current capacity when current load factor is greater than or equal to 0.5
        if self.table_load() >= 0.5:
            self.resize_table(self._next_prime(self._capacity * 2))

        # Uses quadratic probing to find appropriate spot
        index = self._hash_function(key) % self._capacity
        initial_index = index
        probe = 0
        while probe < self._capacity:
            # Adds a new key/value pair if spot is empty or a tombstone and updates size
            if self._buckets[index] is None or self._buckets[index].is_tombstone:
                self._buckets[index] = HashEntry(key, value)
                self._buckets[index].is_tombstone = False
                self._size += 1
                return
            # Replaces associated value if key exists
            if self._buckets[index].key == key:
                self._buckets[index].value = value
                return
            probe += 1
            index = (initial_index + probe ** 2) % self._capacity

    def table_load(self) -> float:
        """
        Returns the current hash table load factor.

        :return: float of load factor
        """
        # Calculates the load factor
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table.

        :return: integer of empty buckets
        """
        # Counts how many empty buckets are in the hash table and returns that count
        count = 0
        for index in range(self._capacity):
            if self._buckets[index] is None or self._buckets[index].is_tombstone:
                count += 1
        return count

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the internal hash table. All existing key/value pairs must remain in the new hash map,
        and all hash table links are rehashed.

        :param new_capacity: integer of capacity to be resized to

        :return: none
        """
        # Does nothing if given capacity less than current number of elements in hash map
        if new_capacity < self._size:
            return

        # Checks if given capacity is prime and finds the closest prime number if not
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # Gets the key/value pairs and clears the internal buckets
        key_value_da = self.get_keys_and_values()
        self.clear()
        # Removes all buckets and adds the new correct amount of buckets
        self._buckets = DynamicArray()
        for space in range(new_capacity):
            self._buckets.append(None)

        # Updates the capacity and rehashes existing key/value pairs in the hash map based on the new capacity
        self._capacity = new_capacity
        for pair in range(key_value_da.length()):
            key, value = key_value_da[pair]
            self.put(key, value)

    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key. Returns None if the key is not in the hash map.

        :param key: string of key to be found

        :return: value associated with key
        """
        # Searches for key in the hash map using quadratic probing and returns value for it if found
        index = self._hash_function(key) % self._capacity
        initial_index = index
        probe = 0
        while probe < self._capacity:
            if self._buckets[index] is not None:
                if not self._buckets[index].is_tombstone and self._buckets[index].key == key:
                    return self._buckets[index].value
            probe += 1
            index = (initial_index + probe ** 2) % self._capacity
        # Returns None if key is not in the hash map
        return None

    def contains_key(self, key: str) -> bool:
        """
        Returns True if given key is in the hash map, otherwise it returns False.

        :param key: string of key to search for

        :return: boolean of whether key was found
        """
        # Searches for key in the hash map using quadratic probing and returns boolean for whether it is found
        index = self._hash_function(key) % self._capacity
        initial_index = index
        probe = 0
        while probe < self._capacity:
            if self._buckets[index] is not None:
                if self._buckets[index].key == key and not self._buckets[index].is_tombstone:
                    return True
            probe += 1
            index = (initial_index + probe ** 2) % self._capacity
        return False

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map. Does nothing if the key is not in it.

        :param key: string of key to be removed

        :return: none
        """
        # Finds key to be removed using quadratic probing
        index = self._hash_function(key) % self._capacity
        initial_index = index
        probe = 0
        while probe < self._capacity:
            if self._buckets[index] is not None:
                # Updates tombstone status and hash map size if key is found and not a tombstone
                if self._buckets[index].key == key and not self._buckets[index].is_tombstone:
                    self._buckets[index].is_tombstone = True
                    self._size -= 1
                    return
            probe += 1
            index = (initial_index + probe ** 2) % self._capacity

    def clear(self) -> None:
        """
        Clears the contents of the hash map. Does not change the underlying hash table capacity.

        :return: none
        """
        # Clears each bucket, leaving current capacity intact
        for index in range(self._capacity):
            self._buckets[index] = None
        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array where each index contains a tuple of a key/value pair stored in the hash map.

        :return: dynamic array with tuples of key/value pairs
        """
        # Creates a new dynamic array and adds each key/value pair in the hash map to it, then returns that array
        key_value_da = DynamicArray()
        for element in self:
            value = element.key, element.value
            key_value_da.append(value)
        return key_value_da

    def __iter__(self):
        """
        Enables the hash map to iterate across itself. Returns self.
        """
        self._index = 0
        while self._index < self._capacity and self._buckets[self._index] is None:
            self._index += 1
        return self

    def __next__(self):
        """
        Obtain next active value and advance iterator.
        """
        while self._index < self._capacity and (self._buckets[self._index] is None or
                                                self._buckets[self._index].is_tombstone):
            self._index += 1

        try:
            current_entry = self._buckets[self._index]
            self._index += 1
            return current_entry
        except DynamicArrayException:
            raise StopIteration
          
