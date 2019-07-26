"""
Sprite Explosion

Simple program to show basic sprite usage.

Artwork from http://kenney.nl
Explosion graphics from http://www.explosiongenerator.com/

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.sprite_explosion
"""
import random
import arcade
import os

SPRITE_SCALING_PLAYER = 0.15
SPRITE_SCALING_COIN = 0.1
SPRITE_SCALING_LASER = 0.15
SPRITE_SCALING_TARGET = 0.15
COIN_COUNT = 50

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Stone|Paper|Scissor Game"

BULLET_SPEED = 5

EXPLOSION_TEXTURE_COUNT = 60


class Explosion(arcade.Sprite):
    """ This class creates an explosion animation """

    # Static variable that holds all the explosion textures
    explosion_textures = []

    def __init__(self, texture_list):
        super().__init__("images/hit.png")

        # Start at the first frame
        self.current_texture = 0
        self.textures = texture_list

    def update(self):

        # Update to the next frame of the animation. If we are at the end
        # of our frames, then delete this sprite.
        self.current_texture += 1
        if self.current_texture < len(self.textures):
            self.set_texture(self.current_texture)
        else:
            self.kill()


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Variables that will hold sprite lists
        self.player_list = None
        self.coin_list = None
        self.bullet_list = None
        self.explosions_list = None

        # Set up the player info
        self.player_sprite = None
        self.score = 0
        self.cpu_score = 0
        self.DRAW = 0
        self.turn = 0

        # Don't show the mouse cursor
        self.set_mouse_visible(True)

        # Pre-load the animation frames. We don't do this in the __init__
        # of the explosion sprite because it
        # takes too long and would cause the game to pause.
        self.explosion_texture_list = []

        # for i in range(EXPLOSION_TEXTURE_COUNT):
        #     # Files from http://www.explosiongenerator.com are numbered sequentially.
        #     # This code loads all of the explosion0000.png to explosion0270.png files
        #     # that are part of this explosion.
        #     texture_name = f'images/target.png'
        #     # value = arcade.load_texture(texture_name, SPRITE_SCALING_TARGET)
        #     # value.center_x = SCREEN_WIDTH -50
        #     # value.center_y =  SCREEN_HEIGHT -50

        #     self.explosion_texture_list.append(arcade.load_texture(texture_name,0.5))

        # # # Load sounds. Sounds from kenney.nl
        # # self.gun_sound = arcade.sound.load_sound("sounds/laser1.wav")
        # # self.hit_sound = arcade.sound.load_sound("sounds/phaseJump1.wav")

        # arcade.set_background_color(arcade.color.LIGHT_BLUE)

    def setup(self):

        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.explosions_list = arcade.SpriteList()
        self.logo_list = arcade.SpriteList()

        # Set up the player
        self.score = 0
        self.cpu_score = 0
        self.DRAW = 0
        self.turn = 0

        # Image 
        self.logo = arcade.Sprite('images/logo.png',0.7)
        self.logo.center_x = 425
        self.logo.center_y = 470
        self.logo_list.append(self.logo)
        self.player_sprite = arcade.Sprite("images/character.png", SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 70
        self.player_list.append(self.player_sprite)

        # Create the coins
        option_stack = ["images/paper.png","images/scissor.png","images/stone.png"]
        minusx, minusy = 180,0
        for coin_index in range(len(option_stack)):

            # Create the coin instance
            # Coin image from kenney.nl
            coin = arcade.Sprite(option_stack[coin_index], SPRITE_SCALING_COIN)

            # Position the coin
            minusx += 100
            minusy = 300    
            coin.center_x = SCREEN_WIDTH - minusx
            coin.center_y =  SCREEN_HEIGHT - minusy

            # Add the coin to the lists
            self.coin_list.append(coin)

        # Set the background color
        arcade.set_background_color(arcade.color.LIGHT_BLUE)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw all the sprites.
        
        arcade.draw_rectangle_filled(400, 500 , 800, 300, arcade.color.YELLOW)
        arcade.draw_rectangle_filled(400, 338 , 800,30, arcade.color.GREEN)
        self.logo_list.draw()
        self.coin_list.draw()
        self.bullet_list.draw()
        self.player_list.draw()
        self.explosions_list.draw()


        # Render the text
        arcade.draw_text(f"Stone   |   Scissor   |   Paper", 300, 330, arcade.color.BLACK, 18)
        arcade.draw_text(f"Your Score: {self.score}", 10, 20, arcade.color.BLACK, 14)
        arcade.draw_text(f"CPU Score: {self.cpu_score}", SCREEN_WIDTH-100, 20, arcade.color.BLACK, 14)
        arcade.draw_text(f"Draws: {self.DRAW}", SCREEN_WIDTH-450, 20, arcade.color.BLACK, 14)
        
        if self.turn == 5:
            arcade.close_window()
        
    def on_mouse_motion(self, x, y, dx, dy):
        """
        Called whenever the mouse moves.
        """
        self.player_sprite.center_x = x

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called whenever the mouse button is clicked.
        """

        # Gunshot sound
        # arcade.sound.play_sound(self.gun_sound)

        # Create a bullet
        bullet = arcade.Sprite("images/arrow.png", SPRITE_SCALING_LASER)

        # The image points to the right, and we want it to point up. So
        # rotate it.
        bullet.angle = 90

        # Give it a BULLET_SPEED
        bullet.change_y = BULLET_SPEED

        # Position the bullet
        bullet.center_x = self.player_sprite.center_x
        bullet.bottom = self.player_sprite.top

        # Add the bullet to the appropriate lists
        self.bullet_list.append(bullet)

    def update(self, delta_time):
        """ Movement and game logic """

        # Call update on bullet sprites
        self.bullet_list.update()
        self.explosions_list.update()

        # Loop through each bullet
        for bullet in self.bullet_list:

            # Check this bullet to see if it hit a coin
            hit_list = arcade.check_for_collision_with_list(bullet, self.coin_list)

            # If it did, get rid of the bullet
            if len(hit_list) > 0:
                explosion = Explosion(self.explosion_texture_list)
                explosion.center_x = hit_list[0].center_x
                explosion.center_y = hit_list[0].center_y
                self.explosions_list.append(explosion)
                bullet.kill()

            # For every coin we hit, add to the score and remove the coin
            paper = self.coin_list[0]
            scissor = self.coin_list[1]
            stone = self.coin_list[2]

            for user in hit_list:
                # coin.kill()
                CPU = random.choice(self.coin_list)
                self.turn += 1
                if user == paper:
                    if CPU == scissor:
                        self.cpu_score += 1
                    elif CPU == stone:
                        self.score += 1
                    else:
                        self.DRAW += 1
                elif user == scissor:
                    if CPU == stone:
                        self.cpu_score += 1
                    elif CPU == paper:
                        self.score += 1
                    else:
                        self.DRAW += 1
                elif user == stone:
                    if CPU == paper:
                        self.cpu_score += 1
                    elif CPU == scissor:
                        self.score += 1
                    else:
                        self.DRAW += 1
                # Hit Sound
                # arcade.sound.play_sound(self.hit_sound)

            # If the bullet flies off-screen, remove it.
            if bullet.bottom > SCREEN_HEIGHT:
                bullet.kill()


def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()