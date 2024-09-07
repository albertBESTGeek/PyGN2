import pygame

class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.sprite_sheet = pygame.image.load('../player8.png')
        self.image = self.get_image(6*40, 3*40)
        self.keyColor = '#000000'
        self.image.set_colorkey(self.keyColor)
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
        self.old_position = self.position.copy()
        self.speed = 2

    def save_location(self):
        self.old_position = self.position.copy()

    def change_animation(self, name):
        self.image = self.image[name]
        self.image.set_colorkey(self.keyColor)  # transparent color

    def move_right(self):
        self.position[0] += self.speed

    def move_left(self):
        self.position[0] -= self.speed

    def move_up(self):
        self.position[1] -= self.speed

    def move_down(self):
        self.position[1] += self.speed

    def update(self) -> None:
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def move_back(self):
        self. position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def get_image(self, x, y):
        image = pygame.Surface([40,40])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 40, 40))
        return image

    def animation(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            self.move_up()
            self.get_image(5 * 40, 3 * 40)
        elif pressed[pygame.K_DOWN]:
            self.move_down()
            self.get_image(6 * 40, 3 * 40)
        elif pressed[pygame.K_LEFT]:
            self.move_left()
            self.get_image(7 * 40, 3 * 40)
        elif pressed[pygame.K_RIGHT]:
            self.move_right()
            self.get_image(8 * 40, 3 * 40)


