import random


class BColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    CBLACK = '\33[30m'
    CRED = '\33[31m'
    CGREEN = '\33[32m'
    CYELLOW = '\33[33m'
    CBLUE = '\33[34m'
    CVIOLET = '\33[35m'
    CBEIGE = '\33[36m'
    CWHITE = '\33[37m'

    CBLACKBG = '\33[40m'
    CREDBG = '\33[41m'
    CGREENBG = '\33[42m'
    CYELLOWBG = '\33[43m'
    CBLUEBG = '\33[44m'
    CVIOLETBG = '\33[45m'
    CBEIGEBG = '\33[46m'
    CWHITEBG = '\33[47m'


class Person:
    def __init__(self, name, hp, mp, atk, df, magic, item):
        self.name = name
        self.maxHp = hp
        self.hp = hp
        self.maxMp = mp
        self.mp = mp
        self.atk = atk
        self.df = df
        self.magic = magic
        self.item = item
        self.action = ["Attack", "Magic", "Item"]

    def generate_damage(self, target):
        # ±5% difference
        atkL = int(self.atk * 0.95)
        atkH = int(self.atk * 1.05)
        return int((random.randrange(atkL, atkH) - 0.5 * target.df))

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0
        return self.hp

    def heal(self, prop):
        self.hp += prop
        if self.hp > self.maxHp:
            self.hp = self.maxHp

    def get_max_hp(self):
        return self.maxHp

    def get_hp(self):
        return self.hp

    def get_max_mp(self):
        return self.maxMp

    def get_mp(self):
        return self.mp

    def reduce_mp(self, cost):
        self.mp -= cost
        return self.mp

    def get_item(self):
        return self.item

    def get_spell_name(self, i):
        return self.magic[i]["name"]

    def get_spell_mp_cost(self, i):
        return self.magic[i]["cost"]

    def choose_action(self):
        print(BColors.BOLD + BColors.OKBLUE + "Action: " + BColors.ENDC)
        i = 1
        for item in self.action:
            print(str(i) + ". ", item)
            i += 1

    def choose_magic(self):
        print(BColors.BOLD + BColors.OKBLUE + "Magic: " + BColors.ENDC)
        i = 1
        for spell in self.magic:
            print(str(i) + ".", spell.name, "(cost:" + str(spell.cost) + ")")
            i += 1

    def choose_item(self):
        print(BColors.BOLD + BColors.OKBLUE + "Items:" + BColors.ENDC)
        i = 1
        for item in self.item:
            print("%d. %s: %s (x%d)" % (i, item["item"].name, item["item"].description, item["quantity"]))
            i += 1

    def choose_target(self, enemies):
        print(BColors.BOLD + BColors.FAIL + "Which is the target? " + BColors.ENDC)
        i = 1
        for enemy in enemies:
            print("%d. %s" % (i, enemy.name))
            i += 1

    def get_stats(self):
        hp_bar = "█" * int((self.hp / self.maxHp) * 25)  # Use 25 spaces to display HP bar
        mp_bar = "█" * int((self.mp / self.maxMp) * 10)  # Use 10 spaces to display MP bar
        cur_hp = f'{self.hp}/{self.maxHp}'
        cur_mp = f'{self.mp}/{self.maxMp}'
        # Align bars
        print(f'{" ":32}{"_" * 25}{" ":12}{"_" * 10}')
        print(f'{self.name:<15} {cur_hp:>15}|{BColors.OKGREEN}{hp_bar:<25}{BColors.ENDC}|'
              f'{cur_mp:>10}|{BColors.OKBLUE}{mp_bar:<10}{BColors.ENDC}|')

    def get_enemy_stats(self):
        hp_bar = "█" * int((self.hp / self.maxHp) * 47)
        cur_hp = f'{self.hp}/{self.maxHp}'
        print(f'{" ":32}{"_" * 47}')
        print(f'{self.name:<15} {cur_hp:>15}|{BColors.FAIL}{hp_bar:<47}{BColors.ENDC}|')
