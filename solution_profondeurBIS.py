

import pygame as py
class board:
    def __init__(self):
        table_pion=[]
        table_cavalier=[]
        table_fou=[]
        table_dame=[]
        table_tour=[]
        self.table=[table_pion,table_cavalier,table_fou,table_tour,table_dame]
        for i in range(8):
            self.table[0].append([])
            for j in range(8):
                self.table[0][i].append(10*((7-i)*(8-2*int(abs((7-2*j)/2)))))
        for i in range(8):
            self.table[1].append([])
            for j in range(8):
                self.table[1][i].append(320-50*(int(abs((7-2*j)/2))+int(abs((7-2*i)/2))))
        for i in range(8):
            self.table[1].append([])
            for j in range(8):
                self.table[1][i].append(0)
        for i in range(8):
            self.table[1].append([])
            for j in range(8):
                self.table[1][i].append(0   )
        for i in range(8):
            self.table[1].append([])
            for j in range(8):
                self.table[1][i].append(0)
b=board()
#crée une copie indépendente:
def copie(A):
    R=[]
    for i in range(8):
        L=[]
        for j in range(8):
           L.append(A[i][j])
        R.append(L)
    return R

#les 2 prochaines fonction servent à savoir ou sont les rois
def roi_blanc(A):

    for i in range(8):
        for j in range(8):
            if A[i][j]=="RB":
                return [i,j]
    return []

def roi_noir(A):

    for i in range(8):
        for j in range(8):
            if A[i][j]=="RN":
                return [i,j]
    return []


