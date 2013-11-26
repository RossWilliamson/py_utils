import struct
from numpy import array,pi,arctan2

class zbf_reader:
    def __init__(self, filename):
        self.fn = filename
        self.read_data()

    def read_data(self):
        with open(self.fn, "rb") as f:
            data = f.read()
            #Boring long list of stuff in the header
            #See page 694-695 of ZEMAX 13 manual 
            #integer is 4 bytes, double i 8 bytes
            #integer is
            self.file_format = struct.unpack('i',data[0:4])
            self.nx,self.ny = struct.unpack('ii',data[4:12])
            self.polarized = struct.unpack('i',data[12:16])
            self.units = struct.unpack('i',data[16:20])
            #next for integers are ignored
            self.unused_integer = struct.unpack('4i',data[20:36])
            self.x_spacing,self.y_spacing = struct.unpack('dd',data[36:52])
            self.x_pos_pilot_z = struct.unpack('d',data[52:60])            
            self.x_rayleigh_distance = struct.unpack('d',data[60:68])
            self.x_waist_size = struct.unpack('d',data[68:76])
            self.y_pos_waist_z = struct.unpack('d',data[76:84])
            self.y_rayleigh_distance = struct.unpack('d',data[84:92])
            self.y_waist_size = struct.unpack('d',data[92:100])
            self.wavelength = struct.unpack('d',data[100:108])
            self.n_i = struct.unpack('d',data[108:116])
            self.rec_eff = struct.unpack('d',data[116:124])
            self.sys_eff = struct.unpack('d',data[124:132])
            self.double_unused = struct.unpack('8d',data[132:196])

            #Ok so we are now at the data section
            num_of_points = self.nx*self.ny*2
            array_start = 196
            array_end = array_start + num_of_points*8
            t_str = "%id" % num_of_points
            temp_data = struct.unpack(t_str, data[array_start:array_end])
            temp_data = array(temp_data)
            self.data = temp_data[::2] + 1j*temp_data[1::2]
            self.data = self.data.reshape(self.nx,self.ny)

            self.I = (self.data*self.data.conjugate()).real
            self.phase = arctan2(self.data.imag,self.data.real)

            #create the x and y axes
            
