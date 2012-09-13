#!/usr/bin/python
# -*- coding: utf-8 -*-

# Author: Sagar Behere <sagar.behere@gmail.com>, 12 Sept. 2012
# DISCLAIMER: I don't know enough of either Python or GTK+, so there
#		is probably a lot of silliness in this script.
# 		It is just something thrown quickly together because I 
#		wanted a systray calendar that emulates the one in
#		gnome2 panel

# CREDITS: Used code ideas from
# http://eurion.net/python-snippets/snippet/Systray%20icon.html
# http://stackoverflow.com/questions/11132929/showing-a-gtk-calendar-in-a-menu		

# LICENSE: GPLv3. See accompanying file LICENSE.txt for full text

# TODO: 1. Currently only works for horizontal panel. Fix for vertical


import gobject
import pygtk
import gtk
import time
import os.path
import ConfigParser
from datetime import datetime
import ConfigParser
from optparse import OptionParser

global_config = None

try:
	import pytz
except ImportError:
	pytz = None

def display_message(message):
	md = gtk.MessageDialog(None,
            gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, 
            gtk.BUTTONS_CLOSE, message)
        md.run()
        md.destroy()

class Calendar:
	def __init__(self):
		self.cal_window = gtk.Window(gtk.WINDOW_POPUP)
		self.cal_window.set_decorated(False)
		self.cal_window.set_resizable(False)
		self.cal_window.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_DOCK)
		self.cal_window.stick()
		cal_vbox = gtk.VBox(False, 10)
		self.cal_window.add(cal_vbox)
		self.cal = gtk.Calendar()
		self.cal.set_property("show-week-numbers", True)
		cal_vbox.pack_start(self.cal, True, False, 0)
		
		self.locations = list()
		self.gtkLabelpointers = list()
		if (global_config != None) and global_config.has_section('Locations'):
			if (pytz != None):
				self.locations = global_config.items('Locations')
				if len(self.locations) > 0:
					for location in self.locations:
						label = gtk.Label(location[0])						
						cal_vbox.pack_start(label, True, False, 0)
						# locations will contain like 
						self.gtkLabelpointers.append(label)
				else:
					display_message("Please install the pytz package for viewing other timezones")
				
		self.visible = False
		# below lines needed to to get proper placement of
		# calendar popup window for the first time
		# My hypothesis is that it allocates the window geometry
		self.cal_window.show_all()
		self.cal_window.hide_all()
	
	def toggle_visibility(self, icon):
		if self.visible == False:
			# Decide coordinates of the popup calendar window
			[screen, iconarea, trayorientation] = icon.get_geometry()
			rect = self.cal_window.get_allocation()
			x = iconarea.x - rect.width			
			if (iconarea.y < screen.get_height()/2.0): #top panel			
				y = iconarea.y + iconarea.height
			else: # bottom panel
				y = iconarea.y - rect.height

			self.cal_window.move(x,y)
			
			now = datetime.now()
			self.cal.select_month(now.month-1, now.year)
			self.cal.select_day(now.day)
			
			# show time for other locations
			for i in range(len(self.locations)):
				# self.locations looks like, e.g 
				# [('mumbai', 'Asia/Kolkata'), ('stockholm', 'Europe/Stockholm')]
				try:
					tz = pytz.timezone(self.locations[i][1])
					labeltext = self.locations[i][0] + " " + datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')
					self.gtkLabelpointers[i].set_text(labeltext)
				except pytz.UnknownTimeZoneError as zone:
					errorstr =  "unknown timezone " + zone.message
					display_message(errorstr)
			
			self.cal_window.show_all()
			self.visible = True
		else:
			self.cal_window.hide_all()
			self.visible = False

class SystrayIconApp:
	def __init__(self):
		self.tray = gtk.StatusIcon()
		self.tray.set_from_stock(gtk.STOCK_ABOUT) 
		self.tray.connect('popup-menu', self.on_right_click)
		self.tray.connect('activate', self.on_left_click)
		self.tray.set_tooltip(('Calendar'))
		self.calendar = Calendar()
		

    	def on_right_click(self, icon, event_button, event_time):
		menu = gtk.Menu()

		about = gtk.MenuItem("About")
		about.show()
		menu.append(about)
		about.connect('activate', self.show_about_dialog)

		quit = gtk.MenuItem("Quit")
		quit.show()
		menu.append(quit)
		quit.connect('activate', gtk.main_quit)
		
		menu.popup(None, None, gtk.status_icon_position_menu,event_button, event_time, self.tray)

	def on_left_click(self, icon):
		self.calendar.toggle_visibility(self.tray)

	def  show_about_dialog(self, widget):
		about_dialog = gtk.AboutDialog()
		about_dialog.set_destroy_with_parent (True)
		about_dialog.set_icon_name ("gtraycal")
		about_dialog.set_name('gtraycal')
		about_dialog.set_version('0.2')
		about_dialog.set_copyright("(C) 2012 Sagar Behere")
		about_dialog.set_comments(("A simple system tray calendar"))
		about_dialog.set_authors(['Sagar Behere <sagar.behere@gmail.com>'])
		about_dialog.run()
		about_dialog.destroy()

def parseConfigFile(filename):
	
	global global_config
	global_config = ConfigParser.RawConfigParser()
	global_config.read(filename)

	return
		

if __name__ == "__main__":
	parser = OptionParser()
	parser.add_option("-c", action="store", 
		type="string", dest="conffile", help="path to configuration file")
	(options, args) = parser.parse_args()
	if options.conffile != None:
		if (os.path.isfile(options.conffile) == True):
			parseConfigFile(options.conffile)
		else:
			errorstr = "Unable to find config file " + options.conffile
			display_message(errorstr)
	SystrayIconApp()
	gtk.main()
   