def déplacement_possible(A,i,j,couleur):  #position donnée, i dans P; une pièce
    L=[0,1,2,3,4,5,6,7]
    #rajouter la contrainte "le déplacement d'une pièce ne doit pas laisser à l'autre la possibilité de manger le roi au prochain coup"

    d=[]  #deplacements possibles sans manger
    m=[]  #deplacements possibles en mangeant


    if couleur=='blanc':

    # les pièces blanches


        if A[i][j]=="PB": #pion blanc

            # à chaque fois il faut
            if i-1 in L and j-1 in L and A[i-1][j-1][1]=="N":# non vide et une pièce noire en la case devant à gauche
                m.append([i-1,j-1])
            if i-1 in L and j+1 in L and A[i-1][j+1][1]=="N":# non vide et une pièce noire en la case devant à droite
                m.append([i-1,j+1])
            if i-1 in L and A[i-1][j]=="XX": # case devant le pion vide on ne va pas sortir de l'échiquier
                d.append([i-1,j])

            #codage du possible départ de 2 cases
            #(pion qui n'a pas bougé= pion sur la ligne de départ)
            if i==6 and A[i-1][j]=="XX" and A[i-2][j]=="XX":
                d.append([i-2,j])
            #promotion du pion i=1 sera codé autre part, pareil prise en passant

        if A[i][j]=="CB": #cheval blanc
            e=[[i-2,j-1],[i-2,j+1],[i-1,j-2],[i-1,j+2],[i+1,j-2],[i+1,j+2],[i+2,j-1],[i+2,j+1]]
            # 8 déplacements envisageables pour le cheval
            for u in e:
                if u[0] in L and u[1] in L: # dans le cadre
                    if A[u[0]][u[1]]=="XX": #pas de pièce
                        d.append(u)
                    if A[u[0]][u[1]][1]=="N": # pièce noire
                        m.append(u)


        if A[i][j]=="FB" or A[i][j]=="DB": #fou blanc


            # boucles pour les 4 directions+sens posibles

            c=0
            while True:
                c+=1
                if i-c not in L or j-c not in L: #limite de l'échiquier
                    break
                if A[i-c][j-c]=="XX": #rencontre pas encore de pièce
                    d.append([i-c,j-c])
                else:  #rencontre une pièce
                    if A[i-c][j-c][1]=="B": # de même couleur donc ne peut pas la manger
                        break
                    else:
                        m.append([i-c,j-c])
                        break

            c=0
            while True:
                c+=1
                if i-c not in L or j+c not in L: #limite de l'échiquier
                    break
                if A[i-c][j+c]=="XX": #rencontre pas encore de pièce
                    d.append([i-c,j+c])
                else:  #rencontre une pièce
                    if A[i-c][j+c][1]=="B": # de même couleur donc ne peut pas la manger
                        break
                    else:
                        m.append([i-c,j+c])
                        break

            c=0
            while True:
                c+=1
                if i+c not in L or j-c not in L: #limite de l'échiquier
                    break
                if A[i+c][j-c]=="XX": #rencontre pas encore de pièce
                    d.append([i+c,j-c])
                else:  #rencontre une pièce
                    if A[i+c][j-c][1]=="B": # de même couleur donc ne peut pas la manger
                        break
                    else:
                        m.append([i+c,j-c])
                        break


            c=0
            while True:
                c+=1
                if i+c not in L or j+c not in L: #limite de l'échiquier
                    break
                if A[i+c][j+c]=="XX": #rencontre pas encore de pièce
                    d.append([i+c,j+c])
                else:  #rencontre une pièce
                    if A[i+c][j+c][1]=="B": # de même couleur donc ne peut pas la manger
                        break
                    else:
                        m.append([i+c,j+c])
                        break



        if A[i][j]=="TB" or A[i][j]=="DB": #tour blanche ou dame blanche


            # boucles pour les 4 directions+sens posibles

            c=0
            while True:
                c+=1
                if i-c not in L: #limite de l'échiquier pour un déplacement vers le haut
                    break
                if A[i-c][j]=="XX": #rencontre pas encore de pièce
                    d.append([i-c,j])
                else:  #rencontre une pièce
                    if A[i-c][j][1]=="B": # de même couleur donc ne peut pas la manger
                        break
                    else:
                        m.append([i-c,j])
                        break

            c=0
            while True:
                c+=1
                if j+c not in L: #limite de l'échiquier pour un déplacement vers la droite
                    break
                if A[i][j+c]=="XX": #rencontre pas encore de pièce
                    d.append([i,j+c])
                else:  #rencontre une pièce
                    if A[i][j+c][1]=="B": # de même couleur donc ne peut pas la manger
                        break
                    else:
                        m.append([i,j+c])
                        break

            c=0
            while True:
                c+=1
                if i+c not in L: #limite de l'échiquier pour un déplacement vers le bas
                    break
                if A[i+c][j]=="XX": #rencontre pas encore de pièce
                    d.append([i+c,j])
                else:  #rencontre une pièce
                    if A[i+c][j][1]=="B": # de même couleur donc ne peut pas la manger
                        break
                    else:
                        m.append([i+c,j])


            c=0
            while True:
                c+=1
                if j-c not in L: #limite de l'échiquier pour un déplacement vers la gauche
                    break
                if A[i][j-c]=="XX": #rencontre pas encore de pièce
                    d.append([i,j-c])
                else:  #rencontre une pièce
                    if A[i][j-c][1]=="B": # de même couleur donc ne peut pas la manger
                        break
                    else:
                        m.append([i,j-c])
                        break




        if A[i][j]=="RB": #roi blanc
            e=[[i-1,j-1],[i,j-1],[i+1,j-1],[i,j-1],[i,j+1],[i+1,j-1],[i+1,j],[i+1,j+1]]
            # 8 déplacements envisageables pour le roi
            for u in e:
                if u[0] in L and u[1] in L:
                 # dans le cadre
                    if A[u[0]][u[1]]=="XX": #pas de pièce
                        d.append(u)
                    else:
                        if A[u[0]][u[1]][1]=="N": # pièce blanche
                            m.append(u)






    if couleur=='noir':

    # les pièces noires


        if A[i][j]=="PN": #pion noir
            if i+1 in L and j-1 in L and A[i+1][j-1][1]=="B":# non vide et une pièce blanche en la case devant le pion à gauche
                m.append([i+1,j-1])
            if i+1 in L and j+1 in L and A[i+1][j+1][1]=="B":# non vide et une pièce blanche en la case devant à droite
                m.append([i+1,j+1])
            if i+1 in L and A[i+1][j]=="XX":# case devant le pion vide on ne vas pas sortir de l'échiquier
                d.append([i+1,j])

            #codage du possible départ de 2 cases
            #(pion qui n'a pas bougé= pion sur la ligne de départ)
            if i==1 and A[i+1][j]=="XX" and A[i+2][j]=="XX":
                d.append([i+2,j])
            #promotion du pion i=6 sera codé autre part, pareil prise en passant



        if A[i][j]=="CN": #cheval noir
            e=[[i-2,j-1],[i-2,j+1],[i-1,j-2],[i-1,j+2],[i+1,j-2],[i+1,j+2],[i+2,j-1],[i+2,j+1]]
            # 8 déplacements envisageables pour le cheval
            for u in e:
                if u[0] in L and u[1] in L:
                 # dans le cadre
                    if A[u[0]][u[1]]=="XX": #pas de pièce
                        d.append(u)
                    else:
                        if A[u[0]][u[1]][1]=="B": # pièce blanche
                            m.append(u)

        if A[i][j]=="FN" or A[i][j]=="DN": #fou noir et remarquons que la dame à au moins tous les déplacements d'un fou


            # boucles pour les 4 directions+sens posibles

            c=0
            while True:
                c+=1
                if i-c not in L or j-c not in L: #limite de l'échiquier
                    break
                if A[i-c][j-c]=="XX": #rencontre pas encore de pièce
                    d.append([i-c,j-c])
                else:  #rencontre une pièce
                    if A[i-c][j-c][1]=="N": # de même couleur donc ne peut pas la manger
                        break
                    else:
                        m.append([i-c,j-c])
                        break

            c=0
            while True:
                c+=1
                if i-c not in L or j+c not in L: #limite de l'échiquier
                    break
                if A[i-c][j+c]=="XX": #rencontre pas encore de pièce
                    d.append([i-c,j+c])
                else:  #rencontre une pièce
                    if A[i-c][j+c][1]=="N": # de même couleur donc ne peut pas la manger
                        break
                    else:
                        m.append([i-c,j+c])
                        break

            c=0
            while True:
                c+=1
                if i+c not in L or j-c not in L: #limite de l'échiquier
                    break
                if A[i+c][j-c]=="XX": #rencontre pas encore de pièce
                    d.append([i+c,j-c])
                else:  #rencontre une pièce
                    if A[i+c][j-c][1]=="N": # de même couleur donc ne peut pas la manger
                        break
                    else:
                        m.append([i+c,j-c])
                        break


            c=0
            while True:
                c+=1
                if i+c not in L or j+c not in L: #limite de l'échiquier
                    break
                if A[i+c][j+c]=="XX": #rencontre pas encore de pièce
                    d.append([i+c,j+c])
                else:  #rencontre une pièce
                    if A[i+c][j+c][1]=="N": # de même couleur donc ne peut pas la manger
                        break
                    else:
                        m.append([i+c,j+c])
                        break


        if A[i][j]=="TN" or A[i][j]=="DN": #tour noire et une dame se déplace pareil qu'une tour et même plus


            # boucles pour les 4 directions+sens posibles

            c=0
            while True:
                c+=1
                if i-c not in L: #limite de l'échiquier pour un déplacement vers le haut
                    break
                if A[i-c][j]=="XX": #rencontre pas encore de pièce
                    d.append([i-c,j])
                else:  #rencontre une pièce
                    if A[i-c][j][1]=="N": # de même couleur donc ne peut pas la manger
                        break
                    else:
                        m.append([i-c,j])
                        break

            c=0
            while True:
                c+=1
                if j+c not in L: #limite de l'échiquier pour un déplacement vers la droite
                    break
                if A[i][j+c]=="XX": #rencontre pas encore de pièce
                    d.append([i,j+c])
                else:  #rencontre une pièce
                    if A[i][j+c][1]=="N": # de même couleur donc ne peut pas la manger
                        break
                    else:
                        m.append([i,j+c])
                        break

            c=0
            while True:
                c+=1
                if i+c not in L: #limite de l'échiquier pour un déplacement vers le bas
                    break
                if A[i+c][j]=="XX": #rencontre pas encore de pièce
                    d.append([i+c,j])
                else:  #rencontre une pièce
                    if A[i+c][j][1]=="N": # de même couleur donc ne peut pas la manger
                        break
                    else:
                        m.append([i+c,j])
                        break


            c=0
            while True:
                c+=1
                if j-c not in L: #limite de l'échiquier pour un déplacement vers la gauche
                    break
                if A[i][j-c]=="XX": #rencontre pas encore de pièce
                    d.append([i,j-c])
                else:  #rencontre une pièce
                    if A[i][j-c][1]=="N": # de même couleur donc ne peut pas la manger
                        break
                    else:
                        m.append([i,j-c])
                        break





        if A[i][j]=="RN": #roi noir
            e=[[i-1,j-1],[i,j-1],[i+1,j-1],[i,j-1],[i,j+1],[i+1,j-1],[i+1,j],[i+1,j+1]]
            # 8 déplacements envisageables pour le roi
            for u in e:
                if u[0] in L and u[1] in L: # dans le cadre
                    if A[u[0]][u[1]]=="XX": #pas de pièce
                        d.append(u)
                    else:
                        if A[u[0]][u[1]][1]=="B": # pièce blanche
                            m.append(u)



    res=m+d

    return res
      # on ne distinguer les coup où l'on mange de ceux dont l'on mange pas ?

        #on a compté le cas "XX"=A[i][j]

        # je n'ai pas compté le cas où une pièce reste sur place, puisqu'avec la définition de positions_atteignables cela fontionne en explorant tous les i,j




