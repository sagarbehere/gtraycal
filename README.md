gtraycal
========

A standalone program providing a dropdown calendar that sits in the systray. Intended to emulate the functionality of the calendar in gnome2 panel

## Installation and execution ##

You need the python gtk2 bindings installed on your computer. For a debian based system, this can be done with

$ sudo aptitude install python-gtk2

You can run the program with the command

$ python gtraycal.py

Alternatively, you can set execute permissions (you need to do this only once)

$ chmod +x gtraycal.py

and run the program with

$ ./gtraycal.py

## Configuration ##

If a configuration file is passed to gtraycal via the -c command line parameter [e.g: ./gtraycal.py -c ./gtraycal.conf], then the program will try to read locations from the configuration file and display the current time at those locations in the dropdown calendar.
An example configuration file, gtraycal.conf,  is provided and it's format should be self-explanatory.
Valid timezone strings may be picked up from /usr/share/zoneinfo on most Linux distributions.

NOTE: The pop up calendar window displays the time in the timezone at the instant when the window pops up. This time is then NOT UPDATED on screen, while the window is being displayed.


