class State():
    def __init__(self, game):
        ''' This class is for the management of all pages or levels of the game 
        we use the stack methode for the data struture'''
        self.game = game 
        self.prev_state = None 
        
    def update(self, delta_time, actions):
        pass
    
    def render(self, surface):
        pass 
    
    def enter_state(self):
        # add new state in self.game.state_stack list
        if len(self.game.state_stack) > 1:
            self.prev_state = self.game.state_stack[-1]
        self.game.state_stack.append(self)
            
    def exit_state(self):
        # delete your last state from the list
        self.game.state_stack.pop()
            
