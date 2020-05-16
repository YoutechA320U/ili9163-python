# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import numbers
import time
import numpy as np

import spidev
import RPi.GPIO as GPIO


__version__ = '0.0.5'

BG_SPI_CS_BACK = 0
BG_SPI_CS_FRONT = 1

SPI_CLOCK_HZ = 16000000

# Constants for interacting with display registers.
ILI9163_TFTWIDTH = 128
ILI9163_TFTHEIGHT = 160

ILI9163_COLS = 128
ILI9163_ROWS = 160

ILI9163_NOP = 0x00
ILI9163_SWRESET = 0x01
ILI9163_RDDID = 0x04
ILI9163_RDDST = 0x09

ILI9163_SLPIN = 0x10
ILI9163_SLPOUT = 0x11
ILI9163_PTLON = 0x12
ILI9163_NORON = 0x13

ILI9163_RDMODE = 0x0A
ILI9163_RDMADCTL = 0x0B
ILI9163_RDPIXFMT = 0x0C
ILI9163_RDIMGFMT = 0x0A
ILI9163_RDSELFDIAG = 0x0F

ILI9163_INVOFF = 0x20
ILI9163_INVON = 0x21
ILI9163_GAMMASET = 0x26
ILI9163_DISPOFF = 0x28
ILI9163_DISPON = 0x29

ILI9163_CASET = 0x2A
ILI9163_RASET = 0x2B
ILI9163_RAMWR = 0x2C
ILI9163_RAMRD = 0x2E

ILI9163_PTLAR = 0x30
ILI9163_MADCTL = 0x36
ILI9163_PIXFMT = 0x3A
ILI9163_COLMOD = 0x3A

ILI9163_FRMCTR1 = 0xB1
ILI9163_FRMCTR2 = 0xB2
ILI9163_FRMCTR3 = 0xB3
ILI9163_INVCTR = 0xB4
ILI9163_DFUNCTR = 0xB6
ILI9163_DISSET5 = 0xB6


ILI9163_PWCTR1 = 0xC0
ILI9163_PWCTR2 = 0xC1
ILI9163_PWCTR3 = 0xC2
ILI9163_PWCTR4 = 0xC3
ILI9163_PWCTR5 = 0xC4
ILI9163_VMCTR1 = 0xC5
ILI9163_VMCTR2 = 0xC7

ILI9163_RDID1 = 0xDA
ILI9163_RDID2 = 0xDB
ILI9163_RDID3 = 0xDC
ILI9163_RDID4 = 0xDD

ILI9163_GMCTRP1 = 0xE0
ILI9163_GMCTRN1 = 0xE1

ILI9163_PWCTR6 = 0xFC

# Colours for convenience
ILI9163_BLACK = 0x0000  # 0b 00000 000000 00000
ILI9163_BLUE = 0x001F  # 0b 00000 000000 11111
ILI9163_GREEN = 0x07E0  # 0b 00000 111111 00000
ILI9163_RED = 0xF800  # 0b 11111 000000 00000
ILI9163_CYAN = 0x07FF  # 0b 00000 111111 11111
ILI9163_MAGENTA = 0xF81F  # 0b 11111 000000 11111
ILI9163_YELLOW = 0xFFE0  # 0b 11111 111111 00000
ILI9163_WHITE = 0xFFFF  # 0b 11111 111111 11111


def color565(r, g, b):
    """Convert red, green, blue components to a 16-bit 565 RGB value. Components
    should be values 0 to 255.
    """
    return ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)


