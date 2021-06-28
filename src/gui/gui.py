import pygame, sys
import abc
sys.path.append('..')
from data.paths import *
from PIL import ImageFont
from tile_engine import tile_indexes, tile_size


BORDER_COLOR = (130, 135, 144)
WHITE = (255, 255, 255)
"""
	TODO: Document
	Added text to buttons. I will not treat the header_btn of the dropdown
	as a Button object but rather as a pygame.Rect and some basic functionality
	
	Remove colors.
	Blend hover color with text.
	Add real function calls. For this to happen ToolBar should probably somehow knows the state of the level editor at all times.
"""

# define font
pygame.init()
font = pygame.font.Font(MAIN_LEVEL_EDITOR_FONT, 14)

cache_fonts = {}

# function for outputting text onto the screen
def draw_text(screen, text, font, text_col, rect, center=True):
    if cache_fonts.get(text) == None:
        img = font.render(text, True, text_col)
        cache_fonts[text] = img
    
    text = cache_fonts[text]
    if center:
        screen.blit(text, text.get_rect(center=rect.center))
    else:
        screen.blit(text, rect)


def draw_text2(screen, text, font, text_col, x,y, center=True):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))
    return img.get_rect()


class ToolBar:
    menubar_clicked = False
    menu_bar_buttons = list()
    tool_names = {"File": 0, "Edit": 1, "Layers": 2, "Help": 3}
    tool_index = -1

    def __init__(self, screen):
        self.x = 0
        self.y = 0
        self.w = screen.get_width()
        self.h = 20
        self.screen = screen

        self.file_tool = ToolBarDropDown("File", 0, 0, 40, 20)
        self.file_tool.add_button("New", 20) #here should add the function
        self.file_tool.add_button("Save", 40)
        self.file_tool.add_button("Load", 60)
        self.edit_tool = ToolBarDropDown("Edit", 40, 0, 60, 20)
        self.edit_tool.add_button("Clear", 20)

        self.layer_tool = ToolBarDropDown("Layers", 100, 0, 55, 20)
        self.layer_tool.add_button("Interactive", 20)
        self.layer_tool.add_button("Foreground", 40)
        self.layer_tool.add_button("Background", 60)


        self.about_tool = ToolBarDropDown("Help", 155, 0, 55, 20)
        self.about_tool.add_button("About", 20)

        ToolBar.menu_bar_buttons = (self.file_tool,self.edit_tool, self.layer_tool,  self.about_tool)


    def draw(self):
        pygame.draw.rect(self.screen, (255, 255, 255), (self.x, self.y, self.w, self.h))

        for i, tool in enumerate(self.menu_bar_buttons):
            tool.draw(self.screen)

        for i, tool in enumerate(self.menu_bar_buttons):
            if ToolBar.menubar_clicked and i == ToolBar.tool_index:
                tool.drawDropDown(self.screen)

        outside_clicks = 0
        for tool in self.menu_bar_buttons:
            tool.update()
            if tool.outside_click:
                outside_clicks+=1


        if outside_clicks == len(self.menu_bar_buttons):
            ToolBar.menubar_clicked = False
            ToolBar.tool_index = -1
            ToolBar.disable_btn()

    @staticmethod
    def disable_btn(index=-1):
        for i, tool in enumerate(ToolBar.menu_bar_buttons):
            if i != index:
                tool.clicked = False
                tool.hovered = False

    @staticmethod
    def get_button(text):
        for tool in ToolBar.menu_bar_buttons:
            for btn in tool.btn_list:
                if btn.text == text:
                    return btn



