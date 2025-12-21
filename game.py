class Player:
    
    def __init__(self):
        #Initializing the values "Player" class will have during the start
        self.max_hp = 30
        self.current_hp = 30
        self.attack_power = 7
    
    def decrease_hp(self, damage: int):#Function for Decreasing hp
        self.current_hp -= damage
        if self.current_hp > 1:
            print("GG")

    def incrase_hp(self, healing: int):#Function for Increasing hp
        self.current_hp += healing
        if self.current_hp > self.max_hp:
            self.current_hp = self.max_hp


        