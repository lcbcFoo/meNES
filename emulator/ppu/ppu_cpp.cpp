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

typedef vector<int> Color;

vector<Color> PALETTES {
        Color{0, 0, 0},
        Color{0, 30, 116},
        Color{8, 16, 144},
        Color{48, 0, 136},
        Color{68, 0, 100},
        Color{92, 0, 48},
        Color{84, 4, 0},
        Color{60, 24, 0},
        Color{32, 42, 0},
        Color{8, 58, 0},
        Color{0, 64, 0},
        Color{0, 60, 0},
        Color{0, 50, 60},
        Color{0, 0, 0},
        Color{0, 0, 0},
        Color{0, 0, 0},
        Color{152, 150, 152},
        Color{8, 76, 196},
        Color{48, 50, 236},
        Color{92, 30, 228},
        Color{136, 20, 176},
        Color{160, 20, 100},
        Color{152, 34, 32},
        Color{120, 60, 0},
        Color{84, 90, 0},
        Color{40, 114, 0},
        Color{8, 124, 0},
        Color{0, 118, 40},
        Color{0, 102, 120},
        Color{0, 0, 0},
        Color{0, 0, 0},
        Color{0, 0, 0},
        Color{236, 238, 236},
        Color{76, 154, 236},
        Color{120, 124, 236},
        Color{176, 98, 236},
        Color{228, 84, 236},
        Color{236, 88, 180},
        Color{236, 106, 100},
        Color{212, 136, 32},
        Color{160, 170, 0},
        Color{116, 196, 0},
        Color{76, 208, 32},
        Color{56, 204, 108},
        Color{56, 180, 204},
        Color{60, 60, 60},
        Color{0, 0, 0},
        Color{0, 0, 0},
        Color{236, 238, 236},
        Color{168, 204, 236},
        Color{188, 188, 236},
        Color{212, 178, 236},
        Color{236, 174, 236},
        Color{236, 174, 212},
        Color{236, 180, 176},
        Color{228, 196, 144},
        Color{204, 210, 120},
        Color{180, 222, 120},
        Color{168, 226, 144},
        Color{152, 226, 180},
        Color{160, 214, 228},
        Color{160, 162, 160},
        Color{0, 0, 0},
        Color{0, 0, 0}
};

class PpuCpp {
public:
    // Register classes
    py::object Register8Bit = py::module::import("ppu.register").attr("Register8Bit");
    py::object Register16Bit = py::module::import("ppu.register").attr("Register16Bit");
    py::object OAMADDR = py::module::import("ppu.registers.oam_address").attr("OAMADDR");
    py::object OAMDATA = py::module::import("ppu.registers.oam_data").attr("OAMDATA");
    py::object OAMDMA = py::module::import("ppu.registers.oam_dma").attr("OAMDMA");
    py::object PPUADDR = py::module::import("ppu.registers.ppu_address").attr("PPUADDR");
    py::object PPUCTRL = py::module::import("ppu.registers.ppu_control").attr("PPUCTRL");
    py::object PPUDATA = py::module::import("ppu.registers.ppu_data").attr("PPUDATA");
    py::object PPUMASK = py::module::import("ppu.registers.ppu_mask").attr("PPUMASK");
    py::object PPUSCROLL = py::module::import("ppu.registers.ppu_scroll").attr("PPUSCROLL");
    py::object PPUSTATUS = py::module::import("ppu.registers.ppu_status").attr("PPUSTATUS");

    // Sprite decoder funcs
    py::object transform_sprites = py::module::import("ppu.sprite_decoder")
        .attr("transform_sprites");

    // Method to draw on screen
    py::object gui_draw;

    // Other objects
    py::object mem_bus;
    py::object cpu;

    // Attributes exposed to python
    bool dma_on_going = false;
    vector<int> oam_memory = vector<int>(256, 0);
    uint8_t dma_page = 0;
    bool nmi_flag = false;

    py::object ppuctrl      = PPUCTRL(this, Register8Bit());
    py::object ppumask      = PPUMASK(this, Register8Bit());
    py::object ppustatus    = PPUSTATUS(this, Register8Bit());
    py::object oamaddr      = OAMADDR(this, Register8Bit());
    py::object oamdata      = OAMDATA(this, Register8Bit());
    py::object ppuscroll    = PPUSCROLL(this, Register16Bit());
    py::object ppuaddr      = PPUADDR(this, Register16Bit());
    py::object ppudata      = PPUDATA(this, Register8Bit());
    py::object oamdma       = OAMDMA(this, Register8Bit());