class ToolBarDropDown:
    def __init__(self, name, x, y, width, height, hidden=False):
        self.name = name
        self.x = x
        self.y = y
        self.col = (255, 255, 255)
        self.hovered_col = (209, 235, 247)
        self.clicked = False
        self.hovered = False
        self.header_btn = pygame.Rect(x, y, width, height)
        self.btn_list = list()
        self.outside_click = False
        self.hidden = hidden

    def update(self):
        pos = pygame.mouse.get_pos()
        mx = pygame.mouse.get_pressed()[0]

        if self.header_btn.collidepoint(pos):
            if not ToolBar.menubar_clicked:
                if not mx:
                    self.hovered = True
                    ToolBar.disable_btn(ToolBar.tool_names[self.name])
                else:
                    ToolBar.menubar_clicked = True
                    ToolBar.tool_index = ToolBar.tool_names[self.name]
                    self.hovered = True
                    self.clicked = True
                    ToolBar.disable_btn(ToolBar.tool_names[self.name])

            else:
                if not mx:
                    self.hovered = True
                    ToolBar.tool_index = ToolBar.tool_names[self.name]
                    ToolBar.disable_btn(ToolBar.tool_names[self.name])

        else:
            if mx:
                self.outside_click = True
            else:
                if not ToolBar.menubar_clicked:
                    self.hovered = False
                self.outside_click = False


    def drawDropDown(self,screen):
        if ToolBar.menubar_clicked and ToolBar.tool_index == ToolBar.tool_names[self.name]:
            for btn in self.btn_list:
                btn.draw(screen)



    def draw(self, screen):
        if self.hovered:
            pygame.draw.rect(screen, self.hovered_col, self.header_btn)
        else:
            pygame.draw.rect(screen, self.col, self.header_btn)

        if not self.hidden:
            draw_text(screen, self.name, font, (0,0,0), self.header_btn)


    def add_button(self, name, y):
        self.btn_list.append(ToolBarButton(name, self.x, y, self))




class Button(metaclass=abc.ABCMeta):
    def __init__(self, text, x, y, col=(250,250,250), hovered_col=(173, 216, 230), w=110, h=20, action=lambda: print("Hola soy boton")):
        self.text = text
        self.col = col
        self.hovered_col = hovered_col
        self.rect = pygame.Rect(x, y, w, h)
        self.action = action

    @abc.abstractmethod
    def draw(self, screen):
        pass

    def set_action(self, action):
        self.action = action



class ToolBarButton(Button):
    def __init__(self, text, x, y, tool, col=(250, 250, 250), hovered_col=(173, 216, 230), w=110, h=20, action=lambda: print("Hola soy boton")):
        super().__init__(text, x, y, col, hovered_col, w, h, action)
        self.tool = tool

    def draw(self, screen):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            pygame.draw.rect(screen, self.hovered_col, self.rect)
            mx = pygame.mouse.get_pressed()[0]
            if mx:
                ToolBar.menubar_clicked = False
                self.tool.clicked = False
                self.tool.hovered = False
                self.action()
        else:
            pygame.draw.rect(screen, self.col, self.rect)
        draw_text(screen, self.text, font, (0,0,0), self.rect)


class Group:
    def __init__(self, text, x, y, width, height):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.radio_buttons = []
        self.radio_buttons_actives = {}

    def add_radiobutton(self, text, dx, dy, r):
        f = ImageFont.truetype(MAIN_LEVEL_EDITOR_FONT, 14)
        size = f.getsize(text)
        self.radio_buttons.append(RadioButton(text, self.x + dx, self.y + dy, r, self, w = size[0] + r * 2 + 10))
        self.radio_buttons_actives[text] = False

    def set_active(self, text):
        for btn in self.radio_buttons:
            if btn.text == text:
                self.radio_buttons_actives[text] = True
            else:
                self.radio_buttons_actives[btn.text] = False


    def draw_group_label(self, screen):
        rect = pygame.Rect(self.x,self.y,self.width,self.height)
        self.draw_group_label_container(screen,  rect)

        for btn in self.radio_buttons:
            btn.draw(screen)  


    def draw_group_label_container(self, screen, rect):
        text_rect = draw_text2(screen, self.text, font, (0,0,0), rect.x + 20, rect.y - 9)
        f = ImageFont.truetype(MAIN_LEVEL_EDITOR_FONT, 14)
        size = f.getsize(self.text)
        pygame.draw.line(screen, BORDER_COLOR, (rect.x, rect.y), (rect.x + 15, rect.y))
        pygame.draw.line(screen, BORDER_COLOR, (rect.x + 20 + size[0] + 5, rect.y), (rect.x + rect.width, rect.y))

        pygame.draw.line(screen, BORDER_COLOR, (rect.x + rect.width, rect.y), (rect.x + rect.width, rect.y + rect.height))
        pygame.draw.line(screen, BORDER_COLOR, (rect.x + rect.width, rect.y + rect.height), (rect.x, rect.y + rect.height))
        pygame.draw.line(screen, BORDER_COLOR, (rect.x, rect.y + rect.height), (rect.x, rect.y))




