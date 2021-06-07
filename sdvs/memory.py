# -*- coding: utf-8 -*-
# ===========================================
# author:         Quentin Ducasse
# email:  quentin.ducasse@ensta-bretagne.org
# github:    https://github.com/QDucasse
# ===========================================
# Memory: Holds the configuration and knows how to access the elements providing an address

from constants import *


def gen_bin_number_ones(width):
    res = 0b1
    for i in range(width):
        res |= 1 << i
    return res


class Memory:

    def __init__(self, size=0, raw_memory=0b0):
        self.raw_memory = raw_memory
        self.size = size

    def set_bits(self, value, address, data_type):
        """
        Replace bits in the memory with the given value.
        :param value: value to add
        :param address: address of the changed value
        :param data_type: type of the value
        """
        type_size = TYPES_TO_SIZE[data_type]
        all_ones = gen_bin_number_ones(self.size - (address + type_size))
        left = all_ones << (address + type_size)  # Set all the bits in the left of address + type size
        right = ((1 << address) - 1)              # Set all the bits in the right of address
        mask = left | right                       # Bitwise or to mask get all bits set except in the range
        masked_memory = self.raw_memory & mask    # Clear bits from address and for the type size
        value_shifted = value << address          # Move the value in the cleared position
        self.raw_memory = masked_memory | value_shifted

    def retrieve_bool_at_address(self, address):
        return (self.raw_memory & (gen_bin_number_ones(SIZE_BOOL) << address)) >> address

    def retrieve_byte_at_address(self, address):
        return (self.raw_memory & (gen_bin_number_ones(SIZE_BYTE) << address)) >> address

    def retrieve_int_at_address(self, address):
        return (self.raw_memory & (gen_bin_number_ones(SIZE_INT) << address)) >> address

    def retrieve_state_at_address(self, address):
        return (self.raw_memory & (gen_bin_number_ones(SIZE_STATE) << address)) >> address

    def retrieve_at_address(self, data_type, address):
        return self.RETRIEVE_TYPE[data_type](self, address)

    def set_bool_at_address(self, bool_value, address):
        self.set_bits(bool_value, address, VAL_BOOL)

    def set_byte_at_address(self, byte_value, address):
        self.set_bits(byte_value, address, VAL_BYTE)

    def set_int_at_address(self, int_value, address):
        self.set_bits(int_value, address, VAL_INT)

    def set_state_at_address(self, state_value, address):
        self.set_bits(state_value, address, VAL_STATE)

    def set_at_address(self, data_type, value, address):
        self.SET_TYPE[data_type](self, value, address)

    RETRIEVE_TYPE = {
        VAL_BOOL: retrieve_bool_at_address,
        VAL_BYTE: retrieve_byte_at_address,
        VAL_INT: retrieve_int_at_address,
        VAL_STATE: retrieve_state_at_address
    }

    SET_TYPE = {
        VAL_BOOL: set_bool_at_address,
        VAL_BYTE: set_byte_at_address,
        VAL_INT: set_int_at_address,
        VAL_STATE: set_state_at_address
    }

    # def __hash__(self):
    #     return hash(self.raw_memory)
    #
    # def __eq__(self, other):
    #     if isinstance(other, Memory):
    #         return (self.raw_memory == other.raw_memory) and (self.size == other.size)
    #     return False