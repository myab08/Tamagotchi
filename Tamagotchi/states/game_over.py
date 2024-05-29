import states.tools as tools
from states.state import State

class Game_Over(State):
    def __init__(self, game):
        State.__init__(self, game)
        ''' This class is for the game-over page'''
        self.bg = self.game.gameover_bg
        self.menu_button = tools.Button(972, 691, self.game.menu_button)
        self.quit_button = tools.Button(456, 691, self.game.quit_button)
        self.newgame_button = tools.Button(685, 695, self.game.newgame_button)
        
    def update(self, delta_time, actions): # update states
        if self.quit_button.click(actions["clicked"]):
            self.game.runing, self.game.playing = False, False
            
        if self.newgame_button.click(actions["clicked"]):
            self.game.actions["start"] = True 
            self.game.button_sound.play()
            while len(self.game.state_stack) > 2:
                self.game.state_stack.pop()
                
        if self.menu_button.click(actions["clicked"]):
            self.game.button_sound.play()
            while len(self.game.state_stack) > 1:
                self.game.state_stack.pop()
        
    def render(self, display): # show on the screen 
        animal = self.game.animal_died[0]
        time = self.game.animal_died[2]
        date = self.game.animal_died[3]
        star = self.game.player_score[0]
        medicine = self.game.player_score[1]
        
        if self.game.animal_died[1] == "hunger":
            cause = "of starvation"
        elif self.game.animal_died[1] == "energy":
            cause = "of fatigue"
        elif self.game.animal_died[1] == "happy":
            cause = "of paranoia"
        else:
            cause = "of thirst"
            
        display.blit(self.bg, (384, 256))
        
        self.game.draw_text(display, animal + " died from " + cause, "black", 420, 540, 30)
        self.game.draw_text(display,  "at " + str(time) +" seconds", "black", 420, 585, 30) 
        self.game.draw_text(display, "and was " + str(date) + " days old", "black", 420, 630, 30) 
        self.game.draw_text(display, str(star) + "   " + str(medicine), "black", 840, 581, 60)
        
        if star < 5:
            display.blit(self.game.medal_b, (896, 398))
        elif star < 15:
            display.blit(self.game.medal_s, (896, 398))
        else:
            display.blit(self.game.medal_g, (896, 398))
            
        self.quit_button.render(display)
        self.menu_button.render(display)
        self.newgame_button.render(display)
  
    