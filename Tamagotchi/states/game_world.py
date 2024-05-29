import pygame, os, random, states.tools as tools
from states.state import State 
from states.game_over import Game_Over 
from states.how_to_play_menu import How_To_Play_Menu
from states.game_exit import Game_Exit

class Game_World(State):
    def __init__(self, game):
        State.__init__(self, game)
        '''This class is for the Game page'''
        self.pos_bar() 
        
        self.total_medicine = 0
        self.medicine_duration = 0
        self.medicine, self.star = 0, 0
        self.healthy_animals_duration = 0
        self.last_time_update, self.time, self.day = 0, 0, 0
        self.prev_sta_med_convert = 1 # nb refrerence for stars converted count
        
        self.healthy_animals = []
        self.function_clicked = None 
        
        self.animals = {self.game.animal_names[1]: Animal(self.bars[0]),
                        self.game.animal_names[2]: Animal(self.bars[1]),
                        self.game.animal_names[3]: Animal(self.bars[2]),
                        self.game.animal_names[4]: Animal(self.bars[3]),
                        self.game.animal_names[5]: Animal(self.bars[4])}
        
        self.medicines = tools.Button(1326, 198, self.game.medicine_button)
        
        self.buttons = {"help": tools.Button(1328, 950, self.game.help_button),
                        "exit": tools.Button(1400, 955, self.game.exit_button)}
        
        self.functions = {"eat": tools.Button(1362, 283, self.game.eat_button),
                          "sleep": tools.Button(1362, 452, self.game.sleep_button),
                          "play": tools.Button(1362, 621, self.game.play_button),
                          "drink": tools.Button(1362, 790, self.game.drink_button)}
        
    def timer_update(self, delta_time): # update the real_time in game 
        self.last_time_update += delta_time
        sec = False
        if self.last_time_update >= 1:
            self.last_time_update = 0
            self.time += 1
            sec = True
        if self.time >= 180:
            self.day += 1
            self.time = self.time - 180
        return sec # return True if 1 sec is passed
    
    def update(self, delta_time, actions): # update states with the logic of the game 
        sec = self.timer_update(delta_time)
        healthy_animals = 0
        medicine = False
        
        if self.medicine != 0 and self.medicines.click(actions["clicked"]): # check if medicine is clicked 
            medicine = True
            if sec :
                self.medicine -= 1
            
        for action, b in self.buttons.items(): # check buttons state update 
            if b.click(actions["clicked"]): 
                if action == "help":
                    new_state = How_To_Play_Menu(self.game) 
                    new_state.enter_state()
                if action == "exit":
                    new_state = Game_Exit(self.game)
                    new_state.enter_state()
                    
        for action, f in self.functions.items(): # check functions state update 
            if f.click(actions["clicked"]):
                if self.function_clicked != action: # if user click an other function
                    self.function_clicked = action 
                    break
            
        for id, animal in self.animals.items(): # check animals state update 
            if animal.died != False:
                self.game.animal_died = [id, animal.died, self.time, self.day]
                self.game.player_score = [self.star, self.total_medicine]
                new_state = Game_Over(self.game)
                new_state.enter_state()
        
            if animal.super_healthy: # stars update 
                healthy_animals += 1
                if id not in self.healthy_animals:
                    self.healthy_animals.append(id)
                    self.star += 1
            else:
                if id in self.healthy_animals:
                    self.healthy_animals.remove(id)
                    
            # if animal is occupied     
            if not animal.update(delta_time, actions, medicine) or  self.function_clicked == None or animal.time_doing != 0:
                continue
            else:
                if self.function_clicked == "eat":
                    animal.eat()
                elif self.function_clicked == "sleep":
                    animal.sleep()
                elif self.function_clicked == "play":
                    animal.play()
                elif self.function_clicked == "drink":
                    animal.drink()
                self.function_clicked = None
                
        self.medicine_star_count(sec, healthy_animals)
        
    def medicine_star_count(self, sec, healthy_animals):
        ''' This function calculate the medicine and start count'''
        if self.star % 5 == 0 and self.star > self.prev_sta_med_convert:
            self.medicine += 1
            self.prev_sta_med_convert = self.star
                
        if healthy_animals < 5 and self.healthy_animals_duration != 0:
            self.healthy_animals_duration = 0
        else: 
            if sec: 
                self.healthy_animals_duration += 1
                if self.healthy_animals_duration == 5: 
                    self.healthy_animals_duration = 0
                    self.medicine += 1  # all 5 animals are super healthy during 5 sec 
                    if self.total_medicine < self.medicine :  self.total_medicine = self.medicine
            
    def render(self, display): # update on the screen 
        display.blit(self.game.G_W_bg, (0, 0))
        self.medicines.render(display)
        pos_name = 0
        
        if self.function_clicked != None: # draw clicked function 
            display.blit(self.functions[self.function_clicked].img, self.functions[self.function_clicked].rect)
        
        for f in self.functions.values():
            f.render(display)
        
        for b in self.buttons.values(): 
            b.render(display)
        
        for name, animal in self.animals.items():
            self.game.draw_text(display, name, (0, 0, 0), 42, self.name_pos[pos_name], 40) # draw animal name 
            animal.render(display) # draw animal animations
            pos_name += 1
        
        # draw the updated time & day on the screen   
        self.game.draw_text(display, str(self.day), (0, 0, 0), 1400, 20, 40)
        self.game.draw_text(display, str(self.time), (0, 0, 0), 1400, 65, 40)
        
        # draw the updated stars & medicines on the screen 
        self.game.draw_text(display, str(self.star), (0, 0, 0), 1440, 140, 45)
        self.game.draw_text(display, str(self.medicine), (0, 0, 0), 1440, 205, 45)
    
    def pos_bar(self): # initial posotion of animals health-bars
        self.bars = [[5, 66], [210], [415], [620], [825]]
        self.name_pos = [5, 210, 415, 620, 825]
        bar_y = 66
        for nb in self.bars:
            while len(nb) < 5:
                bar_y += 39
                nb.append(bar_y)
            bar_y += 49
            
