import pygame
import config
import keyboard
import entity
import entitymanager
import assets
import scorekeeper
import player
import enemy


running = False
window = None
clock = None
p = None
score_text = None
health_text = None
small_text = None
lost = False


def init():
    global running
    global clock
    global window
    global small_text
    global p

    running = True

    pygame.init()

    window = pygame.display.set_mode((config.WIDTH, config.HEIGHT))

    pygame.display.set_caption("Anything But That")

    clock = pygame.time.Clock()

    entity.ConcreteEntity(assets.background_image, 0, 0, float("inf"))
    p = player.Player(488, 42)  # can take 14 hits from bullets

    small_text = pygame.font.Font("freesansbold.ttf", 36)


def update():
    global running
    global window
    global p
    global small_text
    global score_text
    global health_text
    global lost

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    clock.tick(config.FPS)

    keyboard.update()
    entitymanager.update(window)

    enemy.update()

    if lost and keyboard.is_key_down(pygame.K_r):
        entitymanager.entities = []
        init()
        scorekeeper.points = 0

    image2 = small_text.render("Points: " + str(scorekeeper.points), False, (255, 0, 0))
    if score_text is not None:
        score_text.kill()
    score_text = entity.ConcreteEntity(image2, 0, 0, float("inf"))

    image3 = small_text.render("Health: " + (str(p.health) if p is not None else "0"), False, (255, 0, 0))
    if health_text is not None:
        health_text.kill()
    health_text = entity.ConcreteEntity(image3, 0, 38, float("inf"))

    pygame.display.flip()

    if p not in entitymanager.entities and not lost:  # you lose
        large_text = pygame.font.Font('freesansbold.ttf', 115)
        image = large_text.render("YOU LOSE", False, (255, 0, 0))
        entity.ConcreteEntity(image, config.WIDTH / 2 - image.get_width() / 2,
                              config.HEIGHT / 2 - image.get_height() / 2, float("inf"))
        otherthing = small_text.render("Press R to retry", False, (255, 0, 0))
        entity.ConcreteEntity(otherthing, config.WIDTH / 2 - otherthing.get_width() / 2,
                              config.HEIGHT / 2 - otherthing.get_height() / 2 + 70, float("inf"))

        highscores = open("scores.dat")
        scores = highscores.read().split(";")
        biggest = 0
        for sc in scores:
            if int(sc) > biggest:
                biggest = int(sc)

        last_thing = small_text.render("You got a HIGHSCORE of: " + str(scorekeeper.points) + "."
                                       if scorekeeper.points > biggest else "Highscore is " + str(biggest) +
                                       "; you did not beat it.",
                                       False, (255, 0, 0))
        entity.ConcreteEntity(last_thing, config.WIDTH / 2 - last_thing.get_width() / 2,
                              config.HEIGHT / 2 - last_thing.get_height() / 2 + 110, float("inf"))

        highscores.close()

        new_file = open("scores.dat", "a")
        new_file.write(";" + str(scorekeeper.points))

        p = None
        lost = True

    if keyboard.is_key_down(pygame.K_ESCAPE):
        running = False


def close():
    pygame.quit()


if __name__ == "__main__":
    init()

    while running:
        update()

    close()
