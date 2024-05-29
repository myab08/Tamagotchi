import states.tools as tools
from states.state import State
from states.game_world import Game_World

class Name_Set(State):
    def __init__(self, game):
        State.__init__(self, game)
        ''' This class is for the set pets names page'''
        self.bg = self.game.nyp_bg
        
        self.back = tools.Button(340, 210, self.game.back_button)
        self.next = tools.Button(1165, 740, self.game.next_button)
        
        self.boxes = {1: tools.Button(617, 366, self.game.name_box_button), 
                      2: tools.Button(617, 463, self.game.name_box_button),
                      3: tools.Button(617, 560, self.game.name_box_button),
                      4: tools.Button(617, 658, self.game.name_box_button),
                      5: tools.Button(617, 755, self.game.name_box_button)}
        
    def update(self, delta_time, actions): # update states
        if self.next.click(actions["clicked"]) or actions["start"]:
            self.game.button_sound.play()
            
            if actions["start"]:
                self.game.actions["start"] = False 
            
            rounds = len(self.game.parties) 
            self.game.parties[rounds] = Game_World(self.game)
            self.game.parties[rounds].enter_state()
        
        if self.back.click(actions["clicked"]):
            self.game.button_sound.play()
            self.exit_state()
            
        for box in self.boxes.values():
            box.click(actions["clicked"])
    
    def render(self, display): # show on the screen 
        display.blit(self.bg, (268, 163))
        self.back.render(display)
        self.next.render(display)
        
        for box in self.boxes.values():
            box.render(display)
   