    map<int, py::object> io_registers = {
        {0x2000, ppuctrl},
        {0x2001, ppumask},
        {0x2002, ppustatus},
        {0x2003, oamaddr},
        {0x2004, oamdata},
        {0x2005, ppuscroll},
        {0x2006, ppuaddr},
        {0x2007, ppudata},
        {0x4014, oamdma},
    };

    // Other attributes

    int32_t cycle = 0;
    int32_t scanline = -1;
    bool background_ready = false;
    uint32_t count = 0;

    // Shift registers
    py::object nameTableRegister = Register8Bit();
    py::object attributeTableLowRegister = Register16Bit();
    py::object attributeTableHighRegister = Register16Bit();
    py::object patternTableLowRegister = Register16Bit();
    py::object patternTableHighRegister = Register16Bit();

    // Latches
    uint32_t nameTableLatch = 0;
    uint32_t attributeTableLowLatch = 0;
    uint32_t attributeTableHighLatch = 0;
    uint32_t patternTableLowLatch = 0;
    uint32_t patternTableHighLatch = 0;

    uint8_t pattern_table_1[256][8][8];
    uint8_t pattern_table_2[256][8][8];

    // vectors
    vector<vector<Color>> screen =
            vector<vector<Color>>(280, vector<Color>(280, Color{0, 0, 0}));
    vector<vector<Color>> background =
            vector<vector<Color>>(280, vector<Color>(280, Color{0, 0, 0}));
    vector<vector<Color>> blank_bg =
            vector<vector<Color>>(280, vector<Color>(280, Color{0, 0, 0}));
    vector<vector<int>> bg = vector<vector<int>>(280, vector<int>(280, 0));




    PpuCpp(py::object bus, py::object gui) {
        gui_draw = gui.attr("draw_screen");
        mem_bus = bus;

        tuple<py::list, py::list> l = transform_sprites(mem_bus.attr("pattern_tables"))
            .cast<tuple<py::list, py::list>>();

        for (int i = 0; i < 256; ++i) {
            for (int j = 0; j < 8; ++j) {
                for (int k = 0; k < 8; ++k) {
                    pattern_table_1[i][j][k] = get<0>(l)[i]
                                            .cast<py::list>()[j]
                                            .cast<py::list>()[k].cast<uint8_t>();
                    pattern_table_2[i][j][k] = get<1>(l)[i]
                                            .cast<py::list>()[j]
                                            .cast<py::list>()[k].cast<uint8_t>();
                }
            }
        }
        reset();
    }

    void reset() {
        for (auto key: io_registers) {
            key.second.attr("reset")();
        }

        cycle = 0;
        scanline = -1;
        dma_on_going = false;

        for (int i = 0; i < 256; i++)
            oam_memory[i] = 0;

        dma_page = 0;
        nmi_flag = false;

        for(size_t i = 0; i < 256; ++i)
            for(size_t j = 0; j < 256; ++j)
                for(size_t k = 0; k < 3; ++k)
                    screen[i][j][k] = 0;

        background_ready = false;
        count = 0;
    }

    void set_cpu(py::object c) {
        cpu = c;
    }

    void register_write(uint32_t addr, uint32_t value, bool sys = false) {
        io_registers[addr].attr("write")(value, sys);
    }

    uint32_t register_read(uint32_t addr, bool sys = false) {
        return io_registers[addr].attr("read")(sys).cast<uint32_t>();
    }

