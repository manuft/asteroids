import sys

import pygame
from pygame.sprite import Group
from pygame.time import Clock

from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_event, log_state
from player import Player
from shot import Shot


def main():
    pygame.init()

    clock : Clock = pygame.time.Clock()
    dt : float = 0.0

    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    updatable : Group = pygame.sprite.Group()
    drawable : Group = pygame.sprite.Group()
    asteroids : Group = pygame.sprite.Group()
    shots : Group = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, drawable, updatable)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    player: Player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT /2)
    AsteroidField()

    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")

        updatable.update(dt)
        for ast in asteroids:
            if ast.collides_with(player):
                log_event("player_hit")
                print("Game over!")
                sys.exit()

        for ast in asteroids:
            for shot in shots:
                if ast.collides_with(shot):
                    log_event("asteroid_shot")
                    ast.split()
                    shot.kill()

        for drawable_object in drawable:
            drawable_object.draw(screen)

        # Update screen
        pygame.display.flip()

        # set delta time to the number of seconds since last tick call
        dt = clock.tick(60) / 1000



if __name__ == "__main__":
    main()
