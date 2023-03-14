from kivy.uix.relativelayout import RelativeLayout
from kivy.metrics import dp
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line



class RedstoneDisplay(RelativeLayout):
    SPACING =dp(20)
    LINE_COLOR=(242/255, 237/255, 218/255)


    def __init__(self, **kw):
        super().__init__(**kw)
        self.h_lines=[]
        self.v_lines=[]

    def generate_lines(self):

        # HORIZONTAL LINES
        no_h_lines=int(self.height/self.SPACING)
        last_y=0

        for line in self.h_lines:
            last_y+=self.SPACING
            line.points=(0,last_y,self.width,last_y)
        if len(self.h_lines)<no_h_lines:
            with self.canvas:
                Color(0,0,0)
                for _ in range(len(self.h_lines),no_h_lines):
                    last_y+=self.SPACING
                    self.h_lines.append(Line(points=(0,last_y,self.width,last_y),width=1))

        # VERTICAL LINES        
        no_v_lines=int(self.width/self.SPACING)
        last_x=0
        for line in self.v_lines:
            last_x+=self.SPACING
            line.points=(last_x,0,last_x,self.height)
        if len(self.v_lines)<no_v_lines:
            with self.canvas:
                Color(0,0,0)
                for _ in range(len(self.v_lines),no_v_lines):
                    last_x+=self.SPACING
                    self.v_lines.append(Line(points=(last_x,0,last_x,self.height),width=1))


    def on_size(self,j,h):
        self.generate_lines()