class Animal():
    def __init__(self, cor_bar_y):
        ''' This class is for each animal'''
        self.random_pos()
        self.load_animals()
        
        self.bar_y = cor_bar_y # cordinate of health bar 
        self.current_frame, self.last_frame_update, self.last_sec_update = 0, 0, 0 
        
        self.died = False
        self.max_pts = 180
        self.super_healthy = False
        self.time_doing, self.doing = 0, None 
        self.health = {"hunger": 30, "energy": 30, "happy": 30, "hydration": 30}
        self.direction = {"left": False, "right": False, "up": False, "down": False}
        self.random_direc() # random movement of animal 
            
    def click(self, action): # ckeck if animal is clicked
        if self.rect.collidepoint(pygame.mouse.get_pos()) and action:
            return True 
        
    def random_direc(self, exept = None): # random movement for animal
        orientation = ["left", "right", "up", "down"]
        if exept == None:
            direc = random.choice(orientation)
        else:
            orientation.remove(exept)
            direc = random.choice(orientation)
        self.direction[direc] = True 
        
    def random_pos(self): # initial random position for animals
        x = random.randint(256, 1195)
        y = random.randint(0, 939)
        self.pos = [x, y]
        
    def one_sec(self, delta_time): # counter; return True if 1 sec is passe
        self.last_sec_update += delta_time
        if self.last_sec_update >= 1 : 
            self.last_sec_update = 0
            return True 
        return False
            
    def update(self, delta_time, actions, medicine): # update animal states
        self.rect = self.curr_image.get_rect(topleft = self.pos)
        sec = self.one_sec(delta_time)
    
        if sec: # update animal data after 1 sec 
            if self.time_doing >= 1:
                self.time_doing -= 1
                if self.time_doing == 0:
                    self.doing = None 
            for state, pts in self.health.items():
                if pts >= 1:
                    pts -= 1
                else:
                    self.died = state
                    return
                if medicine and pts < 145:
                    pts = 144
                    
        if self.doing == None: # if animal is doing nothing
            direction_x = self.direction["right"] - self.direction["left"]
            direction_y = self.direction["down"] - self.direction["up"]
            # update the position 
            self.pos[0] += 100 * delta_time * direction_x 
            self.pos[1] += 100 * delta_time * direction_y 
        else: 
            direction_x = False
            direction_y = False 
        
        # --- border of animals zone ---
        
        if self.pos[0] <= 256:
            self.random_direc("left") # if animal at border => animal change direction 
            self.direction["left"] = False
            
        if self.pos[0] >= 1152:
            self.random_direc("right")
            self.direction["right"] = False
        
        if self.pos[1] <= 0:
            self.random_direc("up") 
            self.direction["up"] = False
            
        if self.pos[1] >= 896:
            self.random_direc("down")
            self.direction["down"] = False
          
        self.animate(delta_time, direction_x, direction_y) 
        return self.click(actions["clicked"])
    
    def render(self, display): # show animal animation and health bars
        display.blit(self.curr_image, self.pos)
        
        ratio = None 
        exelence_count = 0
        bar_x, bar_y, w, h = 28, 0, 200, 10
        
        for pts in self.health.values(): # show animal health bar
            bar_y += 1
            ratio = pts / self.max_pts
            
            if 0.8 >= ratio > 0.2:
                pygame.draw.rect(display, "green", (bar_x, self.bar_y[bar_y], ratio * w , h))
            elif ratio <= 0.2:
                pygame.draw.rect(display, "red", (bar_x, self.bar_y[bar_y], ratio * w , h))
            else:
                pygame.draw.rect(display, "blue", (bar_x, self.bar_y[bar_y], ratio * w , h))
                exelence_count += 1
                
        if exelence_count == 4: self.super_healthy = True 
        else: self.super_healthy = False # check if every animal health_bar is over 80 %
            
    def animate(self, delta_time, direction_x, direction_y): # update animal image / animation
        self.last_frame_update += delta_time
        
        if self.doing == "sleep":
            self.curr_anim_list = self.sleep_sprites
            
        elif self.doing == "play":
            self.curr_anim_list = self.play_sprites
            
        elif self.doing == "drink":
            self.curr_anim_list = self.drink_sprites
            
        elif self.doing == "eat":
            self.curr_anim_list = self.eat_sprites
            
        elif self.doing == None: # if animal is not occupied
            if direction_x: 
                if direction_x > 0: self.curr_anim_list = self.right_sprites
                else: self.curr_anim_list = self.left_sprites
                
            if direction_y:
                if direction_y > 0: self.curr_anim_list = self.front_sprites
                else: self.curr_anim_list = self.back_sprites
        
        if self.last_frame_update > .15: #  speed changing frame  
            self.last_frame_update = 0
            self.current_frame  = (self.current_frame + 1) % len(self.curr_anim_list) # turn back to index 0 if out of range 
            self.curr_image = self.curr_anim_list[self.current_frame]
    
    def load_animals(self): # animal imgs load
        self.sprite_dir = os.path.join("data", "animals")
        self.front_sprites, self.back_sprites, self.right_sprites, self.left_sprites = [], [], [], []
        self.sleep_sprites, self.play_sprites, self.drink_sprites, self.eat_sprites  = [], [], [], []
        
        for i in range(0, 4): # load imgs into lists
            self.front_sprites.append(pygame.image.load(os.path.join(self.sprite_dir, "go_down", str(i) + ".png")).convert_alpha())
            self.back_sprites.append(pygame.image.load(os.path.join(self.sprite_dir, "go_up", str(i) + ".png")).convert_alpha())
            self.right_sprites.append(pygame.image.load(os.path.join(self.sprite_dir, "walk_right", str(i) + ".png")).convert_alpha())
            self.left_sprites.append(pygame.image.load(os.path.join(self.sprite_dir, "walk", str(i) + ".png")).convert_alpha())
            self.sleep_sprites.append(pygame.image.load(os.path.join(self.sprite_dir, "sleep", str(i) + ".png")).convert_alpha())
            self.play_sprites.append(pygame.image.load(os.path.join(self.sprite_dir, "play", str(i) + ".png")).convert_alpha())
            self.drink_sprites.append(pygame.image.load(os.path.join(self.sprite_dir, "drink", str(i) + ".png")).convert_alpha())
            self.eat_sprites.append(pygame.image.load(os.path.join(self.sprite_dir, "eat", str(i) + ".png")).convert_alpha())
        # Set the default frames to facing front
        self.curr_image = self.front_sprites[0]
        self.curr_anim_list = self.front_sprites
        self.rect = self.curr_image.get_rect(topleft = self.pos)
        
    def eat(self): 
        self.health["hunger"] += 40
        if self.health["hunger"] > self.max_pts:
            self.health["hunger"] = self.max_pts
        self.time_doing += 5
        self.doing = "eat"
        
    def play(self):
        self.health["happy"] += 40
        self.health["energy"] -= 15
        if self.health["happy"] > self.max_pts:
            self.health["happy"] = self.max_pts
        self.time_doing += 10
        self.doing = "play"
    
    def sleep(self):
        time_sleep = random.randint(30, 60)
        if self.health["energy"] + time_sleep > self.max_pts:
            time_sleep = self.max_pts - self.health["energy"] 
            self.health["energy"] = self.max_pts
        else:
            self.health["energy"] += time_sleep
        self.time_doing += time_sleep / 3
        self.doing = "sleep"
        
    def drink(self):
        self.health["hydration"] += 30
        if self.health["hydration"] > self.max_pts:
            self.health["hydration"] = self.max_pts
        self.time_doing += 2
        self.doing = "drink"