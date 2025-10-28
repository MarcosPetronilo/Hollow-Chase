import os
import importlib
import pygame

def main():
    pygame.init()
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("THE HOLLOW CHASE")

    # diretorio base e background
    base_dir = os.path.dirname(__file__)
    bg_path = os.path.join(base_dir, '..', 'assents', 'background.png')
    background = None
    if os.path.isfile(bg_path):
        try:
            background = pygame.image.load(bg_path).convert()
            background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except Exception as e:
            print(f"Erro ao carregar background: {e}")
            background = None

    # Tenta carregar inimigo3 (depois de definir base_dir e inicializar pygame)
    inimigo3_img = None
    inimigo3_path = os.path.join(base_dir, '..', 'assents', 'inimigo3.png')
    if os.path.isfile(inimigo3_path):
        try:
            inimigo3_img = pygame.image.load(inimigo3_path).convert_alpha()
            # aumenta o tamanho do inimigo3 para ficar mais visível na tela inicial
            inimigo3_img = pygame.transform.scale(inimigo3_img, (140, 140))
        except Exception as e:
            print(f"Erro ao carregar inimigo3: {e}")

    # Tenta carregar ichigo1 (lado esquerdo) com mesmo tamanho que inimigo3
    ichigo1_img = None
    ichigo1_path = os.path.join(base_dir, '..', 'assents', 'ichigo1.png')
    if os.path.isfile(ichigo1_path):
        try:
            ichigo1_img = pygame.image.load(ichigo1_path).convert_alpha()
            ichigo1_img = pygame.transform.scale(ichigo1_img, (140, 140))
        except Exception as e:
            print(f"Erro ao carregar ichigo1: {e}")

    # Fonte do botão
    try:
        start_font = pygame.font.Font(pygame.font.match_font('arial'), 48)
    except Exception:
        start_font = pygame.font.Font(None, 48)

    start_text = "START"
    # Move o botão para 65% da altura da tela (antes era 75%)
    text_surf = start_font.render(start_text, True, (40, 40, 40))
    text_rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, int(SCREEN_HEIGHT * 0.69)))
    padding = 18
    button_rect = pygame.Rect(text_rect.left - padding, text_rect.top - padding,
                              text_rect.width + padding * 2, text_rect.height + padding * 2)

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    try:
                        import tela_menu
                        importlib.reload(tela_menu)
                        tela_menu.main()
                    except Exception as e:
                        print("Erro ao abrir tela_menu:", e)
                    running = False
                elif event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_rect.collidepoint(event.pos):
                    try:
                        import tela_menu
                        importlib.reload(tela_menu)
                        tela_menu.main()
                    except Exception as e:
                        print("Erro ao abrir tela_menu:", e)
                    running = False

        # desenha background
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill((245, 245, 247))

        # posição base (mesma para ambos)
        y = int(SCREEN_HEIGHT * 0.36)

        # desenha ichigo1 à esquerda (mesma altura e tamanho do inimigo3)
        if ichigo1_img:
            x_left = SCREEN_WIDTH // 2 - 180 - ichigo1_img.get_width()
            if x_left < 20:
                x_left = 20
            screen.blit(ichigo1_img, (x_left, y))

        # desenha inimigo3 à direita
        if inimigo3_img:
            # posiciona o inimigo mais para baixo, ao lado do título
            # coloca-o próximo ao centro-direita, perto do título principal
            x = SCREEN_WIDTH // 2 + 180
            # ajusta se extrapolar a borda direita
            if x + inimigo3_img.get_width() + 20 > SCREEN_WIDTH:
                x = SCREEN_WIDTH - inimigo3_img.get_width() - 40
            screen.blit(inimigo3_img, (x, y))

        # botão START
        mx, my = pygame.mouse.get_pos()
        hover = button_rect.collidepoint((mx, my))

        # sombra
        shadow = pygame.Surface((button_rect.w, button_rect.h), pygame.SRCALPHA)
        shadow.fill((0, 0, 0, 60))
        screen.blit(shadow, (button_rect.x + 4, button_rect.y + 6))

        # fundo do botão
        btn_surf = pygame.Surface((button_rect.w, button_rect.h), pygame.SRCALPHA)
        bg_color = (255, 255, 255, 220) if not hover else (250, 240, 200, 240)
        pygame.draw.rect(btn_surf, bg_color, btn_surf.get_rect(), border_radius=10)
        pygame.draw.rect(btn_surf, (200, 200, 200), btn_surf.get_rect(), width=2, border_radius=10)
        screen.blit(btn_surf, button_rect.topleft)

        # texto
        text_color = (40, 40, 40) if not hover else (20, 20, 20)
        text_surf = start_font.render(start_text, True, text_color)
        text_rect = text_surf.get_rect(center=button_rect.center)
        screen.blit(text_surf, text_rect.topleft)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()