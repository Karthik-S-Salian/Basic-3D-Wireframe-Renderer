from kivy.uix.relativelayout import RelativeLayout
from kivy.metrics import dp
from kivy.app import App
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line
from kivy.config import Config
from vertex_generator import cuboid,equilateral_triangular_pyramid,square_pyramid
from transformer import rotateX, rotateY
from redstone_display import RedstoneDisplay
from kivy.properties import Clock
from kivy.animation import Animation
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button

Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')


shapes={
    "cuboid":cuboid((300, 300, 300),(0,0, 400)),
    "pyramid 3": equilateral_triangular_pyramid(400, (0,0, 400)),
    "pyramid 4": square_pyramid(400,500,(0,0, 400))
}


class Renderer(RelativeLayout):
    SPACING = dp(20)
    LINE_COLOR = (242 / 255, 237 / 255, 218 / 255)
    FOCAL_LENGTH = dp(1200)

    def __init__(self, vertex_list=tuple(), edge_list=tuple(), **kw):
        super().__init__(**kw)
        self.vertex_list = vertex_list
        self.edge_list = edge_list
        if vertex_list:
            self.compute_projections()

    def blit(self, vertex_list: tuple, edge_list: tuple):
        self.clear_canvas()
        self.vertex_list = vertex_list
        self.edge_list = edge_list
        self.compute_projections()

    def on_size(self, j, h):
        self.adjust_center()

    def project_vertex(self, vertex, focal_length: int):
        x, y, z = vertex

        x_projected = (x * focal_length) // (z + focal_length)
        y_projected = (y * focal_length) // (z + focal_length)

        return (x_projected, y_projected)

    def compute_projections(self):
        self.projected_line_list = []
        with self.canvas:
            Color(*self.LINE_COLOR)
            for edge in self.edge_list:
                x, y = self.project_vertex(self.vertex_list[edge[0]], self.FOCAL_LENGTH)
                x1, y1 = self.project_vertex(self.vertex_list[edge[1]], self.FOCAL_LENGTH)
                self.projected_line_list.append((Line(points=(x, y, x1, y1), width=1.4), x, y, x1, y1))
            self.adjust_center()

    def adjust_center(self):
        for i in range(len(self.edge_list)):
            line, x, y, x1, y1 = self.projected_line_list[i]
            x += self.center_x
            y += self.center_y
            x1 += self.center_x
            y1 += self.center_y
            line.points = (x, y, x1, y1)

    def clear_canvas(self):
        for i in range(len(self.edge_list)):
            self.canvas.remove(self.projected_line_list[i][0])
        self.projected_line_list = []
        self.edge_list = tuple()
        self.vertex_list = tuple()


class MainLayout(RelativeLayout):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.renderer = Renderer(size_hint=(1, 1))
        self.add_widget(self.renderer)
        self.draw_duration=.3
        self.changed=True
        self.vertex_set, self.edge_set, self.object_center = shapes['cuboid']    
        self.drop_down=DropDown()
        Clock.schedule_interval(self.update, .1)

    def on_parent(self,j,k):
        if k:
            self.nav_drawer=self.ids.nav_drawer
            self.drawed=False

            for shape in shapes.keys():
                btn = Button(text=shape, size_hint_y=None, height=44)
                btn.bind(on_release=lambda btn: self.drop_down.select(btn.text))
                self.drop_down.add_widget(btn)

            self.drop_down.bind(on_select=self.update_shape)

    def update_shape(self,instance,shape):
        self.nav_drawer.ids.shape_button.text=shape
        self.vertex_set, self.edge_set, self.object_center = shapes[shape]
        self.changed=True


    def update(self, dt):
        if self.changed:
            self.renderer.blit(self.vertex_set, self.edge_set)
            self.changed=False

    def on_touch_down(self, touch):
        self.previous_touch_pos = touch.pos
        if self.drawed:
            if touch.x>self.nav_drawer.width:
                animation = Animation(pos=(-self.nav_drawer.width, 0),duration=self.draw_duration)
                self.drawed = False
                animation.start(self.nav_drawer)
        return super().on_touch_down(touch)

    def on_size(self,j,k):
        if self.drawed:
            self.nav_drawer.pos=(-self.nav_drawer.width, 0)
            self.drawed=False


    def on_touch_move(self, touch):
        mouseX, mouseY = touch.pos
        if self.drawed:
            if mouseX<=self.nav_drawer.width:
                return super().on_touch_move(touch)
        pmouseX, pmouseY = self.previous_touch_pos
        self.previous_touch_pos = touch.pos
        self.vertex_set = rotateY(self.vertex_set, mouseX - pmouseX, self.object_center)
        self.vertex_set = rotateX(self.vertex_set, mouseY - pmouseY, self.object_center)
        self.changed=True
        return super().on_touch_move(touch)


    def on_draw_request(self):
        if not self.drawed:
            animation = Animation(pos=(0, 0),duration=self.draw_duration)
            self.drawed = True
            animation.start(self.nav_drawer)

    


if __name__ == "__main__":
    class MainApp(App):
        def build(self):
            return MainLayout()


    MainApp().run()
