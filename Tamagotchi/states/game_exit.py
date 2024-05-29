import states.tools as tools
from states.state import State

class Game_Exit(State):
    def __init__(self, game):
        State.__init__(self, game)
        ''' This class is for the Exit page'''
        self.bg = self.game.exit_bg
        self.quit = tools.Button(456, 600, self.game.quit_button)
        self.back = tools.Button(443, 375, self.game.back_button)
        self.menu = tools.Button(972, 600, self.game.menu_button)
        self.newgame = tools.Button(685, 604, self.game.newgame_button)
        
    def update(self, delta_time, actions): # update states
        if self.back.click(actions["clicked"]):
            self.game.button_sound.play()
            self.exit_state()
            
        if self.quit.click(actions["clicked"]):
            self.game.runing, self.game.playing = False, False
            
        if self.newgame.click(actions["clicked"]):
            self.game.actions["start"] = True 
                
        if self.menu.click(actions["clicked"]) or self.game.actions["start"]:
            self.game.button_sound.play()
            while len(self.game.state_stack) > 1:
                self.game.state_stack.pop()
       
    def render(self, display): # show on the screen 
        display.blit(self.bg, (384, 350))
        self.back.render(display)
        self.quit.render(display)
        self.menu.render(display)
        self.newgame.render(display)

    