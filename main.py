from kivy.lang import  Builder
from kivymd.app import  MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivy.uix.screenmanager import NoTransition
from kivymd.uix.menu import  MDDropdownMenu
from kivymd.uix.card import MDCard
from kivy.properties import StringProperty,ObjectProperty

import json

class BookCard(MDCard):
	title = StringProperty()
	file_size = StringProperty()
	downloads = StringProperty()
	file_url = StringProperty()
	cover_photo = StringProperty()

class BookInfoCard(MDCard):
	title = StringProperty()
	file_size = StringProperty()
	downloads = StringProperty()
	file_url = StringProperty()
	cover_photo = StringProperty()

class SearchPage(MDScreen):
	'''search page'''
		
class InformationPage(MDScreen):
	'''book informations'''
	info_card = ObjectProperty()
	
	def render_object(self):
		self.ids.book_info_center.add_widget(self.info_card)
	
class HomePage(MDScreen):
	'''home page'''
	
	def on_enter(self):
		self.list_books()
		
	def list_books(self):
		with open('books.json') as f_obj:
			books = json.load(f_obj)
				
			for book,info in books.items():
				downloads = str(info['downloads'])
				title = info['title']
				file_size = info['file_size']
				cover_photo = info['cover']
				self.ids.books.add_widget(BookCard(title = title, file_size = file_size, downloads = downloads, cover_photo = cover_photo))
	
class BookStoreApp(MDApp):
	def build(self):
		self.theme_cls.theme_style = 'Dark'
		self.load_all_kv_files()
		return MDScreenManager()
		
	def open_menu(self):
		menu_items = [
		{"text": "Dark theme", "on_release": lambda: self.menu_callback('Dark')},
		{"text": "Light Theme", "on_release": lambda: self.menu_callback('Light')}		
		]
		home_screen = self.root.get_screen(name = 'homepage')
		self.menu = MDDropdownMenu(caller = home_screen.ids.menu_trigger, items = menu_items)
		self.menu.open()
		
	def menu_callback(self,theme):
		self.theme_cls.theme_style = theme
		self.menu.dismiss()
		
	def load_all_kv_files(self):
		Builder.load_file('homepage.kv')
		Builder.load_file('bookcard.kv')
		Builder.load_file('infopage.kv')
		Builder.load_file('bookinfocard.kv')
		Builder.load_file('searchpage.kv')
		
	def create_bookinfo_card(self,book_title):
		
		with open('books.json') as f_obj:
			books = json.load(f_obj)
			
			for book,details in books.items():
				
				if  details['title'] == book_title:
					title = details['title']
					downloads = str(details['downloads'])
					cover_photo = details['cover']
					file_size = details['file_size']
					
			infopage = self.root.get_screen('bookinfo')
			infopage.info_card = BookInfoCard(title = title, cover_photo = cover_photo, file_size = file_size, downloads = downloads)		
			infopage.render_object()
			self.root.transition.direction = 'left'
			self.root.current = 'bookinfo'
			
	def search(self,instance):
		print(instance.text)
		instance.text = ''
		
	def on_start(self):
		home_screen = HomePage(name = 'homepage')
		infopage = InformationPage(name = 'bookinfo')
		search_page = SearchPage(name = 'searchpage')
		
		self.root.add_widget(home_screen)
		self.root.add_widget(infopage)
		self.root.add_widget(search_page)
		
		#home_screen.on_enter()
		
BookStoreApp().run()