def piece_mangeable(A,i,j,couleur): #teste si la pièce en i,j est mangeable au prochain coup (celui à qui c'est de jouer=couleur)

    # pt de vue du joueur suivant
    for p in positions_atteignables0(A,couleur):
        if A[i][j][1]!=p[i][j][1]:
            # on ne peut manger qu'une pièce de couleur opposée
            if couleur=='blanc' and A[i][j][1]=='N':
                return True
            if couleur=='noir' and A[i][j][1]=='B':
                return True

    return False # si la case i,j est vide ou si la pièce est mangeable

def creer_vide():
    A=[]
    for i in range(8):
        L=[]

        for j in range(8):
            L.append("XX")
        A.append(L)
    return A


def positions_atteignables_case(A,i,j,couleur):
    RES=[]  # liste de matrices 8*8
    D=déplacement_possible(A,i,j,couleur)


    for k in range(len(D)): # les positions accessibles
        o=A[i][j]
        a,b=D[k][0],D[k][1]
        Position_accessible=creer_vide()
        for i1 in range(8):
            for j1 in range(8):
                Position_accessible[i1][j1]=A[i1][j1]

        Position_accessible[i][j]="XX"  # la pièce quitte sa place
        Position_accessible[a][b]=o  # pour occuper l'autre case
        RES.append(Position_accessible)


    return RES




