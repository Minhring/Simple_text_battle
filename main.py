from CLasses.person import Person, BColors
from CLasses.magic import Spell
from CLasses.inventory import Item
import random

# Create Black Magic
fire = Spell("Fire", 10, 80, "black")
thunder = Spell("Thunder", 20, 100, "black")
blizzard = Spell("Blizzard", 30, 150, "black")
meteor = Spell("Meteor", 70, 500, "black")
quake = Spell("Quake", 50, 350, "black")

# Create White Magic
cure = Spell("Cure", 12, 120, "white")
purification = Spell("Purification", 20, 200, "white")

magic = [fire, thunder, blizzard, meteor, quake, cure, purification]

# Create Items
potion = Item("Potion", "potion", "Heal 20 HP", 20)
superpotion = Item("Super Potion", "potion", "Heal 50 HP", 50)
hyperpotion = Item("Hyper Potion", "potion", "Heal 200 HP", 200)
elixir = Item("Elixir", "elixir", "Fully restores HP/MP.", 9999)
maxelixir = Item("Max Elixir", "elixir", "Fully restores HP/MP of all party member", 9999)
grenade = Item("Grenade", "attack", "Deals 500 damage to the enemy", 500)

items = [{"item": potion, "quantity": 2},
         {"item": superpotion, "quantity": 10},
         {"item": hyperpotion, "quantity": 5},
         {"item": elixir, "quantity": 5},
         {"item": maxelixir, "quantity": 5},
         {"item": grenade, "quantity": 10}]

# Create the characters
player1 = Person("John", 1560, 150, 85, 30, magic, items)
player2 = Person("Nick", 1860, 120, 70, 50, magic, items)
player3 = Person("Minh", 1760, 200, 90, 45, magic, items)
team = [player1, player2, player3]

# Create the enemies
enemy1 = Person("BOSS", 3000, 100, 110, 60, magic, items)
enemy2 = Person("Imp", 800, 100, 65, 40, magic, items)
enemy3 = Person("Imp", 800, 100, 65, 40, magic, items)
enemies = [enemy1, enemy2, enemy3]

# Parameters
running = True
you_win = False
turn = 1


# Check your choice
def get_choice(choice, list_choices):
    while choice is None:
        try:
            choice = int(input("Your choice is: ")) - 1
            if choice not in range(len(list_choices)):
                print(BColors.CRED + "Please select a number in the list above." + BColors.ENDC)
                choice = None
        except ValueError:
            print(BColors.CRED + "Please select a number in the list above." + BColors.ENDC)
            choice = None
    return choice


