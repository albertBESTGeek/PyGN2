def machineAEtats(etatActuel:str,touche:str,mat:{str:{str:str}}):
    nouvelEtat = mat[etatActuel][touche] # renvoie le nouvel état pour l'état actuel
                                    # etatActuel dans le cas où touche est appuyée
    return nouvelEtat
def initialiseMatrice(n:int=4):
    '''
    initialise la matrice de transition (dico de dicos avec le code suivant:
    pour l'état du personnage : rd (rest-down), 0d, 1d, 2d,...,(n-1)d
                                puis $l , $u, $r
    pour l'état des touches : u (Up), d(Down), r (Right), l (Left), N (none)
    '''
    # création des états pour le personnage
    dicoMat = {} #initialisation du dico
    listeDirections = ['d','l', 'u', 'r']
    for direction in listeDirections: # direction du personnage
        # GESTION DES ETATS DE MOUVEMENT
        for i in range(n):
            etatPersonnage = str(i)+direction # état i et direction direction
            # print(etatPersonnage)
            # creer une nouvelle entrée du dictionnaire
            j = (i+1) % n #reste de la division => état suivant
            dicoMat[etatPersonnage] = {direction:str(j)+direction} # on poursuit le mouvement
            autresDirections = [e for e in listeDirections if e != direction]
            for autreDirec in autresDirections: # pour les autres directions
                dicoMat[etatPersonnage][autreDirec]='0'+autreDirec
            # état de repos
            dicoMat[etatPersonnage]['N']='r'+direction #état de repos
        # gestion des états de repos
        dicoMat['r'+direction]={'u':'1u', 'd':'1d','r':'1r', 'l':'1l','N':'r'+direction}
    return dicoMat
if __name__=='__main__':
    maT = initialiseMatrice(n=4)