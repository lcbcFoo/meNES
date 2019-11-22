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

class PPUMASK : public Register8Bit {
public:

    const uint32_t EMPHASIZE_BLUE_BIT = 7;
    const uint32_t EMPHASIZE_GREEN_BIT = 6;
    const uint32_t EMPHASIZE_RED_BIT = 5;
    const uint32_t SHOW_SPRITE_BIT = 4;
    const uint32_t SHOW_BACKGROUND_BIT = 3;
    const uint32_t SHOW_LEFTMOST_SPRITE_BIT = 2;
    const uint32_t SHOW_LEFTMOST_BACKGROUND_BIT = 1;
    const uint32_t GREYSCALE_BIT = 0;

    PPUMASK() : Register8Bit() {}

    void reset() {
        store(0);
    }

    uint32_t read() {
        return load();
    }

    void write(uint32_t value, bool sys) {
        if (sys)
            return;
        store(value);
    }

    bool isEmphasizeBlueEnabled() {
        return isBitSet(EMPHASIZE_BLUE_BIT);
    }
    bool isEmphasizeGreenEnabled() {
        return isBitSet(EMPHASIZE_GREEN_BIT);
    }
    bool isEmphasizeRedEnabled() {
        return isBitSet(EMPHASIZE_RED_BIT);
    }
    bool isSpriteEnabled() {
        return isBitSet(SHOW_SPRITE_BIT);
    }
    bool isBackgroundEnabled() {
        return isBitSet(SHOW_BACKGROUND_BIT);
    }
    bool isLeftmostSpriteEnabled() {
        return isBitSet(SHOW_LEFTMOST_SPRITE_BIT);
    }
    bool isLeftmostBackgroundEnabled() {
        return isBitSet(SHOW_LEFTMOST_BACKGROUND_BIT);
    }
    bool isGrayScaleEnabled() {
        return isBitSet(GREYSCALE_BIT);
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

    py::class_<PPUMASK, Register8Bit>(m, "PPUMASK")
        .def(py::init<>())
        .def("reset", &PPUMASK::reset)
        .def("read", &PPUMASK::read)
        .def("write", &PPUMASK::write)
        .def("isEmphasizeBlueEnabled", &PPUMASK::isEmphasizeBlueEnabled)
        .def("isEmphasizeGreenEnabled", &PPUMASK::isEmphasizeGreenEnabled)
        .def("isEmphasizeRedEnabled", &PPUMASK::isEmphasizeRedEnabled)
        .def("isSpriteEnabled", &PPUMASK::isSpriteEnabled)
        .def("isBackgroundEnabled", &PPUMASK::isBackgroundEnabled)
        .def("isLeftmostBackgroundEnabled", &PPUMASK::isLeftmostBackgroundEnabled)
        .def("isLeftmostSpriteEnabled", &PPUMASK::isLeftmostSpriteEnabled)
        .def("isGrayScaleEnabled", &PPUMASK::isGrayScaleEnabled);
}
