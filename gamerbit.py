"""
    gamerbit.py

    This class is used for monitoring the SparkFun gamer:bit board

    https://www.sparkfun.com/products/14215

    The MIT License (MIT)

    Copyright (c) 2018 Alan Yorinks

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.
"""

from microbit import pin0, pin1, pin2, pin8,\
                     pin12, pin16, button_a, button_b


class GamerBit:
    def __init__(self, callback, scans=1):
        """
        Set the pullups for the on-board switches.
        Note:
            pin 5  is button A and
            pin 11 is button B and both are already pulled up
        Set the callback function and number of
        :param callback: external callback function
        :param scans: Number of scans to perform before callback
        """

        # a list of pins monitored by the gamer:bit
        self.pins = [pin0, pin1, pin2, pin8, pin12, pin16, button_a, button_b]

        # callback function to send reports to when there is a change in
        # pin or button state
        self.callback = callback

        # set the number of scans before the callback is executed
        # this allows the detection of multiple buttons pressed

        self.number_of_scans = scans

        # set the pullup resistors
        # don't set pull ups for the buttons
        for pin in self.pins[:-2]:
            pin.set_pull(pin.PULL_UP)

        # initialize the previous readings list
        self.previous_readings = [0] * 8

        # initialize the current readings list
        self.current_readings = [0] * 8

        # start the scanner event loop
        self._scanner()

    def scan(self):
        """
        Read the pins and buttons and "or" the values into the
        current readings list
        :return:
        """
        readings = [int(not pin.read_digital()) for pin in self.pins[:-2]]

        # read buttons
        readings.append(int(button_a.is_pressed()))
        readings.append(int(button_b.is_pressed()))

        #  "or" in the values
        self.current_readings = [int(self.current_readings[pin] or readings[pin])
                                 for pin in range(0, len(readings))]

    def _scanner(self):
        """
        Scan all the pins and call the callback method the current values
        and changes contained in a scan namedtuple.
        :return:
        """

        pin_ids = ['pin0', 'pin1', 'pin2', 'pin8', 'pin12', 'pin16', 'button_a', 'button_b']

        while True:
            # Read each pin and flip its sense. The board normally returns a 0
            # when the button is pressed and 1 when it is not pressed.
            # slice is to ignore buttons in the list
            # readings = [int(not pin.read_digital()) for pin in self.pins[:-2]]

            # read buttons
            # readings.append(int(button_a.is_pressed()))
            # readings.append(int(button_b.is_pressed()))

            for scans in range(0, self.number_of_scans):
                self.scan()
            # self.scan()
            # instantiate report dictionary
            report = {}

            # compare readings with previous reading
            # if they differ, add an entry into report with pin
            # or button name and its current value
            for x in range(0, 8):
                if self.current_readings[x] != self.previous_readings[x]:
                    report[pin_ids[x]] = self.current_readings[x]

            # overwrite previous writings with current readings
            self.previous_readings = self.current_readings
            self.current_readings = [0] * 8

            # if there are any changes, send out report
            # if no callback was registered, display a SAD image
            if report:
                if self.callback:
                    self.callback(report)
