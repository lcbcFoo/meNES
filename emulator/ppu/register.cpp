#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>
#include <iostream>
#include <vector>
#include <tuple>
#include <algorithm>
#include <map>
#include <cstdlib>

namespace py = pybind11;
using namespace std;

class Register {
public:
    uint32_t size;
    uint32_t mod;
    uint32_t data;

    Register(uint32_t s) {
        size = s;
        mod = 1 << s;
    }

    uint32_t load() {
        return data % mod;
    }

    uint32_t loadBit(uint32_t pos) {
        return (data >> pos) & 1;
    }

    uint32_t loadBits(uint32_t start, uint32_t offset) {
        uint32_t mask = ((mod - 1) >> start) % (1 << offset);
        return ((data >> start) & mask) % mod;
    }

    void store(uint32_t value) {
        data = value % mod;
    }

    void storeBit(uint32_t pos, uint32_t value) {
        uint32_t mask = (1 << pos);
        data &= ~mask;
        data |= (value << pos);
        data %= mod;
    }

    void storeBits(uint32_t start, uint32_t offset, uint32_t val) {
        uint32_t mask = ((1 << offset) - 1) << (start);
        data = (data & ~mask);
        data = (data + ((val << start) & mask)) % mod;
    }

    void clear() {
        data = 0;
    }

    void clearBit(uint32_t pos) {
        storeBit(pos, 0);
    }

    bool isBitSet(uint32_t pos) {
        return loadBit(pos) == 1;
    }

    void increment() {
        data = (data + 1) % mod;
    }

    void add(uint32_t value) {
        data = (data + value) % mod;
    }

    void decrement() {
        data = (data - 1) % mod;
    }

    void sub(uint32_t val) {
        data = (data - val) % mod;
    }

    uint32_t shift(uint32_t carry_in) {
        uint32_t carry_out = loadBit(size - 1);
        data = ((data << 1) + (carry_in & 1)) % mod;
        return carry_out;
    }
};

class Register8Bit : public Register {
public:    
    Register8Bit() : Register(8) {}
};

class Register16Bit : public Register {    
public:
    Register16Bit() : Register(16) {}

    uint32_t loadHigherByte() {
        return loadBits(8, 8);
    }

    uint32_t loadLowerByte() {
        return loadBits(0, 8);
    }

    void storeHigherByte(uint32_t value) {
        storeBits(8, 8, value);
    }

    void storeLowerByte(uint32_t value) {
        storeBits(0, 8, value);
    }
};


PYBIND11_MODULE(register, m) {
    py::class_<Register>(m, "Register")
        .def(py::init<uint32_t>())
        .def("load", &Register::load)
        .def("loadBit", &Register::loadBit)
        .def("loadBits", &Register::loadBits)
        .def("store", &Register::store)
        .def("storeBit", &Register::storeBit)
        .def("storeBits", &Register::storeBits)
        .def("clear", &Register::clear)
        .def("clearBit", &Register::clearBit)
        .def("isBitSet", &Register::isBitSet)
        .def("increment", &Register::increment)
        .def("add", &Register::add)
        .def("decrement", &Register::decrement)
        .def("sub", &Register::sub)
        .def("shift", &Register::shift);

    py::class_<Register8Bit, Register>(m, "Register8Bit")
        .def(py::init<>());

    py::class_<Register16Bit, Register>(m, "Register16Bit")
        .def(py::init<>())
        .def("loadHigherByte", &Register16Bit::loadHigherByte)
        .def("loadLowerByte", &Register16Bit::loadLowerByte)
        .def("storeHigherByte", &Register16Bit::storeHigherByte)
        .def("storeLowerByte", &Register16Bit::storeLowerByte);
}
