#!/usr/bin/python
# -*- coding: utf-8 -*-

from gi.repository import Gtk, Gdk
import sys
from pony.orm import *
import os

UI_INFO = """
<ui>
  <menubar name='MenuBar'>
    <menu action='FileMenu'>
        <menuitem action='createDataBase' />
        <menuitem action='lanzarScrapy' />
        <menuitem action='getDataFromDataBase' />
      <separator />
      <menuitem action='salir' />
    </menu>
    <menu action='Help'>
      <menuitem action='About' />
    </menu>
  </menubar>
  <toolbar name='ToolBar'>
    <toolitem action='createDataBase' />
    <toolitem action='lanzarScrapy' />
    <toolitem action='getDataFromDataBase' />
    <toolitem action='salir' />
  </toolbar>
</ui>
"""

db = Database("sqlite", "europython/europython.sqlite", create_db=True)

class EuropythonSession(db.Entity):
        """
        Pony ORM model of the europython session table
        """
	id = PrimaryKey(int, auto=True)
	author = Required(str)
	title = Required(str)
	description = Required(str)
	date = Required(str)
	tags = Required(str)
	
class EuroPhytonSqlite():

			
	
	@db_session	
	#función para obtener resultados de la BD
	def getResultDB(self):
		
		try:
			# SELECT
			countSessions =  EuropythonSession.select().count()
			print '\nNumber sessions ' + str(countSessions)	    
			
			sessions = EuropythonSession.select_by_sql("SELECT * FROM EuropythonSession")		
		    
			lista =[];
			
			# Imprimimos el registro resultante
			for session in sessions:
				title = session.title.decode('utf-8').encode('cp850','replace').decode('cp850')
				print title
				author = session.author.decode('utf-8').encode('cp850','replace').decode('cp850')
				description = session.description.decode('utf-8').encode('cp850','replace').decode('cp850')
				date = session.date
				tags = session.tags.decode('utf-8')
				
				register = (title,author,description,date,tags)
			    
				lista.append(register)
			    
	
			return lista
	
		except:
			print "0", sys.exc_info()[0]
			print "1", sys.exc_info()[1]
			print "2", sys.exc_info()[2]
			print "Error al obtener resultados"
			pass    
        