while running:
    # Show the players stats
    print(BColors.BOLD + BColors.CBEIGEBG + "*" * 10 + "  TURN %d  " % turn + "*" * 10 + BColors.ENDC)
    print(f'{BColors.BOLD}{"NAME":<32}{"HP":<25}{" ":12}{"MP":<10}{BColors.ENDC}')
    for player in team:
        player.get_stats()
    print("=" * 79)

    # Show the enemy stats
    for enemy in enemies:
        enemy.get_enemy_stats()

    print(BColors.BOLD + BColors.CBEIGE + "...PLAYER TURN..." + BColors.ENDC)
    for player in team:
        print(BColors.BOLD + BColors.OKGREEN + "%s turn." % player.name + BColors.ENDC)
        # while loop for choosing again
        action_choice = -1
        while action_choice == -1:
            # Choose an action from player.action
            player.choose_action()
            action_choice = get_choice(None, player.action)

            # 1. Player Actions (Attack, Magic, Use item)
            # Attack
            if action_choice == 0:
                # Choose an enemy from enemies
                player.choose_target(enemies)
                enemy_target = get_choice(None, enemies)

                dmg = player.generate_damage(enemies[enemy_target])
                enemies[enemy_target].take_damage(dmg)
                print(BColors.BOLD + ">>> " + player.name, "attacked.", enemies[enemy_target].name, "took", dmg,
                      "damage." + BColors.ENDC)
            # Magic
            elif action_choice == 1:
                # Choose a magic from player.magic
                player.choose_magic()
                magic_choice = get_choice(None, player.magic)

                thisSpell = player.magic[magic_choice]
                # MP required
                if player.get_mp() < thisSpell.cost:
                    print(BColors.BOLD + ">>> " + "Not enough MP for casting %s spell" % thisSpell.name + BColors.ENDC)
                    # Choose action again
                    print(BColors.BOLD + BColors.CGREEN + "Please choose an action again for %s" % player.name
                          + BColors.ENDC)
                    action_choice = -1
                    continue
                # Else, reduce player's MP and use this Spell
                player.reduce_mp(thisSpell.cost)
                if thisSpell.type == "black":
                    # Choose an enemy from enemies
                    player.choose_target(enemies)
                    enemy_target = get_choice(None, enemies)

                    dmg = thisSpell.generate_spell_damage()
                    enemies[enemy_target].take_damage(dmg)
                    print(BColors.BOLD + ">>> " + player.name, "attacked with %s magic. %s took %s damage."
                          % (thisSpell.name, enemies[enemy_target].name, dmg) + BColors.ENDC)
                elif thisSpell.type == "white":
                    player.heal(thisSpell.power)
                    print(BColors.BOLD + ">>> " + "Use %s magic." % thisSpell.name, player.name, "restored %d HP."
                          % thisSpell.power + BColors.ENDC)
            # Item
            elif action_choice == 2:
                # Choose an item from items
                player.choose_item()
                item_choice = get_choice(None, player.item)
                # Quantity required
                if player.item[item_choice]["quantity"] == 0:
                    print(BColors.BOLD + ">>> " + "%s is out of stock." % player.item[item_choice][
                        "item"].name + BColors.ENDC)
                    # Choose action again
                    print(BColors.BOLD + BColors.CGREEN + "Please choose an action again for %s" % player.name
                          + BColors.ENDC)
                    action_choice = -1
                    continue
                # Else, use this item
                thisItem = player.item[item_choice]["item"]
                player.item[item_choice]["quantity"] -= 1

                if thisItem.type == "potion":
                    player.heal(thisItem.prop)
                    print(BColors.BOLD + ">>> " + "Use %s." % thisItem.name, player.name, "restored %d HP."
                          % thisItem.prop + BColors.ENDC)
                elif thisItem.type == "elixir":
                    if thisItem.name == "Max Elixir":
                        for member in team:
                            member.hp = member.maxHp
                            member.mp = member.maxMp
                        print(BColors.BOLD + ">>> " + "Use %s." % thisItem.name,
                              "All team restored full HP & MP." + BColors.ENDC)
                    else:
                        player.hp = player.maxHp
                        player.mp = player.maxMp
                        print(BColors.BOLD + ">>> " + "Use %s." % thisItem.name,
                              "%s restored full HP & MP." % player.name + BColors.ENDC)
                elif thisItem.type == "attack":
                    # Choose an enemy from enemies
                    player.choose_target(enemies)
                    enemy_target = get_choice(None, enemies)

                    enemies[enemy_target].take_damage(thisItem.prop)
                    print(BColors.BOLD + ">>> " + player.name, "attacked with the %s. %s took %d damage."
                          % (thisItem.name, enemies[enemy_target].name, thisItem.prop) + BColors.ENDC)

        # Check if you win
        for i, enemy in enumerate(enemies):
            if enemy.hp == 0:
                # This enemy has fainted. Remove it.
                enemies.pop(i)
        if not enemies:
            print(BColors.BOLD + BColors.OKGREEN + "All enemy has fainted. You win!" + BColors.ENDC)
            running = False
            you_win = True
            break

    if you_win:
        break

    # 2. Enemy Action
    print(BColors.BOLD + BColors.CRED + "...ENEMY TURN..." + BColors.ENDC)

    for enemy in enemies:
        # A little intelligence. The enemies will always attack the player with HP < 50%
        player_target = None
        for index, player in enumerate(team):
            if player.hp <= 0.5 * player.maxHp:
                player_target = index
        # If any enemy has HP low (< 50%), its Attack will increase 20% after each turn.
        if enemy.hp < 0.5 * enemy.maxHp:
            enemy.atk *= 1.2
        if player_target is None:
            player_target = random.randrange(len(team))

        dmg = enemy.generate_damage(team[player_target])
        team[player_target].take_damage(dmg)
        print(BColors.BOLD + ">>> " + enemy.name, "attacked.", team[player_target].name, "took", dmg, "damage"
              + BColors.ENDC)
    print("-" * 79)

    for i, player in enumerate(team):
        if player.hp == 0:
            team.pop(i)
    if not team:
        print(BColors.BOLD + BColors.FAIL + "All member in your team has fainted. You lose!" + BColors.ENDC)
        running = False

    # End turn
    turn += 1