    void run() {
        if (scanline == -1 && cycle == 1) {
            io_registers[0x2002].attr("reg").attr("storeBit")(7, 0);

            if (io_registers[0x2001].attr("isBackgroundEnabled")().cast<bool>())
                render_background();
            else {
                // TODO copy blank_bg to screen
                for(size_t i = 0; i < 240; ++i)
                    for(size_t j = 0; j < 256; ++j)
                        for(size_t k = 0; k < 3; ++k) {
                            screen[i][j][k] = blank_bg[i][j][k];
                        }
            }
        }

        if (scanline >= 0 && scanline < 240) {
            // do nothing
        }

        if (scanline == 240 && cycle == 1 &&
                io_registers[0x2001].attr("isSpriteEnabled")().cast<bool>()) {
            render_sprites();
        }

        if (scanline == 241 && cycle == 1) {
            io_registers[0x2002].attr("reg").attr("storeBit")(7, 1);

            if (io_registers[0x2000].attr("isNMIEnabled")().cast<bool>()) {
                nmi_flag = true;
            }
        }

        cycle++;
        if (cycle == 341) {
            cycle = 0;
            scanline++;

            if (scanline == 261) {
                scanline = -1;
                py::array_t<uint8_t> np_array(240 * 256 * 3);
                uint8_t* ptr = static_cast<uint8_t*>(np_array.request().ptr);

                for(size_t i = 0; i < 240; ++i)
                    for(size_t j = 0; j < 256; ++j)
                        for(size_t k = 0; k < 3; ++k) {
                            ptr[i * 256 * 3 + j * 3 + k] = screen[i][j][k];
                        }
                np_array.resize({240, 256, 3});
                gui_draw(np_array);
            }
        }
    }

    void render_background() {
        uint8_t bg_table[256][8][8];
        if (ppuctrl.attr("isBackgroundPatternTable1000")().cast<bool>())
            memcpy(bg_table, pattern_table_2, 256 * 8 * 8);
        else
            memcpy(bg_table, pattern_table_1, 256 * 8 * 8);

        background_ready = true;
        uint32_t bg_base = 0x2000;
        vector<uint8_t> pallete_map =
                        mem_bus.attr("read")(0x3f00, 8 * 4 + 1).cast<vector<uint8_t>>();
        for (int i = 0; i < 8 * 4 + 1; ++i)
            pallete_map[i] = pallete_map[i] & 0x3f;

        // Background name table is composed by 32 * 32 bytes
        // Last 2 rows of bytes are attributes for color, we will look later

        // Read each byte of the 30 x 32 bytes that are not attribute
        // Each of these bytes is an ID to be looked on the pattern table (sprites)
        for (int i = 0; i < 30; ++i) {
            for (int j = 0; j < 32; j++) {
                uint32_t addr = bg_base + (32 * i) + j;
                uint8_t sprite[8][8];
                int sprite_number = mem_bus.attr("read")(addr, 1).cast<int>();
                memcpy(sprite, &bg_table[sprite_number], 64);

                for (int k1 = 0; k1 < 8; ++k1)
                    for (int k2 = 0; k2 < 8; ++k2) {
                        uint32_t base_i = 8 * i;
                        uint32_t base_j = 8 * j;
                        bg[base_i + k1][base_j + k2] = sprite[k1][k2];
                    }
            }
        }

        // Read the 64 bytes that tell us which palette to use to each sprite
        for (int i = 30; i < 32; ++i) {
            for (int j = 0; j < 32; j++) {
                uint32_t addr = bg_base + (32 * i) + j;
                uint8_t byte = mem_bus.attr("read")(addr, 1).cast<uint8_t>();

                // each attribute separates a tile into 4 2x2 quadrants
                // pal_1 is for the top left, pal_2 for top right,
                // pal_3 bot left and pal_4 bot right

                // palettes are located at address 0x3f00-3f1d
                // 0x3f00 is the background color
                // 0x3f01 - 0x3f04 is the palette ID 1 and so on
                // then the palette ID is basically an offset to add to the
                // pixel bits (0, 1, 2, 3) to search for its matching color

                // Compose the mapping number:color for each palette
                // In all maps, value 0 mirrors background color, which
                // is located at 0x3f00
                uint8_t pal_1 = byte & 0b00000011;
                uint8_t pal_2 = (byte & 0b00001100) >> 2;
                uint8_t pal_3 = (byte & 0b00110000) >> 4;
                uint8_t pal_4 = (byte & 0b11000000) >> 6;

                uint8_t map_1[4];
                uint8_t map_2[4];
                uint8_t map_3[4];
                uint8_t map_4[4];

                map_1[0] = pallete_map[0];
                map_2[0] = pallete_map[0];
                map_3[0] = pallete_map[0];
                map_4[0] = pallete_map[0];
                memcpy(&map_1[1], &pallete_map[pal_1 * 4 + 1], 3);
                memcpy(&map_2[1], &pallete_map[pal_2 * 4 + 1], 3);
                memcpy(&map_3[1], &pallete_map[pal_3 * 4 + 1], 3);
                memcpy(&map_4[1], &pallete_map[pal_4 * 4 + 1], 3);


                // Now we have each map for each quadrant of the 32x32 tile
                // Meaning, 4 16x16 squares
                //     16 16
                //      _ _
                // 16  |_|_| 16
                // 16  |_|_| 16
                //     16 16

                // We define the base address (top left) of the tile we
                // are coloring with this attibute
                uint32_t base_y = (32 * (j / 8)) + 128 * (i - 30);
                uint32_t base_x = (32 * j) % 256;

                // This represents the end of the screen -> finish
                if (base_y >= 224)
                    break;

                for (int k1 = 0; k1 < 16; ++k1) {
                    for (int k2 = 0; k2 < 16; ++k2) {
                        uint32_t y1 = base_y + k1;
                        uint32_t x1 = base_x + k2;
                        uint32_t addr1 = bg[y1][x1];
                        uint32_t val1 = map_1[addr1];
                        screen[y1][x1] = update_color(PALETTES[val1]);

                        uint32_t y2 = base_y + k1;
                        uint32_t x2 = base_x + k2 + 16;
                        uint32_t addr2 = bg[y2][x2];
                        uint32_t val2 = map_2[addr2];
                        screen[y2][x2] = update_color(PALETTES[val2]);

                        uint32_t y3 = base_y + k1 + 16;
                        uint32_t x3 = base_x + k2;
                        uint32_t addr3 = bg[y3][x3];
                        uint32_t val3 = map_3[addr3];
                        screen[y3][x3] = update_color(PALETTES[val3]);

                        uint32_t y4 = base_y + k1 + 16;
                        uint32_t x4 = base_x + k2 + 16;
                        uint32_t addr4 = bg[y4][x4];
                        uint32_t val4 = map_4[addr4];
                        screen[y4][x4] = update_color(PALETTES[val4]);
                    }
                }
            }
        }

        // copy background to screen
        // equivalent to using screen on upper loop, saves a copy
        /* for(size_t i = 0; i < 240; ++i){ */
        /*     for(size_t j = 0; j < 256; ++j) { */
        /*         for(size_t k = 0; k < 3; ++k) { */
        /*             screen[i][j][k] = background[i][j][k]; */
        /*         } */
        /*     } */
        /* } */
    }

