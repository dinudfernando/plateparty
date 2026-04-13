
#IMPORTS
import os
import arcade
import arcade.gui as agui
import random

#GLOBAL VARS

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Plate Party"


GAME_PATH = os.path.dirname(os.path.abspath(__file__))

def get_asset_path(filename: str) -> str:
    '''Returns the path to an asset file, given its filename.'''
    return os.path.join(GAME_PATH, "assets", filename)

class GameView(arcade.View):
    
    def __init__(self):
        super().__init__()

        self.manager = agui.UIManager()
        self.background = arcade.load_texture(get_asset_path("bg.png"))

        #Cracked & Stacked Plates
        self.cracked_plate_list = arcade.SpriteList()
        self.caught_plates = 0
        self.stacked_plate_list = arcade.SpriteList()

        # Physics and Wind Variables
        self.stack_offset = 0
        self.stack_velocity = 0
        self.balance_limit = 60
        self.game_over = False

        self.wind_force = 0
        self.wind_timer = 0

        self.spawn_timer = 0
        self.spawn_delay = 1.0

        #Textures: Croissant & Settings icons
        croissant_texture = arcade.load_texture(get_asset_path("croissant.png"))
        settings_icon = arcade.load_texture(get_asset_path("settings_icon.png"))
        settings_icon_dark = arcade.load_texture(get_asset_path("settings_icon_dark.png"))
        self.croissant_icon = agui.UIImage(texture=croissant_texture, width=64, height=64)
        self.croissant_label = agui.UILabel(
            text=f"X {self.caught_plates}",
            font_size=18,
            font_name="Press Start 2P",
            text_color=arcade.color.WHITE
        )

        # Icon & Label to a layout
        layout_left = agui.UIBoxLayout(vertical=False, space_between=8)
        layout_left.add(self.croissant_icon)
        layout_left.add(self.croissant_label)

        self.settings_button = agui.UITextureButton(
            texture=settings_icon,
            texture_hovered=settings_icon_dark,
            width=64,
            height=64
        )
        self.settings_button.on_click = self.on_click_settings


        # Anchoring to UI Manager
        anchor = agui.UIAnchorLayout()
        anchor.add(child=layout_left, anchor_x="left", anchor_y="top", align_x=0, align_y=0)
        anchor.add(child=self.settings_button, anchor_x="right", anchor_y="top", align_x=0, align_y=0)
        self.manager.add(anchor)

        # Pete Sprite
        self.pete_list = arcade.SpriteList()
        self.pete = arcade.Sprite(get_asset_path("pete_neutral.png"), scale=0.3)
        self.pete.center_x = self.window.width//2 
        self.ground_y = int(self.window.height*0.39)
        self.pete.bottom = self.ground_y
        self.pete_list.append(self.pete)
        self.movement_speed = 5


        self.plate_list = arcade.SpriteList()
        self.plate_speed_x, self.plate_speed_y = 4, -2


    def on_click_settings(self, event):
        print("settings opened")

    def close_settings(self, event):
        print("settings closed")


    def on_show_view(self):
        '''Runs upon showing this view'''
        self.manager.enable()

    def on_hide_view(self):
        '''Runs upon hiding this view'''
        self.manager.disable()

    def on_draw(self):
        '''Runs every time the screen is rendered'''
        self.clear()

        arcade.draw_texture_rect(
            self.background,
            rect=arcade.LBWH(0, 0, self.window.width, self.window.height)
        )
        self.cracked_plate_list.draw()
        self.plate_list.draw()
        self.pete_list.draw()
        self.stacked_plate_list.draw()
        self.manager.draw()

        balance_ratio = min(abs(self.stack_offset)/ self.balance_limit, 1)

        arcade.draw_lrbt_rectangle_filled(40, 240, 80, 60, arcade.color.DARK_BLUE_GRAY)
        arcade.draw_lrbt_rectangle_filled(
            40,
            40 + (200 * balance_ratio),
            80,
            60,
            arcade.color.RED_ORANGE
        )
        arcade.draw_text("BALANCE", 40, 90, arcade.color.WHITE, 14)
        arcade.draw_text(f"WIND: {self.wind_force:.2f}", 40, 35, arcade.color.WHITE, 14)

        if self.game_over:
            arcade.draw_text(
                "GAME OVER",
                self.window.width/2,
                self.window.height/2,
                arcade.color.WHITE,
                32,
                anchor_x="center"
            )

            arcade.draw_text(
                "Press R to restart",
                self.window.width/2,
                self.window.height/2 - 40,
                arcade.color.WHITE,
                18,
                anchor_x="center"
            )

    def on_update(self, delta):
        if self.game_over:
            return
        
        
        self.pete_list.update()
        self.plate_list.update()

        hit_list = arcade.check_for_collision_with_list(self.pete, self.plate_list)
        wind_strength = min(0.4 + self.caught_plates * 0.03, 1.2)

        self.wind_timer += delta
        if self.wind_timer > 2:
            self.wind_timer = 0
            wind_strength = min(0.4 + self.caught_plates * 0.03, 1.2)
            self.wind_force = random.uniform(-wind_strength, wind_strength)
        
        self.stack_velocity += self.wind_force
         
        for plate in hit_list:
            plate.remove_from_sprite_lists()
            self.caught_plates += 1
            self.croissant_label.text = f"X {self.caught_plates}"

            stacked_plate = arcade.Sprite(get_asset_path("plate.png"), scale=0.2)
            self.stacked_plate_list.append(stacked_plate)

        if len(self.plate_list) == 0:
            self.spawn_timer += delta
            if self.spawn_timer >= self.spawn_delay:
                self.spawn_plate()
                self.spawn_timer = 0
        else:
            self.spawn_timer = 0
        
        if len(self.cracked_plate_list) > 10:
            self.cracked_plate_list.pop(0)

        # Movement Bounds for Plates
        for plate in self.plate_list:
            if plate.bottom <= self.ground_y:
                x = plate.center_x
                plate.remove_from_sprite_lists()

                cracked = arcade.Sprite(get_asset_path("cracked_plate.png"), scale=0.2)
                cracked.center_x = x
                cracked.bottom = self.ground_y
                self.cracked_plate_list.append(cracked)
            
        #Movement Bounds for Pete
        if self.pete.left <0:
            self.pete.left = 0
        if self.pete.right > self.window.width:
            self.pete.right = self.window.width

        if self.pete.change_x != 0:
            self.stack_velocity += self.pete.change_x * 0.015 * max(1,len(self.stacked_plate_list))

        # Plate stacl physics        
        self.stack_velocity *= 0.9
        self.stack_offset += self.stack_velocity
        self.stack_offset *= 0.96

        for i, plate in enumerate(self.stacked_plate_list):
            lean_factor = (i + 1) / max(1, len(self.stacked_plate_list))
            plate.center_x = self.pete.center_x + self.stack_offset * lean_factor
            plate.bottom = self.pete.top + 6 + (i*10)

        if abs(self.stack_offset) > self.balance_limit:
            self.game_over = True
            self.pete.change_x = 0
            self.spill_stack()
        




    def on_key_press(self, key, modifiers):
        if self.game_over and key == arcade.key.R:
            self.window.show_view(GameView())
            return
        #Key Movement
        if key in (arcade.key.LEFT, arcade.key.A):
            self.pete.change_x = -1*(self.movement_speed)
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.pete.change_x = self.movement_speed
    
    def on_key_release(self, key, modifiers):
        #To make sure sprite stops
        if key in (arcade.key.LEFT, arcade.key.A, arcade.key.RIGHT, arcade.key.D):
            self.pete.change_x = 0

    #Plate Mechanics
    def spawn_plate(self):
        if len(self.plate_list) > 0:
            return
        
        speed_bonus = min(self.caught_plates * 0.2, 4)
        vertical_bonus = min(self.caught_plates * 0.1, 2)

        plate = arcade.Sprite(get_asset_path("plate.png"), scale=0.2)

        from_left_side = random.choice([True,False])
        if from_left_side:
            plate.center_x = -50
            plate.change_x = self.plate_speed_x
        else:
            plate.center_x = self.window.width + 50
            plate.change_x = -self.plate_speed_x
        
        plate.center_y = self.window.height - 120
        plate.change_y = self.plate_speed_y
        
        self.plate_list.append(plate)

    def spill_stack(self):
        for plate in self.stacked_plate_list:
                cracked = arcade.Sprite(get_asset_path("cracked_plate.png"), scale=0.2)
                cracked.center_x = plate.center_x
                cracked.bottom = self.ground_y
                self.cracked_plate_list.append(cracked)

        self.stacked_plate_list.clear()


