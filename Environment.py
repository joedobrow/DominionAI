class Environment:
    
    
    def __init__(self):
        
        # Key:
        # 0 -- copper
        # 1 -- silver
        # 2 -- gold
        # 3 -- estate
        # 4 -- duchy
        # 5 -- province
        # 6 -- curse
        
        self.card_counts = [45, 30, 30, 8, 8, 8 ,8]
        self.money_map = {0:0, 1:3, 2:6, 3:2, 4:5, 5:8, 6:0}
        
    def update(self, card_num):
        
        self.card_counts[card_num] -= 1        
        
    def check_win(self):
        if self.card_counts[5] == 0:
            return True
        else:
            count = 0
            for i in self.card_counts:
                if i == 0:
                    count += 1
            if count > 2:
                return True
            else:
                return False
