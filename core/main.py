from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.uix.button import Button,Label
from kivy.properties import StringProperty
from kivy.utils import platform

from kivy.garden.mapview import MapView,MapLayer,MapMarkerPopup
from mapview.mbtsource import MBTilesMapSource
import pickle

from routedrawhelper import LineMapLayer
from gpshelper import GpsHelper

#import routes and their center coordinates of routes
routes_data = pickle.load(open("../routes_data.pickle","rb"))
route_center_coords = pickle.load(open("../route_center_coords.pickle","rb"))

class WindowManager(ScreenManager):
    pass      
          
class RoutesIndexWindow(Screen):
    dagindexwindow = StringProperty()
    
    def btn1_pressed(self):
        self.dagindexwindow = 'dag 1'
    def btn2_pressed(self):
        self.dagindexwindow = 'dag 2'
    def btn3_pressed(self):
        self.dagindexwindow = 'dag 3'
    def btn4a_pressed(self):
        self.dagindexwindow = 'dag 4 kort'
    def btn4b_pressed(self):
        self.dagindexwindow = 'dag 4 lang'
    def btn5_pressed(self):
        self.dagindexwindow = 'dag 5'
    def btn6_pressed(self):
        self.dagindexwindow = 'dag 6'
        
    pass
        
class RouteMap(Screen):
    dag = StringProperty()
    
    def __init__(self, **kwargs):
        super(RouteMap, self).__init__(**kwargs)
        
    def on_pre_enter(self):
        GpsHelper().run()
      
    def on_enter(self):    
        Clock.schedule_once(self.post,0)
    
    def post(self,*args):       
        source = MBTilesMapSource("../paastocht2020.mbtiles")
        self.ids.mapview.map_source = source
        self.layer = LineMapLayer(self.dag)
        self.ids.mapview.add_layer(self.layer, mode="scatter")   # window scatter
        self.ids.mapview.center_on(route_center_coords[self.dag][0],route_center_coords[self.dag][1])
        self.ids.start_marker.lat = routes_data[self.dag][1]
        self.ids.start_marker.lon = routes_data[self.dag][0]
        self.ids.eind_marker.lat = routes_data[self.dag][-1]
        self.ids.eind_marker.lon = routes_data[self.dag][-2]
        self.ids.label_start_marker.text = f"Start {self.dag}"
        self.ids.label_eind_marker.text = f"Eind {self.dag}"
        
        #add button to return to menu
        self.button = Button(text="Menu", size_hint=(0.15,0.06),pos_hint={'x':0, 'y':0.94},font_size=30)
        self.button.bind(on_release=self.switch_screen)
        self.add_widget(self.button)
        
    def switch_screen(self, *args):
        self.manager.current = 'routesindexwindow'
        self.manager.transition.direction = "right"
   
    def on_leave(self):
        self.ids.mapview.remove_layer(self.layer)
        self.ids.mapview.zoom = 6
        
class MainApp(App):
    def build(self):
        return WindowManager()
    

if __name__ == "__main__":
    MainApp().run()
