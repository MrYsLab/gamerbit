# This is a work in progress! Use At Your Own Caution

## A micro:bit MicroPython Class To Control The  [Sparkfun gamer:bit Board](https://www.sparkfun.com/products/14215)
![logo](https://raw.github.com/MrYsLab/gamerbit/master/images/gamer_bit.jpg)


## gamerbit.py
The GamerBit class provides an easy to use Python interface for the Sparkfun gamer:bit board.
It contains its own self-starting event loop that monitors 
state changes for all the gamer:bit buttons, including the *Poke home connectors* 
used for external inputs. 

It uses an event driven pattern that only sends changes upon a state detection and frees
your application from having to poll the individual pins.

To receive notification of state changes, you must specify a callback
function when instantiating the GamerBit class. A callback function must be specified when GamerBit is
instantiated.

```
# GamerBit API:
class GamerBit:
    """
    This class supports the Sparkfun gamer:bit board.
    When instantiating, you must specify a callback function
    that will receive a state change report when a button is pressed
    or released.

    A callback report is a Python dictionary that contains elements for all pins
    that have changed state. The keys for this report are:
    'pin0', 'pin1', 'pin2', 'pin8', 'pin12', 'pin16', 'button_a', 'button_b'
    
    For example, if the P0 button is pressed, the report you should expect
    to see is:
    
    {'pin0': 1}
    
    The value for the entry specifies the state, 1 = pressed or on and 0 = released or off.

    Reports are only generated when there is a state change, allowing you to
    craft event driven applications.
    

    Be cautious in crafting your callback function, since it is a blocking
    call. Keep it as short as possible.

    If you wish to receive notification of multiple buttons being pressed
    simultaneously, increast the scans parameter to a value where multiple
    button presses are being reported. For example, to get notification of
    2 buttons being pressed simultaneously, set scans to 4.
    
    """
    def __init__(self, callback, scans=1):
        """
        
        Set the callback function and number of scans
        per polling cycle
        :param callback: external callback function
        :param scans: Number of scans to perform before report is generated
        """
        
        
# Usage Example:
def my_gamer_bit_callback_handler(report):
   # examine the report and act upon it to support your
   # application
   
# instantiate the GamerBit class

gb = GamerBit(my_gamer_bit_callback_handler)

```

## Using the class
[This article](https://microbit-playground.co.uk/howto/add-python-module-microbit-micropython) explains how to add
a third party library, like k_motor.py, to the micro:bit persistent file system.

Although more "pythonic" than simply adding the GamerBit class to the top of of the application, as was done for the [included
example](https://github.com/MrYsLab/gamerbit/blob/master/examples/example.py), this method has some drawbacks. If you
make any changes to the application, the entire procedure of loading of the application and library has to be repeated.

Therefore, adding the GamerBit class to the top of the application during development is more convenient. Once the application is
debugged and complete, using the persistent file system method is totally appropriate.

To help save value memory space in the micro:bit, a minimized file, 
[gamer_bit_minimized.py](https://github.com/MrYsLab/gamerbit/blob/master/gamer_bit_minimized.py)
 has been provided for your convenience. It removes all comments and 
unnecessary while space from gamerbit.py.

