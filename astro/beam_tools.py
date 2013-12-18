from numpy import radians,exp,log10,sin,meshgrid
from numpy import linspace,sqrt
import scipy.constants as con
import scipy.integrate as sciint
import scipy.special as special

def calc_obj_angle(ang, units="arcsec"):
    if units == "radians":
        ang_r = ang
    else:
        if units == "arcsec":
            div = 3600.0
        if units == "min":
            div = 60.0
        if units == "deg":
            div = 1.0
        ang_r = radians(ang/div)

    return ang_r**2/(con.pi/4)

def plank_intensity(freq, T,units="si"):
    si = 2.0*con.h*(freq**3)/(con.c**2)/(exp((con.h*freq)/(con.k*T)) - 1.0)

    if units == "si":
        return si
    else:
        return si/(1.0e-26)

def rj_intensity(wavelength, T, units="si"):
    si = 2*con.k*T/(wavelength**2)
    if units == "si":
        return si
    else:
        return si/1.0e-26

def rj_integral(wav1, wav2, T, units="si"):
    val,error = sciint.quad(lambda x: rj_intensity(x,T), wav1, wav2)
    return val

def calc_sky_power(cf,bw,sky_T,dish_diameter,units="w"):
    #This does do any site conditions
    #Also does redundant calcs

    cl = con.c/cf
    A_eff = con.pi*pow(dish_diameter/2.0,2)
    solid_angle = pow(cl,2)/A_eff
    intensity = plank_intensity(cf,sky_T)

    flux = solid_angle*intensity
    recieved_power = flux*A_eff*bw

    if units == "w":
        return recieved_power
    else:
        return 10*log10(recieved_power) + 30

def calc_power(cf,bw,obj_size,obj_T,dish_diameter,units="w"):
    solid_angle = calc_obj_angle(obj_size)
    intensity = plank_intensity(cf,obj_T)

    A_eff = con.pi*pow(dish_diameter/2.0,2)

    flux = solid_angle*intensity
    recieved_power = flux*A_eff*bw

    if units == "w":
        return recieved_power
    else:
        return 10*log10(recieved_power) + 30

def calc_rj_power(cf,bw,obj_size,obj_T,dish_diameter,units="w"):
    solid_angle = calc_obj_angle(obj_size)
    intensity = rj_intensity((con.c/cf),obj_T)

    A_eff = con.pi*pow(dish_diameter/2.0,2)

    flux = solid_angle*intensity
    recieved_power = flux*A_eff*bw

    if units == "w":
        return recieved_power
    else:
        return 10*log10(recieved_power) + 30

def oned_rec_beam(freq,fnumber, dish_diameter,x_samples):
    wl = con.c/freq
    dish_r = dish_diameter/2.0
    wavek = 2*con.pi/wl
    platescale = 1/(dish_r*2.0*fnumber)
    x_scaled = x_samples*platescale/1000.0
    u = wavek*dish_r*sin(x_scaled)
    AA = pow(2*special.j1(u)/u,2)

    return AA


def twod_rec_beam(freq,fnumber,dish_diameter,size,n_samples):
    wl = con.c/freq
    dish_r = dish_diameter/2.0
    wavek = 2*con.pi/wl
    platescale = 1/(dish_r*2.0*fnumber)

    x = linspace(-size/2.0, size/2.0,n_samples)
    xx,yy = meshgrid(x,x)
    rr = sqrt(xx*xx + yy*yy)

    r_scaled = rr*platescale/1000.0
    u = wavek*dish_r*sin(r_scaled)
    AA = pow(2*special.j1(u)/u,2)

    return AA
    

