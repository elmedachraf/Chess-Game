import pygame as py

class Button :
    def __init__(self,x,y,width,height,fg,bg,content,fontsize):
        self.font = py.font.Font('Styles/GothicA1-Black.ttf',fontsize)
        self.content = content
        self.x=x
        self.y=y
        self.width=width
        self.height=height

        self.fg=fg
        self.bg=bg

        self.image0=py.Surface((self.width+4,self.height+4))
        self.image0.fill('#ebc934')

        self.image=py.Surface((self.width,self.height))
        self.image.fill(self.bg)

        self.rect0 = self.image0.get_rect()
        self.rect = self.image.get_rect()


        self.rect.x = self.x
        self.rect.y = self.y

        self.rect0.x = self.x-2
        self.rect0.y = self.y-2

        self.text = self.font.render(self.content, True, self.fg)
        self.text_rect = self.text.get_rect(center=(self.width/2,self.height/2))
        self.image.blit(self.text,self.text_rect)

    def is_pressed(self,pos,pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False

    def survole (self,pos):
        if self.rect.collidepoint(pos):
            self.image.fill('#ebc934')

class ButtonIMG:
    def __init__(self, x, y, width, height, content):
        self.x=x
        self.y=y
        self.width=width
        self.height=height


        self.image = py.transform.scale(py.image.load(content).convert_alpha() , (self.width,self.height) )
        self.rect = self.image.get_rect(center=(self.width/2,self.height/2))

        self.rect.x = self.x
        self.rect.y = self.y


    def is_pressed(self,pos,pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False

class BoutonGlobal:
    def __init__(self, x, y, width, height, contenttexte, fg , contentimage,fontsize):
        self.font = py.font.Font('Styles/GothicA1-Black.ttf',fontsize)
        # Position du bouton
        self.x=x
        self.y=y
        # Dimensions du bouton
        self.width=width
        self.height=height
        # Texte à afficher
        self.contenttexte = contenttexte
        # Couleur du texte
        self.fg=fg
        # Image à afficher (cadre du bouton par exemple)
        self.image = py.transform.scale(py.image.load(contentimage).convert_alpha() , (self.height,self.height) )
        self.rect = self.image.get_rect(center=(self.width/2,self.height/2))

        self.rect.x = self.x
        self.rect.y = self.y

        self.text = self.font.render(self.contenttexte , True , self.fg)
        self.text_rect = self.text.get_rect(center=(self.width/2,self.height/2))
        self.image.blit(self.text,self.text_rect)

    def is_pressed(self,pos,pressed):
        if self.rect.collidepoint(pos):
            if pressed:
                return True
            return False
        return False


class RadioButton(py.sprite.Sprite):
    def __init__(self, x, y, w, h, fontsize, text,color):
        super().__init__()

        self.font = py.font.Font('Styles/GothicA1-Black.ttf',fontsize)
        text_surf = self.font.render(text, True, (0, 0, 0))

        self.button_image = py.Surface((w, h))
        self.button_image.fill(color)
        self.button_image.blit(text_surf, text_surf.get_rect(center = (w // 2, h // 2)))
        self.hover_image = py.Surface((w, h))
        self.hover_image.fill(color)
        self.hover_image.blit(text_surf, text_surf.get_rect(center = (w // 2, h // 2)))
        py.draw.rect(self.hover_image, (196, 196, 96), self.hover_image.get_rect(), 3)
        self.clicked_image = py.Surface((w, h))
        self.clicked_image.fill((196, 196, 96))
        self.clicked_image.blit(text_surf, text_surf.get_rect(center = (w // 2, h // 2)))
        self.image = self.button_image
        self.rect = py.Rect(x, y, w, h)
        self.clicked = False
        self.clickaction=False
        self.buttons = None

    def setRadioButtons(self, buttons):
        self.buttons = buttons

    def update(self, event_list):
        hover = self.rect.collidepoint(py.mouse.get_pos())
        for event in event_list:
            if event.type == py.MOUSEBUTTONDOWN:
                if hover and event.button == 1:
                    for rb in self.buttons:
                        rb.clicked = False
                    self.clicked = True

        self.image = self.button_image
        if self.clicked:
            self.image = self.clicked_image
        elif hover:
            self.image = self.hover_image