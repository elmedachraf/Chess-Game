import pygame as py
import numpy as np
import cv2
import copy

from Boutons import *
from solution_profondeurBIS import elagage
from minimax_classes import positions_atteignables_legales
from minimax_classes import deplacement
from minimax_classes import piece_mangeable
from Main import *

"""
Contient les informations sur l'état actuel du jeu (plateau, pièces, coups autorisés ou non...
"""

class Plateau:
    def __init__(self):
        self.plateau = [
        ["TN","CN","FN","DN","RN","FN","CN","TN"],
        ["PN","PN","PN","PN","PN","PN","PN","PN"],
        ["XX","XX","XX","XX","XX","XX","XX","XX"],
        ["XX","XX","XX","XX","XX","XX","XX","XX"],
        ["XX","XX","XX","XX","XX","XX","XX","XX"],
        ["XX","XX","XX","XX","XX","XX","XX","XX"],
        ["PB","PB","PB","PB","PB","PB","PB","PB"],
        ["TB","CB","FB","DB","RB","FB","CB","TB"],
        ]
        self.TourBlanc = True  #c'est le tour du blanc
        self.coupLog=[]

        self.piecemangees=[]

        self.score=[1,1]

        self.roqueND=True
        self.roqueNG=True
        self.roqueBD=True
        self.roqueBG=True

        self.pause=True

        self.PP = []

    # Undo The last move
    def undoMove(self,g):
        if not g.ironman :
            if len(self.coupLog) != 0 :             #check if there is a move to undo
                if self.TourBlanc :
                    coupIA = self.coupLog.pop()
                    coupJoueur = self.coupLog.pop()

                    self.plateau[coupIA.LigneDepart][coupIA.ColDepart] = coupIA.piececoup
                    self.plateau[coupIA.LigneArrivee][coupIA.ColArrivee] = coupIA.pieceCapturee

                    self.plateau[coupJoueur.LigneDepart][coupJoueur.ColDepart] = coupJoueur.piececoup
                    self.plateau[coupJoueur.LigneArrivee][coupJoueur.ColArrivee] = coupJoueur.pieceCapturee

                    #self.whiteToMove = not self.whiteToMove

                else :
                    coupJoueur = self.coupLog.pop()
                    self.plateau[coupJoueur.LigneDepart][coupJoueur.ColDepart] = coupJoueur.piececoup
                    self.plateau[coupJoueur.LigneArrivee][coupJoueur.ColArrivee] = coupJoueur.pieceCapturee
                    self.TourBlanc = not self.TourBlanc                     #switch turns (coup.LigneArrivee,coup.ColArrivee)

                """
                if move.pieceMoved == 'KB' :                                                #actualiser la position du roi
                    self.whiteKingLocation = (move.startRow , move.startCol)
                elif move.pieceMoved == 'KN' :
                    self.blackKingLocation = (move.startRow , move.startCol)            """

    def FaireCoup(self,coup,g,support):
        L=[0,1,2,3,4,5,6,7]
        coupSpecial=False
        couleur='noir'
        if not self.TourBlanc:
            py.time.wait(1000)
            couleur='blanc'

        effetsonore=py.mixer.Sound('Musique/effet1.mp3')
        effetsonore.play()

        #Pieces mangées et score
        piecemangee=self.plateau[coup.LigneArrivee][coup.ColArrivee]
        if piecemangee !='XX':
            self.piecemangees.append(piecemangee)

        if len(self.piecemangees)!=0:
            sb=0
            sn=0
            for k in self.piecemangees:
                if k[1]=='N':
                    if k[0]=='D': sn+=10
                    if k[0]=='T': sn+=5
                    if k[0]=='F': sn+=3
                    if k[0]=='C': sn+=3
                    if k[0]=='P': sn+=1
                if k[1]=='B':
                    if k[0]=='D': sb+=10
                    if k[0]=='T': sb+=5
                    if k[0]=='F': sb+=3
                    if k[0]=='C': sb+=3
                    if k[0]=='P': sb+=1
            self.score=[sb,sn]
        print(self.score)

        #pour Roque
        if (coup.LigneArrivee,coup.ColArrivee)==(0,2) and self.roqueNG and coup.piececoup=="RN":
            self.plateau[0][2] = "RN"
            self.plateau[0][4] = "XX"
            self.plateau[0][0] = "XX"
            self.plateau[0][3] = "TN"


        elif (coup.LigneArrivee,coup.ColArrivee)==(0,6) and self.roqueND and coup.piececoup=="RN":
            self.plateau[0][6] = "RN"
            self.plateau[0][4] = "XX"
            self.plateau[0][7] = "XX"
            self.plateau[0][5] = "TN"


        elif (coup.LigneArrivee,coup.ColArrivee)==(7,2) and self.roqueBG and coup.piececoup=="RB":
            self.plateau[7][2] = "RB"
            self.plateau[7][4] = "XX"
            self.plateau[7][0] = "XX"
            self.plateau[7][3] = "TB"


        elif (coup.LigneArrivee,coup.ColArrivee)==(7,6) and self.roqueBD and coup.piececoup=="RB":
            self.plateau[7][6] = "RB"
            self.plateau[7][4] = "XX"
            self.plateau[7][7] = "XX"
            self.plateau[7][5] = "TB"

        elif self.PP!=[] and ([coup.LigneDepart,coup.ColDepart],[coup.LigneArrivee,coup.ColArrivee])==self.PP:
            if coup.piececoup=="PB":
                self.plateau[coup.LigneArrivee][coup.ColArrivee] = "PB"
                self.plateau[coup.LigneArrivee+1][coup.ColArrivee] = "XX"
                self.plateau[coup.LigneDepart][coup.ColDepart] = "XX"

            if coup.piececoup=="PN":
                self.plateau[coup.LigneArrivee][coup.ColArrivee] = "PN"
                self.plateau[coup.LigneArrivee-1][coup.ColArrivee] = "XX"
                self.plateau[coup.LigneDepart][coup.ColDepart] = "XX"

        #promotion du pion
        elif coup.LigneArrivee==0 and coup.piececoup=='PB':
            self.plateau[coup.LigneDepart][coup.ColDepart] = "XX"
            #self.plateau[coup.LigneArrivee][coup.ColArrivee]="DB"



            #g.popup = True
            #g.makepopup(support,coup)

            g.echec = True
            g.echec_et_mat('Blanc',self.score[0])


        elif coup.LigneArrivee==7 and coup.piececoup=='PN':
            self.plateau[coup.LigneDepart][coup.ColDepart]="XX"
            self.plateau[coup.LigneArrivee][coup.ColArrivee]="DN"

        #modifie la matrice 8*8 pour un coup classique
        else :
            self.plateau[coup.LigneDepart][coup.ColDepart] = "XX"
            self.plateau[coup.LigneArrivee][coup.ColArrivee] = coup.piececoup

        piecedecoup=coup.piececoup
        # invalidation du Roque
        if piecedecoup[0] == 'R':
            if piecedecoup[1]=='N':
                self.roqueND=False
                self.roqueNG=False
            else:
                self.roqueBD=False
                self.roqueBG=False
        if piecedecoup[0] == 'T':
            if (coup.LigneDepart,coup.ColDepart)==(0,0):
                self.roqueNG=False
            if (coup.LigneDepart,coup.ColDepart)==(0,7):
                self.roqueND=False
            if (coup.LigneDepart,coup.ColDepart)==(7,0):
                self.roqueBG=False
            if (coup.LigneDepart,coup.ColDepart)==(7,7):
                self.roqueBD=False

        self.coupLog.append(coup)  #enregistre le dernier coup pour undo
        self.TourBlanc= not self.TourBlanc #tour au joueur noir
        self.PP=[]



    def coupPossibles (self,screen):
        coup=self.coupPossibles_standards(self.plateau)
        plateau0=np.copy(self.plateau)

        A=plateau0
        if A[0][0]=='TN' and self.roqueNG: #grand roque Noir
            c=True
            for j in range(1,4):
                if A[0][j]!='XX' or piece_mangeable(A,0,j,'blanc'):
                    c=False
            if A[0][4]!='RN' or piece_mangeable(A,0,4,'blanc'):
                c=False
            if c:
                coup.append(Coups([0,4],[0,2],self))

        if A[0][7]=='TN' and self.roqueND: #petit roque Noir
            c=True
            for j in range(5,7):
                if A[0][j]!='XX' or piece_mangeable(A,0,j,'blanc'):
                    c=False
            if A[0][4]!='RN' or piece_mangeable(A,0,4,'blanc'):
                c=False
            if c:
                coup.append(Coups([0,4],[0,6],self))

        if A[7][0]=='TB' and self.roqueBG: #grand roque Blanc
            c=True
            for j in range(1,4):
                if A[7][j]!='XX' or piece_mangeable(A,7,j,'noir'):
                    c=False
            if A[7][4]!='RB' or piece_mangeable(A,7,4,'noir'):
                c=False
            if c:
                coup.append(Coups([7,4],[7,2],self))

        if A[7][7]=='TB' and self.roqueBD: #petit roque Blanc
            c=True
            for j in range(5,7):
                if A[7][j]!='XX' or piece_mangeable(A,7,j,'noir'):
                    c=False
            if A[7][4]!='RB' or piece_mangeable(A,7,4,'noir'):
                c=False
            if c:
                coup.append(Coups([7,4],[7,6],self))

        #prise ne passant
        L=[0,1,2,3,4,5,6,7]
        if len(self.coupLog)!=0:
            d=self.coupLog[-1]
            der=[(d.LigneDepart,d.ColDepart),(d.LigneArrivee,d.ColArrivee)]


        if len(self.coupLog)!=0 : # les blancs peuvent PP
            for j in range (8):
                if A[3][j]=="PB" and d.piececoup=="PN":
                    if j==0 and der==[(1,1),(3,1)]:
                        coup.append(Coups([3,j],[2,1],self))
                        self.PP=([3,j],[2,1])
                    elif j==7 and der==[(1,6),(3,6)]:
                        coup.append(Coups([3,j],[2,6],self))
                        self.PP=([3,j],[2,6])
                    elif der==[(1,j-1),(3,j-1)]:
                        coup.append(Coups([3,j],[2,j-1],self))
                        self.PP=([3,j],[2,j-1])
                    elif der==[(1,j+1),(3,j+1)]:
                        coup.append(Coups([3,j],[2,j+1],self))
                        self.PP=([3,j],[2,j+1])

        if len(self.coupLog)!=0 : # les noirs peuvent PP
            for j in range (8):
                if A[4][j]=="PN" and d.piececoup=="PB":
                    if j==0 and der==[(6,1),(4,1)]:
                        coup.append(Coups([4,j],[5,1],self))
                        self.PP=([3,j],[5,1])
                    elif j==7 and der==[(6,6),(4,6)]:
                        coup.append(Coups([4,j],[5,6],self))
                        self.PP=([3,j],[5,6])
                    elif der==[(6,j-1),(4,j-1)]:
                        coup.append(Coups([4,j],[5,j-1],self))
                        self.PP=([3,j],[5,j-1])
                    elif der==[(6,j+1),(4,j+1)]:
                        coup.append(Coups([4,j],[5,j+1],self))
                        self.PP=([3,j],[5,j+1])


        if not self.TourBlanc:
            D=np.copy(self.plateau)
            coups_Roi=[]

            #purge les coups du roi
            for les_coups in coup:
                if les_coups.piececoup=='RN':
                    coups_Roi.append(les_coups)

            Coups_Possibles_Roi=[]

            for les_coups_roi in coups_Roi:
                j=les_coups_roi.ColArrivee
                i=les_coups_roi.LigneArrivee
                j0=les_coups_roi.ColDepart
                i0=les_coups_roi.LigneDepart

                B= copy.deepcopy(self.plateau)
                B[i][j]='RN'
                B[i0][j0]='XX'
                coup2=self.coupPossibles_standards(B)

                Coups_Possibles_Roi.append(les_coups_roi)

                for le_coup in coup2:
                    if le_coup.piececoup=='PB' and ((le_coup.LigneDepart+1==i and le_coup.ColDepart-1==j) or (le_coup.LigneDepart+1==i and le_coup.ColDepart+1==j)):
                        Coups_Possibles_Roi.pop()
                        break

                    elif le_coup.piececoup!='PB' and le_coup.piececoup[1]=='B' and le_coup.ColArrivee==j and le_coup.LigneArrivee==i:
                        Coups_Possibles_Roi.pop()
                        break

            print(len(Coups_Possibles_Roi))

            coup_temp=[]
            for le_coup in coup:
                if le_coup.piececoup=='RN' and (le_coup in Coups_Possibles_Roi) :
                    coup_temp.append(le_coup)
                elif le_coup.piececoup!='RN':
                    coup_temp.append(le_coup)

            coup=coup_temp

            #Menace de mat pour les autres pièces
            mat=False
            print(len(coup))
            for le_coup in coup:  #sommes nous en situation de mat ?
                if le_coup.piececoup[1]=="B" and le_coup.piececoup!='PB' and self.plateau[le_coup.LigneArrivee][le_coup.ColArrivee]=="RN":
                    mat=True
                    break

                elif le_coup.piececoup=='PB' and self.plateau[le_coup.LigneArrivee][le_coup.ColArrivee]=="RN" and (le_coup.ColArrivee == le_coup.ColDepart+1  or le_coup.ColArrivee == le_coup.ColDepart-1):
                    mat=True
                    break
            print('mat : ' +str(mat)+' noir')


            if mat :
                Nouveaux_Coups=[]
                for le_coup in coup:

                    if le_coup.piececoup[1]=="N":    #pour chaque coups des blancs

                        C3=np.copy(self.plateau)

                        C3[le_coup.LigneDepart][le_coup.ColDepart]='XX'
                        C3[le_coup.LigneArrivee][le_coup.ColArrivee]=le_coup.piececoup

                        coup2=self.coupPossibles_standards(C3)   #déplacements possibles des noirs

                        mat2=False
                        for le_coup_2 in coup2:    #sommes nous toujours en mat ?
                            if le_coup_2.piececoup[1]=="B" and le_coup_2.piececoup!="PB" and C3[le_coup_2.LigneArrivee][le_coup_2.ColArrivee]=="RN":
                                mat2=True
                                break
                            elif le_coup_2.piececoup=="PB" and C3[le_coup_2.LigneArrivee][le_coup_2.ColArrivee]=="RN" and (le_coup_2.ColArrivee == le_coup_2.ColDepart+1  or le_coup_2.ColArrivee == le_coup_2.ColDepart-1):
                                mat2=True
                                break

                        if not mat2: #sinon ce coup est autorisé
                            Nouveaux_Coups.append(le_coup)

                coup=Nouveaux_Coups

            #échec et mat
            if coup==[]:
                self.mat(screen)

        else:
            D=np.copy(self.plateau)
            coups_Roi=[]

            #purge les coups du roi
            for les_coups in coup:
                if les_coups.piececoup=='RB':
                    coups_Roi.append(les_coups)

            Coups_Possibles_Roi=[]

            for les_coups_roi in coups_Roi:
                j=les_coups_roi.ColArrivee
                i=les_coups_roi.LigneArrivee
                j0=les_coups_roi.ColDepart
                i0=les_coups_roi.LigneDepart

                B= copy.deepcopy(self.plateau)
                B[i][j]='RB'
                B[i0][j0]='XX'
                coup2=self.coupPossibles_standards(B)

                Coups_Possibles_Roi.append(les_coups_roi)

                for le_coup in coup2:
                    if le_coup.piececoup=='PN' and ((le_coup.LigneDepart+1==i and le_coup.ColDepart-1==j) or (le_coup.LigneDepart+1==i and le_coup.ColDepart+1==j)):
                        Coups_Possibles_Roi.pop()
                        break

                    elif le_coup.piececoup!='PN' and le_coup.piececoup[1]=='N' and le_coup.ColArrivee==j and le_coup.LigneArrivee==i:
                        Coups_Possibles_Roi.pop()
                        break

            print(len(Coups_Possibles_Roi))

            coup_temp=[]
            for le_coup in coup:
                if le_coup.piececoup=='RB' and (le_coup in Coups_Possibles_Roi) :
                    coup_temp.append(le_coup)
                elif le_coup.piececoup!='RB':
                    coup_temp.append(le_coup)

            coup=coup_temp

            #Menace de mat pour les autres pièces
            mat=False
            print(len(coup))
            for le_coup in coup:  #sommes nous en situation de mat ?
                if le_coup.piececoup[1]=="N" and le_coup.piececoup!='PN' and self.plateau[le_coup.LigneArrivee][le_coup.ColArrivee]=="RB":
                    mat=True
                    break

                elif le_coup.piececoup=='PN' and self.plateau[le_coup.LigneArrivee][le_coup.ColArrivee]=="RB" and (le_coup.ColArrivee == le_coup.ColDepart+1  or le_coup.ColArrivee == le_coup.ColDepart-1):
                    mat=True
                    break
            print('mat : ' +str(mat)+' blanc')


            if mat :
                Nouveaux_Coups=[]
                for le_coup in coup:

                    if le_coup.piececoup[1]=="B":    #pour chaque coups des blancs

                        C3=np.copy(self.plateau)

                        C3[le_coup.LigneDepart][le_coup.ColDepart]='XX'
                        C3[le_coup.LigneArrivee][le_coup.ColArrivee]=le_coup.piececoup

                        coup2=self.coupPossibles_standards(C3)   #déplacements possibles des noirs

                        mat2=False
                        for le_coup_2 in coup2:    #sommes nous toujours en mat ?
                            if le_coup_2.piececoup[1]=="N" and le_coup_2.piececoup!="PN" and C3[le_coup_2.LigneArrivee][le_coup_2.ColArrivee]=="RB":
                                mat2=True
                                break
                            elif le_coup_2.piececoup=="PN" and C3[le_coup_2.LigneArrivee][le_coup_2.ColArrivee]=="RB" and (le_coup_2.ColArrivee == le_coup_2.ColDepart+1  or le_coup_2.ColArrivee == le_coup_2.ColDepart-1):
                                mat2=True
                                break

                        if not mat2: #sinon ce coup est autorisé
                            Nouveaux_Coups.append(le_coup)

                coup=Nouveaux_Coups

            #échec et mat
            if coup==[]:
                self.mat(screen)

        return coup



    def mat(self,screen):
        vainqueur='Blancs' if self.TourBlanc else 'Noirs'

        #py.draw.rect(screen, py.Color(45,45,45), py.Rect(TaillePlateau, TaillePlateau,TaillePlateau ,TaillePlateau ))
        # fontsize=18
        # font = py.font.Font('GothicA1-Black.ttf',fontsize)
        # Victoire = font.render('Victoire des '+vainqueur, True, (140,140,140))
        # Victoire_rect = py.Rect(TaillePlateau, TaillePlateau,TaillePlateau ,TaillePlateau )
        # screen.blit(Victoire,Victoire_rect)

        g.echec = True
        g.echec_et_mat(vainqueur)



    def coupPossibles_standards (self,A):
        L=[0,1,2,3,4,5,6,7]
        coup=[]
        for i in range (len(A)):
            for j in range(len(A)):

                    if A[i][j]=="PB": #pion blanc
                        # à chaque fois il faut
                        if i-1 in L and j-1 in L and A[i-1][j-1][1]=="N":# non vide et une pièce noire en la case devant à gauche
                            coup.append(Coups([i,j],[i-1,j-1],self))
                        if i-1 in L and j+1 in L and A[i-1][j+1][1]=="N":# non vide et une pièce noire en la case devant à droite
                            coup.append(Coups([i,j],[i-1,j+1],self))
                        if i-1 in L and A[i-1][j]=="XX": # case devant le pion vide on ne va pas sortir de l'échiquier
                            coup.append(Coups([i,j],[i-1,j],self))
                        #codage du possible départ de 2 cases
                        #(pion qui n'a pas bougé= pion sur la ligne de départ)
                        if i==6 and A[i-1][j]=="XX" and A[i-2][j]=="XX":
                            coup.append(Coups([i,j],[i-2,j],self))
                        #promotion du pion i=1 sera codé autre part, pareil prise en passant

                    if A[i][j]=="CB": #cheval blanc
                        e=[[i-2,j-1],[i-2,j+1],[i-1,j-2],[i-1,j+2],[i+1,j-2],[i+1,j+2],[i+2,j-1],[i+2,j+1]]
                        # 8 déplacements envisageables pour le cheval
                        for u in e:
                            if u[0] in L and u[1] in L: # dans le cadre
                                if A[u[0]][u[1]]=="XX": #pas de pièce
                                    coup.append(Coups([i,j],u,self))
                                if A[u[0]][u[1]][1]=="N": # pièce noire
                                    coup.append(Coups([i,j],u,self))

                    if A[i][j]=="FB" or A[i][j]=="DB": #fou blanc
                        # boucles pour les 4 directions+sens posibles
                        c=0
                        while True:
                            c+=1
                            if i-c not in L or j-c not in L: #limite de l'échiquier
                                break
                            if A[i-c][j-c]=="XX": #rencontre pas encore de pièce
                                coup.append(Coups([i,j],[i-c,j-c],self))
                            else:  #rencontre une pièce
                                if A[i-c][j-c][1]=="B": # de même couleur donc ne peut pas la manger
                                    break
                                if A[i-c][j-c][1]=="N":
                                    coup.append(Coups([i,j],[i-c,j-c],self))
                                    break
                                else:
                                    coup.append(Coups([i,j],[i-c,j-c],self))
                        c=0
                        while True:
                            c+=1
                            if i-c not in L or j+c not in L: #limite de l'échiquier
                                break
                            if A[i-c][j+c]=="XX": #rencontre pas encore de pièce
                                coup.append(Coups([i,j],[i-c,j+c],self))
                            else:  #rencontre une pièce
                                if A[i-c][j+c][1]=="B": # de même couleur donc ne peut pas la manger
                                    break
                                if A[i-c][j+c][1]=="N":
                                    coup.append(Coups([i,j],[i-c,j+c],self))
                                    break
                                else:
                                    coup.append(Coups([i,j],[i-c,j+c],self))
                        c=0
                        while True:
                            c+=1
                            if i+c not in L or j-c not in L: #limite de l'échiquier
                                break
                            if A[i+c][j-c]=="XX": #rencontre pas encore de pièce
                                coup.append(Coups([i,j],[i+c,j-c],self))
                            else:  #rencontre une pièce
                                if A[i+c][j-c][1]=="B": # de même couleur donc ne peut pas la manger
                                    break
                                if A[i+c][j-c][1]=="N":
                                    coup.append(Coups([i,j],[i+c,j-c],self))
                                    break
                                else:
                                    coup.append(Coups([i,j],[i+c,j-c],self))
                        c=0
                        while True:
                            c+=1
                            if i+c not in L or j+c not in L: #limite de l'échiquier
                                break
                            if A[i+c][j+c]=="XX": #rencontre pas encore de pièce
                                coup.append(Coups([i,j],[i+c,j+c],self))
                            else:  #rencontre une pièce
                                if A[i+c][j+c][1]=="B": # de même couleur donc ne peut pas la manger
                                    break
                                if A[i+c][j+c][1]=="N":
                                    coup.append(Coups([i,j],[i+c,j+c],self))
                                    break
                                else:
                                    coup.append(Coups([i,j],[i+c,j+c],self))

                    if A[i][j]=="TB" or A[i][j]=="DB": #tour blanche ou dame blanche
                        # boucles pour les 4 directions+sens posibles
                        c=0
                        while True:
                            c+=1
                            if i-c not in L: #limite de l'échiquier pour un déplacement vers le haut
                                break
                            if A[i-c][j]=="XX": #rencontre pas encore de pièce
                                coup.append(Coups([i,j],[i-c,j],self))
                            else:  #rencontre une pièce
                                if A[i-c][j][1]=="B": # de même couleur donc ne peut pas la manger
                                    break
                                if A[i-c][j][1]=="N":
                                    coup.append(Coups([i,j],[i-c,j],self))
                                    break
                                else:
                                    coup.append(Coups([i,j],[i-c,j],self))
                                    break
                        c=0
                        while True:
                            c+=1
                            if j+c not in L: #limite de l'échiquier pour un déplacement vers la droite
                                break
                            if A[i][j+c]=="XX": #rencontre pas encore de pièce
                                coup.append(Coups([i,j],[i,j+c],self))
                            else:  #rencontre une pièce
                                if A[i][j+c][1]=="B": # de même couleur donc ne peut pas la manger
                                    break
                                if A[i][j+c][1]=="N":
                                    coup.append(Coups([i,j],[i,j+c],self))
                                    break
                                else:
                                    coup.append(Coups([i,j],[i,j+c],self))
                                    break
                        c=0
                        while True:
                            c+=1
                            if i+c not in L: #limite de l'échiquier pour un déplacement vers le bas
                                break
                            if A[i+c][j]=="XX": #rencontre pas encore de pièce
                                coup.append(Coups([i,j],[i+c,j],self))
                            else:  #rencontre une pièce
                                if A[i+c][j][1]=="B": # de même couleur donc ne peut pas la manger
                                    break
                                if A[i+c][j][1]=="N": # de même couleur donc ne peut pas la manger
                                    coup.append(Coups([i,j],[i+c,j],self))
                                    break
                                else:
                                    coup.append(Coups([i,j],[i+c,j],self))
                                    break
                        c=0
                        while True:
                            c+=1
                            if j-c not in L: #limite de l'échiquier pour un déplacement vers la gauche
                                break
                            if A[i][j-c]=="XX": #rencontre pas encore de pièce
                                coup.append(Coups([i,j],[i,j-c],self))
                            else:  #rencontre une pièce
                                if A[i][j-c][1]=="B": # de même couleur donc ne peut pas la manger
                                    break
                                if A[i][j-c][1]=="N":
                                    coup.append(Coups([i,j],[i,j-c],self))
                                    break
                                else:
                                    coup.append(Coups([i,j],[i,j-c],self))
                                    break

                    if A[i][j]=="RB": #roi blanc
                        e=[[i-1,j-1],[i,j-1],[i-1,j],[i-1,j+1],[i,j+1],[i+1,j-1],[i+1,j],[i+1,j+1]]
                        # 8 déplacements envisageables pour le roi
                        for u in e:
                            if u[0] in L and u[1] in L:
                            # dans le cadre
                                if A[u[0]][u[1]]=="XX": #pas de pièce
                                    coup.append(Coups([i,j],u,self))
                                else:
                                    if A[u[0]][u[1]][1]=="N": # pièce blanche
                                        coup.append(Coups([i,j],u,self))


                    if A[i][j]=="PN": #pion noir
                        if i+1 in L and j-1 in L and A[i+1][j-1][1]=="B":# non vide et une pièce blanche en la case devant le pion à gauche
                            coup.append(Coups([i,j],[i+1,j-1],self))
                        if i+1 in L and j+1 in L and A[i+1][j+1][1]=="B":# non vide et une pièce blanche en la case devant à droite
                            coup.append(Coups([i,j],[i+1,j+1],self))
                        if i+1 in L and A[i+1][j]=="XX":# case devant le pion vide on ne vas pas sortir de l'échiquier
                            coup.append(Coups([i,j],[i+1,j],self))
                        #codage du possible départ de 2 cases
                        #(pion qui n'a pas bougé= pion sur la ligne de départ)
                        if i==1 and A[i+1][j]=="XX" and A[i+2][j]=="XX":
                            coup.append(Coups([i,j],[i+2,j],self))
                        #promotion du pion i=6 sera codé autre part, pareil prise en passant

                    if A[i][j]=="CN": #cheval noir
                        e=[[i-2,j-1],[i-2,j+1],[i-1,j-2],[i-1,j+2],[i+1,j-2],[i+1,j+2],[i+2,j-1],[i+2,j+1]]
                        # 8 déplacements envisageables pour le cheval
                        for u in e:
                            if u[0] in L and u[1] in L:
                            # dans le cadre
                                if A[u[0]][u[1]]=="XX": #pas de pièce
                                    coup.append(Coups([i,j],u,self))
                                else:
                                    if A[u[0]][u[1]][1]=="B": # pièce blanche
                                        coup.append(Coups([i,j],u,self))

                    if A[i][j]=="FN" or A[i][j]=="DN": #fou noir et remarquons que la dame à au moins tous les déplacements d'un fou
                        # boucles pour les 4 directions+sens posibles
                        c=0
                        while True:
                            c+=1
                            if i-c not in L or j-c not in L: #limite de l'échiquier
                                break
                            if A[i-c][j-c]=="XX": #rencontre pas encore de pièce
                                coup.append(Coups([i,j],[i-c,j-c],self))
                            else:  #rencontre une pièce
                                if A[i-c][j-c][1]=="N": # de même couleur donc ne peut pas la manger
                                    break
                                if A[i-c][j-c][1]=="B":
                                    coup.append(Coups([i,j],[i-c,j-c],self))
                                    break
                                else:
                                    coup.append(Coups([i,j],[i-c,j-c],self))
                                    break
                        c=0
                        while True:
                            c+=1
                            if i-c not in L or j+c not in L: #limite de l'échiquier
                                break
                            if A[i-c][j+c]=="XX": #rencontre pas encore de pièce
                                coup.append(Coups([i,j],[i-c,j+c],self))
                            else:  #rencontre une pièce
                                if A[i-c][j+c][1]=="N": # de même couleur donc ne peut pas la manger
                                    break
                                if A[i-c][j+c][1]=="B":
                                    coup.append(Coups([i,j],[i-c,j+c],self))
                                    break
                                else:
                                    coup.append(Coups([i,j],[i-c,j+c],self))
                                    break
                        c=0
                        while True:
                            c+=1
                            if i+c not in L or j-c not in L: #limite de l'échiquier
                                break
                            if A[i+c][j-c]=="XX": #rencontre pas encore de pièce
                                coup.append(Coups([i,j],[i+c,j-c],self))
                            else:  #rencontre une pièce
                                if A[i+c][j-c][1]=="N": # de même couleur donc ne peut pas la manger
                                    break
                                if A[i+c][j-c][1]=="B":
                                     coup.append(Coups([i,j],[i+c,j-c],self))
                                     break
                                else:
                                    coup.append(Coups([i,j],[i+c,j-c],self))
                                    break
                        c=0
                        while True:
                            c+=1
                            if i+c not in L or j+c not in L: #limite de l'échiquier
                                break
                            if A[i+c][j+c]=="XX": #rencontre pas encore de pièce
                                coup.append(Coups([i,j],[i+c,j+c],self))
                            else:  #rencontre une pièce
                                if A[i+c][j+c][1]=="N": # de même couleur donc ne peut pas la manger
                                    break
                                if A[i+c][j+c][1]=="B":
                                    coup.append(Coups([i,j],[i+c,j+c],self))
                                    break
                                else:
                                    coup.append(Coups([i,j],[i+c,j+c],self))
                                    break

                    if A[i][j]=="TN" or A[i][j]=="DN": #tour noire et une dame se déplace pareil qu'une tour et même plus
                        # boucles pour les 4 directions+sens posibles
                        c=0
                        while True:
                            c+=1
                            if i-c not in L: #limite de l'échiquier pour un déplacement vers le haut
                                break
                            if A[i-c][j]=="XX": #rencontre pas encore de pièce
                                coup.append(Coups([i,j],[i-c,j],self))
                            else:  #rencontre une pièce
                                if A[i-c][j][1]=="N": # de même couleur donc ne peut pas la manger
                                    break
                                if A[i-c][j][1]=="B":
                                    coup.append(Coups([i,j],[i-c,j],self))
                                    break
                                else:
                                    coup.append(Coups([i,j],[i-c,j],self))
                                    break
                        c=0
                        while True:
                            c+=1
                            if j+c not in L: #limite de l'échiquier pour un déplacement vers la droite
                                break
                            if A[i][j+c]=="XX": #rencontre pas encore de pièce
                                coup.append(Coups([i,j],[i,j+c],self))
                            else:  #rencontre une pièce
                                if A[i][j+c][1]=="N": # de même couleur donc ne peut pas la manger
                                    break
                                if A[i][j+c][1]=="B":
                                    coup.append(Coups([i,j],[i,j+c],self))
                                    break
                                else:
                                    coup.append(Coups([i,j],[i,j+c],self))
                                    break
                        c=0
                        while True:
                            c+=1
                            if i+c not in L: #limite de l'échiquier pour un déplacement vers le bas
                                break
                            if A[i+c][j]=="XX": #rencontre pas encore de pièce
                                coup.append(Coups([i,j],[i+c,j],self))
                            else:  #rencontre une pièce
                                if A[i+c][j][1]=="N": # de même couleur donc ne peut pas la manger
                                    break
                                if A[i+c][j][1]=="B":
                                    coup.append(Coups([i,j],[i+c,j],self))
                                    break
                                else:
                                    coup.append(Coups([i,j],[i+c,j],self))
                                    break
                        c=0
                        while True:
                            c+=1
                            if j-c not in L: #limite de l'échiquier pour un déplacement vers la gauche
                                break
                            if A[i][j-c]=="XX": #rencontre pas encore de pièce
                                coup.append(Coups([i,j],[i,j-c],self))
                            else:  #rencontre une pièce
                                if A[i][j-c][1]=="N": # de même couleur donc ne peut pas la manger
                                    break
                                if A[i][j-c][1]=="B":
                                    coup.append(Coups([i,j],[i,j-c],self))
                                    break
                                else:
                                    coup.append(Coups([i,j],[i,j-c],self))
                                    break

                    if A[i][j]=="RN": #roi noir
                        e=[[i-1,j-1],[i,j-1],[i-1,j],[i-1,j+1],[i,j+1],[i+1,j-1],[i+1,j],[i+1,j+1]] # 8 déplacements envisageables pour le roi
                        for u in e:
                            if u[0] in L and u[1] in L: # dans le cadre
                                if A[u[0]][u[1]]=="XX": #pas de pièce
                                    coup.append(Coups([i,j],u,self))
                                else:
                                    if A[u[0]][u[1]][1]=="B": # pièce blanche
                                        coup.append(Coups([i,j],u,self))

        return coup

