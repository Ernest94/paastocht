from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.uix.button import Button,Label
from kivy.uix.popup import Popup
from kivy.properties import StringProperty
from kivy.utils import platform

from kivy.garden.mapview import MapView,MapLayer,MapMarkerPopup
from mapview.mbtsource import MBTilesMapSource
import pickle

from routedrawhelper import LineMapLayer
from gpshelper import GpsHelper
from routeinfopopup import RouteInfoPopUp

#import routes, their center coordinates and the route info
routes_data = pickle.load(open("routes_data.pickle","rb"))
route_center_coords = pickle.load(open("route_center_coords.pickle","rb"))
route_info = pickle.load(open("route_info.pickle","rb"))

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
        source = MBTilesMapSource("paastocht2020.mbtiles")
        source.bounds = 5.274382,49.994698,5.849791,50.249160
        self.ids.mapview.map_source = source
        self.layer = LineMapLayer(self.dag)
        self.ids.mapview.add_layer(self.layer, mode="scatter")   # window scatter
        self.ids.mapview.center_on(routes_data[self.dag][1],routes_data[self.dag][0])
        self.ids.eind_marker.lat = routes_data[self.dag][-1]
        self.ids.eind_marker.lon = routes_data[self.dag][-2]+0.0003
        self.ids.label_eind_marker.text = f"Eind {self.dag}"
        
        #add button to return to menu
        self.button_menu = Button(text="Menu", size_hint=(0.15,0.06),pos_hint={'x':0, 'y':0.94},font_size=30)
        self.button_menu.bind(on_release=self.switch_screen)
        self.add_widget(self.button_menu)
        
        #add button to get route-info
        self.button_info = Button(text="Route""\n""  Info", size_hint=(0.15,0.08),pos_hint={'x':1-0.15, 'y':0.92},font_size=30)
        self.button_info.bind(on_release=self.route_info_popup)
        self.add_widget(self.button_info)
        
        #add button to recentre on GPS or on start of route
        self.button_gps = Button(size_hint=(0.12,0.08),pos_hint={'x':0.05,'y':0.03},background_normal='recentre_gps_icon.png',background_down='recentre_gps_icon_down.png')
        if self.ids.gps_tracker.lat>49.994698 and self.ids.gps_tracker.lat<50.249160 and self.ids.gps_tracker.lon>5.274382 and self.ids.gps_tracker.lon<5.849791:
            self.button_gps.bind(on_press=self.center_map_on_gps)
        else:
            self.button_gps.bind(on_press=self.center_map_on_route)
        self.add_widget(self.button_gps)
        
    def switch_screen(self, *args):
        self.manager.current = 'routesindexwindow'
        self.manager.transition.direction = "right"
        
    def route_info_popup(self,*args):
        popup = Popup(title=route_info[self.dag][0],content=Label(text=route_info[self.dag][1], text_size=(self.width*0.5,self.width*0.6) ,halign='left',valign='top'),size_hint=(0.65,0.6),pos_hint={'x':0.2, 'y':0.2})
        popup.open()
        
    def center_map_on_gps(self,*args):
        self.ids.mapview.center_on(self.ids.gps_tracker.lat,self.ids.gps_tracker.lon)
        
    def center_map_on_route(self,*args):
        self.ids.mapview.center_on(routes_data[self.dag][1],routes_data[self.dag][0])
        
    

    def on_leave(self):
        self.ids.mapview.remove_layer(self.layer)
        self.ids.mapview.zoom = 14
        
class MainApp(App):
    def build(self):
        return WindowManager()
    

if __name__ == "__main__":
    MainApp().run()
