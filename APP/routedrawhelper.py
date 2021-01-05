import sqlite3;

from kivy.garden.mapview import MapLayer
from kivy.graphics import Color, Line
from kivy.graphics.context_instructions import Translate, Scale

class LineMapLayer(MapLayer):
    
    def __init__(self,day,**kwargs):
        super(LineMapLayer, self).__init__(**kwargs)
        self.zoom = 2
        self.day = day

    def reposition(self):
        self.draw_line()

    def draw_line(self, *args):
        mapview = self.parent
        self.zoom = mapview.zoom        
        point_list=[]
        
        filename = "map_data.mbtiles"
        db_mbtiles = sqlite3.connect(filename)
        c_mbtiles = db_mbtiles.cursor()
        sql = "SELECT * FROM route_coordinates WHERE day = ?"
        day = (self.day, )
        c_mbtiles.execute(sql, day)
        myresult = c_mbtiles.fetchall()
        if self.day=='6':
            coordinates_list = eval(myresult[0][1][2:-2])
        else:
            coordinates_list = eval(myresult[0][1][2:-1])
        db_mbtiles.close()

        for index,geo_coordinates in enumerate(coordinates_list):
            screen_coordinates = mapview.get_window_xy_from(coordinates_list[2*index+1], coordinates_list[2*index], mapview.zoom)
            point_list.append(screen_coordinates[0])
            point_list.append(screen_coordinates[1])
            if index==int((len(coordinates_list))/2-1):
                break
            
        # When zooming we must undo the current scatter transform
        # or the animation makes the line misplaced
        scatter = mapview._scatter
        x,y,s = scatter.x, scatter.y, scatter.scale
        
        with self.canvas:
            self.canvas.clear()
            Scale(1/s,1/s,1)
            Translate(-x,-y)
            Color(1, 0, 0, 1)
            Line(points=point_list, width=2, joint="miter")         
            
            
   