    void render_sprites() {
        uint8_t sprite_table[256][8][8];
        if (ppuctrl.attr("isSpritePatternTable1000")().cast<bool>())
            memcpy(sprite_table, pattern_table_2, 256 * 8 * 8);
        else
            memcpy(sprite_table, pattern_table_1, 256 * 8 * 8);

        uint32_t line_count[280] = {0};
        vector<uint8_t> pallete_map =
                        mem_bus.attr("read")(0x3f10, 8 * 4 + 1).cast<vector<uint8_t>>();
        for (int i = 0; i < 8 * 4 + 1; ++i)
            pallete_map[i] = pallete_map[i] & 0x3f;

        for (int i = 0; i < 64; ++i) {
            uint8_t base_addr = 4 * i;

            uint8_t y = oam_memory[base_addr];
            uint8_t sprite_num = oam_memory[base_addr + 1];
            uint8_t attr = oam_memory[base_addr + 2];
            uint8_t x = oam_memory[base_addr + 3];

            // 76543210 - attr
            // ||||||||
            // ||||||++- Palette (4 to 7) of sprite
            // |||+++--- Unimplemented
            // ||+------ Priority (0: in front of background; 1: behind background)
            // |+------- Flip sprite horizontally
            // +-------- Flip sprite vertically
            uint8_t priority = (attr >> 5) & 1;
            if (priority == 1)
                continue;

            uint8_t flip_horizontal = (attr >> 6) & 1;
            uint8_t flip_vertical = (attr >> 7) & 1;

            uint8_t curr_sprite[8][8];
            memcpy(curr_sprite, &sprite_table[sprite_num], 64);

            if (flip_horizontal == 1) {
                for (int ih = 0; ih < 8; ih++) {
                  for (int jh = 0; jh < 4; jh++) {
                    uint8_t htmp = curr_sprite[ih][jh];
                    curr_sprite[ih][jh] = curr_sprite[ih][7-jh];
                    curr_sprite[ih][7-jh] = htmp;
                  }
                }
            }
            if (flip_vertical == 1) {
              for (int iv = 0; iv < 4; iv++) {
                for (int jv = 0; jv < 8; jv++) {
                  uint8_t vtmp = curr_sprite[iv][jv];
                  curr_sprite[iv][jv] = curr_sprite[7-iv][jv];
                  curr_sprite[7-iv][jv] = vtmp;
                }
              }
            }

            uint8_t pal_1 = attr & 0b00000011;

            uint8_t map_1[4];
            map_1[0] = 0x00;
            memcpy(&map_1[1], &pallete_map[pal_1 * 4 + 1], 3);

            for (int iy = 0; iy < 8; iy++) {
                if (line_count[y + iy] < 8) {
                    line_count[y + iy]++;

                    for (int ix = 0; ix < 8; ++ix) {
                        uint8_t cor = map_1[curr_sprite[iy][ix]];

                        if (cor != 0) {
                            screen[y + iy][x + ix] = update_color(PALETTES[cor]);
                        }
                    }
                }
            }
        }
    }

