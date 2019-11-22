#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <iostream>

namespace py = pybind11;
using namespace std;

class DecoderCpp {
public:
    py::object get_x;
    py::object get_y;
    py::object get_pc;
    py::object mem_bus;
    py::object mem_read;

    // Accessible by python
    uint32_t cont_zp = 0;
    uint32_t cont_zp_y = 0;
    uint32_t cont_zp_x = 0;
    uint32_t addr_y = 0;
    uint32_t addr_x = 0;
    uint32_t full_addr = 0;
    uint32_t full_addr_x = 0;
    uint32_t full_addr_y = 0;
    uint32_t pointer_content_x = 0;
    uint32_t pointer_content_y = 0;
    uint32_t pointer_addr_x = 0;
    uint32_t pointer_addr_y = 0;
    uint32_t pointer_addr = 0;
    uint32_t content_x = 0;
    uint32_t content_y = 0;
    uint32_t content = 0;
    uint32_t immediate = 0;



    DecoderCpp(py::object cpu, py::object mem_bus) {
        get_y = cpu.attr("get_y");
        get_x = cpu.attr("get_x");
        get_pc = cpu.attr("get_pc");
        this->mem_bus = mem_bus;
        this->mem_read = mem_bus.attr("read");
    }

    void update(string instr_type) {
        uint32_t pc = get_pc().cast<uint32_t>();
        uint32_t x = get_x().cast<uint32_t>();
        uint32_t y = get_y().cast<uint32_t>();

        uint32_t opcode = mem_read(pc, 1, true).cast<uint32_t>() & 0xff;
        uint32_t low = mem_read(pc + 1, 1, true).cast<uint32_t>() & 0xff;
        uint32_t high = mem_read(pc + 2, 1, true).cast<uint32_t>() & 0xff;

        /* cout << "Decoder: op = " << hex << opcode */
        /*     << ", low = " << hex << low << ", high = " << hex << high << endl; */

        immediate = low;

        // Zeropage
        if (instr_type == "zeropage") {
            cont_zp = mem_read(low, 1, true).cast<uint32_t>() & 0xff;
            return;
        }

        uint32_t local_addr_x = low + x;
        addr_x = local_addr_x & 0xff;
        uint32_t local_addr_y = low + y;
        addr_y = local_addr_y & 0xff;

        if (instr_type == "zeropage_x") {
            cont_zp_x = mem_read(addr_x, 1, true).cast<uint32_t>() & 0xff;
            return;
        }

        if (instr_type == "zeropage_y") {
            cont_zp_y = mem_read(addr_y, 1, true).cast<uint32_t>() & 0xff;
            return;
        }

        // Absolute
        full_addr = (high << 8) + low;
        full_addr_x = (high << 8) + local_addr_x;
        full_addr_y = (high << 8) + local_addr_y;

        if (instr_type == "absolute") {
            if (opcode >= 0x8C && opcode <= 0x8E){
              return;
            }
            content = mem_read(full_addr, 1).cast<uint32_t>() & 0xff;
            return;
        }

        if (instr_type == "absolute_x") {
            content_x = mem_read(full_addr_x, 1).cast<uint32_t>() & 0xff;
            return;
        }

        if (instr_type == "absolute_y") {
            content_y = mem_read(full_addr_y, 1).cast<uint32_t>() & 0xff;
            return;
        }

        // Indirect
        if (instr_type == "indirect") {
            pointer_addr = mem_read(full_addr, 1, true).cast<uint32_t>();
            pointer_addr += mem_read((full_addr + 1) & 0xff, 1, true)
                                .cast<uint32_t>() << 8;
        }

        if (instr_type == "indirect_x") {
            pointer_addr_x = mem_read(addr_x, 1, true).cast<uint32_t>();
            pointer_addr_x += mem_read((addr_x + 1) & 0xff, 1, true)
                                .cast<uint32_t>() << 8;
            pointer_content_x =
                mem_read(pointer_addr_x, 1, true).cast<uint32_t>() & 0xff;
        }

        if (instr_type == "indirect_y") {
            pointer_addr_y = mem_read(low, 1, true).cast<uint32_t>();
            pointer_addr_y += y;
            pointer_addr_y += mem_read((low + 1) & 0xff, 1, true)
                                .cast<uint32_t>() << 8;
            pointer_content_y =
                mem_read(pointer_addr_y, 1, true).cast<uint32_t>() & 0xff;
        }
    }
};

PYBIND11_MODULE(decoder_cpp, m) {
    py::class_<DecoderCpp>(m, "DecoderCpp")
        .def(py::init<py::object, py::object>())
        .def_readwrite("cont_zp", &DecoderCpp::cont_zp)
        .def_readwrite("cont_zp_y", &DecoderCpp::cont_zp_y)
        .def_readwrite("cont_zp_x", &DecoderCpp::cont_zp_x)
        .def_readwrite("addr_y", &DecoderCpp::addr_y)
        .def_readwrite("addr_x", &DecoderCpp::addr_x)
        .def_readwrite("full_addr", &DecoderCpp::full_addr)
        .def_readwrite("full_addr_x", &DecoderCpp::full_addr_x)
        .def_readwrite("full_addr_y", &DecoderCpp::full_addr_y)
        .def_readwrite("pointer_content_x", &DecoderCpp::pointer_content_x)
        .def_readwrite("pointer_content_y", &DecoderCpp::pointer_content_y)
        .def_readwrite("pointer_addr_x", &DecoderCpp::pointer_addr_x)
        .def_readwrite("pointer_addr_y", &DecoderCpp::pointer_addr_y)
        .def_readwrite("pointer_addr", &DecoderCpp::pointer_addr)
        .def_readwrite("content_x", &DecoderCpp::content_x)
        .def_readwrite("content_y", &DecoderCpp::content_y)
        .def_readwrite("content", &DecoderCpp::content)
        .def_readwrite("immediate", &DecoderCpp::immediate)
        .def("update", &DecoderCpp::update);
}