class Europython(Gtk.Window):

    #inicializar ventana y componentes
	def __init__(self):
		
		db.generate_mapping(check_tables=True, create_tables=True)
		
		Gtk.Window.__init__(self, title="Europython conferences")
		self.set_border_width(0)

		action_group = Gtk.ActionGroup("my_actions")

		self.add_file_menu_actions(action_group)
		self.getInfoDialog(action_group)
        
		uimanager = self.create_ui_manager()
		uimanager.insert_action_group(action_group)

		menubar = uimanager.get_widget("/MenuBar")

		box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		box.pack_start(menubar, False, False, 0)

		toolbar = uimanager.get_widget("/ToolBar")
		box.pack_start(toolbar, False, False, 0)

		#Grid para mostrar los componentes
		self.grid = Gtk.Grid()
		self.grid = Gtk.Grid()
		self.grid.set_column_homogeneous(True)
		self.grid.set_row_homogeneous(True)

		#Tabla de datos lista de conferencias
		self.conferenceList = Gtk.ListStore(str,str,str,str,str)
		self.current_filter_date = None

		#Filtro para la tabla
		self.day_filter = self.conferenceList.filter_new()
		self.day_filter.set_visible_func(self.day_filter_func)

		#columnas para la tabla
		self.treeview = Gtk.TreeView.new_with_model(self.day_filter)
		self.treeview.set_hexpand(True)
		self.treeview.set_vexpand(True)

		for i, column_title in enumerate(["Titulo","Autor","Descripcion","Fecha","Tags"]):
			renderer = Gtk.CellRendererText()
			column = Gtk.TreeViewColumn(column_title, renderer, text=i)
			self.treeview.append_column(column)

		#botones para el filtro por dias
		self.buttons = list()
		
		for days in ["Monday 20 July", "Tuesday 21 July", "Wednesday 22 July", "Thursday 23 July", "Friday 24 July","Saturday 25 July"]:
			button = Gtk.Button(days)
			self.buttons.append(button)
			button.connect("clicked", self.on_selection_button_clicked)

		#layout ventana con scroll para la lista de conferencias
		self.scrollable_treelist = Gtk.ScrolledWindow()
		self.scrollable_treelist.set_vexpand(True)
		self.scrollable_treelist.set_hexpand(True)
        
		self.grid.attach(self.scrollable_treelist, 0, 0, 10, 10)
		self.grid.attach_next_to(self.buttons[0], self.scrollable_treelist, Gtk.PositionType.BOTTOM, 1, 1)
		for i, button in enumerate(self.buttons[1:]):
			self.grid.attach_next_to(button, self.buttons[i], Gtk.PositionType.RIGHT, 1, 1)
			self.scrollable_treelist.add(self.treeview)

		toolbar = uimanager.get_widget("/ToolBar")
		box.pack_start(self.grid, False, False, 0)


		self.label = Gtk.Label()
		self.label.set_line_wrap(True)
		self.label.set_justify(Gtk.Justification.LEFT)
		box.pack_start(self.label, False, False, 0)
		box.set_hexpand(True)
		box.set_vexpand(True)
        
		self.add(box)
        
		self.show_all()

	def day_filter_func(self, model, iter, data):
		"""Tests if the day in the row is the one in the filter"""
		if self.current_filter_date is None or self.current_filter_date == "None":
			return True
		else:
			return  self.current_filter_date in model[iter][3]

	def on_selection_button_clicked(self, widget):
		#establecer filtro
		self.current_filter_date = widget.get_label()
		print("%s day selected!" % self.current_filter_date)
		#actualizar filtro para la tabla
		self.day_filter.refilter()

	#acciones de menu
	def add_file_menu_actions(self, action_group):
		action_filemenu = Gtk.Action("FileMenu", "File", None, None)
		action_group.add_action(action_filemenu)

		action_getDataFromDataBase = Gtk.Action("getDataFromDataBase", "_obtener Datos","getDataFromDataBase", Gtk.STOCK_REFRESH)
		action_getDataFromDataBase.connect("activate", self.on_menu_getDataFromDataBase)
		action_group.add_action_with_accel(action_getDataFromDataBase, None)

		action_lanzarScrapy = Gtk.Action("lanzarScrapy", "_lanzar Scrapy","lanzarScrapy", Gtk.STOCK_EXECUTE)
		action_lanzarScrapy.connect("activate", self.on_menu_lanzarScrapy)
		action_group.add_action_with_accel(action_lanzarScrapy, None)

		action_createDataBase = Gtk.Action("createDataBase", "_crear Base Datos","createDataBase", Gtk.STOCK_EXECUTE)
		action_createDataBase.connect("activate", self.on_menu_createDataBase)
		action_group.add_action_with_accel(action_createDataBase, None)

		action_filequit = Gtk.Action("salir", None, "salir", Gtk.STOCK_QUIT)
		action_filequit.connect("activate", self.on_menu_file_quit)
		action_group.add_action(action_filequit)

	#dialogo info
	def getInfoDialog(self, action_group):
		action_group.add_actions([
		        ("Help", None, "About"),
		        ("About", Gtk.STOCK_DIALOG_INFO, None, None, None,
		         self.on_menu_dialog_info)
		])

	def create_ui_manager(self):
		uimanager = Gtk.UIManager()

		uimanager.add_ui_from_string(UI_INFO)

		accelgroup = uimanager.get_accel_group()
		self.add_accel_group(accelgroup)
		return uimanager
	
	
	def on_menu_createDataBase(self, widget):
        
		print("createDataBase")
		try:
			euroPhytonSqlite = EuroPhytonSqlite()
        
			self.label.set_markup("<i>"+"BD created EuroPython"+"</i>")
        
		except:
			print "0", sys.exc_info()[0]
			print "1", sys.exc_info()[1]
			print "2", sys.exc_info()[2]
			self.label.set_markup("\n<b>"+str(sys.exc_info()[1])+"</b>")
            
			pass
	
	#Obtener registros de la BD y pintarlos en la tabla
	def on_menu_getDataFromDataBase(self, widget):
		print("getDataFromDataBase")
		try:

			euroPhytonSqlite = EuroPhytonSqlite()
	
			listaConferencias = euroPhytonSqlite.getResultDB()

			self.conferenceList.clear()
			self.current_filter_date = None
	    
			for conference in listaConferencias:
				self.conferenceList.append(list(conference))


			if len(listaConferencias)==0:
				self.label.set_markup("<i>"+"No hay registros en la BD"+"</i>")
        
		except:
			print "0", sys.exc_info()[0]
			print "1", sys.exc_info()[1]
			print "2", sys.exc_info()[2]
			self.label.set_markup("\n<b>"+str(sys.exc_info()[1])+"</b>")
            
			pass
    
	#mostrar ventana de dialogo
	def on_menu_dialog_info(self, widget):
		print("dialog info")
		dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,Gtk.ButtonsType.OK, "Proyecto final")
		dialog.format_secondary_text(
		        "Se conecta con el sitio https://ep2015.europython.eu para obtener las conferencias de la europython,las registra en la base de datos y las visualiza en la ventana\n\n"
		        +"Jose Manuel Ortega Candel jmoc25@gmail.com")
		dialog.run()
		print("INFO dialog closed")

		dialog.destroy()

	def on_menu_file_quit(self, widget):
		Gtk.main_quit()
		sys.exit(1)

	def on_menu_lanzarScrapy(self, widget):
		
		print("lanzando scrapy...............")
		print("Ejecutar comando")
		print("scrapy crawl europython_spyder")
		self.label.set_markup("<b>"+"Ejecutar comando >> scrapy crawl europython_spyder"+"</b>")
		os.system("scrapy crawl europython_spyder")

	def on_button_press_event(self, widget, event):
		# Check if right mouse button was preseed
		if event.type == Gdk.EventType.BUTTON_PRESS and event.button == 3:
			self.popup.popup(None, None, None, None, event.button, event.time)
			return True # event has been handled


win = Europython()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
