import time
import pygame
import pytmx
import pyscroll
from player import Player


class Panneaux:
    def __init__(self):
        self.list = []
        self.examenActif = False
        self.afficheActif = False
        self.iPanneau = -1
        self.textes = []  # liste de string vide

class Game:
    def __init__(self):
        # creation de la fenetre du jeu
        self.panneaux = Panneaux()

        self.screen = pygame.display.set_mode((1600, 900))
        pygame.display.set_caption("Pygamon - Aventure")
        tmx_data = pytmx.util_pygame.load_pygame('../bestCarte.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        self.map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        self.map_layer.zoom = 2
        ## générer un joueur
        player_position = tmx_data.get_object_by_name("player")
        self.player = Player(player_position.x, player_position.y)
        # genere les rectangles de collision
        self.panneaux.examenActif = False
        self.walls = []
        self.panneaux.list = []
        iVar = 0
        for obj in tmx_data.objects:
            # print(obj.type,obj.properties)
            if obj.type == 'collision':
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            if obj.type == 'panneau':
                if 'texte' in obj.properties:
                    iVar += 1
                    print(iVar, obj.type, obj.properties)
                self.panneaux.list.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
                if 'texte' in obj.properties:
                    textePanneau = obj.properties['texte']
                    self.panneaux.textes.append(textePanneau)

        #  dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=4)
        self.group.add(self.player)
    def handle_input(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            self.player.move_up()
            self.player.change_animation('up')
        elif pressed[pygame.K_DOWN]:
            self.player.move_down()
            self.player.change_animation('down')
        elif pressed[pygame.K_LEFT]:
            self.player.move_left()
            self.player.change_animation('left')
        elif pressed[pygame.K_RIGHT]:
            self.player.move_right()
            self.player.change_animation('right')
        elif pressed[pygame.K_a]:  # gestion de la touche A
            if self.panneaux.examenActif:  # il y a un panneau examinable?
                if not self.panneaux.afficheActif:
                    # print('tu examines le panneau ', self.panneaux.iPanneau)
                    print(self.panneaux.textes[self.panneaux.iPanneau])
                    self.panneaux.afficheActif = True
        else:
            pass

    def update(self):
        self.group.update()
        # verif de la collision

        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back()
            iPanneau = sprite.feet.collidelist(self.panneaux.list)
            if iPanneau > -1:
                if not self.panneaux.examenActif:
                    print('[A] examiner ?')
                    self.panneaux.examenActif = True
                self.panneaux.iPanneau = iPanneau
            else:
                self.panneaux.examenActif = False
                self.panneaux.afficheActif = False

    def run(self):
        clock = pygame.time.Clock()
        # boucle du jeu
        running = True
        while running:
            self.player.save_location()  # save la position
            self.handle_input()  # gestion des touches
            self.update()  # recalcule les nouvelles positions, collisions
            self.group.center(self.player.rect.center)  # gèrer la vue
            self.group.draw(self.screen)  # recrée l'affichage
            pygame.display.flip()  # réactualise l'affichage au premier plan
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            clock.tick(100)
        pygame.quit()