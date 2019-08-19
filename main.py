import pygame
import config
import keyboard
import entity
import entitymanager
import assets
import sound_player
import scorekeeper
import player
import os
import enemy
import weapon


__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


running = False
window = None
clock = None
p = None
score_text = None
health_text = None
small_text = None
lost = False
count = 0
in_store = False
potential_purchases = []
purchase_count = 0


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

    scorekeeper.cumulated = 0

    sound_player.init()
    sound_player.music()

    pygame.mixer.music.set_endevent(pygame.USEREVENT + 1)


def update():
    global running
    global window
    global p
    global small_text
    global score_text
    global health_text
    global lost
    global in_store
    global potential_purchases
    global count
    global purchase_count

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.USEREVENT + 1:
            sound_player.music()

    clock.tick(config.FPS)

    keyboard.update()

    count += 1
    if keyboard.is_key_down(pygame.K_s) and count > 30 and not lost:
        count = 0
        in_store = not in_store

    if in_store:
        alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k"]
        key_linker = {"a": pygame.K_a, "b": pygame.K_b, "c": pygame.K_c, "d": pygame.K_d, "e": pygame.K_e,
                      "f": pygame.K_f, "g": pygame.K_g, "h": pygame.K_h, "i": pygame.K_i, "j": pygame.K_j,
                      "k": pygame.K_k}
        potential_purchases = [w for w in weapon.weapons if w not in p.weapons]

        purchase_count += 1
        if keyboard.is_key_down(pygame.K_z) and p.health < 42 and scorekeeper.points >= 10 and purchase_count > 30:
            # purchase health
            p.health += 3
            scorekeeper.points -= 10
            if p.health > 42:
                p.health = 42
            purchase_count = 0

        cthing = 0
        window.blit(assets.background_image, (0, 0))
        tiny_text = pygame.font.Font("freesansbold.ttf", 24)

        for purchase in potential_purchases:
            if keyboard.is_key_down(key_linker[alphabet[cthing]]) \
                    and scorekeeper.points >= purchase.cost and purchase_count > 30:
                p.weapons.append(purchase)
                scorekeeper.points -= purchase.cost
                purchase_count = 0

            img = tiny_text.render("Press " + alphabet[cthing] + " to purchase " + purchase.name + " for " +
                                   str(purchase.cost) + " points", False, (0, 255, 0)
                                   if purchase.cost <= scorekeeper.points else (255, 0, 0))
            window.blit(img, (0, cthing * 40))
            cthing += 1
        img = tiny_text.render("Press z to repair by 3 health for 10 points",
                               False, ((0, 255, 0) if scorekeeper.points > 10 else (255, 0, 0)))
        window.blit(img, (0, cthing * 40))
        pygame.display.flip()
        return

    entitymanager.update(window)

    enemy.update()

    if lost and keyboard.is_key_down(pygame.K_r):
        entitymanager.entities = []
        lost = False
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
        otherthing = small_text.render("Press R to retry", False, (0, 0, 255))
        entity.ConcreteEntity(otherthing, config.WIDTH / 2 - otherthing.get_width() / 2,
                              config.HEIGHT / 2 - otherthing.get_height() / 2 + 70, float("inf"))

        highscores = open(os.path.join(__location__, "scores.dat"))
        scores = highscores.read().split(";")
        biggest = 0
        for sc in scores:
            if int(sc) > biggest:
                biggest = int(sc)

        last_thing = small_text.render("You got a HIGHSCORE of: " + str(scorekeeper.cumulated) + "."
                                       if scorekeeper.cumulated > biggest else "Highscore is " + str(biggest) +
                                       "; you did not beat it.",
                                       False, (0, 0, 255))
        entity.ConcreteEntity(last_thing, config.WIDTH / 2 - last_thing.get_width() / 2,
                              config.HEIGHT / 2 - last_thing.get_height() / 2 + 110, float("inf"))

        highscores.close()

        new_file = open(os.path.join(__location__, "scores.dat"), "a")
        new_file.write(";" + str(scorekeeper.cumulated))

        p = None
        lost = True

    if keyboard.is_key_down(pygame.K_ESCAPE):
        running = False


def close():
    pygame.quit()
    exit(0)


if __name__ == "__main__":
    init()

    while running:
        update()

    close()
