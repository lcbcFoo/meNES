#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <iostream>

namespace py = pybind11;
using namespace std;


typedef struct MemPair {
    int type;
    uint8_t* mem;
    int addr;
} MemPair;

class MemBusCpp {
public:
    uint8_t ram[0x2000] = {0};
    uint8_t io[0x2020] = {0};
    uint8_t exp_rom[0x1FE0] = {0};
    uint8_t sram[0x2000] = {0};
    uint8_t prg_rom[0x8000] = {0};
    uint8_t null[1] = {0};
    bool _16kb = true;

    py::object controllers;
    py::object ppu;
    bool ppu_init = false;

    MemBusCpp(bool is16kb) {
        py::object Controller = py::module::import("cpu.controllers").attr("Controller");
        controllers = Controller();

        _16kb = is16kb;
    }
    
    inline MemPair addr_mux(int bus_addr) {
        MemPair ret;
        ret.type = 0;

        if (bus_addr < 0x2000) {
            ret.mem = ram;
            ret.addr = bus_addr % 0x0800;
        }

        else if (bus_addr < 0x4000) {
            ret.mem = io;
            ret.type = 1;
            ret.addr = (bus_addr - 0x2000) % 0x0008;
        } 
        else if (bus_addr < 0x4020) {
            ret.mem = io;
            ret.type = 1;
            ret.addr = (bus_addr - 0x2000);
        } 
        else if (bus_addr < 0x6000) {
            ret.mem = exp_rom;
            ret.addr = bus_addr - 0x4020;
        } 
        else if (bus_addr < 0x8000) {
            ret.mem = sram;
            ret.addr = bus_addr - 0x6000;
        } 
        else if (bus_addr < 0x10000) {
            if (_16kb) {
                ret.mem = prg_rom;
                ret.addr = (bus_addr - 0x8000) % 0x4000;
            }
            else{
                ret.mem = prg_rom;
                ret.addr = bus_addr - 0x8000;
            }
        } 
        else {
            ret.mem = null;
            ret.addr = 0;
        }
        return ret;
    }

    inline bool is_ppu_addr(const MemPair mem, int curr_addr) {
        return (mem.type == 1 && 
                ((curr_addr >= 0x2000 && curr_addr <= 0x2007) 
                 || curr_addr == 0x4014));
    }

    void set_ppu(py::object ppu_obj) {
        ppu = ppu_obj;
        ppu_init = true;
    }

    void write(int addr, int data, bool sys) { 
        const MemPair mem = addr_mux(addr);
        int curr_addr = mem.addr + 0x2000;

        if (is_ppu_addr(mem, curr_addr)) {
            // write to ppu
            if (ppu_init) {
                py::object wr = ppu.attr("register_write");
                wr(curr_addr, data & 0xff, sys);
            }
        }

        else if (mem.mem == io) {
            if (curr_addr == 0x4016) {
                py::object p1 = controllers.attr("get_ctrl1_input");
                data = p1().cast<int>();
                py::object s = controllers.attr("set_state");
                s(0, data & 0xff);
            }
            else if (curr_addr == 0x4017) {
                py::object p2 = controllers.attr("get_ctrl2_input");
                data = p2().cast<int>();
                py::object s = controllers.attr("set_state");
                s(1, data & 0xff);
            }
        }

        mem.mem[mem.addr] = static_cast<uint8_t>(data & 0xFF);
    }

    void write_n(int base_addr, int n,
            py::array_t<uint8_t, py::array::c_style | py::array::forcecast> data,
            bool sys) {
        py::buffer_info buf1 = data.request();
        uint8_t* ptr = static_cast<uint8_t*>(buf1.ptr);

        for (int i = 0; i < n; ++i) {
            write(base_addr + i, ptr[i], sys);
        }
    }

    uint8_t read(int addr, bool sys) {
        const MemPair mem = addr_mux(addr);
        int data = 0;
        int curr_addr = mem.addr + 0x2000;
        if (is_ppu_addr(mem, curr_addr)) {
            // read from ppu
            if (ppu_init) {
                py::object rd = ppu.attr("register_read");
                data = rd(curr_addr, sys).cast<int>();
            }
        }
        else if (mem.mem == io && (curr_addr == 0x4016 || curr_addr == 0x4017)) {
            py::object s = controllers.attr("get_state");
            data = (s(curr_addr % 2).cast<int>() & 0x80) >> 7;
        }
        else {
            data = mem.mem[mem.addr];
        }
        return static_cast<uint8_t> (data);
    }

    py::array_t<uint8_t> read_n(int base_addr, int n, bool sys) {
        py::array_t<uint8_t> res = py::array_t<uint8_t>(n);
        py::buffer_info buf1 = res.request();
        uint8_t* ptr = static_cast<uint8_t*>(buf1.ptr);
    
        for (int i = 0; i < n; ++i) {
            ptr[i] = read(base_addr + i, sys);
        }
        return res;
    } 
};

PYBIND11_MODULE(mem_bus_cpp, m) {
    py::class_<MemBusCpp>(m, "MemBus")
        .def(py::init<bool>())
        .def("write", &MemBusCpp::write)
        .def("read", &MemBusCpp::read)
        .def("set_ppu", &MemBusCpp::set_ppu)
        .def("write_n", &MemBusCpp::write_n)
        .def("read_n", &MemBusCpp::read_n);
}
