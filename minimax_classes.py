
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

def feval(L,couleur):
    N=[0,0,0,0,0,0]
    B=[0,0,0,0,0,0]
    for i in range(len(L)):
      for el in L[i]:
        if el=="RN": N[0]+=1                                  #nombre de roi noir
        if el=="DN": N[1]+=1                                  # nombre de dames ...
        if el=="TN": N[2]+=1
        if el=="CN": N[3]+=1
        if el=="FN": N[4]+=1
        if el=="PN": N[5]+=1
        if el=="RB": B[0]+=1
        if el=="DB": B[1]+=1
        if el=="TB": B[2]+=1
        if el=="CB": B[3]+=1
        if el=="FB": B[4]+=1
        if el=="PB": B[5]+=1
    if couleur=='noir':
        a=200*(N[0]-B[0]+200)**11  +  9*(N[1]-B[1]+200)**9  +  5*(N[2]-B[2]+200)**7  + 3*(N[3]+N[4]-B[3]-B[4]+200)**5   +     (N[5]-B[5]+200)**3 + (nbr(L,'noir'))
    if couleur=='blanc':
        a=-(200*(N[0]-B[0]-200)**11  +  9*(N[1]-B[1]-200)**9  +  5*(N[2]-B[2]-200)**7  + 3*(N[3]+N[4]-B[3]-B[4]-200)**5   +     (N[5]-B[5]-200)**3 )+ (nbr(L,'blanc'))
    return a                                    # La fonction d'évaluation en une couleur est l'opposé de celle de l'autre couleur





































class Noeud:
    def __init__(self,configuration, poids, mere, filles, profondeur,c,l):   # c=0 noirs, c=1 blancs
        self.configuration=configuration
        self.poids = poids
        self.mere = []
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

    def set_mere(self,mere):
        self.mere=mere

    def set_filles(self,filles):
        self.filles=filles

    def creer_filles(self):
        C=['noir','blanc']
        L=positions_atteignables(self.configuration,C[self.c],[])
        K=[]

        for i in range(len(L)):
            d=deplacement(self.configuration,L[i])
            K.append(Noeud(L[i],0,self.configuration,[],self.profondeur+1,1-self.c,self.l+d))

        self.filles=K

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

    def __str__(self):  #__str__
        return f"Configuration {self.configuration},    poids {self.poids} ,     mere {self.mere} ,     filles {[self.filles[i].__str__() for i in range(len(self.filles))] if type(self.filles)==list else self.filles},    profondeur {self.profondeur} ,     c= {self.c} "





def ARBRE(N,Pmax):
    p=N.profondeur
    c=N.c
    mere=N.mere
    if p<Pmax:
        #******il faut vu les modif de positions_atteignables avoir accés aux coups pr&c&dents, par self.mere ? ajout de l'attribut l dans class Noeud je pense
        A=N.configuration
        L=['noir','blanc']
        couleur=L[N.c]
        l=N.l
        D=positions_atteignables(A,couleur,l)
        RES=[]
        for i in range(len(D)):
            d=deplacement(N.configuration,D[i])
            RES.append( ARBRE( Noeud(D[i],0,A,[],p,1-c,l+d),Pmax-1 ) )


        return Noeud(A,0,mere,RES,p,c,l)
    else:
        return N



def minimax(AR,couleur): # cela ne retourne rien d'intéressant mais modifie l'arbre AR avec les poids que l'on veut
    if AR.filles==[]:
        AR.poids=feval(AR.configuration,couleur)
        return AR.poids
    K=[]
    for i in range(len(AR.filles)):
        K.append(minimax(AR.filles[i],couleur))
    if AR.c==0:
        AR.poids=max(K)
    if AR.c==1:
        AR.poids=min(K)
    return AR.poids

def minimax0(N,Pmax,couleur):
    A=ARBRE(N,Pmax) # N devient un arbre, ce n'est plus seulement un noeud
    if couleur=='noir' and Pmax%2==0: B=minimax(A,'blanc')
    if couleur=='noir' and Pmax%2==1: B=minimax(A,'noir')
    if couleur=='blanc' and Pmax%2==0: B=minimax(A,'noir')
    if couleur=='blanc' and Pmax%2==1: B=minimax(A,'blanc')
    for i in range(len(A.filles)):
        if A.filles[i].poids==A.poids:
            return deplacement(A.configuration,A.filles[i].configuration)
            
def minimax1(A,Pmax,c,couleur):
    N=Noeud(A,0,[],[],0,c,['bonne','partie'])
    return minimax0(N,Pmax,couleur)
