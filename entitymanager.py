entities = []


def update(window):
    for entity in entities:
        window.blit(entity.image, (entity.x, entity.y))
        entity.update()
        for otherentity in entities:
            # 'is not' is a deliberate choice to compare memory
            # locations rather than anything else with the two entities
            if otherentity is not entity and otherentity.rect.colliderect(entity.rect):
                entity.on_collide(otherentity)
                otherentity.on_collide(entity)
