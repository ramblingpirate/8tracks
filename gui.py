import pygtk
pygtk.require('2.0')
import gtk
import urllib

import search_by_tag as sbt

class pirateTracks():
    
    def __init__(self):
        self.window = gtk.Window()
        self.window.set_title("pirateTracks")
        
        self.create_widgets()
        self.connect_signals()
        
        self.window.show_all()
        gtk.main()
    
    def create_widgets(self):
        self.hbox = gtk.HBox()
        
        # Create VBox Left
        self.vbox_left = gtk.VBox()
        self.label_left = gtk.Label("Reserved")
        self.vbox_left.pack_start(self.label_left)
        
        # Create VBox Center
        self.vbox_center = gtk.VBox()
        self.search_pic = gtk.Image()
        self.vbox_center.pack_start(self.search_pic)
        
        # Create VBox Right
        self.vbox_right = gtk.VBox()
        self.entry_search = gtk.Entry()
        self.button_search = gtk.Button("Search")
        self.button_exit = gtk.Button("Exit")
        self.search_results = gtk.Label()
        self.vbox_right.pack_start(self.entry_search)
        self.vbox_right.pack_start(self.button_search)
        self.vbox_right.pack_start(self.button_exit)
        self.vbox_right.pack_start(self.search_results)
        self.vbox_right.pack_start(self.search_pic)
        
        # Pack all into HBox
        self.hbox.pack_start(self.vbox_left)
        self.hbox.pack_start(self.vbox_center)
        self.hbox.pack_start(self.vbox_right)
        
        # Add HBox to Window
        self.window.add(self.hbox)
        
    def connect_signals(self):
        self.button_search.connect("clicked", self.search)
        self.button_exit.connect("clicked", self.exit)
    
    def exit(self, widget):
        self.window.hide_all()
        gtk.main_quit()
        
    def search(self, widget):
        mix = sbt.search_by_tag(self.entry_search.get_text())
        for desc, name in mix.iteritems():
            previous = self.search_results.get_text()
            self.search_results.set_text("{}\nName: {}\nDesc: {}\n".format(previous,name[0], name[1]))
            url = name[2]
            self.show_pic(url)
    
    def show_pic(self, url):
        response = urllib.urlopen(url)
        loader = gtk.gdk.PixbufLoader()
        loader.write(response.read())
        loader.close()
        self.search_pic.set_from_pixbuf(loader.get_pixbuf())
    
    
if __name__ == "__main__":
    app = pirateTracks()
