
#IMPORTS
import os
import arcade
import arcade.gui as agui

#GLOBAL VARS

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Plate Party"


GAME_PATH = os.path.dirname(os.path.abspath(__file__))

def get_asset_path(filename: str) -> str:
    '''Returns the path to an asset file, given its filename.'''
    return os.path.join(GAME_PATH, "assets", filename)


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
        self.background = arcade.load_texture(get_asset_path("menu_bg.png"))

        #Game Logo
        game_logo_texture = arcade.load_texture(get_asset_path("plate_party_logo.png"))
        game_logo = agui.UIImage(texture=game_logo_texture, width=330, height=300)

        # Menu Buttons
        play_button = agui.UIFlatButton(text="Play", width=175, height=30, style=self.menu_button_styling)
        settings_button = agui.UIFlatButton(text="Settings", width=175, height=30, style=self.menu_button_styling)
        credits_button = agui.UIFlatButton(text="Credits", width=175, height=30, style=self.menu_button_styling)
        quit_button = agui.UIFlatButton(text="Quit", width=175, height= 30, style=self.menu_button_styling)
       
        # Menu Button Methods
        


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



    def on_show_view(self):
        '''Runs upon showing this view'''
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)
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


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = agui.UIManager()
            #Background
        self.background = arcade.load_texture(get_asset_path("menu_bg.png"))
    
    def on_show_view(self):
        '''Runs upon showing this view'''
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)
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
