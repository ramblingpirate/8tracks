import pygtk
pygtk.require('2.0')
import gtk
import urllib

import search_by_tag as sbt

class pirateTracks():
    
    def __init__(self):
        self.window = gtk.Window()
        self.window.set_title("pirateTracks")
        self.window.set_icon_from_file("pirateTracks.jpg")
        self.window.set_size_request(1024, 1024)
        #self.window.set_opacity(.75) Because, amusing.
        
        self.create_widgets()
        self.connect_signals()
        
        self.window.show_all()
        gtk.main()
        
    def delete_event(self, widget, event):
        gtk.main_quit()
        return False
    
    def create_widgets(self):
        self.hbox = gtk.HBox()
        
        # Create VBox Left
        self.vbox_left = gtk.VBox()
        self.label_left = gtk.Label("Reserved")
        self.vbox_left.pack_start(self.label_left)
        
        # Create VBox Center
        self.vbox_center = gtk.VBox()
        self.vbox_center.set_spacing(0)
        self.search_pic = gtk.Image()
        self.sw_review_text = gtk.ScrolledWindow()
        self.review_text = gtk.TextView()
        self.review_text.set_editable(False)
        self.review_text.set_wrap_mode(gtk.WRAP_WORD)
        self.sw_review_text.add(self.review_text)
        self.vbox_center.pack_start(self.search_pic, 0, 0, 0)
        self.vbox_center.pack_start(self.sw_review_text, 1, 1, 0)
        
        # Create VBox Right
        self.vbox_right = gtk.VBox(False, spacing=0)
        self.hbutton_box = gtk.HButtonBox()
        self.hbutton_box.set_layout(gtk.BUTTONBOX_START)
        self.hbutton_box.set_spacing(1)
        self.hbutton_box.set_border_width(0)
        
        self.entry_search = gtk.Entry()
        self.button_search = gtk.Button("_Search")
        self.button_search.set_relief(gtk.RELIEF_NONE)
        self.button_exit = gtk.Button("Exit")
        self.button_exit.set_relief(gtk.RELIEF_NONE)
        self.sw_search_results = gtk.ScrolledWindow()
        
        # Create treeView
        self.treeView = gtk.TreeView()
        self.treeView.set_rules_hint(True)
        self.tooltips = gtk.Tooltips()
        self.sw_search_results.add(self.treeView)
        self.create_columns(self.treeView)
        
        self.hbutton_box.add(self.button_search)
        self.hbutton_box.add(self.button_exit)
        
        self.vbox_right.pack_start(self.entry_search, False)
        self.vbox_right.pack_start(self.hbutton_box, False)
        self.vbox_right.pack_start(self.sw_search_results, True, True)
        self.vbox_right.pack_start(self.search_pic)
        
        # Pack all into HBox
        self.hbox.pack_start(self.vbox_left)
        self.hbox.pack_start(self.vbox_center)
        self.hbox.pack_start(self.vbox_right)
        
        # Add HBox to Window
        self.window.add(self.hbox)
        
    def on_tree_activated(self, widget):
        # DISPLAY ALL THE THINGS!
        selection = self.treeView.get_selection()
        tree_model, iter = selection.get_selected()
        url = sbt.get_mix_cover(tree_model.get_value(iter, 2))
        self.show_pic(url)
        self.show_reviews(sbt.get_mix_reviews(tree_model.get_value(iter, 2)))
        
    def connect_signals(self):
        self.button_search.connect("clicked", self.search)
        self.button_exit.connect("clicked", self.exit)
        self.treeView.connect("cursor-changed", self.on_tree_activated)
        self.window.connect("delete_event", self.delete_event)
    
    def exit(self, widget):
        self.window.hide_all()
        gtk.main_quit()
    
    def search(self, widget):
        self.mix = sbt.search_by_tag(self.entry_search.get_text())
        self.treeView.set_model(model=self.create_model())
        return self.mix
    
    def create_model(self):
        store = gtk.ListStore(str, str, int)
        try:
            for id, name in self.mix.iteritems():
                store.append((name[0], name[1], id))
        except AttributeError:
            self.search()
        
        return store
    
    def create_columns(self, treeView):
        rendererText = gtk.CellRendererText()
        self.column_name = gtk.TreeViewColumn("Name", rendererText, text=0)
        self.column_name.set_sort_column_id(0)
        self.treeView.append_column(self.column_name)
        rendererText = gtk.CellRendererText()
        self.column_desc = gtk.TreeViewColumn("Description", rendererText, text=1)
        self.column_desc.set_sort_column_id(0)
        self.treeView.append_column(self.column_desc)
    
    def show_reviews(self, buffer):
        
        self.tbuffer = gtk.TextBuffer()
        rstring = ''
        try:
            for review, created in buffer.iteritems():
                rstring = rstring + '{}\nUser said: {}\n\n'.format(review, created)
        except AttributeError:
            pass
        
        self.tbuffer.set_text(rstring)
        self.review_text.set_buffer(self.tbuffer)
        
    
    def show_pic(self, url):
        response = urllib.urlopen(url)
        loader = gtk.gdk.PixbufLoader()
        loader.write(response.read())
        loader.close()
        self.search_pic.set_from_pixbuf(loader.get_pixbuf())
    
    
if __name__ == "__main__":
    app = pirateTracks()