from gi.repository import Gtk, Gdk

class pirateTracks(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="pirateTracks")
        self.set_default_size(500,500)
        
        self.create_widgets()
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()
        Gtk.main()
        
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
        
        # Ignoring for now, but will contain play/pause and cover photo. Moving on.
        # Create HBox to contain updated item containers
        self.hbox_updated_items = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.vbox_overall.pack_start(self.hbox_updated_items, False, False, 0)
        
        # Create 3.
        self.vbox_left = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.vbox_center = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.vbox_right = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.hbox_updated_items.pack_start(self.vbox_left, False, False, 0)
        self.hbox_updated_items.pack_start(self.vbox_center, False, False, 0)
        self.hbox_updated_items.pack_start(self.vbox_right, False, False, 0)
        
        # Create 3a.
        self.user_pic = Gtk.Image()
        self.user_pic.set_from_file("user.png")
        self.vbox_left_user = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.vbox_left.pack_start(self.user_pic, False, False, 0)
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
        self.hbox_submit.pack_start(self.entry_submit, False, False, 0)
        
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