def positions_atteignables0(A,couleur):   # A=l'échiquier, et on a la donnée de "à qui le tour ?"      reourner une listes de matrice 8*8 du type liste de liste
    res=[]
    for i in range(8):
        for j in range(8):
            p=positions_atteignables_case(A,i,j,couleur)
            if len(p)!=0:
                res=res+p


    return res

def piecebouge(A,i,j,l):
    for e in l:
        if e[0]==[i,j]:
            return True
    return False


# il faut rajouter la condition que ni le roi ni la tour n'a bougé
def roque(A,couleur,l): #A la position, couleur : à qui c'est de jouer, l la liste des coups qui ont été joués
    #il faut pas qu'il y ai de pièce entre le roi et la tour
    res=[]
    if couleur=='noir' and A[0][4]=='RN' and not piecebouge(A,0,4,l):
        # grand roque : on examine chaque case du déplacement du roi : si il y a une pièce entre les deux ou une menace c'est mort
        if A[0][0]=='TN' and not piecebouge(A,0,0,l):
            c=True
            for j in range(1,4):
                if A[0][j]!='XX' or piece_mangeable(A,0,j,'blanc'):
                    c=False
            if A[0][4]!='RN' or piece_mangeable(A,0,4,'blanc'):
                c=False
            if c:
                B=copie(A)
                B[0][0]='XX'
                B[0][4]='XX'
                B[0][2]='RN'
                B[0][3]='TN'
                res.append(B)

        #petit roque : on examine chaque case du déplacement du roi : si il y a une pièce entre les deux ou une menace c'est mort
        if A[0][7]=='TN' and not piecebouge(A,0,7,l):
            c=True
            for j in range(5,7):
                if A[0][j]!='XX' or piece_mangeable(A,0,j,'blanc'):
                    c=False
            if A[0][4]!='RN' or piece_mangeable(A,0,4,'blanc'):
                c=False

            if c:
                B=copie(A)

                B[0][7]='XX'
                B[0][6]='RN'
                B[0][4]='XX'
                B[0][5]='TN'
                res.append(B)


    if couleur=='blanc' and A[7][4]=='RB' and not piecebouge(A,7,4,l):
        # grand roque : on examine chaque case du déplacement du roi : si il y a une pièce entre les deux ou une menace c'est mort
        if A[7][0]=='TB' and not piecebouge(A,7,0,l):
            c=True
            for j in range(5,7):
                if A[7][j]!='XX' or piece_mangeable(A,7,j,'noir'):
                    c=False
            if A[7][4]!='RB' or piece_mangeable(A,7,4,'noir'):
                c=False
            if c:
                B=copie(A)
                B[7][7]='XX'
                B[7][6]='RB'
                B[7][4]='XX'
                B[7][5]='TB'
                res.append(B)

        #petit roque : on examine chaque case du déplacement du roi : si il y a une pièce entre les deux ou une menace c'est mort
        if A[7][7]=='TB' and not piecebouge(A,7,7,l):
            c=True
            for j in range(1,4):
                if A[7][j]!='XX' or piece_mangeable(A,7,j,'noir'):
                    c=False
            if A[7][4]!='RB' or piece_mangeable(A,7,4,'noir'):
                c=False

            if c:
                B=copie(A)
                B[7][0]='XX'
                B[7][4]='XX'
                B[7][2]='RB'
                B[7][3]='TB'
                res.append(B)

    return res





     # il faut pion sur la première ligne et si il avance de 2 et qu'il attérie à coté d'un autre pion alors l'autre pion peut le manger comme si il n'avait avancé que d'un
