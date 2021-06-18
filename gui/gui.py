import pygame, sys



class ToolBar:
    menubar_clicked = False
    menu_bar_buttons = list()
    tool_names = {"File": 0, "Layers": 1, "About": 2}
    tool_index = -1

    def __init__(self, screen):
        self.x = 0
        self.y = 0
        self.w = screen.get_width()
        self.h = 20
        self.screen = screen

        self.file_tool = ToolBarDropDown("File", 0, 0, 40, 20)
        self.file_tool.add_button("New", 20)
        self.file_tool.add_button("Save", 40)
        self.file_tool.add_button("Load", 60)

        self.layer_tool = ToolBarDropDown("Layers", 40, 0, 40, 20)
        self.layer_tool.add_button("Interactive", 20)
        self.layer_tool.add_button("Foreground", 40)
        self.layer_tool.add_button("Background", 60)
        self.layer_tool.add_button("Background", 80)

        self.about_tool = ToolBarDropDown("About", 80, 0, 40, 20)
        self.about_tool.add_button("Contact", 20)

        ToolBar.menu_bar_buttons = (self.file_tool, self.layer_tool, self.about_tool)


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



class ToolBarDropDown:
    def __init__(self, name, x, y, width, height):
        self.name = name
        self.x = x
        self.y = y
        self.clicked = False
        self.hovered = False
        self.header_btn = pygame.Rect(x, y, width, height)
        self.btn_list = list()
        self.outside_click = False

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
            pygame.draw.rect(screen, (0, 255, 0), self.header_btn)
        else:
            pygame.draw.rect(screen, (255, 0, 0), self.header_btn)


    def add_button(self, name, y):
        self.btn_list.append(Button(name, self.x, y, self))


class Button:
    def __init__(self, text, x, y, tool, col=(255, 255, 255), w=100, h=20, action=lambda: print("Hola soy boton")):
        self.text = text
        self.col = col
        self.rect = pygame.Rect(x, y, w, h)
        self.action = action
        self.tool = tool

    def draw(self, screen):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            pygame.draw.rect(screen, (0, 0, 255), self.rect)
            mx = pygame.mouse.get_pressed()[0]
            if mx:
                ToolBar.menubar_clicked = False
                self.tool.clicked = False
                self.tool.hovered = False
                self.action()
        else:
            pygame.draw.rect(screen, self.col, self.rect)


    def set_action(self, action):
        self.action = action