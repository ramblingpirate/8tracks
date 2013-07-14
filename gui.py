import urllib

from gi.repository import Gtk, Gdk, GdkPixbuf, Pango

import pirateTracks as pirate
import search_by_tag as sbt

class pirateTracks(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="pirateTracks")
        self.set_name('pirateTracks')
        self.set_default_size(500,500)
        self.icon_pix = GdkPixbuf.Pixbuf.new_from_file("pirateTracks.jpg")
        self.set_icon(self.icon_pix)
        
        self.style_provider = Gtk.CssProvider()
        
        css = open(('style.css'), 'rb')
        css_data = css.read()
        css.close()
        self.style_provider.load_from_data(css_data)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            self.style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        
        self.create_widgets()
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()
        Gtk.main()
        
    def load_image():
        pass
        
    def create_widgets(self):
        # *****
        # 1. VBox container for all, 2 rows
        # 2. HBox container for updated item containers, 3 columns
        # 3. x3 VBox containers for updated items
        #   3a. VBox_Left contains user info
        #       3a1. Picture container for user photo
        #       3a2. User specific functions
        #   3b. TreeView or un-editable TextBox for user reviews on mix
        #       3b1. HBox containing EditBox for user review/posting and submit button
        #   3c. TreeView for Mix List
        # *****
        
        # VBox overall container creation
        self.vbox_overall = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        
        # Create HBox for Play/Pause/Cover photo
        self.hbox_playpause = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        
        # Create items for hbox_playpause, attach button to playpause_buttonbox
        self.playpause_buttonbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.cover_photo = Gtk.Image()
        #self.cover_photo.set_from_file("mixcover.jpg")
        self.play_button_image = Gtk.Image()
        self.pause_button_image = Gtk.Image()
        self.skip_button_image = Gtk.Image()
        self.play_button_image.set_from_stock(Gtk.STOCK_MEDIA_PLAY, Gtk.IconSize.BUTTON)
        self.pause_button_image.set_from_stock(Gtk.STOCK_MEDIA_PAUSE, Gtk.IconSize.BUTTON)
        self.skip_button_image.set_from_stock(Gtk.STOCK_MEDIA_NEXT, Gtk.IconSize.BUTTON)
        self.play_button = Gtk.Button()
        self.skip_button = Gtk.Button()
        self.play_button.connect("clicked", self.on_play_clicked)
        self.skip_button.connect("clicked", self.on_skip_clicked)
        self.play_button.set_image(self.play_button_image)
        self.skip_button.set_image(self.skip_button_image)
        self.hbox_playpause.pack_start(self.cover_photo, False, False, 0)
        self.playpause_buttonbox.pack_start(self.play_button, False, False, 0)
        self.playpause_buttonbox.pack_start(self.skip_button, False, False, 0)
        self.hbox_playpause.pack_start(self.playpause_buttonbox, False, False, 0)
        self.playpause_sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        self.vbox_overall.pack_start(self.hbox_playpause, False, False, 0)
        self.vbox_overall.pack_start(self.playpause_sep, False, False, 0)
        
        # Create HBox to contain updated item containers
        self.hbox_updated_items = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.vbox_overall.pack_start(self.hbox_updated_items, True, True, 0)
        
        # Create 3.
        self.vbox_left = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.verseperator1 = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
        self.verseperator2 = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
        self.vbox_center = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.vbox_right = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.hbox_updated_items.pack_start(self.vbox_left, True, True, 0)
        self.hbox_updated_items.pack_start(self.verseperator1, True, True, 0)
        self.hbox_updated_items.pack_start(self.vbox_center, True, True, 0)
        self.hbox_updated_items.pack_start(self.verseperator2, True, True, 0)
        self.hbox_updated_items.pack_start(self.vbox_right, True, True, 0)
        
        # Create 3a.
        self.user_pic = Gtk.Image()
        self.user_pic.set_from_file("user.jpeg")
        self.vbox_left_user = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.left_user_listening_history = Gtk.Button("Listening History")
        self.left_user_recommended = Gtk.Button("Recommended")
        self.left_user_favorite_tracks = Gtk.Button("Favorite Tracks")
        self.left_user_favorite_tracks.connect("clicked", self.on_favorite_clicked)
        self.left_user_liked_mixes = Gtk.Button("Liked Mixes")
        self.left_user_mix_feed = Gtk.Button("Mix Feed")
        self.left_user_settings = Gtk.Button("Settings")
        self.left_user_liked_mixes.connect("clicked", self.on_liked_clicked)
        self.left_user_button_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.vbox_left_user.pack_start(self.left_user_listening_history, False, False, 0)
        self.vbox_left_user.pack_start(self.left_user_recommended, False, False, 0)
        self.vbox_left_user.pack_start(self.left_user_favorite_tracks, False, False, 0)
        self.vbox_left_user.pack_start(self.left_user_liked_mixes, False, False, 0)
        self.vbox_left_user.pack_start(self.left_user_mix_feed, False, False, 0)
        self.vbox_left_user.pack_start(self.left_user_settings, False, False, 0)
        
        self.vbox_left.pack_start(self.user_pic, True, False, 0)
        self.vbox_left.pack_start(self.vbox_left_user, False, False, 0)
        
        # Create 3b.
        self.mix_review_text = Gtk.TextView()
        self.mix_review_text.set_editable(False)
        self.mix_review_text.set_cursor_visible(False)
        self.mix_review_text.set_wrap_mode(Gtk.WrapMode.WORD)
        self.mix_review_sw = Gtk.ScrolledWindow()
        self.mix_review_sw.set_border_width(0)
        self.mix_review_sw.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.mix_review_sw.set_min_content_height(450)
        self.mix_review_sw.add(self.mix_review_text)
        self.vbox_center.pack_start(self.mix_review_sw, False, False, 0)
        self.hbox_submit = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.vbox_center.pack_start(self.hbox_submit, False, False, 0)
        self.submit_button = Gtk.Button(label="Review!")
        self.submit_button.connect("clicked", self.on_review_click)
        self.entry_submit = Gtk.Entry()
        #self.entry_submit.set_text("Enter your review here. Remember, they are people too.")
        self.hbox_submit.pack_start(self.submit_button, False, False, 0)
        self.hbox_submit.pack_start(self.entry_submit, True, True, 0)
        
        # Create 3c
        self.mix_tree_sw = Gtk.ScrolledWindow()
        self.mix_tree_sw.set_border_width(0)
        self.mix_tree_sw.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.mix_tree_sw.set_min_content_height(450)
        #self.mix_tree_sw.set_max_content_width(100)
        self.mix_tree_view = Gtk.TreeView()
        self.mix_tree_view.set_model(model=self.create_mix_list_model())
        self.create_column(self.mix_tree_view)
        self.mix_tree_view.get_selection().connect("changed", self.on_results_activated)
        self.mix_tree_sw.add(self.mix_tree_view)
        self.vbox_right.pack_start(self.mix_tree_sw, True, True, 0)
        
        # Add all to main window
        self.add(self.vbox_overall)
        
    # ********************************************************************************
    #
    # This next area is defining all the signal hooks and such.
    # 1. Play/Pause button hooks (from pirateTracks)
    # 2. Skip button hook (from pirateTracks)
    # 3. Click/Double Click on the TreeView
    # 4. Favorite Tracks/ Liked Mixes hooks (from user_context)
    # 5. "Now Playing" by "Artist" label listening for new song.
    # ********************************************************************************
    
    def on_play_clicked(self, widget):
        # Calls play_stream from pirateTracks, changes button image to "Pause"
        # Not actually adding the play_stream yet, because of reasons.
        print("Now simulating the playing of the songs and the stuff.")
        # Here is where we would switch the button image to "Pause"
        # not sure how to implement yet.
        
    def on_skip_clicked(self, widget):
        # Calls to skip_track from pirateTracks
        print("Now simulating the skipping.")
    
    def on_favorite_clicked(self, widget):
        from user_context import list_favorites
        list_favorites()
        
    def on_liked_clicked(self, widget):
        from user_context import list_liked_mixes
        list_liked_mixes()
        
    def on_review_click(self, widget):
        # *****
        # Call post_review from user_context using entry_submit.get_text() as data
        # *****
        from user_context import post_review as pr
        pr(body=self.entry_submit.get_text())
        
    def create_mix_list_model(self):
        # Create model
        self.feed_model = Gtk.ListStore(str, int, int)
        self.mixes = pirate.gather_mixes()
        for id, name in self.mixes.iteritems():
            self.feed_model.append((name[1], name[2], name[0]))
        return self.feed_model
        
    def create_column(self, treeview):
        # Create TreeView with model
        self.renderer = Gtk.CellRendererText()
        self.column_names = Gtk.TreeViewColumn("Mix Name", self.renderer, text=0)
        self.column_descr = Gtk.TreeViewColumn("No. of Tracks", self.renderer, text=1)
        self.column_names.set_sort_column_id(0)
        self.column_descr.set_sort_column_id(1)
        self.mix_tree_view.append_column(self.column_names)
        self.mix_tree_view.append_column(self.column_descr)
        
    def on_results_activated(self, selection):
        # Here, we want to set the cover photo (or maybe I'll add another area for not-currently-playing
        # mix covers and such. I'm not sure yet) to the selected cover.
        (model, treeiter) = selection.get_selected()
        url = sbt.get_mix_cover(model[treeiter][2])
        self.get_cover_as_file(url)
        
        # Here, we'll call the show_reviews function to display reviews and such.
        self.show_the_critics(sbt.get_mix_reviews(model[treeiter][2]))
        
    def show_the_critics(self, buffer):
        review_tbuffer = Gtk.TextBuffer()
        review_string = ''
        #print buffer
        for id, (review_body, created_at, user_id) in buffer.items():
            review_string = review_string + '=====\n{} :: {}\n====='.format(sbt.get_user_info(buffer[id].user_id), buffer[id].review_body.encode('utf-8'))
            
        review_tbuffer.set_text(review_string)
        self.mix_review_text.set_buffer(review_tbuffer)
        
    def get_cover_as_file(self, parse_url):
        loader = GdkPixbuf.PixbufLoader()
        loader.write(urllib.urlopen(parse_url).read())
        loader.close()
        pixbuf = loader.get_pixbuf()
        self.cover_photo.set_from_pixbuf(pixbuf)
        
if __name__ == '__main__':
    pirateTracks()