    void write_oam_mem(uint8_t addr, uint8_t val) {
        oam_memory[addr] = val;
    }

    Color update_color(Color color) {
        int output_color[3];
        output_color[0] = color[0];
        output_color[1] = color[1];
        output_color[2] = color[2];

        if (ppumask.attr("isEmphasizeRedEnabled")().cast<bool>())
            output_color[0] = 255;
        if (ppumask.attr("isEmphasizeGreenEnabled")().cast<bool>())
            output_color[1] = 255;
        if (ppumask.attr("isEmphasizeBlueEnabled")().cast<bool>())
            output_color[2] = 255;
        if (ppumask.attr("isEmphasizeBlueEnabled")().cast<bool>()) {
            uint8_t red = output_color[0];
            uint8_t green = output_color[1];
            uint8_t blue = output_color[2];
            uint8_t grayscale = static_cast<uint8_t>(0.3 * red + 0.59 * green +
                    0.11 * blue);
            output_color[0] = grayscale;
            output_color[1] = grayscale;
            output_color[2] = grayscale;
        }

        return Color{output_color[0], output_color[1], output_color[2]};
    }
};


PYBIND11_MODULE(ppu_cpp_module, m) {
    py::class_<PpuCpp>(m, "PpuCpp")
        .def(py::init<py::object, py::object>())
        .def("run", &PpuCpp::run)
        .def("reset", &PpuCpp::reset)
        .def("set_cpu", &PpuCpp::set_cpu)
        .def("register_read", &PpuCpp::register_read)
        .def("register_write", &PpuCpp::register_write)
        .def("write_oam_mem", &PpuCpp::write_oam_mem)
        .def_readwrite("mem_bus", &PpuCpp::mem_bus)
        .def_readwrite("dma_on_going", &PpuCpp::dma_on_going)
        .def_readwrite("dma_page", &PpuCpp::dma_page)
        .def_readwrite("io_registers", &PpuCpp::io_registers)
        .def_readwrite("nmi_flag", &PpuCpp::nmi_flag)
        .def_readwrite("ppuctrl", &PpuCpp::ppuctrl)
        .def_readwrite("ppumask", &PpuCpp::ppumask)
        .def_readwrite("ppustatus", &PpuCpp::ppustatus)
        .def_readwrite("oamaddr", &PpuCpp::oamaddr)
        .def_readwrite("oamdata", &PpuCpp::oamdata)
        .def_readwrite("ppuscroll", &PpuCpp::ppuscroll)
        .def_readwrite("ppuaddr", &PpuCpp::ppuaddr)
        .def_readwrite("ppudata", &PpuCpp::ppudata)
        .def_readwrite("oamdma", &PpuCpp::oamdma);

}
/* int main () { */
/*     for (int i = 0; i < 0x40; i++) */
/*         cout << "(" << get<0>(PALETTES[i]) << ", " << get<1>(PALETTES[i]) << endl; */
/* } */
