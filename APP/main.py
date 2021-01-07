import sqlite3;
import base64
import os
import json

from kivymd.app import MDApp

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.uix.button import Button,Label
from kivy.uix.popup import Popup
from kivy.properties import StringProperty
from kivy.network.urlrequest import UrlRequest
from kivy.garden.mapview import MapView
from mapview.mbtsource import MBTilesMapSource
from routedrawhelper import LineMapLayer
from gpshelper import GpsHelper

class StartWindowManager(ScreenManager):
    pass

class WindowManager(ScreenManager):
    pass

class DownloadMapData():
    def fillTileTable(self,req1):
        filename = "map_data.mbtiles"
        db_mbtiles = sqlite3.connect(filename)
        c_mbtiles = db_mbtiles.cursor()
        c_mbtiles.execute("CREATE TABLE `tiles` (`zoom_level` int NOT NULL, `tile_column` int NOT NULL, `tile_row` int NOT NULL, `tile_data` BLOB NOT NULL)")
        
        ##Strip the long string
        list_tile_row_strings = req1.result.split("sAndErnEstrow")
        for index,value in enumerate(list_tile_row_strings[1:]):
            try:
                list_tile_row_col_string = value.split("sAndErnEstcol")
                row_4_bytes = base64.decodebytes(list_tile_row_col_string[5].encode('utf-8'))
                sql = "INSERT INTO tiles (zoom_level,tile_column,tile_row,tile_data) VALUES (?,?,?,?)"
                val = (int(list_tile_row_col_string[2]),int(list_tile_row_col_string[3]),int(list_tile_row_col_string[4]),row_4_bytes)
                c_mbtiles.execute(sql,val)
            except:
                pass
        db_mbtiles.commit()
        db_mbtiles.close()
        return print("tile table is filled")

    def fillMetaDataTable(self,req2):
        filename = "map_data.mbtiles"
        db_mbtiles = sqlite3.connect(filename)
        c_mbtiles = db_mbtiles.cursor()
        c_mbtiles.execute("CREATE TABLE `metadata` (`name` string NOT NULL, `value` string NOT NULL)")

        #Strip the long string
        list_metadata_row_strings = req2.result.split("sAndErnEstrow")
        for index,value in enumerate(list_metadata_row_strings[1:]):
            try:
                list_metadata_row_col_string = value.split("sAndErnEstcol")
                sql = "INSERT INTO metadata (name,value) VALUES (?,?)"
                val = (str(list_metadata_row_col_string[2]),str(list_metadata_row_col_string[3]))
                c_mbtiles.execute(sql,val)
            except:
                pass
        db_mbtiles.commit()
        db_mbtiles.close()
        return print("metadata table is filled")

    def fillRouteInfoTable(self,req3):
        filename = "map_data.mbtiles"
        db_mbtiles = sqlite3.connect(filename)
        c_mbtiles = db_mbtiles.cursor()
        c_mbtiles.execute("CREATE TABLE `route_info` (`day` varchar(10) NOT NULL, `title` string NOT NULL,`body` string NOT NULL)")

        #Strip the long string
        list_route_info_row_strings = req3.result.split("sAndErnEstrow")
        for index,value in enumerate(list_route_info_row_strings[1:]):
            try:
                list_route_info_row_col_string = value.split("sAndErnEstcol")
                sql = "INSERT INTO route_info (day,title,body) VALUES (?,?,?)"
                val = (str(list_route_info_row_col_string[2]),str(list_route_info_row_col_string[3]),str(list_route_info_row_col_string[4]))
                c_mbtiles.execute(sql,val)
            except:
                pass
        db_mbtiles.commit()
        db_mbtiles.close()
        return print("route_info table is filled")

    def fillRouteCoordinatesTable(self,req4):
        filename = "map_data.mbtiles"
        db_mbtiles = sqlite3.connect(filename)
        c_mbtiles = db_mbtiles.cursor()
        c_mbtiles.execute("CREATE TABLE `route_coordinates` (`day` varchar(10) NOT NULL, `coordinate_string` blob NOT NULL)")

        #Strip the long string
        list_route_coordinates_row_strings = req4.result.split("sAndErnEstrow")
        for index,value in enumerate(list_route_coordinates_row_strings[1:]):
            try:
                list_route_coordinates_row_col_string = value.split("sAndErnEstcol")
                sql = "INSERT INTO route_coordinates (day,coordinate_string) VALUES (?,?)"
                val = (str(list_route_coordinates_row_col_string[2]),list_route_coordinates_row_col_string[3])
                c_mbtiles.execute(sql,val)
            except:
                pass
        db_mbtiles.commit()
        db_mbtiles.close()
        return print("route_coordinates table is filled")

    def initialize(self,*args):
        filename = "map_data.mbtiles"
        db_mbtiles = sqlite3.connect(filename)
        db_mbtiles.close()
        try:
            req1 = UrlRequest("http://192.168.1.16:5000/tiles")
            req1.wait()
            self.fillTileTable(req1)
            req2 = UrlRequest("http://192.168.1.16:5000/metadata")
            req2.wait()
            self.fillMetaDataTable(req2)
            req3 = UrlRequest("http://192.168.1.16:5000/route/info")
            req3.wait()
            self.fillRouteInfoTable(req3)
            req4 = UrlRequest("http://192.168.1.16:5000/route/coordinates")
            req4.wait()
            self.fillRouteCoordinatesTable(req4)
        except:
            os.remove(filename)
            print("Something went wrong")
        finally:
            print("The 'try except' is finished")
    

