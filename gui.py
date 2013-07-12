from gi.repository import Gtk, Gdk, GdkPixbuf

class pirateTracks(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="pirateTracks")
        self.set_default_size(500,500)
        self.icon_pix = GdkPixbuf.Pixbuf.new_from_file("pirateTracks.jpg")
        self.set_icon(self.icon_pix)
        
        
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
        self.cover_photo.set_from_file("mixcover.jpg")
        self.play_button_image = Gtk.Image()
        self.skip_button_image = Gtk.Image()
        self.play_button_image.set_from_stock(Gtk.STOCK_MEDIA_PLAY, Gtk.IconSize.BUTTON)
        self.skip_button_image.set_from_stock(Gtk.STOCK_MEDIA_NEXT, Gtk.IconSize.BUTTON)
        self.play_button = Gtk.Button()
        self.skip_button = Gtk.Button()
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
        self.left_user_favorite_tracks = Gtk.Button("Favorite Tracks")
        self.left_user_liked_mixes = Gtk.Button("Liked Mixes")
        self.left_user_button_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.vbox_left_user.pack_start(self.left_user_favorite_tracks, False, False, 0)
        self.vbox_left_user.pack_start(self.left_user_liked_mixes, False, False, 0)
        
        self.vbox_left.pack_start(self.user_pic, True, False, 0)
        self.vbox_left.pack_start(self.vbox_left_user, False, False, 0)
        
        # Create 3b.
        self.mix_review_text = Gtk.TextView()
        self.mix_review_text.set_editable(False)
        self.mix_review_text.set_cursor_visible(False)
        self.mix_review_text.set_wrap_mode(Gtk.WrapMode.WORD)
        self.vbox_center.pack_start(self.mix_review_text, False, False, 0)
        self.hbox_submit = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.vbox_center.pack_start(self.hbox_submit, False, False, 0)
        self.submit_button = Gtk.Button(label="Review!")
        self.submit_button.connect("clicked", self.on_review_click)
        self.entry_submit = Gtk.Entry()
        #self.entry_submit.set_text("Enter your review here. Remember, they are people too.")
        self.hbox_submit.pack_start(self.submit_button, False, False, 0)
        self.hbox_submit.pack_start(self.entry_submit, True, True, 0)
        
        # Create 3c
        self.label = Gtk.Label("Place holder for textview stuff.")
        self.vbox_right.pack_start(self.label, False, False, 0)
        
        # Add all to main window
        self.add(self.vbox_overall)
        
    def on_review_click(self, widget):
        # *****
        # Call post_review from user_context using entry_submit.get_text() as data
        # *****
        from user_context import post_review as pr
        pr(body=self.entry_submit.get_text())
        
if __name__ == '__main__':
    pirateTracks()