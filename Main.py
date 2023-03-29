import pygame as py
from Boutons import *
import sys
import numpy as np
from JEU import *
import numpy
import sqlite3

TaillePlateau = 400 #8*64
TailleCase = TaillePlateau//8

TailleBordure = 3*TailleCase

TailleBordDroit= 3*TailleCase

TailleBordGauche= 3*TailleCase

TailleSeparatrice = 20

BordureHaute=3*(TailleCase//2)

TailleFenetreLargeur = TaillePlateau+2*TailleBordure+TailleBordDroit+ TailleBordGauche
TailleFenetreHauteur = BordureHaute+TaillePlateau+2*TailleBordure

TailleTexte = int(TaillePlateau/20)

class Game:
    def __init__(self):
        py.init()
        self.screen = py.display.set_mode((TaillePlateau+2*TailleBordure+TailleBordDroit+ TailleBordGauche, BordureHaute+TaillePlateau+2*TailleBordure))
        self.clock=py.time.Clock()
        self.font = py.font.Font('Styles/GothicA1-Black.ttf',TailleTexte)
        self.running = True
        self.intro_background = py.transform.scale(py.image.load('Fonds/SuperChess.png'),(TaillePlateau+2*TailleBordure+TailleBordDroit+ TailleBordGauche, BordureHaute+TaillePlateau+2*TailleBordure))

        self.score_background = py.transform.scale(py.image.load('Fonds/Chess3.jpg'),(TaillePlateau+2*TailleBordure+TailleBordDroit+ TailleBordGauche, BordureHaute+TaillePlateau+2*TailleBordure))

        self.On=py.transform.scale(py.image.load('Fonds/traffic_light_green.png'),(BordureHaute//3,BordureHaute//3))

        self.Off=py.transform.scale(py.image.load('Fonds/traffic_light.png'),(BordureHaute//3,BordureHaute//3))

        self.ironman=False

        self.pause = False

        self.intro=True
        self.popup = False
        self.echec=False
        self.popup_background = py.transform.scale(py.image.load('Fonds/popbackground.jpeg.jpg'),(TaillePlateau+2*TailleBordure+TailleBordDroit+ TailleBordGauche, BordureHaute+TaillePlateau+2*TailleBordure))
        self.screenpop = py.display.set_mode((TaillePlateau+2*TailleBordure+TailleBordDroit+ TailleBordGauche, BordureHaute+TaillePlateau+2*TailleBordure))
        self.options = False
        self.scores = False
        self.difficulty_level = 2

        musiquedebase=py.mixer.music.load('Musique/Pop Goes the Weasel.mp3')
        py.mixer.music.play(-1)

    #fonction pop up
    def makepopup(self,support,coup):
        title= self.font.render('Choisissez une pièce',True,py.Color(220,200,0))
        title_rect = title.get_rect(x=TailleFenetreLargeur * 0.38 , y = TailleFenetreHauteur * 0.85)

        #popupSurf = py.Surface(TaillePlateau, TaillePlateau)
        YBoutonPromo = TailleFenetreHauteur * 0.9
        TailleTextePromo2  = int(TaillePlateau/21)

        options = [
            RadioButton(TailleFenetreLargeur * 0.23 , YBoutonPromo , TailleFenetreLargeur/10 , TailleFenetreHauteur/12 , TailleTextePromo2 , "Cavalier",(96,96,96)),
            RadioButton(TailleFenetreLargeur * 0.38 , YBoutonPromo , TailleFenetreLargeur/10 , TailleFenetreHauteur/12 , TailleTextePromo2 , "Tour",(96,96,96)),
            RadioButton(TailleFenetreLargeur * 0.53 , YBoutonPromo , TailleFenetreLargeur/10 , TailleFenetreHauteur/12 , TailleTextePromo2 , "Fou",(96,96,96)),
            RadioButton(TailleFenetreLargeur * 0.68 , YBoutonPromo , TailleFenetreLargeur/10 , TailleFenetreHauteur/12 , TailleTextePromo2 , "Dame",(96,96,96)) ]

        for rb in options:
            rb.setRadioButtons(options)


        group = py.sprite.Group(options)

        while self.popup :
            event_list = py.event.get()
            for event in event_list:
                if event.type == py.QUIT:
                    self.intro = False
                    self.running = False

            mouse_pos = py.mouse.get_pos()
            mouse_pressed = py.mouse.get_pressed()

            if options[0].clicked:
                support.plateau[coup.LigneArrivee][coup.ColArrivee]="CB"
                self.popup = False
                #py.quit()
                #exit()

            if options[1].clicked:
                support.plateau[coup.LigneArrivee][coup.ColArrivee]="TB"
                self.popup = False
                #py.quit()
                #exit()

            if options[2].clicked:
                support.plateau[coup.LigneArrivee][coup.ColArrivee]="FB"
                self.popup = False
                #py.quit()
                #exit()
            if options[3].clicked:
                support.plateau[coup.LigneArrivee][coup.ColArrivee]="DB"
                self.popup = False
                #py.quit()
                #exit()


            #self.screenpop.blit(self.popup_background, (0,0))
            self.screen.blit(title,title_rect)

            group.update(event_list)

            #self.screen.fill(0)
            group.draw(self.screen)
            py.display.flip()

            py.display.update()
            #py.display.set_caption('just pop')


    #Fin du jeu
    def echec_et_mat(self,vainqueur,score):
        if vainqueur =='Blancs' :
            title= self.font.render('Victoire !',True,py.Color(220,200,0))
            title_rect = title.get_rect(x=TailleFenetreLargeur * 0.38 , y = TailleFenetreHauteur * 0.85)
        else:
            title= self.font.render('Défaite',True,py.Color(220,200,0))
            title_rect = title.get_rect(x=TailleFenetreLargeur * 0.38 , y = TailleFenetreHauteur * 0.85)


        YBoutonPromo = TailleFenetreHauteur * 0.9
        TailleTextePromo2  = int(TaillePlateau/21)

        options = [
            RadioButton(TailleFenetreLargeur * 0.23 , YBoutonPromo , TailleFenetreLargeur/10 , TailleFenetreHauteur/12 , TailleTextePromo2 , "Cavalier",(96,96,96)),
            RadioButton(TailleFenetreLargeur * 0.38 , YBoutonPromo , TailleFenetreLargeur/10 , TailleFenetreHauteur/12 , TailleTextePromo2 , "Tour",(96,96,96)),
            RadioButton(TailleFenetreLargeur * 0.53 , YBoutonPromo , TailleFenetreLargeur/10 , TailleFenetreHauteur/12 , TailleTextePromo2 , "Fou",(96,96,96)),
            RadioButton(TailleFenetreLargeur * 0.68 , YBoutonPromo , TailleFenetreLargeur/10 , TailleFenetreHauteur/12 , TailleTextePromo2 , "Dame",(96,96,96)) ]

        for rb in options:
            rb.setRadioButtons(options)


        group = py.sprite.Group(options)

        input_box = py.Rect(100, 100, 140, 32)
        color_inactive = py.Color('lightskyblue3')
        color_active = py.Color('dodgerblue2')
        color = color_inactive
        active = False
        text = ''
        done = False

        if not self.ironman:
            score=0
        else:
            score=score*self.difficulty_level

        while not done:
            for event in py.event.get():
                if event.type == py.QUIT:
                    done = True
                if event.type == py.MOUSEBUTTONDOWN:
                    # If the user clicked on the input_box rect.
                    if input_box.collidepoint(event.pos):
                        # Toggle the active variable.
                        active = not active
                    else:
                        active = False
                    # Change the current color of the input box.
                    color = color_active if active else color_inactive
                if event.type == py.KEYDOWN:

                    if active:
                        if event.key == py.K_RETURN:
                            conn = sqlite3.connect('table.db')
                            curseur = conn.cursor()
                            curseur.execute("INSERT OR REPLACE INTO `Scores` (`Pseudo`,`Score`) VALUES (?,?)",(text,score))
                            conn.commit()
                            done=True
                            self.intro=True
                            self.intro_screen()



                        elif event.key == py.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode

            # self.screen.fill((30, 30, 30))
            # Render the current text.
            font = py.font.Font(None, 32)
            txt_surface = font.render(text, True, color)
            # Resize the box if the text is too long.
            width = max(200, txt_surface.get_width()+10)
            input_box.w = width
            # Blit the text.
            self.screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
            # Blit the input_box rect.
            py.draw.rect(self.screen, color, input_box, 2)

            py.display.flip()


    # Option screen :
    def option_screen(self):
        title= self.font.render('Choisissez votre niveau',True,py.Color(220,200,0))
        title_rect = title.get_rect(x=TailleFenetreLargeur * 0.6 , y = TailleFenetreHauteur * 0.15)

        #popupSurf = py.Surface(TaillePlateau, TaillePlateau)
        #YBoutonPromo = TailleFenetreHauteur * 0.5
        TailleTextePromo2  = int(TaillePlateau/20)

        options = [
            RadioButton(TailleFenetreLargeur * 0.6 , TailleFenetreHauteur * 0.25 , TailleFenetreLargeur/5 , TailleFenetreHauteur/10 , TailleTextePromo2 , "AMATEUR",(96,96,96)),
            RadioButton(TailleFenetreLargeur * 0.6 , TailleFenetreHauteur * 0.4 , TailleFenetreLargeur/5 , TailleFenetreHauteur/10 , TailleTextePromo2 , "INTERMÉDIAIRE",(96,96,96)),
            RadioButton(TailleFenetreLargeur * 0.6 , TailleFenetreHauteur * 0.55 , TailleFenetreLargeur/5 , TailleFenetreHauteur/10 , TailleTextePromo2 , "AVANCÉ",(96,96,96)),
            RadioButton(TailleFenetreLargeur * 0.6 , TailleFenetreHauteur * 0.7 , TailleFenetreLargeur/5 , TailleFenetreHauteur/10 , TailleTextePromo2 , "DYNAMIQUE",(96,96,96)),
            RadioButton(TailleFenetreLargeur * 0.6 , TailleFenetreHauteur * 0.85 , TailleFenetreLargeur/5 , TailleFenetreHauteur/10 , TailleTextePromo2 , "Mode Ironman",(96,96,96)) ]

        for rb in options:
            rb.setRadioButtons(options)


        group = py.sprite.Group(options)

        while self.options :
            event_list = py.event.get()
            for event in event_list:
                if event.type == py.QUIT:
                    self.intro = False
                    self.running = False

            mouse_pos = py.mouse.get_pos()
            mouse_pressed = py.mouse.get_pressed()

            if options[0].clicked:
                self.difficulty_level = 1
                self.options = False
                self.intro = True
                self.intro_screen()
                #py.quit()
                #exit()

            if options[1].clicked:
                self.difficulty_level = 2
                self.options = False
                self.intro = True
                self.intro_screen()
                #py.quit()
                #exit()

            if options[2].clicked:
                self.difficulty_level = 3
                self.options = False
                #py.quit()
                #exit()
                self.intro = True
                self.intro_screen()

            if options[3].clicked:
                self.difficulty_level = 3
                self.options = False
                #py.quit()
                #exit()
                self.intro = True
                self.intro_screen()

            if options[4].clicked:
                self.ironman = not self.ironman
                py.time.wait(75)
                options[4].clicked = False
                py.display.update()



            self.screen.blit(self.intro_background, (0,0))
            #self.screenpop.blit(self.popup_background, (0,0))
            self.screen.blit(title,title_rect)
            py.draw.rect(self.screen, py.Color(45,45,45), py.Rect(0,0,TaillePlateau+2*TailleBordure+TailleBordDroit+TailleBordGauche, BordureHaute))

            if self.ironman :
                self.screen.blit(self.On, (TaillePlateau+2*TailleBordure+TailleBordDroit+TailleBordGauche-50,BordureHaute//3))
            else :
                self.screen.blit(self.Off, (TaillePlateau+2*TailleBordure+TailleBordDroit+TailleBordGauche-50,BordureHaute//3))

            group.update(event_list)

            #self.screen.fill(0)
            group.draw(self.screen)
            py.display.flip()

            py.display.update()
            #py.display.set_caption('just pop')

    # Score screen :
    def score_screen(self):

        conn = sqlite3.connect('table.db')
        curseur = conn.cursor()
        curseur.execute("SELECT * FROM Scores_joueurs ORDER BY score DESC")
        Liste_scores=curseur.fetchall()


        largeurBoutons=100
        HauteurBoutons=63

        menu_button_score = BoutonGlobal(largeurBoutons, (BordureHaute-HauteurBoutons)//2, largeurBoutons, HauteurBoutons, '', (60,60,60) , 'Icones/Arrow.png',20)

        N=min(len(Liste_scores),10)

        Tableau=[]

        for i in range(N):
            pseudo,score=Liste_scores[i][0],Liste_scores[i][1]
            print(pseudo,score)

            textp= self.font.render('{}'.format(pseudo),True,py.Color(220,200,0))
            texts= self.font.render('{}'.format(score),True,py.Color(220,200,0))

            title_rectp = textp.get_rect(x=TailleFenetreLargeur * 0.1,y = TailleFenetreHauteur * 0.1*(i+2.5))
            title_rects = texts.get_rect(x=TailleFenetreLargeur * 0.4,y = TailleFenetreHauteur * 0.1*(i+2.5))

            Tableau.append([textp,title_rectp,texts,title_rects])


        title= self.font.render('Tableau des scores',True,py.Color(220,200,0))
        title_rect = title.get_rect(x=TailleFenetreLargeur * 0.2 , y = TailleFenetreHauteur * 0.15)

        TailleTextePromo2  = int(TaillePlateau/20)

        while self.scores :
            event_list = py.event.get()
            for event in event_list:
                if event.type == py.QUIT:
                    self.intro = False
                    self.running = False
                elif event.type==py.MOUSEBUTTONUP:
                    mouse_pos = py.mouse.get_pos()
                    if menu_button_score.rect.collidepoint(mouse_pos):
                        self.scores=False
                        self.intro=True
                        self.intro_screen()

            mouse_pos = py.mouse.get_pos()
            mouse_pressed = py.mouse.get_pressed()


            self.screen.blit(self.score_background, (0,0))
            self.screen.blit(title,title_rect)
            py.draw.rect(self.screen, py.Color(45,45,45), py.Rect(0,0,TaillePlateau+2*TailleBordure+TailleBordDroit+TailleBordGauche, BordureHaute))
            self.screen.blit(menu_button_score.image, menu_button_score.rect)

            if self.ironman :
                self.screen.blit(self.On, (TaillePlateau+2*TailleBordure+TailleBordDroit+TailleBordGauche-50,BordureHaute//3))
            else :
                self.screen.blit(self.Off, (TaillePlateau+2*TailleBordure+TailleBordDroit+TailleBordGauche-50,BordureHaute//3))

            for i in range(N):
                self.screen.blit(Tableau[i][0],Tableau[i][1])
                self.screen.blit(Tableau[i][2],Tableau[i][3])
            py.display.flip()

            py.display.update()


    def intro_screen(self):

        largeurBoutons=100
        HauteurBoutons=63
        font20 = py.font.Font('Styles/GothicA1-Black.ttf',BordureHaute//2)
        title= font20.render('SUPER CHESS',True,py.Color(220,200,0))
        title_rect = title.get_rect(x=(TaillePlateau+2*TailleBordure+TailleBordDroit+TailleBordGauche)*0.37,y=BordureHaute//3)

        sound_button0 = BoutonGlobal(TaillePlateau+2*TailleBordure+TailleBordDroit-2*largeurBoutons+TailleBordGauche, (BordureHaute-HauteurBoutons)//2, largeurBoutons, HauteurBoutons, '', (60,60,60) , 'Icones/MutedSpeaker.png',20)

        sound_button_m0 = BoutonGlobal(TaillePlateau+2*TailleBordure+TailleBordDroit-2*largeurBoutons+TailleBordGauche, (BordureHaute-HauteurBoutons)//2, largeurBoutons, HauteurBoutons, '', (60,60,60) , 'Icones/Speaker.png',20)

        # font20 = py.font.Font('Styles/GothicA1-Black.ttf',20)
        # ironman= font20.render('Ironman',True,py.Color(220,200,0))
        # ironman_rect = ironman.get_rect(x=(TaillePlateau+2*TailleBordure+TailleBordDroit+TailleBordGauche)*0.95,y=BordureHaute//5)


        play_button = Button(600,200,100,62.5,"WHITE",(60, 60, 60),'Jouer',20)

        option_button = Button(600,300,100,62.5,"WHITE",(60, 60, 60),'Options',20)

        quit_button = Button(600,400,100,62.5,"WHITE",(60, 60, 60),'Quitter',20)


        #----------------------radiobuttons-------------------------
        Buttons = [
    RadioButton(700,150,150,85, 32, "Jouer",(96,96,96)),
    RadioButton(700,275,150,85, 32, "Options",(86,86,86)),
    RadioButton(700,400,150,85, 32, "Scores",(86,86,86)),
    RadioButton(700,525,150,85, 32, "Quitter",(76,76,76))]

        for rb in Buttons:
            rb.setRadioButtons(Buttons)
        #Buttons[0].clicked = True

        group = py.sprite.Group(Buttons)

        #----------------------------------------------------------
        while self.intro:
            event_list = py.event.get()
            for event in event_list:
                if event.type == py.QUIT:
                    self.intro = False
                    self.running = False

                elif event.type==py.MOUSEBUTTONUP:
                    mouse_pos = py.mouse.get_pos()
                    if sound_button0.rect.collidepoint(mouse_pos):
                        if self.pause==True:
                            py.mixer.music.play(-1)
                            self.pause=False
                        elif self.pause==False:
                            py.mixer.music.pause()
                            self.pause=True

            mouse_pos = py.mouse.get_pos()
            mouse_pressed = py.mouse.get_pressed()


            if Buttons[0].clicked:
                self.intro = False

            if Buttons[1].clicked:
                self.intro = False
                self.options = True
                self.option_screen()

            if Buttons[2].clicked:
                self.intro = False
                self.scores = True
                self.score_screen()

            if Buttons[3].clicked:
                #self.intro = False
                #self.running = False
                py.quit()
                exit()


            self.screen.blit(self.intro_background, (0,0))

            py.draw.rect(self.screen, py.Color(45,45,45), py.Rect(0,0,TaillePlateau+2*TailleBordure+TailleBordDroit+TailleBordGauche, BordureHaute))

            self.screen.blit(title,title_rect)

            # self.screen.blit(ironman,ironman_rect)

            if self.ironman :
                self.screen.blit(self.On, (TaillePlateau+2*TailleBordure+TailleBordDroit+TailleBordGauche-50,BordureHaute//3))
            else :
                self.screen.blit(self.Off, (TaillePlateau+2*TailleBordure+TailleBordDroit+TailleBordGauche-50,BordureHaute//3))

            #self.screen.blit(option_button.image0, option_button.rect0)
            #self.screen.blit(option_button.image, option_button.rect)

            #self.screen.blit(play_button.image0, play_button.rect0)
            #self.screen.blit(play_button.image, play_button.rect)

            #self.screen.blit(quit_button.image0, quit_button.rect0)
            #self.screen.blit(quit_button.image, quit_button.rect)

            if self.pause:
                self.screen.blit(sound_button0.image, sound_button0.rect)
            else:
                self.screen.blit(sound_button_m0.image, sound_button_m0.rect)

            group.update(event_list)

            #self.screen.fill(0)
            group.draw(self.screen)
            py.display.flip()

            py.display.update()
            py.display.set_caption('SuperChess')

if __name__=="__main__":
    g=Game()
    while g.running:
        if g.intro:
            g.intro_screen()
        if g.intro or Partie(g):
            g.intro=True
            g.intro_screen()
        else:
            Partie(g)

    py.quit()
    exit()