def prise_en_passant(A,couleur,der): # il faut savoir si le dernier coup est le pion qui avance de 2
    L=[0,1,2,3,4,5,6,7]
    #der=********** dernier coup joué par le joueur d'avant cf autre fichier (liste de 2 points du type [x,y]
    res=[]
    for j in range(8):
        if couleur=='blanc' and der==[[1,j],[3,j]] and A[3][j]=='PN': # maintenant c'est aux blanc de peut etre faire pp
            if j-1 in L and A[3][j-1]=='PB':
                B=copie(A)
                B[3][j]='XX'
                B[3][j-1]='XX'
                B[2][j]='PB'
                res.append(B)

            if j+1 in L and A[3][j+1]=='PB':
                B=copie(A)
                B[3][j]='XX'
                B[3][j+1]='XX'
                B[2][j]='PB'
                res.append(B)


        if couleur=='noir' and der==[[6,j],[4,j]] and A[4][j]=='PB':# maintenant c'est aux blanc de peut etre faire pp
            if j-1 in L and A[4][j-1]=='PN':
                B=copie(A)
                B[4][j]='XX'
                B[4][j-1]='XX'
                B[5][j]='PN'
                res.append(B)

            if j+1 in L and A[4][j+1]=='PN':
                B=copie(A)
                B[4][j]='XX'
                B[4][j+1]='XX'
                B[5][j]='PN'
                res.append(B)

    return res


def promotion_du_pion(A,couleur):
    res=[]
    L=[i for i in range(8)]
    for j in range(8):
        if couleur=='blanc' and A[1][j]=='PB':
            if A[0][j]=='XX':
                B=copie(A)
                B[1][j]='XX'
                B[0][j]='DB'# à l'avenir il faudra proposer le choix
                res.append(B)
            if j-1 in L and  A[0][j-1][1]=='N':
                B=copie(A)
                B[1][j]='XX'
                B[0][j-1]='DB'# à l'avenir il faudra proposer le choix
                res.append(B)
            if j+1 in L and A[0][j+1][1]=='N':
                B=copie(A)
                B[1][j]='XX'
                B[0][j+1]='DB'# à l'avenir il faudra proposer le choix
                res.append(B)
        if couleur=='noir' and A[6][j]=='PN':
            if A[7][j]=='XX':
                B=copie(A)
                B[6][j]='XX'
                B[7][j]='DN'# à l'avenir il faudra proposer le choix
                res.append(B)
            if j-1 in L and A[7][j-1][1]=='B':
                B=copie(A)
                B[6][j]='XX'
                B[7][j-1]='DN'# à l'avenir il faudra proposer le choix
                res.append(B)
            if j+1 in L and A[7][j+1][1]=='B':
                B=copie(A)
                B[6][j]='XX'
                B[7][j+1]='DN'# à l'avenir il faudra proposer le choix
                res.append(B)

    return res




def positions_atteignables(A,couleur,l): #faut il ajouter la liste des coups joué en argument, peut ^tre il faudrait tout fusionner (autre .py)
    if l==[]:
        return positions_atteignables0(A,couleur)
    der=l[-1]
    return positions_atteignables0(A,couleur)+prise_en_passant(A,couleur,der)+roque(A,couleur,l) +promotion_du_pion(A,couleur)




def deplacement(I,F): #deux matrices

    for i in range(8):
        for j in range(8):
            if I[i][j]!=F[i][j]:
                if F[i][j]=='XX':
                    ci=[i,j]
                else:
                    cf=[i,j]

    return [ci,cf]



















# maintenant corrigeons la fonction précédente pour que les roi ne soient pas suicidaires



#le joueur=couleur a joué pour aboutir à P mais sont coût laissait l'opportunité à l'adv de manger son roi
def coup_preced_illegal(P,couleur,l):

    if couleur=='noir':
        for p in positions_atteignables(P,'blanc',l):
            if len(roi_noir(p))!=2:  # les 2 indices qui définissent l'emplacements du roi noir existent
                return True # alors le coup coup précédent dans la partie était illégal
        return False

    if couleur=='blanc':
        for p in positions_atteignables(P,'noir',l):
            if len(roi_blanc(p))!=2:  # les 2 indices qui définissent l'emplacements du roi noir existent
                return True # alors le coup coup précédent dans la partie était illégal
        return False



