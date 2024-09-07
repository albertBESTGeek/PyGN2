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
        self.walls = []
        iVar = 0
        for obj in tmx_data.objects:
            # print(obj.type,obj.properties)
            if obj.type == 'collision':
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        #  dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=4)
        self.group.add(self.player)

    def update(self):
        self.group.update()
        # verif de la collision

        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back()
    def run(self):
        clock = pygame.time.Clock()
        # boucle du jeu
        running = True
        while running:
            self.player.save_location()  # save la position
            self.update()  # recalcule les nouvelles positions, collisions
            self.group.center(self.player.rect.center)  # gèrer la vue
            self.group.draw(self.screen)  # recrée l'affichage
            pygame.display.flip()  # réactualise l'affichage au premier plan
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            clock.tick(100)
        pygame.quit()