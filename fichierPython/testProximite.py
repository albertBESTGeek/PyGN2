
import pygame
import sys

pygame.init()

# Dimensions de la fenêtre et des éléments
screen_width, screen_height = 640, 480
tile_size = 32

# Créer la fenêtre
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Proximity Text Display")

# Couleurs
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)

# Position initiale du joueur
player_pos = [100, 100]
player_size = 32

# Panneau
panel_pos = [200, 200]
panel_size = 32

# Police pour le texte
font = pygame.font.Font(None, 36)


# Fonction pour vérifier si le joueur est proche
def is_near(player_pos, panel_pos, threshold=100):
    return abs(player_pos[0] - panel_pos[0]) < threshold and abs(player_pos[1] - panel_pos[1]) < threshold


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_pos[0] -= 5
    if keys[pygame.K_RIGHT]:
        player_pos[0] += 5
    if keys[pygame.K_UP]:
        player_pos[1] -= 5
    if keys[pygame.K_DOWN]:
        player_pos[1] += 5

    if is_near(player_pos, panel_pos):
        text = font.render("TU ES PROCHE DU PANNEAU !", True, blue)
    else:
        text = None

    # Dessiner tout
    screen.fill(black)  # Fond noir
    pygame.draw.rect(screen, blue, (*panel_pos, panel_size, panel_size))  # Panneau
    if text:
        screen.blit(text, (panel_pos[0] - 40, panel_pos[1] - 40))
    pygame.draw.rect(screen, white, (*player_pos, player_size, player_size))  # Joueur
    pygame.display.flip()
    pygame.time.Clock().tick(60)

# Quitter Pygame
pygame.quit()
sys.exit()