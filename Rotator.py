from kivy.clock import Clock


class Rotator(object):
    ''' A class that handles the rotation of widgets '''
    def __init__(self):
        self.angle = 0
        self.widgets = []
        self.velocity = 1

    def rotate_this(self, widget):
        ''' Starts rotating the given widget '''
        self.widgets.append(widget)
        if len(self.widgets) == 1:
            Clock.schedule_interval(self.rotate, 0.05)

    def rotate(self, dt):
        self.angle += self.velocity*0.5
        self.update()
        if abs(self.angle) >= 8:
            self.velocity *= -1

    def update(self):
        for widget in self.widgets:
            widget.angle = self.angle

    def end_rotate(self):
        Clock.unschedule(self.rotate)
        self.angle = 0
        self.update()
        self.widgets = []
