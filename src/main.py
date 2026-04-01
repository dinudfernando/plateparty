
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
        self.croissant_count = 0

        #Textures: Croissant & Settings icons
        croissant_texture = arcade.load_texture(get_asset_path("croissant.png"))
        settings_icon = arcade.load_texture(get_asset_path("settings_icon.png"))
        settings_icon_dark = arcade.load_texture(get_asset_path("settings_icon_dark.png"))
        self.croissant_icon = agui.UIImage(texture=croissant_texture, width=64, height=64)
        self.croissant_label = agui.UILabel(
            text=f"X {self.croissant_count}",
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
        self.pete = arcade.Sprite(get_asset_path(get_asset_path("pete_neutral.png")), scale=0.3)
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
        self.pete_list.draw()
        self.plate_list.draw()
        self.manager.draw()

    def on_update(self, delta):
        self.pete_list.update()
    
    #Movement Bounds
        if self.pete.left <0:
            self.pete.left = 0
        if self.pete.right > self.window.width:
            self.pete.right = self.window.width
    

    def on_key_press(self, key, modifiers):
        #Key Movement
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.pete.change_x = -1*(self.movement_speed)
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.pete.change_x = self.movement_speed
    
    def on_key_release(self, key, modifiers):
        #To make sure sprite stops
        if key in (arcade.key.LEFT, arcade.key.A, arcade.key.RIGHT, arcade.key.D):
            self.pete.change_x = 0

    #Plate Mechanics
    def spawn_plate(self):
        if len(self.plate_list) > 0:
            return
        
        plate = arcade.Sprite(get_asset_path("plate.png"), scale=0.2)
        from_left_side = random.choice([True,False])
        if from_left_side:
            plate.center_x = -50
            plate.change_x = self.plate_speed_x
        else:
            plate.center_x = self.window.width + 50
            plate.center_x = self.plate_speed_x
        
        plate.center_y = self.window.height - 120
        plate.change_y = self.plate_speed_y
        
        self.plate_list.append(plate)



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
