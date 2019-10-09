import os

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

from pidev.MixPanel import MixPanel
from pidev.kivy.PassCodeScreen import PassCodeScreen
from pidev.kivy.PauseScreen import PauseScreen
from pidev.kivy import DPEAButton
from pidev.kivy import ImageButton
from kivy.properties import ObjectProperty
from kivy.uix.slider import Slider
from kivy.animation import Animation
from threading import Thread
from time import sleep

from pidev.Joystick import Joystick

s = Slider(min=-100, max=100, value=25)

MIXPANEL_TOKEN = "x"
MIXPANEL = MixPanel("Project Name", MIXPANEL_TOKEN)

SCREEN_MANAGER = ScreenManager()
MAIN_SCREEN_NAME = 'main'
ADMIN_SCREEN_NAME = 'admin'
NEW_SCREEN = 'NewScreen'


class ProjectNameGUI(App):
    """
    Class to handle running the GUI Application
    """

    def build(self):
        """
        Build the application
        :return: Kivy Screen Manager instance
        """
        return SCREEN_MANAGER


Window.clearcolor = (1, 1, 1, 1)  # White


class MainScreen(Screen):
    """
    Class to handle the main screen and its associated touch events
    """
    joystick = Joystick(0, True)
    countButton = ObjectProperty(None)
    counter = 0
    x_position_joystick1 = ObjectProperty()
    y_position_joystick1 = ObjectProperty()

    def pressed(self):
        """
        Function called on button touch event for button with id: testButton
        :return: None
        """
        PauseScreen.pause(pause_scene_name='pauseScene', transition_back_scene='main', text="Test", pause_duration=1)

    def admin_action(self):
        """
        Hidden admin button touch event. Transitions to passCodeScreen.
        This method is called from pidev/kivy/PassCodeScreen.kv
        :return: None
        """
        SCREEN_MANAGER.current = 'passCode'

    def iterateButton(self, val):
        return str(int(val)+1)

    def changeButton(self, val):
        if val == "On":
            return "Off"
        else:
            return "On"

    def changeMotorLabel(self, val):
        if val == "Motor On":
            return "Motor Off"
        else:
            return "Motor On"


    def goToNewScreen(self):

        SCREEN_MANAGER.current = NEW_SCREEN


    def start_joy_thread(self):
        x = Thread(target=self.updateJoystick)
        x.start()


    def updateJoystick(self):

        while True:
            #print("hello")
            self.x_position_joystick1 = self.joystick.get_axis('x')
            self.ids.PositionJoystick.center_x = (self.x_position_joystick1 * (self.width / 2) + (self.width / 2))

            self.y_position_joystick1 = self.joystick.get_axis('y')
            self.ids.PositionJoystick.center_y = (self.y_position_joystick1 * (self.height / 2) + (self.height / 2))
            self.ids.PositionJoystick.text = "x= {:.3f}, y= {:.3f}".format(self.joystick.get_axis('x'), self.joystick.get_axis('y'))
            sleep(.1)
            #print(str(self.x_position_joystick1))
            #print(str(self.y_position_joystick1))





class AdminScreen(Screen):
    """
    Class to handle the AdminScreen and its functionality
    """

    def __init__(self, **kwargs):
        """
        Load the AdminScreen.kv file. Set the necessary names of the screens for the PassCodeScreen to transition to.
        Lastly super Screen's __init__
        :param kwargs: Normal kivy.uix.screenmanager.Screen attributes
        """
        Builder.load_file('AdminScreen.kv')

        PassCodeScreen.set_admin_events_screen(ADMIN_SCREEN_NAME)  # Specify screen name to transition to after correct password
        PassCodeScreen.set_transition_back_screen(MAIN_SCREEN_NAME)  # set screen name to transition to if "Back to Game is pressed"

        super(AdminScreen, self).__init__(**kwargs)

    @staticmethod
    def transition_back():
        """
        Transition back to the main screen
        :return:
        """
        SCREEN_MANAGER.current = MAIN_SCREEN_NAME

    @staticmethod
    def shutdown():
        """
        Shutdown the system. This should free all steppers and do any cleanup necessary
        :return: None
        """
        os.system("sudo shutdown now")

    @staticmethod
    def exit_program():
        """
        Quit the program. This should free all steppers and do any cleanup necessary
        :return: None
        """
        quit()


class NewScreen(Screen):

    def __init__(self, **kwargs):
        Builder.load_file('NewScreen.kv')
        super(NewScreen, self).__init__(**kwargs)

    @staticmethod
    def returnToMain():
        SCREEN_MANAGER.current = MAIN_SCREEN_NAME
#        quit()

    def animateButton(self):
        self.anim = Animation(x=500, y=0,)
        self.anim.start(self.ids.animatedButton)






"""
Widget additions
"""

Builder.load_file('main.kv')
SCREEN_MANAGER.add_widget(MainScreen(name=MAIN_SCREEN_NAME))
SCREEN_MANAGER.add_widget(PassCodeScreen(name='passCode'))
SCREEN_MANAGER.add_widget(PauseScreen(name='pauseScene'))
SCREEN_MANAGER.add_widget(AdminScreen(name=ADMIN_SCREEN_NAME))
SCREEN_MANAGER.add_widget(NewScreen(name = NEW_SCREEN))

"""
MixPanel
"""


def send_event(event_name):
    """
    Send an event to MixPanel without properties
    :param event_name: Name of the event
    :return: None
    """
    global MIXPANEL

    MIXPANEL.set_event_name(event_name)
    MIXPANEL.send_event()


if __name__ == "__main__":
    # send_event("Project Initialized")
    # Window.fullscreen = 'auto'
    ProjectNameGUI().run()