class RadioButton(Button):
    def __init__(self, text, x, y, r, group, col=(255, 255, 255), hovered_col=(173, 216, 230), w=130, h=20):
        super().__init__( text, x, y, col, hovered_col, w, h)
        self.r = r
        self.group = group
        self.circle = (self.rect.x + self.r, self.rect.y + self.r)
        self.aux = pygame.Rect(self.rect.x, self.rect.y, self.r, self.r)


    def draw(self, screen):
        if self.active():
            pygame.draw.circle(screen, (0,0,150), self.circle, self.r - 3)
            pygame.draw.circle(screen, BORDER_COLOR, self.circle, self.r , 1)
        else:
            pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(pos):
                pygame.draw.circle(screen, self.hovered_col, self.circle, self.r - 1)
                pygame.draw.circle(screen, BORDER_COLOR, self.circle, self.r , 1)
                mx = pygame.mouse.get_pressed()[0]
                if mx:
                    self.group.set_active(self.text)
            else:
                pygame.draw.circle(screen, WHITE, self.circle, self.r - 1)
                pygame.draw.circle(screen, BORDER_COLOR, self.circle, self.r , 1)
        draw_text2(screen, self.text, font, (0,0,0), self.rect.x + 20, self.rect.y)



    def active(self):
        return self.group.radio_buttons_actives[self.text] == True



class ListView:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.tileset = []
        self._init_tileset()
        self.clicked_tile_index = 2


    def _init_tileset(self):
        dx = 16
        dy = 16
        increment = 35 
        for tile in tile_indexes:
            tile_img = tile_indexes[tile]
            self.tileset.append(TileButton(self.x + dx, self.y + dy, tile_img, tile, self))
            dx += increment
            if dx + increment >= self.width:
                dy += increment
                dx = 0



    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, (self.rect.x-1, self.rect.y-1, self.rect.width-1, self.rect.height-1))
        pygame.draw.rect(screen, BORDER_COLOR, self.rect, 1)
        self._draw_tileset(screen)



    def _draw_tileset(self, screen):
        for tile_btn in self.tileset:
            tile_btn.draw(screen)

    def check(self):
        index = self.clicked_tile_index
        for tile_btn in self.tileset:
            index = tile_btn.check()
            if index != -1:
                self.clicked_tile_index = index

        if index != -1:
            return index
        else:
            return self.clicked_tile_index


            

class TileButton:
    def __init__(self, x, y, img, tile_index, listview, clicked_col=(255, 105, 108), hovered_col=(255, 140, 105)):
        self.x = x
        self.y = y
        self.img = pygame.transform.scale(img, (32, 32))
        self.w = self.img.get_width()
        self.h = self.img.get_height()
        self.clicked_col = clicked_col
        self.hovered_col = hovered_col
        self.rect = pygame.Rect(x, y, self.w, self.h)
        self.clicked = False
        self.tile_index = tile_index
        self.listview = listview

    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y, self.w, self.h))
        pos = pygame.mouse.get_pos()
        mx = pygame.mouse.get_pressed()[0]
        if self.rect.collidepoint(pos):
            pygame.draw.rect(screen, self.hovered_col, (self.x, self.y, self.w, self.h), 2)
        if self.listview.clicked_tile_index == self.tile_index:
            pygame.draw.rect(screen, self.clicked_col, self.rect, 3)


    def check(self):
        pos = pygame.mouse.get_pos()
        mx = pygame.mouse.get_pressed()[0]
        if self.rect.collidepoint(pos):
            if mx:
                return self.tile_index 
        return -1

