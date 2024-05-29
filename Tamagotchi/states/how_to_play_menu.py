import states.tools as tools
from states.state import State

class How_To_Play_Menu(State):
    def __init__(self, game):
        State.__init__(self, game)
        ''' This class is for the How To Play page'''
        self.bg1 = self.game.htp1_bg
        self.bg2 = self.game.htp2_bg
        self.back = tools.Button(340, 210, self.game.back_button)
        self.page1 = tools.Button(733, 296, self.game.page1_button)
        self.page2 = tools.Button(780, 296, self.game.page2_button)
        self.state = 1
        
    def update(self, delta_time, actions): # update states
        if self.back.click(actions["clicked"]):
            if self.state == 1:
                self.game.button_sound.play()
                self.exit_state()
            else:
                self.state = 1
        if self.page1.click(actions["clicked"]):
            self.state = 1
            
        if self.page2.click(actions["clicked"]):
            self.state = 2
        
    def render(self, display): # show on the screen 
        if self.state == 1:
            display.blit(self.bg1, (268, 163))
        else: 
            display.blit(self.bg2, (268, 163))
        self.page1.render(display)
        self.page2.render(display)
        self.back.render(display)
