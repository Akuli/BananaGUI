from gi.repository import Gtk, Gdk


#provider = Gtk.CssProvider()
#screen = Gdk.Display.get_default().get_default_screen()
#Gtk.StyleContext.add_provider_for_screen(
#    screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)
#provider.load_from_path('shit.css')

window = Gtk.Window()
window.show()

provider = Gtk.CssProvider()
provider.load_from_path('shit.css')
context = window.get_style_context()
context.add_provider(provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

window2 = Gtk.Window()
window2.show()

Gtk.main()
