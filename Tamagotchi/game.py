import pygame, os, time
from states.title import Title

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Tagomachi')
        self.clock = pygame.time.Clock()
        self.size_window = [1536, 1024]
        self.canvas = pygame.Surface(self.size_window)
        self.screen = pygame.display.set_mode(self.size_window)
        
        self.runing, self.playing = True, True
      
        self.actions = {"start": False, "clicked": False, "name_box": None, "use_medicine": False}   # store actions get from player 
        self.dt, self.prev_time = 0, 0 # time controle 
        self.state_stack = [] # store game display layers 
        self.parties = {}
        self.animal_died = None 
        self.player_score = None
        self.animal_names = {1: "Animal 1", 2: "Animal 2", 3: "Animal 3", 4: "Animal 4", 5: "Animal 5"}
        self.input_text = []
        
        self.load_assets() # load data 
        self.load_states() # call first layer of the game --> Title
        
    def game_loop(self):
        while self.playing:
            self.get_dt() # time update 
            self.get_events() # update player inputs or actions
            self.update() # update game logic
            self.render() # draw on display 
            self.clock.tick(60) # update 60 frame / sec 
    
    def get_events(self):
        # limite the events detection --> optimize the code 
        pygame.event.set_allowed([pygame.QUIT, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.KEYDOWN, pygame.KEYUP])
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT: # if player quite = game stope
                self.runing, self.playing = False, False
            
            if event.type == pygame.MOUSEBUTTONDOWN: 
                if event.button == 1:
                    self.actions["clicked"] = True
                  
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                   self.actions["clicked"] = False
        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: 
                    self.runing, self.playing = False, False
                    
                if event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                self.input_text += event.unicode
     
                if event.key == pygame.K_RETURN:
                    if self.actions["name_box"] != None and len(self.input_text) != 0:
                        self.animal_names[self.actions["name_box"]] = self.input_text
                        self.input_text = []
                    
    def update(self):
        # update the last state from the liste of self.state_stack
        self.state_stack[-1].update(self.dt, self.actions)
      
    def render(self):
        # render the last state from the liste of self.state_stack
        self.state_stack[-1].render(self.canvas)
        self.screen.blit(self.canvas,(0,0))
        pygame.display.flip()
    
    def get_dt(self):
        now = time.time() # return in sec 
        self.dt = now - self.prev_time
        self.prev_time = now
    
    def draw_text(self, surface, text, color, x, y, size):
        self.font = pygame.font.Font(self.fonts, size)
        self.texte_surface = self.font.render(text, True, color)
        self.text_rect = self.texte_surface.get_rect(topleft = (x, y))
        surface.blit(self.texte_surface, self.text_rect)
    
    def load_assets(self): #create pointers to directories
        self.assets_dir = os.path.join('data')
        self.fonts_dir = os.path.join(self.assets_dir, "font")
        self.animals_dir = os.path.join(self.assets_dir, "animals")
        self.buttons_dir = os.path.join(self.assets_dir, "buttons")
        self.backgrounds_dir = os.path.join(self.assets_dir, "backgrounds")
        
        # load data 
        self.fonts = os.path.join(self.fonts_dir, "ARCADE.TTF")
        self.button_sound = pygame.mixer.Sound(os.path.join(self.buttons_dir, "sleep.mp3"))
        self.medal_b = pygame.image.load(os.path.join(self.buttons_dir, "medal_b.png")).convert_alpha()
        self.medal_s = pygame.image.load(os.path.join(self.buttons_dir, "medal_s.png")).convert_alpha()
        self.medal_g = pygame.image.load(os.path.join(self.buttons_dir, "medal_g.png")).convert_alpha()
        self.help_button = pygame.image.load(os.path.join(self.buttons_dir, "help.png")).convert_alpha()
        self.menu_button = pygame.image.load(os.path.join(self.buttons_dir, "menu.png")).convert_alpha()
        self.exit_button = pygame.image.load(os.path.join(self.buttons_dir, "exit.png")).convert_alpha()
        self.quit_button = pygame.image.load(os.path.join(self.buttons_dir, "quit.png")).convert_alpha()
        self.back_button = pygame.image.load(os.path.join(self.buttons_dir, "back.png")).convert_alpha()
        self.h_t_p_button = pygame.image.load(os.path.join(self.buttons_dir, "htp.png")).convert_alpha()
        self.page1_button = pygame.image.load(os.path.join(self.buttons_dir, "page1.png")).convert_alpha()
        self.page2_button = pygame.image.load(os.path.join(self.buttons_dir, "page2.png")).convert_alpha()
        self.start_button = pygame.image.load(os.path.join(self.buttons_dir, "start.png")).convert_alpha()
        self.next_button = pygame.image.load(os.path.join(self.buttons_dir, "continue.png")).convert_alpha()
        self.name_box_button1 = pygame.image.load(os.path.join(self.buttons_dir, "name.png")).convert_alpha()
        self.newgame_button = pygame.image.load(os.path.join(self.buttons_dir, "newgame.png")).convert_alpha()
        self.medicine_button = pygame.image.load(os.path.join(self.buttons_dir, "medicine.png")).convert_alpha()
        self.name_box_button = pygame.image.load(os.path.join(self.buttons_dir, "name_box.png")).convert_alpha()
    
        self.eat_button = pygame.image.load(os.path.join(self.buttons_dir, "eat.png")).convert_alpha()
        self.play_button = pygame.image.load(os.path.join(self.buttons_dir, "play.png")).convert_alpha()
        self.sleep_button = pygame.image.load(os.path.join(self.buttons_dir, "sleep.png")).convert_alpha()
        self.drink_button = pygame.image.load(os.path.join(self.buttons_dir, "drink.png")).convert_alpha()
        
        self.G_W_bg = pygame.image.load(os.path.join(self.backgrounds_dir, "frame1.png")).convert_alpha()
        self.htp1_bg = pygame.image.load(os.path.join(self.backgrounds_dir, "htp_bg1.png")).convert_alpha()
        self.htp2_bg = pygame.image.load(os.path.join(self.backgrounds_dir, "htp_bg2.png")).convert_alpha()
        self.nyp_bg = pygame.image.load(os.path.join(self.backgrounds_dir, "nyp_bg.png")).convert_alpha()
        self.exit_bg = pygame.image.load(os.path.join(self.backgrounds_dir, "exit_bg.png")).convert_alpha()
        self.Title_bg = pygame.image.load(os.path.join(self.backgrounds_dir, "Title_bg.png")).convert_alpha()
        self.gameover_bg = pygame.image.load(os.path.join(self.backgrounds_dir, "gameover_bg.png")).convert_alpha()
            
    def load_states(self): # enter in first state 
        self.title_screen = Title(self)
        self.state_stack.append(self.title_screen)
        
if __name__ == "__main__":
    g = Game()
    while g.runing:
        g.game_loop()
    