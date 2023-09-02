# Description: Contains a Hash map ADT that uses dynamic array and singly linked lists as underlying data structures.
#              Contains a standalone find mode function using a hash map instance.


from underlying-data-structures import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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
        # Doubles current capacity when current load factor is greater than or equal to 1.0
        if self.table_load() >= 1.0:
            self.resize_table(self._next_prime(self._capacity * 2))

        # Replaces associated value if key exists, otherwise adds a new key/value pair
        bucket = self._hash_function(key) % self._capacity
        linked_list = self._buckets[bucket]
        if linked_list.contains(key):
            linked_list.contains(key).value = value
        else:
            linked_list.insert(key, value)
            self._size += 1

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table

        :return: integer of empty buckets
        """
        # Counts how many empty buckets are in the has table and returns that count
        count = 0
        for bucket in range(self._capacity):
            if self._buckets[bucket].length() == 0:
                count += 1
        return count

    def table_load(self) -> float:
        """
        Returns the current hash table load factor.

        :return: float of load factor
        """
        # Calculates the load factor
        return self._size / self._capacity

    def clear(self) -> None:
        """
        Clears the contents of the hash map. Does not change the underlying hash table capacity.

        :return: none
        """
        # Clears each bucket, leaving current capacity intact
        for bucket in range(self._capacity):
            self._buckets[bucket] = LinkedList()
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the internal hash table. All existing key/value pairs must remain in the new hash map,
        and all hash table links must be rehashed.

        :param new_capacity: integer of capacity to be resized to

        :return: none
        """
        # Does nothing if given capacity less than 1
        if new_capacity < 1:
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
            self._buckets.append(LinkedList())
        # Updates the capacity and rehashes existing key/value pairs in the hash map based on the new capacity
        self._capacity = new_capacity
        for pair in range(key_value_da.length()):
            key, value = key_value_da[pair]
            self.put(key, value)

    def get(self, key: str):
        """
        Returns the value associated with the given key. Returns None if the key is not in the hash map.

        :param key: string of key to be found

        :return: value associated with key
        """
        # Returns None if key is not in the hash map
        if not self.contains_key(key):
            return None

        # Finds node with given value and returns the associated value
        bucket = self._hash_function(key) % self._capacity
        linked_list = self._buckets[bucket]
        for node in linked_list:
            if node.key == key:
                return node.value

    def contains_key(self, key: str) -> bool:
        """
        Returns True if given key is in the hash map, otherwise it returns False.

        :param key: string of key to search for

        :return: boolean of whether key was found
        """
        # Returns False if hash map is empty
        if self._size == 0:
            return False

        # Checks bucket where given key would be and returns True if found or False if not
        bucket = self._hash_function(key) % self._capacity
        if self._buckets[bucket].contains(key):
            return True
        return False

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map. Does nothing if the key is not in it.

        :param key: string of key to be removed

        :return: none
        """
        # Does nothing if key is not in the hash map
        if not self.contains_key(key):
            return

        # Finds key and removes it, then updates the hash map size
        for bucket in range(self._capacity):
            if self._buckets[bucket].contains(key):
                self._buckets[bucket].remove(key)
                self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array where each index contains a tuple of a key/value pair stored in the hash map.

        :return: dynamic array with tuples of key/value pairs
        """
        # Creates a new dynamic array and adds each key/value pair in the hash map to it, then returns that array
        key_value_da = DynamicArray()
        for bucket in range(self._capacity):
            for node in self._buckets[bucket]:
                value = node.key, node.value
                key_value_da.append(value)
        return key_value_da


def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Returns a tuple with a dynamic array consisting of the mode values, and an integer that represents the frequency.
    Implemented with O(N) time complexity.

    :param da: dynamic array, not guaranteed to be sorted

    :return: tuple with dynamic array of mode values, and frequency
    ** endgame is like assignment 2
    """
    # Creates a hash map instance and a new DynamicArray object to hold mode value(s)
    map = HashMap()
    mode_da = DynamicArray()

    # Finds frequency of each element of dynamic array and updates the hash map appropriately
    for i in range(da.length()):
        value = da[i]
        # Uses dynamic array element as key and its frequency as value, updates value with occurrences
        if map.contains_key(value):
            map.put(value, map.get(value) + 1)
        else:
            map.put(value, 1)

    # Finds maximum frequency
    map_da = map.get_keys_and_values()
    frequency = 0
    for pair in range(map_da.length()):
        key, value = map_da[pair]
        frequency = max(frequency, value)

    # Finds values with the maximum frequency and adds to the dynamic array holding the mode value(s)
    for pair in range(map_da.length()):
        key, value = map_da[pair]
        if value == frequency:
            mode_da.append(key)

    # Returns tuple with dynamic array of mode value(s), and frequency
    return mode_da, frequency
  
