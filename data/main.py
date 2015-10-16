from . import prepare,tools
from .states import splash_screen, easing_tester

def main():
    controller = tools.Control(prepare.ORIGINAL_CAPTION)
    states = {"SPLASH": splash_screen.SplashScreen(),
                  "TESTING": easing_tester.EasingTest()}
    controller.setup_states(states, "SPLASH")
    controller.main()