class MainMenuUI(arcade.View):
    '''Main Menu for the game.'''
    arcade.load_font(get_asset_path("PressStart2P-Regular.ttf"))

    # Menu Styles
    menu_button_styling = {
        "normal": agui.UIFlatButton.UIStyle(
            font_size=15,
            font_name="Press Start 2P",
            font_color= arcade.color.WHITE,
            bg=arcade.color.GRAY_BLUE,

        ),
        "hover": agui.UIFlatButton.UIStyle(
            font_size=15,
            font_name="Press Start 2P",
            font_color= arcade.color.WHITE,
            bg=arcade.color.BLUE_GRAY,
        ),
        "press": agui.UIFlatButton.UIStyle(
            font_size=15,
            font_name="Press Start 2P",
            font_color= arcade.color.LIGHT_GRAY,
            bg=arcade.color.PRUSSIAN_BLUE,

        ),
        "disabled": agui.UIFlatButton.UIStyle(
            font_size=15,
            font_name="Press Start 2P",
            font_color= arcade.color.GRAY,
            bg=arcade.color.DARK_SLATE_GRAY,

        )
    }


    def __init__(self):
        super().__init__()
        
        # Initialize Arcade UI Manager as self.manager
        self.manager = agui.UIManager()
        self.manager.enable()


        # Vertical Box Layout 
        self.v_box = agui.UIBoxLayout(space_between=10)

        #Background
        self.background = arcade.load_texture(get_asset_path("bg.png"))

        #Game Logo
        game_logo_texture = arcade.load_texture(get_asset_path("plate_party_logo.png"))
        game_logo = agui.UIImage(texture=game_logo_texture, width=330, height=300)

        # Menu Buttons
        play_button = agui.UIFlatButton(text="Play", width=175, height=30, style=self.menu_button_styling)
        settings_button = agui.UIFlatButton(text="Settings", width=175, height=30, style=self.menu_button_styling)
        credits_button = agui.UIFlatButton(text="Credits", width=175, height=30, style=self.menu_button_styling)
        quit_button = agui.UIFlatButton(text="Quit", width=175, height= 30, style=self.menu_button_styling) 

        play_button.on_click = self.on_click_play
        quit_button.on_click = self.on_click_quit

        self.v_box.add(game_logo.with_padding(bottom=30))
        self.v_box.add(play_button)
        self.v_box.add(settings_button)
        self.v_box.add(credits_button)
        self.v_box.add(quit_button)

        anchor = agui.UIAnchorLayout()
        anchor.add(
            child=self.v_box,
            anchor_x="center_x",
            anchor_y="center_y",
            )
        self.manager.add(anchor)

        # Menu Button Methods

    def on_click_play(self, event):
        game_view = GameView()
        self.window.show_view(game_view)

    def on_click_quit(self, event):
        arcade.exit()

    def on_show_view(self):
        '''Runs upon showing this view'''
        self.manager.enable()

    def on_hide_view(self):
        '''Runs upon hiding this view'''
        self.manager.disable()

    def on_draw(self):
        '''Runs every time the screen is rendered'''
        self.clear()

        arcade.draw_texture_rect(
            self.background,
            rect=arcade.LBWH(0, 0, self.window.width, self.window.height)
        )

        self.manager.draw()



def main():
    window = arcade.Window(SCREEN_WIDTH,SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)
    menu = MainMenuUI()
    window.show_view(menu)
    arcade.run()


if __name__ == "__main__":
    main()
