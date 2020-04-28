from kivy.garden.mapview import MapLayer
import pickle

from kivy.graphics import Color, Line
from kivy.graphics.context_instructions import Translate, Scale

#import routes of all days
routes_data = pickle.load(open("../routes_data.pickle","rb"))


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
        for index,geo_coordinates in enumerate(routes_data[self.day]):
            screen_coordinates = mapview.get_window_xy_from(routes_data[self.day][2*index+1], routes_data[self.day][2*index], mapview.zoom)
            point_list.append(screen_coordinates[0])
            point_list.append(screen_coordinates[1])
            if index==int((len(routes_data[self.day]))/2-1):
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
            
            
   
