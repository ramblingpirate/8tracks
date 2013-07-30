import Queue, threading

from gi.repository import Gst


class Player():
    
    def __init__(self):
        print "Now constructing...."
        self.qq = Queue.Queue()
        Gst.init(None)
        self.audio = Gst.ElementFactory.make("playbin", None)
        
        self.bus = self.audio.get_bus()
        self.bus.add_signal_watch()
        self.bus.enable_sync_message_emission()
        self.bus.connect('message', self.message_handler)
        self.bus.connect('message::tag', self.on_tag)
        self.is_playing = False

    def on_tag(self, bus, msg):
        taglist = msg.parse_tag()
        #print taglist.to_string()
    
    def message_handler(self, bus, message):
        if message.type == Gst.MessageType.EOS:
            print "eos, calling 'is_done'..."
            self.audio.set_state(Gst.State.NULL)
            self.is_playing = False
            self.next()
        elif message.type == Gst.MessageType.ERROR:
            print message.parse_error()
            self.next()
    
    def play(self):
        self.is_playing = True
        self.audio.set_state(Gst.State.PLAYING)
        
    def next(self):
        if not self.qq.empty():
            song = self.qq.get()
            self.audio.set_property("uri", song.url)
            self.print_tags(song.artist, song.title)
            self.play()
        else:
            print "Nothing left to play..."
            
    def print_tags(self, artist, title):
        print "'{}' by {}".format(title, artist)
        
    def queue_q(self, track):
        self.qq.put(track)
        