def image_to_data(image, rotation=0):
    """Generator function to convert a PIL image to 16-bit 565 RGB bytes."""
    # NumPy is much faster at doing this. NumPy code provided by:
    # Keith (https://www.blogger.com/profile/02555547344016007163)
    pb = np.rot90(np.array(image.convert('RGB')), rotation // 90).astype('uint16')
    color = ((pb[:, :, 0] & 0xF8) << 8) | ((pb[:, :, 1] & 0xFC) << 3) | (pb[:, :, 2] >> 3)
    return np.dstack(((color >> 8) & 0xFF, color & 0xFF)).flatten().tolist()


class ILI9163(object):
    """Representation of an ILI9163 TFT LCD."""

    def __init__(self, port, cs, dc, backlight=None, rst=None, width=ILI9163_TFTWIDTH,
                 height=ILI9163_TFTHEIGHT, rotation=90, offset_left=None, offset_top=None, invert=True, spi_speed_hz=4000000):
        """Create an instance of the display using SPI communication.

        Must provide the GPIO pin number for the D/C pin and the SPI driver.

        Can optionally provide the GPIO pin number for the reset pin as the rst parameter.

        :param port: SPI port number
        :param cs: SPI chip-select number (0 or 1 for BCM
        :param backlight: Pin for controlling backlight
        :param rst: Reset pin for ILI9163
        :param width: Width of display connected to ILI9163
        :param height: Height of display connected to ILI9163
        :param rotation: Rotation of display connected to ILI9163
        :param offset_left: COL offset in ILI9163 memory
        :param offset_top: ROW offset in ILI9163 memory
        :param invert: Invert display
        :param spi_speed_hz: SPI speed (in Hz)

        """

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        self._spi = spidev.SpiDev(port, cs)
        self._spi.mode = 0
        self._spi.lsbfirst = False
        self._spi.max_speed_hz = spi_speed_hz

        self._dc = dc
        self._rst = rst
        self._width = width
        self._height = height
        self._rotation = rotation
        self._invert = invert

        # Default left offset to center display
        if offset_left is None:
            offset_left = (ILI9163_COLS - width) // 2

        self._offset_left = offset_left

        # Default top offset to center display
        if offset_top is None:
            offset_top = (ILI9163_ROWS - height) // 2

        self._offset_top = offset_top

        # Set DC as output.
        GPIO.setup(dc, GPIO.OUT)

        # Setup backlight as output (if provided).
        self._backlight = backlight
        if backlight is not None:
            GPIO.setup(backlight, GPIO.OUT)
            GPIO.output(backlight, GPIO.LOW)
            time.sleep(0.1)
            GPIO.output(backlight, GPIO.HIGH)

        # Setup reset as output (if provided).
        if rst is not None:
            GPIO.setup(rst, GPIO.OUT)

        self.reset()
        self._init()

    def send(self, data, is_data=True, chunk_size=4096):
        """Write a byte or array of bytes to the display. Is_data parameter
        controls if byte should be interpreted as display data (True) or command
        data (False).  Chunk_size is an optional size of bytes to write in a
        single SPI transaction, with a default of 4096.
        """
        # Set DC low for command, high for data.
        GPIO.output(self._dc, is_data)
        # Convert scalar argument to list so either can be passed as parameter.
        if isinstance(data, numbers.Number):
            data = [data & 0xFF]
        self._spi.xfer3(data)

    def set_backlight(self, value):
        """Set the backlight on/off."""
        if self._backlight is not None:
            GPIO.output(self._backlight, value)

    @property
    def width(self):
        return self._width if self._rotation == 0 or self._rotation == 180 else self._height

    @property
    def height(self):
        return self._height if self._rotation == 0 or self._rotation == 180 else self._width

    def command(self, data):
        """Write a byte or array of bytes to the display as command data."""
        self.send(data, False)

    def data(self, data):
        """Write a byte or array of bytes to the display as display data."""
        self.send(data, True)

    def reset(self):
        """Reset the display, if reset pin is connected."""
        if self._rst is not None:
            GPIO.output(self._rst, 1)
            time.sleep(0.500)
            GPIO.output(self._rst, 0)
            time.sleep(0.500)
            GPIO.output(self._rst, 1)
            time.sleep(0.500)

    def _init(self):
        # Initialize the display.

        self.command(ILI9163_SWRESET)    # Software reset
        time.sleep(0.150)               # delay 150 ms

        self.command(ILI9163_SLPOUT)     # Out of sleep mode
        time.sleep(0.500)               # delay 500 ms

        self.command(ILI9163_FRMCTR1)    # Frame rate ctrl - normal mode
        self.data(0x0a)
        self.data(0x14)

        self.command(ILI9163_PWCTR1)     # Power control
        self.data(0xA2)
        self.data(0x02)                 # -4.6V
        self.data(0x84)                 # auto mode

        self.command(ILI9163_VMCTR1)     # Power control
        self.data(0x2f)
        self.data(0x3e)

        self.command(ILI9163_VMCTR2)     # Power control
        self.data(0x40)

        if self._invert:
            self.command(ILI9163_INVOFF)  # Don't invert display
        else:
            self.command(ILI9163_INVON)   # Invert display

        self.command(ILI9163_MADCTL)     # Memory access control (directions)
        self.data(0xC0)                 # row addr/col addr, bottom to top refresh

        self.command(ILI9163_COLMOD)     # set color mode
        self.data(0x05)                 # 16-bit color

        self.command(ILI9163_CASET)      # Column addr set
        self.data(0x00)                 # XSTART = 0
        self.data(0x00)
        self.data(0x00)
        self.data(0x7f)

        self.command(ILI9163_RASET)      # Row addr set
        self.data(0x00)
        self.data(0x00)
        self.data(0x00)
        self.data(0x9f)

        self.command(ILI9163_GMCTRP1)    # Set Gamma
        self.data(0x02)
        self.data(0x1c)
        self.data(0x07)
        self.data(0x12)
        self.data(0x37)
        self.data(0x32)
        self.data(0x29)
        self.data(0x2d)
        self.data(0x29)
        self.data(0x25)
        self.data(0x2B)
        self.data(0x39)
        self.data(0x00)
        self.data(0x01)
        self.data(0x03)
        self.data(0x10)

        self.command(ILI9163_GMCTRN1)    # Set Gamma
        self.data(0x03)
        self.data(0x1d)
        self.data(0x07)
        self.data(0x06)
        self.data(0x2E)
        self.data(0x2C)
        self.data(0x29)
        self.data(0x2D)
        self.data(0x2E)
        self.data(0x2E)
        self.data(0x37)
        self.data(0x3F)
        self.data(0x00)
        self.data(0x00)
        self.data(0x02)
        self.data(0x10)

        self.command(ILI9163_NORON)      # Normal display on
        time.sleep(0.10)                # 10 ms

        self.command(ILI9163_DISPON)     # Display on
        time.sleep(0.100)               # 100 ms

    def begin(self):
        """Set up the display

        Deprecated. Included in __init__.

        """
        pass

    def set_window(self, x0=0, y0=0, x1=None, y1=None):
        """Set the pixel address window for proceeding drawing commands. x0 and
        x1 should define the minimum and maximum x pixel bounds.  y0 and y1
        should define the minimum and maximum y pixel bound.  If no parameters
        are specified the default will be to update the entire display from 0,0
        to width-1,height-1.
        """
        if x1 is None:
            x1 = self._width - 1

        if y1 is None:
            y1 = self._height - 1

        y0 += self._offset_top
        y1 += self._offset_top

        x0 += self._offset_left
        x1 += self._offset_left

        self.command(ILI9163_CASET)       # Column addr set
        self.data(x0 >> 8)
        self.data(x0)                    # XSTART
        self.data(x1 >> 8)
        self.data(x1)                    # XEND
        self.command(ILI9163_RASET)       # Row addr set
        self.data(y0 >> 8)
        self.data(y0)                    # YSTART
        self.data(y1 >> 8)
        self.data(y1)                    # YEND
        self.command(ILI9163_RAMWR)       # write to RAM

    def display(self, image):
        """Write the provided image to the hardware.

        :param image: Should be RGB format and the same dimensions as the display hardware.

        """
        # Set address bounds to entire display.
        self.set_window()
        # Convert image to array of 16bit 565 RGB data bytes.
        # Unfortunate that this copy has to occur, but the SPI byte writing
        # function needs to take an array of bytes and PIL doesn't natively
        # store images in 16-bit 565 RGB format.
        pixelbytes = list(image_to_data(image, self._rotation))
        # Write data to hardware.
        self.data(pixelbytes)