class Coups():
    ranksToRows = {"1":7,"2":6,"3":5,"4":4,"5":3,"6":2,"7":1,"8":0}
    rowsToRank = {v:k for k,v in ranksToRows.items()}
    filesToCols = {"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7}
    colsToFiles = {v:k for k,v in filesToCols.items()}

    def __init__(self, CaseDepart, CaseArrivee, support):
        echiquier=support.plateau
        self.LigneDepart = CaseDepart[0]
        self.ColDepart = CaseDepart[1]
        self.LigneArrivee = CaseArrivee[0]
        self.ColArrivee = CaseArrivee[1]
        self.piececoup = echiquier[self.LigneDepart][self.ColDepart]
        self.pieceCapturee = echiquier[self.LigneArrivee][self.ColArrivee]

    def getChessNotation(self):
        return self.getRankFile(self.LigneDepart, self.ColDepart)+self.getRankFile(self.LigneArrivee,self.ColArrivee)

    def getRankFile (self, r, c):
        return self.colsToFiles[c] + self.rowsToRank[r]

#%%Va recevoir les coups des joueurs et afficher l'état actuel du jeu

"""
Paramètres du plateau (à modifier plus tard)
"""

TaillePlateau = 400 #8*64
TailleCase = TaillePlateau//8

TailleBordure = 3*TailleCase

TailleBordDroit= 3*TailleCase

TailleBordGauche= 3*TailleCase

TailleSeparatrice = 20

BordureHaute=3*(TailleCase//2)

"""
Téléchargement des images
"""

Images = {}
Textures = {}

def ChargeImages ():
    pieces = ["TN","CN","FN","DN","RN","PN","TB","CB","FB","DB","RB","PB"]
    for piece in pieces :
        print(py.image.load("Pieces/" + piece + ".png"))
        Images[piece] = py.transform.scale(py.image.load("Pieces/" + piece + ".png"),(TailleCase,TailleCase))

    #textures
    Textures['Bord'] = py.transform.scale(py.image.load('Fonds/texture4' + ".jpg"),(TaillePlateau+2*TailleBordure+TailleBordGauche+TailleBordDroit,TaillePlateau+2*TailleBordure))

    #Textures['BordD'] = py.transform.scale(py.image.load('texture4droite' + ".jpg"),(TaillePlateau+2*TailleBordure,TaillePlateau+2*TailleBordure))
    #Textures['BordG'] = py.transform.scale(py.image.load('texture4gauche' + ".jpg"),(TaillePlateau+2*TailleBordure,TaillePlateau+2*TailleBordure))

    #Textures['BordDroit'] = py.transform.scale(py.image.load('texture1' + ".png"),(TailleBordDroit,TaillePlateau+2*TailleBordure))

    Textures['Separation']= py.transform.scale(py.image.load('Fonds/texture3.png'),(TailleSeparatrice,TaillePlateau+2*TailleBordure))

"""
Mise à jour des graphiques & récupération du coup du joueur
"""

def Partie (g):
    py.init()
    screen=py.display.set_mode((TaillePlateau+2*TailleBordure+TailleBordDroit+ TailleBordGauche, BordureHaute+TaillePlateau+2*TailleBordure))
    clock = py.time.Clock()
    #clock.tick(1)
    font = py.font.SysFont(None, 80)

    screen.fill(py.Color("white"))

    ChargeImages ()

    support=Plateau()

    #---------------- musiques-------------------
    musiquedebase=py.mixer.music.load('Musique/One-eyed Maestro.mp3')
    #musiquedebase=py.mixer.music.load('Musique/Kevin MacLeod - Monkeys Spinning Monkeys.mp3')

    #----------------- boutons ----------------
    #sound_button = Button(0,0,110,35,"WHITE",(60, 60, 60),'Son',20)

    largeurBoutons=100
    HauteurBoutons=63

    sound_button = BoutonGlobal(TaillePlateau+2*TailleBordure+TailleBordDroit-2*largeurBoutons+TailleBordGauche, (BordureHaute-HauteurBoutons)//2, largeurBoutons, HauteurBoutons, '', (60,60,60) , 'Icones/MutedSpeaker.png',20)

    support.pause=True

    sound_button_m = BoutonGlobal(TaillePlateau+2*TailleBordure+TailleBordDroit-2*largeurBoutons+TailleBordGauche, (BordureHaute-HauteurBoutons)//2, largeurBoutons, HauteurBoutons, '', (60,60,60) , 'Icones/Speaker.png',20)



    menu_button = BoutonGlobal(largeurBoutons, (BordureHaute-HauteurBoutons)//2, largeurBoutons, HauteurBoutons, '', (60,60,60) , 'Icones/Arrow.png',20)


    #-------------- compteurs ----------------
    counterb = 599
    counterinitb=counterb
    minutesb = counterb//60
    secondesb = counterb % 60

    if secondesb//10==0:
        textb = font.render(str(minutesb)+":0"+str(secondesb), True, py.Color("#e5e9f4"))
    else:
        textb = font.render(str(minutesb)+":"+str(secondesb), True, py.Color("#e5e9f4"))

    timer_eventb = py.USEREVENT+1
    py.time.set_timer(timer_eventb, 1000)

    countern = 599
    counterinitn=countern
    minutesn = countern//60
    secondesn = countern % 60

    if secondesn//10==0:
        textn = font.render(str(minutesn)+":0"+str(secondesn), True, py.Color("#e5e9f4"))
    else:
        textn = font.render(str(minutesn)+":"+str(secondesn), True, py.Color("#e5e9f4"))

    timer_eventn = py.USEREVENT+1
    py.time.set_timer(timer_eventn, 1000)



    Couleur=''
    if support.TourBlanc:
        Couleur='blanc'
    else:
        Couleur='noir'

    CoupFait=False #variable qui vérifie si le déplacement a eu lieu

    Coups_Possibles=support.coupPossibles(screen)

    running=True

    CaseSelectionnee = () #aucune case sélectionnée, garde la trace du dernier click de l'utilisateur (i,j)
    playerClicks = []  #garde la trace des clicks du joueur (i,j)

    while running: # boucle principale du jeu
        clock.tick(10)

        for event in py.event.get():
            if event.type == py.QUIT:
                running=False
                py.quit()
                exit()
            elif event.type==py.MOUSEBUTTONDOWN:
                position = py.mouse.get_pos()  #position (x,y) de la souris
                y = (position[0]-TailleBordure-TailleBordGauche)//TailleCase

                x = (position[1]-TailleBordure-BordureHaute)//TailleCase

                if (TaillePlateau+TailleBordure+BordureHaute)>=position[1]>=(TailleBordure+BordureHaute) and (TailleBordure+TailleBordGauche)<=position[0]<=(TaillePlateau+TailleBordure+TailleBordGauche):
                    if CaseSelectionnee == (x,y): #l'utilisateur a clické sur la même case
                        CaseSelectionnee = ()   #deselect
                        playerClicks = []  #clear player clicks
                    else:
                        CaseSelectionnee = (x,y)
                        playerClicks.append(CaseSelectionnee) #fonctionne pour clicks droits et gauches

                    if len(playerClicks)==2: #après 2nd click
                        coup=Coups(playerClicks[0],playerClicks[1],support)



                        for les_coups in Coups_Possibles:
                            condition=les_coups.LigneDepart==coup.LigneDepart and les_coups.ColDepart==coup.ColDepart and les_coups.LigneArrivee==coup.LigneArrivee and  les_coups.ColArrivee==coup.ColArrivee
                            if condition and support.TourBlanc:
                                support.FaireCoup(coup,g,support)
                                CoupFait=True
                        CaseSelectionnee = ()
                        playerClicks=[]
            elif event.type == py.KEYDOWN :
                if event.key == py.K_u :                                     # press U to return back <-> undo the move
                    support.undoMove(g)
                    CoupFait = True                                     #!!!!!!!!!!!!!
                    #animate = False


            elif event.type == timer_eventb and support.TourBlanc:
                counterb -= 1

                if minutesb!=0 and secondesb==0:
                    secondesb=59
                    minutesb-=1

                else:
                    secondesb-=1

                if secondesb//10==0:
                    textb = font.render(str(minutesb)+":0"+str(secondesb), True, py.Color("#e5e9f4"))
                else:
                    textb = font.render(str(minutesb)+":"+str(secondesb), True, py.Color("#e5e9f4"))

                if counterb == 0:
                    py.time.set_timer(timer_eventb, 0)

            elif event.type == timer_eventn and not support.TourBlanc:
                countern -= 1

                if minutesn!=0 and secondesn==0:
                    secondesn=59
                    minutesn-=1

                else:
                    secondesn-=1

                if secondesn//10==0:
                    textn = font.render(str(minutesn)+":0"+str(secondesn), True, py.Color("#e5e9f4"))
                else:
                    textn = font.render(str(minutesn)+":"+str(secondesn), True, py.Color("#e5e9f4"))

                if countern == 0:
                    py.time.set_timer(timer_eventn, 0)


            #-----------------gestion des boutons-----------------
            elif event.type==py.MOUSEBUTTONUP:
                mouse_pos = py.mouse.get_pos()
                if sound_button.rect.collidepoint(mouse_pos):
                    if support.pause==True:
                        py.mixer.music.play(-1)
                        support.pause=False
                    elif support.pause==False:
                        py.mixer.music.pause()
                        support.pause=True

                if menu_button.rect.collidepoint(mouse_pos):
                    py.mixer.music.pause()

                    py.mixer.music.load('Musique/Pop Goes the Weasel.mp3')
                    py.mixer.music.play(-1)
                    g.pause=False
                    running=False
                    return True

            if  not support.TourBlanc and not CoupFait:


                displayeur(screen,support,Coups_Possibles,CaseSelectionnee,g)
                #Pmax=2
                Pmax = g.difficulty_level
                CaseDepart,CaseArrivee=elagage(support.plateau,Pmax,0)  #l'IA joue les noirs
                coup=Coups(CaseDepart, CaseArrivee,support)      #case init et finale

                print(coup.getChessNotation())
                support.FaireCoup(coup,g,support)
                CoupFait=True
                sqSelected = ()
                playerClicks=[]
                cond=False

        if CoupFait:
            #Animation(support.coupLog[-1],screen,support,clock)
            Coups_Possibles=support.coupPossibles(screen)
            CoupFait=False
            displayeur(screen,support,Coups_Possibles,CaseSelectionnee,g)

        #if menu_button.is_pressed(mouse_pos,mouse_pressed):
         #   running=False

        #------------ dessinateur ---------------
        displayeur(screen,support,Coups_Possibles,CaseSelectionnee,g)
        text_rectb = (TaillePlateau+2*TailleBordure+TailleBordGauche-55,TaillePlateau+TailleBordure-25,10,20)
        screen.blit(textb, text_rectb)
        drawArcCv2(screen, (75,75,75), (TaillePlateau+2*TailleBordure+TailleBordGauche,TaillePlateau+TailleBordure), 70, 10, 360*counterb/counterinitb)

        #text_rect = ((TaillePlateau+2*TailleBordure+TailleCase+8),(TaillePlateau+TailleBordure)//2+5,10,20)
        #screen.blit(text,text_rect)
        #drawArcCv2(screen, (84,56, 11), (TaillePlateau+2*TailleBordure+2*TailleCase,TaillePlateau//2+TailleBordure), 70, 10, 360*counter/counterinit)
        #screen.blit(sound_button.image0, sound_button.rect0)

        if support.pause:
            screen.blit(sound_button.image, sound_button.rect)
        else:
            screen.blit(sound_button_m.image, sound_button_m.rect)

        screen.blit(menu_button.image, menu_button.rect)

        text_rectn = (TaillePlateau+2*TailleBordure+TailleBordGauche-55,2*TailleBordure-25,10,20)
        screen.blit(textn, text_rectn)
        drawArcCv2(screen, (75,75,75), (TaillePlateau+2*TailleBordure+TailleBordGauche,2*TailleBordure), 70, 10, 360*countern/counterinitn)

        py.display.flip()

"""
Surbrillance et animations de coup
"""
def surbrillance (screen,support,Coups_Possibles,CaseSelectionnee):
    if CaseSelectionnee != ():
        i,j = CaseSelectionnee
        if support.plateau[i][j][1]==('B' if support.TourBlanc else 'N'): #La case sélectionnée contient une pièce du joueur qui a le tour
            s=py.Surface((TailleCase,TailleCase))
            s.set_alpha(200)#valeur de transparence (0 à 255)
            s.fill(py.Color('green'))
            screen.blit(s, ((j*TailleCase+TailleBordure+TailleBordGauche,i*TailleCase+TailleBordure+BordureHaute)))
            s.fill(py.Color('red'))

            for coup in Coups_Possibles:
                if coup.LigneDepart == i and coup.ColDepart ==j:
                    if support.plateau[coup.LigneArrivee][coup.ColArrivee]!='XX':
                        screen.blit(s, (coup.ColArrivee*TailleCase+TailleBordure+TailleBordGauche,coup.LigneArrivee*TailleCase+BordureHaute+TailleBordure))
                    else:
                        py.draw.circle(screen, py.Color('red'), (coup.ColArrivee*TailleCase+TailleBordure+TailleCase//2+TailleBordGauche,coup.LigneArrivee*TailleCase+BordureHaute+TailleBordure+TailleCase//2), TailleCase//6)


def Animation (coup, screen, support, clock):
    colors = [py.Color("#705c28"),py.Color("#ffe194")]
    Dl = coup.LigneArrivee - coup.LigneDepart
    Dc = coup.ColArrivee - coup.ColDepart
    FPC = 3 #frames pour bouger une case
    FT = FPC*(abs(Dl)+abs(Dc))

    for frame in range (FT+1):
        i,j = (coup.LigneDepart + Dl*frame/FT, coup.ColDepart + Dc*frame/FT)
        BoardDrawer(g,screen,support)
        PiecesDrawer(g,screen,support)

        #Supprime la pièce bougée de sa case d'arrivée
        color = colors[(coup.LigneArrivee+coup.ColArrivee)%2]
        CaseArrivee = py.Rect(coup.ColArrivee*TailleCase+TailleBordure+TailleBordGauche, coup.LigneArrivee*TailleCase+TailleBordure+BordureHaute, TailleCase,TailleCase)
        py.draw.rect(screen, color, CaseArrivee)

        #Ajoute Pièce capturée dans le rectangle
        if coup.pieceCapturee !="XX":
            screen.blit(Images[coup.pieceCapturee], CaseArrivee)


        #Ajoute les pièces de transfert
        screen.blit(Images[str(coup.piececoup)], py.Rect(j*TailleCase+TailleBordure+TailleBordGauche, i*TailleCase+TailleBordure+BordureHaute, TailleCase, TailleCase))
        py.display.update()

"""
Environnement
"""


"""
Graphismes
"""

def displayeur (screen,support,Coups_Possibles,CaseSelectionnee,g):
    BoardDrawer(g,screen,support)
    surbrillance(screen,support,Coups_Possibles,CaseSelectionnee)
    PiecesDrawer(screen,support)

def BoardDrawer(g,screen,support):
    colors = [py.Color("#3f3e43"),py.Color("#e5e9f4")]
    font20 = py.font.Font('Styles/GothicA1-Black.ttf',BordureHaute//2)
    title= font20.render('SUPER CHESS',True,py.Color(220,200,0))
    title_rect = title.get_rect(x=(TaillePlateau+2*TailleBordure+TailleBordDroit+TailleBordGauche)*0.37,y=BordureHaute//3)

    #screen.fill(py.Color("#fae6cb"))

    #py.draw.rect(screen, py.Color(120,120,120), py.Rect(TaillePlateau+2*TailleBordure+TailleBordGauche,BordureHaute,TailleBordDroit,TaillePlateau+2*TailleBordure))

    py.draw.rect(screen, py.Color(45,45,45), py.Rect(0,0,TaillePlateau+2*TailleBordure+TailleBordDroit+TailleBordGauche, BordureHaute))
    screen.blit(title,title_rect)

    #screen.blit(Textures['Bord'],py.Rect(TailleBordGauche,BordureHaute,TaillePlateau+2*TailleBordure, TaillePlateau+2*TailleBordure))

    screen.blit(Textures['Bord'],py.Rect(0,BordureHaute,TaillePlateau+2*TailleBordure, TaillePlateau+2*TailleBordure+TailleBordGauche+TailleBordDroit))


    #screen.blit(Textures['BordG'],py.Rect(TaillePlateau+2*TailleBordure+TailleBordGauche,BordureHaute,TailleBordDroit,TaillePlateau+2*TailleBordure))
    #screen.blit(Textures['BordD'],py.Rect(0,BordureHaute,TaillePlateau+2*TailleBordure, TailleBordGauche))


    #screen.blit(Textures['BordDroit'],py.Rect(TaillePlateau+2*TailleBordure,BordureHaute,TailleBordDroit,TaillePlateau+2*TailleBordure))

    #screen.blit(Textures['Separation'],py.Rect(TaillePlateau+2*TailleBordure+TailleBordGauche,BordureHaute,TailleSeparatrice,TaillePlateau+2*TailleBordure))

    #screen.blit(Textures['Separation'],py.Rect(TailleBordGauche-TailleSeparatrice,BordureHaute,TailleSeparatrice,TaillePlateau+2*TailleBordure))

    #-----------Barre de score----------------
    [b,a]=support.score

    L=TaillePlateau
    T=a+b
    py.draw.rect(screen, py.Color("#3f3e43"), py.Rect((TailleBordGauche+TailleBordure)//2, TailleBordure+BordureHaute,50,b/T*L))
    py.draw.rect(screen, py.Color("#e5e9f4"), py.Rect((TailleBordGauche+TailleBordure)//2,  TaillePlateau+BordureHaute+TailleBordure-(L-b/T*L),50,a/T*L))


    fontsize=18
    font = py.font.Font('Styles/GothicA1-Black.ttf',fontsize)
    scoreblanc = font.render(str(a), True, (140,140,140))
    scoreblanc_rect = py.Rect((TailleBordGauche+TailleBordure)//2+5, TailleBordure+BordureHaute+TaillePlateau+5,50,b/T*L)
    screen.blit(scoreblanc,scoreblanc_rect)

    fontsize=18
    font = py.font.Font('Styles/GothicA1-Black.ttf',fontsize)
    scorenoir = font.render(str(b), True, (140,140,140))
    scorenoir_rect = py.Rect((TailleBordGauche+TailleBordure)//2+5, TailleBordure+BordureHaute-20,50,b/T*L)
    screen.blit(scorenoir,scorenoir_rect)

    if g.ironman :
        g.screen.blit(g.On, (TaillePlateau+2*TailleBordure+TailleBordDroit+TailleBordGauche-50,BordureHaute//3))
    else :
        g.screen.blit(g.Off, (TaillePlateau+2*TailleBordure+TailleBordDroit+TailleBordGauche-50,BordureHaute//3))

    #-----------Marquage plateau----------------
    for i in range (8):
        L1=['A','B','C','D','E','F','G','H']
        fontsize=18
        font = py.font.Font('Styles/GothicA1-Black.ttf',fontsize)
        text = font.render(L1[i], True, (255,255,255))
        text_rect = py.Rect(TailleBordure+(i)*TailleCase+TailleCase/2-5+TailleBordGauche,TailleBordure+BordureHaute-30,100,100)
        screen.blit(text,text_rect)

        text2 = font.render(L1[i], True, (255,255,255))
        text_rect2 = py.Rect(TailleBordure+(i)*TailleCase+TailleCase/2-5+TailleBordGauche,TailleBordure+BordureHaute-45+TailleCase+TaillePlateau,100,100)
        screen.blit(text2,text_rect2)

    for j in range (8):
        L2=['1','2','3','4','5','6','7','8']
        fontsize=18
        font = py.font.Font('Styles/GothicA1-Black.ttf',fontsize)
        text = font.render(L2[-j-1], True, (255,255,255))
        text_rect = py.Rect(TailleBordure+TailleBordGauche-30,TailleBordure+(j)*TailleCase+TailleCase/2-5+BordureHaute,100,100)
        screen.blit(text,text_rect)

        text3 = font.render(L2[-j-1], True, (255,255,255))
        text_rect3 = py.Rect(TailleBordure+TailleBordGauche+TaillePlateau+25,TailleBordure+(j)*TailleCase+TailleCase/2-5+BordureHaute,100,100)
        screen.blit(text3,text_rect3)



    #----------Plateau lui-même-----------------
    for i in range (8):
        for j in range (8):
            color = colors[((i+j)%2)]

            py.draw.rect(screen, color, py.Rect(j*TailleCase+TailleBordure+TailleBordGauche, i*TailleCase+TailleBordure+BordureHaute,TailleCase,TailleCase)) #plateau

            #py.draw.rect(screen, py.Color("#fae6cb"), py.Rect(TaillePlateau+2*TailleBordure,0,TailleBordDroit,TaillePlateau+2*TailleBordure))  #bande droite


def PiecesDrawer(screen,support):
    plato=support.plateau
    for i in range(8):
        for j in range(8):
            piece=plato[i][j]
            if piece != "XX":
                screen.blit(Images[piece], py.Rect(j*TailleCase+TailleBordure+TailleBordGauche,i*TailleCase+TailleBordure+BordureHaute,TailleCase,TailleCase))


    #----pieces mangées -------
    Liste=support.piecemangees
    n=len(Liste)
    npn=0
    nfcn=0
    ndtn=0
    #print(Liste)
    npb=0
    nfcb=0
    ndtb=0
    for k in range(n):
        if Liste[k][1]=='N':
            ligne=BordureHaute+TaillePlateau+TailleBordure+TailleBordure//2
            if Liste[k][0]=='C' or Liste[k][0]=='F':
                ligne+=TailleCase//2
                nfcn+=1
                screen.blit(py.transform.scale(Images[Liste[k]],(TailleCase//2,TailleCase//2)), py.Rect(TaillePlateau+2*TailleBordure+20+8*nfcn,ligne,TailleCase//2,TailleCase//2))

            elif Liste[k][0]=='D' or Liste[k][0]=='T':
                ligne+=TailleCase
                ndtn+=1
                screen.blit(py.transform.scale(Images[Liste[k]],(TailleCase//2,TailleCase//2)), py.Rect(TaillePlateau+2*TailleBordure+20+8*ndtn,ligne,TailleCase//2,TailleCase//2))
            else:
                npn+=1
                screen.blit(py.transform.scale(Images[Liste[k]],(TailleCase//2,TailleCase//2)), py.Rect(TaillePlateau+2*TailleBordure+20+8*npn,ligne,TailleCase//2,TailleCase//2))

        else:
            ligne=BordureHaute+TailleBordure//2-TailleCase//2

            if Liste[k][0]=='C' or Liste[k][0]=='F':
                ligne+=TailleCase//2
                nfcb+=1
                screen.blit(py.transform.scale(Images[Liste[k]],(TailleCase//2,TailleCase//2)), py.Rect(TaillePlateau+2*TailleBordure+20+8*nfcb,ligne,TailleCase//2,TailleCase//2))

            elif Liste[k][0]=='D' or Liste[k][0]=='T':
                ligne+=TailleCase
                ndtb+=1
                screen.blit(py.transform.scale(Images[Liste[k]],(TailleCase//2,TailleCase//2)), py.Rect(TaillePlateau+2*TailleBordure+20+8*ndtb,ligne,TailleCase//2,TailleCase//2))
            else:
                npb+=1
                screen.blit(py.transform.scale(Images[Liste[k]],(TailleCase//2,TailleCase//2)), py.Rect(TaillePlateau+2*TailleBordure+20+8*npb,ligne,TailleCase//2,TailleCase//2))

        if Liste[k][0]=='C' or Liste[k][0]=='F':
            ligne+=TailleCase//2

        if Liste[k][0]=='D' or Liste[k][0]=='T':
            ligne+=TailleCase




def drawArcCv2(surf, color, center, radius, width, end_angle):
    width2=width-6
    radius2=radius-3
    circle_image2 = np.zeros((radius2*2+4, radius2*2+4, 4), dtype = np.uint8)
    circle_image2 = cv2.ellipse(circle_image2, (radius2+2, radius2+2),
        (radius2-width2//2, radius2-width2//2), 0, 0, 360, (200,200,200, 255), width2, lineType=cv2.LINE_AA)
    circle_surface = py.image.frombuffer(circle_image2.flatten(), (radius2*2+4, radius2*2+4), 'RGBA')
    surf.blit(circle_surface, circle_surface.get_rect(center = center))

    circle_image = np.zeros((radius*2+4, radius*2+4, 4), dtype = np.uint8)
    circle_image = cv2.ellipse(circle_image, (radius+2, radius+2),
        (radius-width//2, radius-width//2), 0, 0, end_angle, (*color, 255), width, lineType=cv2.LINE_AA)
    circle_surface = py.image.frombuffer(circle_image.flatten(), (radius*2+4, radius*2+4), 'RGBA')
    surf.blit(circle_surface, circle_surface.get_rect(center = center))


if __name__ == '__main__':
    Partie()
