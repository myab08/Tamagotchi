import states.tools as tools
from states.state import State
from states.name_set import Name_Set
from states.how_to_play_menu import How_To_Play_Menu

class Title(State):
    def __init__(self, game):
        State.__init__(self, game)
        ''' This class is for the menu page'''
        self.start = tools.Button(615, 510, self.game.start_button) 
        self.help_menu = tools.Button(507, 720, self.game.h_t_p_button)

    def update(self, delta_time, actions): # update states
        if self.start.click(actions["clicked"]):
            self.game.button_sound.play()
            name_set_up = Name_Set(self.game)
            name_set_up.enter_state()
            
        if self.help_menu.click(actions["clicked"]):
            new_state = How_To_Play_Menu(self.game)
            new_state.enter_state()

    def render(self, display): # show on the screen 
        display.blit(self.game.Title_bg,(0, 0))
        self.start.render(display)
        self.help_menu.render(display)
   
