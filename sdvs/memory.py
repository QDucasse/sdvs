# -*- coding: utf-8 -*-
# ===========================================
# author:         Quentin Ducasse
# email:  quentin.ducasse@ensta-bretagne.org
# github:    https://github.com/QDucasse
# ===========================================
# Memory: Holds the configuration and knows how to access the elements providing an address

from sdvs.constants import *


def gen_bin_number_ones(width):
    res = 0b1
    for i in range(width):
        res |= 1 << i
    return res


def gen_bin_number_zeros(width):
    return ~(gen_bin_number_ones(width))


class Memory:

    def __init__(self):
        self.raw_memory = 0b0

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
        self.raw_memory |= (gen_bin_number_zeros(SIZE_BOOL) << address)
        self.raw_memory |= (bool_value << address)

    def set_byte_at_address(self, byte_value, address):
        self.raw_memory |= (gen_bin_number_zeros(SIZE_BYTE) << address)
        self.raw_memory |= (byte_value << address)

    def set_int_at_address(self, int_value, address):
        self.raw_memory |= (gen_bin_number_zeros(SIZE_INT) << address)
        self.raw_memory |= (int_value << address)

    def set_state_at_address(self, state_value, address):
        self.raw_memory |= (gen_bin_number_zeros(SIZE_STATE) << address)
        self.raw_memory |= (state_value << address)

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