# le roi évite à tout prix de se faire manger !!!
def positions_atteignables_legales(A,couleur,l):
    L=positions_atteignables(A,couleur,l)
    res=[]
    for k in range(len(L)):
        if not coup_preced_illegal(L[k],couleur,l):
            res.append(L[k])


    if len(res)==0 and couleur=='blanc':
        if piece_mangeable(A,roi_noir(A)[0],roi_noir(A)[1],'blanc'):
            return 'blancs matent'
    if len(res)==0 and couleur=='noirs':
        if piece_mangeable(A,roi_blanc(A)[0],roi_blanc(A)[1],'noir'):
            return 'noirs matent'

    if len(res)==0:
        return 'pat'

    return res
# normalement si on par d'une position légale (au prochain tour les 2 rois sont présents) alors on ne tombera pas dans une position illégale, et lorsque ça retourne une liste vide c'est le mat ou le pat

def nbr(A,couleur):
    return len(positions_atteignables0(A,couleur))

def feval(L):
    N=[0,0,0,0,0,0]
    B=[0,0,0,0,0,0]
    PB=[]
    PN=[]
    DN=[]
    DB=[]
    TN=[]
    TB=[]
    CN=[]
    CB=[]
    FN=[]
    FB=[]
    for i in range(len(L)):
      for j in range(len(L[i])):
        if L[i][j]=="RN": N[0]+=1                                  #nombre de roi noir
        if L[i][j]=="DN": 
            N[1]+=1                                  # nombre de dames ...
            DN.append([i,j])
        if L[i][j]=="TN": 
            N[2]+=1
            TN.append([i,j])
        if L[i][j]=="CN": 
            N[3]+=1
            CN.append([i,j])
        if L[i][j]=="FN": 
            N[4]+=1
            FN.append([i,j])
        if L[i][j]=="PN": 
            N[5]+=1
            PN.append([i,j])
        if L[i][j]=="RB":  B[0]+=1
        if L[i][j]=="DB": 
            B[1]+=1
            DB.append([i,j])
        if L[i][j]=="TB": 
            B[2]+=1
            TB.append([i,j])
        if L[i][j]=="CB": 
            B[3]+=1
            CB.append([i,j])
        if L[i][j]=="FB": 
            B[4]+=1
            FB.append([i,j])
        if L[i][j]=="PB": 
            B[5]+=1
            PB.append([i,j])
    material= (9999*(N[0]-B[0])  +  900*(N[1]-B[1])  +  500*(N[2]-B[2]) + 330*(N[4]-B[4])  + 320*(N[3]-B[3])    +     100*(N[5]-B[5]))
    VPB=0
    VPN=0
    VCN=0
    VCB=0
    VFN=0
    VFB=0
    VTN=0
    VTB=0
    VDN=0
    VDB=0
    for i in range(len(PB)):
        VPB+=b.table[0][PB[i][0]][PB[i][1]]
    for i in range(len(PN)):
        VPN+=b.table[0][7-PN[i][0]][PN[i][1]]
    for i in range(len(CN)):
        VCN+=b.table[1][7-CN[i][0]][CN[i][1]]
    for i in range(len(CB)):
        VCB+=b.table[1][CB[i][0]][CB[i][1]]
    """
    for i in range(len(FN)):
        VFN+=b.table[2][7-FN[i][0]][FN[i][1]]
    for i in range(len(FB)):
        VFB+=b.table[2][FB[i][0]][FB[i][1]]
    for i in range(len(TN)):
        VTN+=b.table[3][7-TN[i][0]][TN[i][1]]
    for i in range(len(TB)):
        VTB+=b.table[3][TB[i][0]][TB[i][1]]
    for i in range(len(DB)):
        VDB+=b.table[4][DB[i][0]][DB[i][1]]
    for i in range(len(DN)):
        VDN+=b.table[4][7-DN[i][0]][DN[i][1]]
    """
    PSQ=VPB-VPN
    CSQ=VCB-VCN
    FSQ=VFB-VFN
    DSQ=VDB-VDN
    TSQ=VTB-VTN
    boardvalue=material-(PSQ+CSQ+FSQ+DSQ+TSQ)
    return boardvalue







