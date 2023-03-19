import pygame
import pytmx
import pyscroll

from Player import Player


class Game:

    def __init__(self):
        # Crée la fenetre
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("JeuxVideo trop bien")

        # charger la carte
        tmx_data = pytmx.util_pygame.load_pygame('Map test 1.2 .tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2  # zoom 2 fois plus grand

        # générer un joueur
        player_position = tmx_data.get_object_by_name("spawn")
        self.player = Player(player_position.x, player_position.y)

        # liste de stockage des rectangles de collision
        self.walls = []

        for obj in tmx_data.objects:
            if obj.collision:
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=4)
        self.group.add(self.player)

    def update(self):
        self.group.update()

        # verif collision
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back()

    def run(self):

        clock = pygame.time.Clock()

        # Loop Game
        running = True

        while running:

            self.player.save_localisation()
            #self.handle_input()
            self.update()
            self.group.center(self.player.rect.center)
            self.group.draw(self.screen)
            pygame.display.flip()  # actualiser en temps réel

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            clock.tick(60)

        pygame.quit()

if __name__ == '__main__':
    pygame.init()
    game = Game()
    game.run()