class LogginScreen(Screen):
    def __init__(self, **kwargs):
        super(LogginScreen, self).__init__(**kwargs)

    def verify_password(self, *args):
        headers = {'Content-type': 'application/json',
            'Accept': 'text/plain'}
        values = {'password':self.ids.password_input.text}
        params = json.dumps(values)
        password_req = UrlRequest('http://192.168.1.16:5000/verify', req_body=params, req_headers=headers)
        password_req.wait()
        if password_req.result=="1":
            print("password is correct")
            DownloadMapData().initialize()
            self.switch_screen()
        else:
            print("wrong password")

    def switch_screen(self, *args):
        self.manager.current = 'routesindexwindow'
        self.manager.transition.direction = "left"
    
class RoutesIndexWindow(Screen):
    dagindexwindow = StringProperty()
    def btn1_pressed(self):
        self.dagindexwindow = '1'
    def btn2_pressed(self):
        self.dagindexwindow = '2'
    def btn3_pressed(self):
        self.dagindexwindow = '3'
    def btn4a_pressed(self):
        self.dagindexwindow = '4'
    # def btn4b_pressed(self):
    #    self.dagindexwindow = '4-kort'
    def btn5_pressed(self):
        self.dagindexwindow = '5'
    def btn6_pressed(self):
        self.dagindexwindow = '6'
    pass

class RouteMap(Screen):
    dag = StringProperty()

    def __init__(self, **kwargs):
        super(RouteMap, self).__init__(**kwargs)

    def on_pre_enter(self):
        GpsHelper().run()

    def on_enter(self):
        Clock.schedule_once(self.build_map,0)

    def build_map(self,*args):
        source = MBTilesMapSource("map_data.mbtiles")
        self.ids.mapview.map_source = source
        self.layer = LineMapLayer(self.dag)
        self.ids.mapview.add_layer(self.layer, mode="scatter")   # window scatter

        filename = "map_data.mbtiles"
        db_mbtiles = sqlite3.connect(filename)
        c_mbtiles = db_mbtiles.cursor()
        sql = "SELECT * FROM route_coordinates WHERE day = ?"
        day = (self.dag, )
        c_mbtiles.execute(sql, day)
        myresult = c_mbtiles.fetchall()
        if self.dag=='6':
            coordinates_list = eval(myresult[0][1][2:-2])
        else:
            coordinates_list = eval(myresult[0][1][2:-1])
        db_mbtiles.close()

        self.ids.mapview.center_on(coordinates_list[1],coordinates_list[0])
        self.ids.eind_marker.lat = coordinates_list[-1]
        self.ids.eind_marker.lon = coordinates_list[-2]+0.0003
        self.ids.label_eind_marker.text = f"Eind dag {self.dag}"

        #add button to return to menu
        self.button_menu = Button(text="Menu", size_hint=(0.15,0.06),pos_hint={'x':0, 'y':0.94},font_size=30)
        self.button_menu.bind(on_release=self.switch_screen)
        self.add_widget(self.button_menu)

        #add button to get route-info
        self.button_info = Button(text="Route""\n""  Info", size_hint=(0.15,0.08),pos_hint={'x':1-0.15, 'y':0.92},font_size=30)
        self.button_info.bind(on_release=self.route_info_popup)
        self.add_widget(self.button_info)

        # add button to recentre on GPS or on start of route
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
        filename = "map_data.mbtiles"
        db_mbtiles = sqlite3.connect(filename)
        c_mbtiles = db_mbtiles.cursor()
        sql = "SELECT * FROM route_info WHERE day = ?"
        day = (self.dag, )
        c_mbtiles.execute(sql, day)
        myresult = c_mbtiles.fetchall()
        db_mbtiles.close()

        popup = Popup(             
                title=myresult[0][1],
                content=Label(text=myresult[0][2], 
                        text_size=(self.width*0.5,self.width*0.6),
                        halign='left',
                        valign='top'),
                size_hint=(0.65,0.6),
                pos_hint={'x':0.2, 'y':0.2})
        popup.open()

    def center_map_on_gps(self,*args):
        self.ids.mapview.center_on(self.ids.gps_tracker.lat,self.ids.gps_tracker.lon)

    def center_map_on_route(self,*args):
        filename = "map_data.mbtiles"
        db_mbtiles = sqlite3.connect(filename)
        c_mbtiles = db_mbtiles.cursor()
        sql = "SELECT * FROM route_coordinates WHERE day = ?"
        day = (self.dag, )
        c_mbtiles.execute(sql, day)
        myresult = c_mbtiles.fetchall()
        if self.dag=='6':
            coordinates_list = eval(myresult[0][1][2:-2])
        else:
            coordinates_list = eval(myresult[0][1][2:-1])
        db_mbtiles.close()
        self.ids.mapview.center_on(coordinates_list[1],coordinates_list[0])

    def on_leave(self):
        self.ids.mapview.remove_layer(self.layer)
        self.ids.mapview.zoom = 16

class MainApp(MDApp):
    def build(self,*args):
        filename = "map_data.mbtiles"
        if os.path.exists(filename):
            print("map_data exists")
            return WindowManager()
        else:
            print("map_data does not exists")
            return StartWindowManager()

if __name__ == "__main__":
    MainApp().run()
