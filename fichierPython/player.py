import pygame
def machineAEtats(etatActuel:str,touche:str,mat:{str:{str:str}}):
    nouvelEtat = mat[etatActuel][touche] # renvoie le nouvel état pour l'état actuel
                                    # etatActuel dans le cas où touche est appuyée
    return nouvelEtat

class Player(pygame.sprite.Sprite):
    def initializeMatrice(self, n: int = 4):
        '''
        initialise la matrice de transition (dico de dicos avec le code suivant:
        pour l'état du personnage : rd (rest-down), 0d, 1d, 2d,...,(n-1)d
                                    puis $l , $u, $r
        pour l'état des touches : u (Up), d(Down), r (Right), l (Left), N (none)
        '''
        # création des états pour le personnage
        dicoMat = {}  # initialisation du dico
        images = {}
        listeDirections = ['d', 'l', 'r','u']
        for direction in listeDirections:  # direction du personnage
            # GESTION DES ETATS DE MOUVEMENT
            for i in range(n):
                etatPersonnage = str(i) + direction  # état i et direction direction
                # print(etatPersonnage)
                # creer une nouvelle entrée du dictionnaire
                j = (i + 1) % n  # reste de la division => état suivant
                dicoMat[etatPersonnage] = {direction: str(j) + direction}  # on poursuit le mouvement
                autresDirections = [e for e in listeDirections if e != direction]
                for autreDirec in autresDirections:  # pour les autres directions
                    dicoMat[etatPersonnage][autreDirec] = '0' + autreDirec
                # état de repos
                dicoMat[etatPersonnage]['N'] = 'r' + direction  # état de repos
            # gestion des états de repos
            dicoMat['r' + direction] = {'u': '1u', 'd': '1d', 'r': '1r', 'l': '1l', 'N': 'r' + direction}
        for etat in dicoMat:
            j = listeDirections.index(etat[1]) # d l r u = 0 1 2 3
            if etat[0] =='r': i=1
            else:
                i=int(etat[0])
            # print(etat,i,j)
            images[etat]=self.get_image(i*32, j*32)
            images[etat].set_colorkey(self.keyColor)

        return images,dicoMat
    def __init__(self, x, y):
        super().__init__()
        self.sprite_sheet = pygame.image.load('../player.png')
        self.image = self.get_image(0, 0)
        self.keyColor = '#000000'
        self.image.set_colorkey(self.keyColor)
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.state='rd'
        # self.images = {
        #     'down': self.get_image(0*32, 0*32),
        #     'left': self.get_image(0*32, 1*32),
        #     'right': self.get_image(0*32, 2*32),
        #     'up': self.get_image(0*32, 3*32),
        # }
        # self.image=self.defineImages()
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
        self.old_position = self.position.copy()
        self.speed = 2
        self.images,self.mat = self.initializeMatrice(n=3)
        self.dicoMove={'d':(0,1),'l':(-1,0),'r':(+1,0),'u':(0,-1)}
    def save_location(self):
        self.old_position = self.position.copy()
    def setNewState(self,codeDir):
        newState=machineAEtats(self.state,codeDir,self.mat)
        # print(self.state,codeDir,newState)
        self.state = newState
        self.image=self.images[self.state]
    # def change_animation(self, name):
    #     self.image = self.images[name]
    #     self.image.set_colorkey(self.keyColor)  # transparent color

    def move_direction(self,codeDir):
        i,j = self.dicoMove[codeDir]
        self.position[0] += i*self.speed
        self.position[1] += j*self.speed

    # def move_right(self):
    #     self.position[0] += self.speed
    #
    # def move_left(self):
    #     self.position[0] -= self.speed
    #
    # def move_up(self):
    #     self.position[1] -= self.speed
    #
    # def move_down(self):
    #     self.position[1] += self.speed
    def update(self) -> None:
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def move_back(self):
        self. position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def get_image(self, x, y):
        image = pygame.Surface([32,32])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))
        return image