class Noeud:
    def __init__(self,configuration, poids, mere, filles, profondeur,c,l):   # c=0 noirs, c=1 blancs
        self.configuration=configuration
        self.poids = poids
        self.mere = mere
        self.c=c
        L=['noir','blanc']
        self.filles = filles
        if type(self.filles)==list:
            for i in range(len(self.filles)):
                self.filles[i]=self.filles[i]

        self.profondeur = 0
        #ajout attribut l= liste des coups joués
        self.l=l


    def set_configuration(self,configuration):
        self.configuration=configuration

    def set_poids(self,poids):
        self.poids=poids



    def set_filles(self,filles):
        self.filles=filles


    def set_soeurs(self,poids):
        for i in range(len(self.mere.filles)):
            if self.mere.filles[i].poids!=self.poids:
                self.mere.filles[i].poids=poids




    def creer_filles0(self):
        C=['noir','blanc']
        L=positions_atteignables(self.configuration,C[self.c],[])
        K=[]

        for i in range(len(L)):
            d=deplacement(self.configuration,L[i])
            configuration=L[i]
            c=1-self.c
            l=self.l+d
            K.append(Noeud(configuration,0,self.mere+[i],[],0,c,l))   #on marque le chemin

        return K

    def creer_filles(self):
        self.filles=self.creer_filles0()



    def get_profondeur(self):
        if len(self.mere)==0:
            return 0
        else:
            m=self.mere
            return m.profondeur+1

    def set_profondeur(self,profondeur):
        self.profondeur=profondeur

    def set_c(self,c):
        self.c=c

    # (valable pour toutes les fonctions élagage) les hypothese (critere qui disent quand appliquer cette méthode seront spécifié dans la fonction d'utilisant
    def set_elagage_alpha(self):
        m=self.mere
        l=len(m.filles)
        assert m!=0
        p=self.poids
        for i in range(m):
            for j in range(m):
                if m.filles[i].filles[j].poids<p and self.c==1: #à self, les blancs jouent donc maximisent feval (le poids)
                    m.filles.pop(i)
                    break




                if m.filles[i].filles[j].poids>p and self.c==0: #à self, les jouent jouent donc minimisent feval (le poids)
                    m.filles.pop(i)
                    break
    def heuristique(self): #choix de la fille la plus prometteuse
        pass

    def set_elagage_grand_tonton(self):
        pass #à coder


    def __str__(self):  #__str__
        return f"Configuration {self.configuration},    poids {self.poids} ,     mere {self.mere} ,     filles {[self.filles[i].__str__() for i in range(len(self.filles))] if type(self.filles)==list else self.filles},    profondeur {self.profondeur} ,     c= {self.c} "



    #indexation : à chaque Noeud je donne un référence
def get_mere(self,AR): #self est un sous du noeud qu'est l'arbre
    x=AR
    if self==AR:
        return []
    L=self.mere
    if len(L)>0:
        L.pop()
    while len(L)>0:
        x=x.filles[L.pop(0)]
    return x




#
#
# def ARBRE(N,Pmax):  # dans créer arbre il faut mettre à jour les meres
#     p=N.profondeur
#     c=N.c
#
#     if p<Pmax:  #N ne change pas dans la récursivité ça pose pb
#         #******il faut vu les modif de positions_atteignables avoir accés aux coups pr&c&dents, par self.mere ? ajout de l'attribut l dans class Noeud je pense
#         A=N.configuration
#         L=['noir','blanc']
#         couleur=L[N.c]
#         l=N.l
#         D=positions_atteignables(A,couleur,l)
#         RES=[]
#
#         for i in range(len(D)):
#             d=deplacement(N.configuration,D[i])
#
#             RES.append( ARBRE( Noeud(D[i],0,N.mere+[i],[],p,1-c,l+d),Pmax-1 ) )
#
#
#         return Noeud(A,0,N.mere,RES,p,c,l)
#     else:
#         return N




def ARBRE(N,Pmax):
    if Pmax>=1:
        N.creer_filles()
        if Pmax>=2:
            for i in range(len(N.filles)):
                N.filles[i].creer_filles()
                if Pmax>=3:
                    for j in range(len(N.filles[i].filles)):
                        N.filles[i].filles[j].creer_filles()
                        if Pmax>=4:
                            for k in range(len(N.filles[i].filles[j].filles)):
                                N.filles[i].filles[j].filles[k].creer_filles()
    return N



