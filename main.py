from Logic.game import Game
import pygame

SIZE = WIDTH, HEIGHT = 600, 600  # the width and height of our screen
BG_COLOR = pygame.Color('#3f3818')
pygame.display.set_caption("Sola's CRUSH")
FPS = 40


def main():
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    game = Game(screen)
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEMOTION and event.buttons == (0, 0, 1):
                x = event.pos
                if WIDTH >= x[0] >= 0 and HEIGHT >= x[1] >= 0:
                    game.select(event.pos)
                elif len(game.switch) == 1:
                    game.switch = []
                    # print(pygame.BUTTON_RIGHT)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                game.mouse_up = False
                game.select(event.pos)

            if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                if len(game.switch) == 1:
                    game.switch = []
                game.mouse_up = True

        screen.fill(BG_COLOR)
        game.swap()
        game.clean()
        if not game.drop():
            if game.mouse_up and not game.switch:
                game.can_swap = True
            game.correct()
            game.make_suggestion()
        game.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
