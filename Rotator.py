
from kivy.clock import Clock


class Rotator(object):
    ''' A class that handles the rotation of buttons '''
    def __init__(self):
        self.angle = 0
        self.buttons = []

    def rotateThisButton(self, button):
        ''' Starts rotating the given button '''

        self.buttons.append(button)
        # It is already rotating
        if len(self.buttons) > 1:
            self.buttons[-1].angle = self.angle
        else:
            Clock.schedule_interval(self.rotateLeft, 0.05)

    def rotateLeft(self, dt):
        if self.angle < 8:
            self.angle += 0.5
        for button in self.buttons:
            button.angle = self.angle
        if self.angle == 8:
            Clock.unschedule(self.rotateLeft)
            Clock.schedule_interval(self.rotateRight, 0.05)

    def rotateRight(self, dt):
        if self.angle > -8:
            self.angle -= 0.5
        for button in self.buttons:
            button.angle = self.angle
        if self.angle == -8:
            Clock.unschedule(self.rotateRight)
            Clock.schedule_interval(self.rotateLeft, 0.05)

    def endRotate(self):
        Clock.unschedule(self.rotateRight)
        Clock.unschedule(self.rotateLeft)
        for button in self.buttons:
            # The bizarre way to get the angles back to 0
            while button.angle != 0:
                if button.angle > 0:
                    button.angle -= 0.5
                else:
                    button.angle += 0.5
        self.buttons = []