A=[['TN', 'CN', 'FN', 'DN', 'RN', 'FN', 'CN', 'TN'], ['PN', 'PN', 'PN', 'PN', 'PN', 'PN', 'PN', 'PN'], ['XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX'], ['XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX'], ['XX', 'XX', 'XX', 'PB', 'XX', 'XX', 'XX', 'XX'], ['XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX'], ['PB', 'PB', 'PB', 'PB', 'PB', 'PB', 'PB', 'PB'], ['XX', 'CB', 'FB', 'DB', 'RB', 'FB', 'CB', 'TB']]
AR=ARBRE(Noeud(A,0,[],[],0,0,['bonne','partie']),2)
##
# e=AR
# for i in range(len(AR.filles)):
#     print(get_mere(AR.filles[i],AR)==AR)
#     for j in range(len(AR.filles[i].filles)):
#         print(get_mere(AR.filles[i].filles[j],AR)==AR.filles[i])
#         print(get_mere(get_mere(AR.filles[i].filles[j],AR),AR)==AR)        la methode get_mere marche bien !!!!


def Pmax(AR):# ca marche et normalement ca modifie pas l'arbre
    c=0
    A=AR
    while A.filles!=[]:

        c+=1
        A=A.filles[0]
    return c








def elagage0(A,Pmax,c): #pour mieux comprendre, faire cet algo sous forme de graphe d'état, puis essayer avec un exemple
    N=Noeud(A,0,[],[],0,c,['bonne','partie'])
    AR=ARBRE(N,Pmax)

    X=AR



    while True:
        if len(X.filles)!=0:   # X a une fille
            z=False

            for i in range(len(X.filles)):
                if X.filles[i].profondeur!=-1: # X a une fille non modifiée
                    X=X.filles[i]
                    z=True
                    break    # on descend sur la première fille non modifiée




            if not z:     # X a une/des fille; elles sont toute(s) modifiée(s)    ->application de minimax
                L=[X.filles[i].poids for i in range(len(X.filles))]
                if X.c==0:
                    X.poids=max(L)


                if X.c==1:
                    X.poids=min(L)


                X.profondeur=-1

                #on voit si on est à la racine, auquel cas on sor
                M=get_mere(X,AR)
                if type(M)==list:
                    break
                else:
                    X=M





        else:  #c'est forcément une feuille
            X.poids=feval(X.configuration)
            X.profondeur=-1
            M=get_mere(X,AR)
            if type(M)==list:
                return X
            else:
                X=M



    return X





A=[
        ["TN","CN","FN","DN","RN","FN","CN","TN"],
        ["PN","PN","PN","PN","PN","PN","PN","PN"],
        ["XX","XX","XX","XX","XX","XX","XX","XX"],
        ["XX","XX","PN","XX","XX","XX","XX","XX"],
        ["XX","XX","XX","PB","XX","XX","XX","XX"],
        ["XX","XX","XX","XX","XX","XX","XX","XX"],
        ["PB","PB","PB","PB","PB","PB","PB","PB"],
        ["XX","CB","FB","DB","RB","FB","CB","TB"],
        ]

# N=Noeud(A,0,[],[],0,0,['bonne','partie'])
# AR1=elagage0(A,4,0,'noir')
# print(AR1.filles[0].filles[0].poids)
# print(AR1.filles[0].filles[0].profondeur)
# print(AR1.filles[0].poids)
# print(AR1.filles[0].profondeur)
# print(AR1.poids)
# print(AR1.profondeur)













def elagage(A,Pmax,c):
    X=elagage0(A,Pmax,c)
    for i in range(len(X.filles)):
        if X.filles[i].poids==X.poids:
            return deplacement(X.configuration,X.filles[i].configuration)

AR=elagage0(A,2,0)
d=elagage(A,2,0)
print(AR.poids)
print(feval(A))


###


#
# import time
# t=time.time()
#
# N=Noeud(A, 0, [], [], 0,0,[])
# a=ARBRE(N,2)
#
#
# t1=time.time()
# print(t1-t)

# b=minimax1([
#         ["TN","CN","FN","DN","RN","FN","CN","TN"],
#         ["PN","PN","PN","PN","PN","PN","PN","PN"],
#         ["XX","XX","XX","XX","XX","XX","XX","XX"],
#         ["XX","XX","XX","XX","XX","XX","XX","XX"],
#         ["XX","XX","XX","XX","XX","XX","XX","XX"],
#         ["XX","XX","XX","XX","XX","XX","XX","XX"],
#         ["PB","PB","PB","PB","PB","PB","PB","PB"],
#         ["TB","CB","FB","DB","RB","FB","CB","TB"],
#         ],2,0,'blanc')
# t2=time.time()
# print(t2-t1)
# print('ratio Tarbre/Tminimax')
# print((t1-t)/(t2-t1))
