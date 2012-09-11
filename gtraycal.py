#!/usr/bin/python
# -*- coding: utf-8 -*-

# Author: Sagar Behere <sagar@sagar.se>, 12 Sept. 2012
# DISCLAIMER: I don't know enough of either Python or GTK+, so there
#		are probably silly errors in this script.
# 		It is just something thrown quickly together because I 
#		wanted a systray calendar that emulates the one in
#		gnome2 panel

# CREDITS: Used code from
# http://eurion.net/python-snippets/snippet/Systray%20icon.html
# http://stackoverflow.com/questions/11132929/showing-a-gtk-calendar-in-a-menu		

# LICENSE: Do whatever you want with it, and don't blame me for whatever
#	   it does :)

# TODO: 1. Currently only works for horizontal panel. Fix for verticle
#	2. Add locations support to see time in specific timezones

import gobject
import pygtk
import gtk
import time

class Calendar:
	def __init__(self):
		self.cal_window = gtk.Window(gtk.WINDOW_POPUP)
		self.cal_window.set_decorated(False)
		self.cal_window.set_resizable(False)
		self.cal_window.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_DOCK)
		self.cal_window.stick()
		cal_vbox = gtk.VBox(False, 10)
		self.cal_window.add(cal_vbox)
		cal = gtk.Calendar()
		cal.set_property("show-week-numbers", True)
		cal_vbox.pack_start(cal, True, False, 0)
		cal_vbox.pack_start(gtk.Button("Dummy locations"), True, False, 0)
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
		about_dialog.set_version('0.1')
		about_dialog.set_copyright("(C) 2012 Sagar Behere")
		about_dialog.set_comments(("A simple system tray calendar"))
		about_dialog.set_authors(['Sagar Behere <sagar@sagar.se>'])
		about_dialog.run()
		about_dialog.destroy()

if __name__ == "__main__":
	SystrayIconApp()
	gtk.main()
   

