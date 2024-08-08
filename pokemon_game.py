import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pokémon Battle Game")

# Load images with error handling
def load_image(filename):
    try:
        return pygame.image.load(filename).convert_alpha()
    except pygame.error as e:
        print(f"Failed to load image {filename}: {e}")
        pygame.quit()
        exit()

# Load images
bulbasaur_img = load_image("bulbasaur.png")
charmander_img = load_image("charmander.png")
squirtle_img = load_image("squirtle.png")
wild_pokemon_imgs = [load_image("pidgey.png"), load_image("rattata.png"), load_image("caterpie.png")]

class Pokemon:
    def __init__(self, name, image, type, hp, attack, x, y):
        self.name = name
        self.image = image
        self.type = type
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.x = x
        self.y = y
    
    def draw(self):
        screen.blit(self.image, (self.x, self.y))
    
    def attack_opponent(self, opponent):
        damage = random.randint(self.attack - 5, self.attack + 5)
        opponent.hp -= damage
        return damage

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    surface.blit(textobj, (x, y))

def choose_starter():
    print("Choose your starter Pokémon:")
    print("1. Bulbasaur (Grass)")
    print("2. Charmander (Fire)")
    print("3. Squirtle (Water)")
    choice = input("Enter the number of your choice: ")
    if choice == "1":
        return Pokemon("Bulbasaur", bulbasaur_img, "Grass", 45, 10, 100, 100)
    elif choice == "2":
        return Pokemon("Charmander", charmander_img, "Fire", 39, 12, 100, 100)
    elif choice == "3":
        return Pokemon("Squirtle", squirtle_img, "Water", 44, 11, 100, 100)
    else:
        print("Invalid choice, choosing Bulbasaur by default.")
        return Pokemon("Bulbasaur", bulbasaur_img, "Grass", 45, 10, 100, 100)

def encounter_wild_pokemon():
    return Pokemon("Wild Pokémon", random.choice(wild_pokemon_imgs), "Normal", 30, 5, 500, 300)

def display_battle_status(player_pokemon, wild_pokemon, font, message):
    screen.fill(WHITE)
    player_pokemon.draw()
    wild_pokemon.draw()
    draw_text(message, font, BLACK, screen, 10, 50)
    draw_text(f"{player_pokemon.name} HP: {player_pokemon.hp}/{player_pokemon.max_hp}", font, BLACK, screen, 10, 10)
    draw_text(f"{wild_pokemon.name} HP: {wild_pokemon.hp}/{wild_pokemon.max_hp}", font, BLACK, screen, SCREEN_WIDTH - 300, 10)
    pygame.display.flip()
    time.sleep(1)

def battle(player_pokemon, wild_pokemon):
    font = pygame.font.Font(None, 36)
    battle_running = True

    while player_pokemon.hp > 0 and wild_pokemon.hp > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
        # Player attack
        damage = player_pokemon.attack_opponent(wild_pokemon)
        display_battle_status(player_pokemon, wild_pokemon, font, f"{player_pokemon.name} attacks {wild_pokemon.name} for {damage} damage!")
        if wild_pokemon.hp <= 0:
            display_battle_status(player_pokemon, wild_pokemon, font, f"{wild_pokemon.name} has fainted!")
            break
        
        # Wild Pokémon attack
        damage = wild_pokemon.attack_opponent(player_pokemon)
        display_battle_status(player_pokemon, wild_pokemon, font, f"{wild_pokemon.name} attacks {player_pokemon.name} for {damage} damage!")
        if player_pokemon.hp <= 0:
            display_battle_status(player_pokemon, wild_pokemon, font, f"{player_pokemon.name} has fainted! Game over.")
            battle_running = False
            break

    return battle_running

def main():
    running = True
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    player_pokemon = choose_starter()
    print(f"You chose {player_pokemon.name}!")

    while running:
        moving = False  # Track if the player is moving

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        move_speed = 8  # Increased movement speed
        
        # Save the old position
        old_x, old_y = player_pokemon.x, player_pokemon.y

        # Update position based on key presses
        if keys[pygame.K_LEFT]:
            player_pokemon.x -= move_speed
            moving = True
        if keys[pygame.K_RIGHT]:
            player_pokemon.x += move_speed
            moving = True
        if keys[pygame.K_UP]:
            player_pokemon.y -= move_speed
            moving = True
        if keys[pygame.K_DOWN]:
            player_pokemon.y += move_speed
            moving = True

        # Check boundaries and revert if necessary
        if player_pokemon.x < 0:
            player_pokemon.x = 0
        elif player_pokemon.x > SCREEN_WIDTH - player_pokemon.image.get_width():
            player_pokemon.x = SCREEN_WIDTH - player_pokemon.image.get_width()
        if player_pokemon.y < 0:
            player_pokemon.y = 0
        elif player_pokemon.y > SCREEN_HEIGHT - player_pokemon.image.get_height():
            player_pokemon.y = SCREEN_HEIGHT - player_pokemon.image.get_height()

        screen.fill(WHITE)
        player_pokemon.draw()
        draw_text(f"HP: {player_pokemon.hp}/{player_pokemon.max_hp}", font, BLACK, screen, 10, 10)
        pygame.display.flip()

        # Random encounter with a wild Pokémon only if moving
        if moving and random.random() < 0.005:
            wild_pokemon = encounter_wild_pokemon()
            print(f"A wild {wild_pokemon.name} appeared!")
            if not battle(player_pokemon, wild_pokemon):
                running = False

        clock.tick(30)  # Adjusted frame rate for better performance

    pygame.quit()

if __name__ == "__main__":
    main()
