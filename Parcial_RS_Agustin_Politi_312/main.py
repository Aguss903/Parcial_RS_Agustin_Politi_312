import pygame
import random
import sys
import csv
from player import Player
from enemy import Enemy

# Inicialización de Pygame
pygame.init()
size = (1800, 1000)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Aniquilador")

# Cargar imagen de fondo para el menú principal desde la carpeta /images
fondo_pantalla_principal = pygame.image.load('images/fondo_panta_principal.png').convert()

# Redimensionar la imagen de fondo si no es del tamaño 1800x1000
fondo_pantalla_principal = pygame.transform.scale(fondo_pantalla_principal, size)

# Fuentes
scoreFont = pygame.font.Font(None, 30)
healthFont = pygame.font.Font(None, 50)
titleFont = pygame.font.Font(None, 100)
buttonFont = pygame.font.Font(None, 40)
buttonFontOptions = pygame.font.Font(None, 60)

# Inicialización de música
pygame.mixer.init()
pygame.mixer.music.load('music/Base_After_Base.mp3')
pygame.mixer.music.set_volume(0.5)

clock = pygame.time.Clock()

class Game:
    """
    Clase principal que gestiona el ciclo de juego y las pantallas.
    """
    def __init__(self):
        """
        Inicializa el juego con el estado inicial y variables necesarias.
        """
        self.state = 'start_screen'  # Estado inicial: pantalla de inicio
        self.player = None
        self.enemies = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.score = 0
        self.last_enemy_spawn_time = 0
        self.max_scores = 5  # Máximo número de puntajes a guardar

    def start(self):
        """
        Método principal que inicia el bucle principal del juego.
        """
        while True:
            if self.state == 'start_screen':
                self.start_screen()
            elif self.state == 'game_loop':
                self.game_loop()
            elif self.state == 'game_over':
                self.game_over_screen()
            elif self.state == 'options':
                self.options_screen()

    def start_screen(self):
        """
        Pantalla inicial del juego donde se muestra el título y opciones.
        """
        pygame.mixer.music.play(-1)

        while self.state == 'start_screen':
            screen.blit(fondo_pantalla_principal, (0, 0))  # Dibujar el fondo de pantalla
            
            draw_text(screen, "Aniquilador", titleFont, pygame.Color('white'), (size[0]//2 - 200, size[1]//4))
            
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()

            start_button = pygame.Rect(size[0]//2 - 100, size[1]//2 - 50, 200, 50)
            options_button = pygame.Rect(size[0]//2 - 100, size[1]//2, 200, 50)
            quit_button = pygame.Rect(size[0]//2 - 100, size[1]//2 + 50, 200, 50)

            if start_button.collidepoint(mouse_pos):
                pygame.draw.rect(screen, (40, 40, 40), start_button)
                if mouse_click[0]:
                    pygame.mixer.music.stop()  
                    pygame.mixer.music.load('music/Base_After_Base2.mp3') 
                    pygame.mixer.music.play(-1)
                    self.state = 'game_loop'  # Cambio el estado al bucle del juego
                    self.setup_game()  # Inicializar el juego
            else:
                pygame.draw.rect(screen, (140, 140, 140), start_button)
            
            if options_button.collidepoint(mouse_pos):
                pygame.draw.rect(screen, (40, 40, 40), options_button)
                if mouse_click[0]:
                    self.state = 'options'
            else:
                pygame.draw.rect(screen, (140, 140, 140), options_button)
            
            if quit_button.collidepoint(mouse_pos):
                pygame.draw.rect(screen, (40, 40, 40), quit_button)
                if mouse_click[0]:
                    pygame.quit()
                    sys.exit()
            else:
                pygame.draw.rect(screen, (140, 140, 140), quit_button)
            
            draw_text(screen, "Comenzar", buttonFont, pygame.Color('white'), (start_button.x + 30, start_button.y + 10))
            draw_text(screen, "Opciones", buttonFont, pygame.Color('white'), (options_button.x + 35, options_button.y + 10))
            draw_text(screen, "Salir", buttonFont, pygame.Color('white'), (quit_button.x + 70, quit_button.y + 10))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.flip()
            clock.tick(60)

    def options_screen(self):
        """
        Pantalla de opciones donde se puede ajustar el volumen del juego.
        """
        volume = 5

        while self.state == 'options':
            screen.blit(fondo_pantalla_principal, (0, 0))  # Dibujar el fondo de pantalla
            draw_text(screen, "Opciones", titleFont, pygame.Color('white'), (size[0]//2 - 150, size[1]//4))
            
            draw_text(screen, f"Volúmen: {volume}", buttonFontOptions, pygame.Color('white'), (size[0]//2 - 100, size[1]//2 - 150))
        
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()

            back_button = pygame.Rect(size[0]//2 - 100, size[1]//2 + 150, 250, 50)

            if back_button.collidepoint(mouse_pos):
                pygame.draw.rect(screen, (40, 40, 40), back_button)
                if mouse_click[0]:
                    self.state = 'start_screen'
            else:
                pygame.draw.rect(screen, (140, 140, 140), back_button)

            draw_text(screen, "Volver", buttonFont, pygame.Color('white'), (back_button.x + 80, back_button.y + 10))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        volume = max(0, volume - 1)
                        pygame.mixer.music.set_volume(volume / 10)
                    elif event.key == pygame.K_RIGHT:
                        volume = min(10, volume + 1)
                        pygame.mixer.music.set_volume(volume / 10)

            pygame.display.flip()
            clock.tick(60)

    def setup_game(self):
        """
        Prepara el juego inicializando al jugador y otros elementos del juego.
        """
        self.player = Player(size)
        self.enemies = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.score = 0
        self.last_enemy_spawn_time = pygame.time.get_ticks()
        pygame.time.set_timer(pygame.USEREVENT + 1, 500)

    def game_loop(self):
        """
        Bucle principal del juego donde ocurre la interacción y lógica del juego.
        """
        self.setup_game()

        while self.state == 'game_loop':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.USEREVENT + 1:
                    if pygame.time.get_ticks() - self.last_enemy_spawn_time >= 500:
                        enemy = Enemy((random.randint(0, size[0]), random.randint(0, size[1])))
                        self.enemies.add(enemy)
                        self.last_enemy_spawn_time = pygame.time.get_ticks()

            keys = pygame.key.get_pressed()
            self.player.movementVector = [0, 0]

            if keys[pygame.K_w]:
                self.player.movementVector[1] = -1
            if keys[pygame.K_s]:
                self.player.movementVector[1] = 1
            if keys[pygame.K_a]:
                self.player.movementVector[0] = -1
            if keys[pygame.K_d]:
                self.player.movementVector[0] = 1
            if keys[pygame.K_SPACE]:
                mouse_pos = pygame.mouse.get_pos()
                proj = self.player.shoot(mouse_pos)
                if proj:
                    self.projectiles.add(proj)
            if keys[pygame.K_e]:  
                self.player.activate_shield()

            self.player.move(size, clock.get_time() / 1000.0)
            self.player.update_shield()

            for enemy in self.enemies:
                enemy.move(self.enemies, self.player.rect.center, clock.get_time() / 1000.0)
                if pygame.sprite.collide_circle(self.player, enemy):
                    if not self.player.shielded:
                        self.player.health -= 1
                    enemy.kill()
                enemy_proj = enemy.shoot(self.player.rect.center)
                if enemy_proj:
                    self.projectiles.add(enemy_proj)

            self.projectiles.update(clock.get_time() / 1000.0)

            for proj in self.projectiles:
                if isinstance(proj, self.player.Projectile):
                    hit_enemies = pygame.sprite.spritecollide(proj, self.enemies, True)
                    if hit_enemies:
                        proj.kill()
                        self.score += len(hit_enemies)
                elif isinstance(proj, Enemy.Projectile):
                    if pygame.sprite.spritecollide(proj, [self.player], False, pygame.sprite.collide_circle):
                        if not self.player.shielded:
                            self.player.health -= 1
                        proj.kill()

            if self.player.health <= 0:
                self.state = 'game_over'

            screen.blit(fondo_pantalla_principal, (0, 0))
            self.player.render(screen)
            self.enemies.draw(screen)
            self.projectiles.draw(screen)

            draw_text(screen, f"Salud: {self.player.health}", scoreFont, pygame.Color('white'), (10, 10))
            draw_text(screen, f"Puntuación: {self.score}", scoreFont, pygame.Color('white'), (10, 50))

            pygame.display.flip()
            clock.tick(60)

    def game_over_screen(self):
        """
        Pantalla que se muestra cuando el jugador pierde todas las vidas.
        """
        player_name = ""

        while self.state == 'game_over':
            screen.blit(fondo_pantalla_principal, (0, 0))
            draw_text(screen, "Juego terminado", titleFont, pygame.Color('white'), (size[0]//2 - 280, size[1]//4))
            
            draw_text(screen, "Ingresa tu nombre:", buttonFont, pygame.Color('white'), (size[0]//2 - 150, size[1]//2 - 50))

            input_box = pygame.Rect(size[0]//2 - 100, size[1]//2, 200, 50)
            pygame.draw.rect(screen, (255, 255, 255), input_box, 2)
            
            draw_text(screen, player_name, buttonFont, pygame.Color('white'), (input_box.x + 5, input_box.y + 10))

            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()

            restart_button = pygame.Rect(size[0]//2 - 100, size[1]//2 + 100, 200, 50)
            main_menu_button = pygame.Rect(size[0]//2 - 180, size[1]//2 + 170, 360, 50)
            
            if restart_button.collidepoint(mouse_pos):
                pygame.draw.rect(screen, (40, 40, 40), restart_button)
                if mouse_click[0]:
                    # Guardar la puntuación en un archivo CSV
                    self.save_score(player_name, self.score)
                    self.state = 'game_loop'
            else:
                pygame.draw.rect(screen, (140, 140, 140), restart_button)
            
            if main_menu_button.collidepoint(mouse_pos):
                pygame.draw.rect(screen, (40, 40, 40), main_menu_button)
                if mouse_click[0]:
                    # Guardar la puntuación en un archivo CSV
                    self.save_score(player_name, self.score)
                    self.state = 'start_screen'
            else:
                pygame.draw.rect(screen, (140, 140, 140), main_menu_button)
            
            draw_text(screen, "Reiniciar", buttonFont, pygame.Color('white'), (restart_button.x + 40, restart_button.y + 10))
            draw_text(screen, "Menú Principal", buttonFont, pygame.Color('white'), (main_menu_button.x + 80, main_menu_button.y + 10))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    elif event.key == pygame.K_RETURN:
                        # Guardar la puntuación en un archivo CSV
                        self.save_score(player_name, self.score)
                        self.state = 'start_screen'
                    else:
                        player_name += event.unicode

            pygame.display.flip()
            clock.tick(60)

    def save_score(self, player_name, score):
        """
        Guarda la puntuación del jugador en un archivo CSV.

        Args:
        - player_name: Nombre del jugador.
        - score: Puntuación obtenida.
        """
        scores = self.load_scores()
        scores.append((player_name, score))
        scores.sort(key=lambda x: x[1], reverse=True)
        scores = scores[:self.max_scores]  # Mantener solo los primeros max_scores registros
        
        with open('scores.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for score in scores:
                writer.writerow(score)

    def load_scores(self):
        """
        Carga los puntajes de los jugadores desde el archivo CSV.

        Returns:
        - Una lista de tuplas (player_name, score).
        """
        scores = []
        try:
            with open('scores.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) == 2:
                        scores.append((row[0], int(row[1])))
        except FileNotFoundError:
            pass
        
        return scores

def draw_text(surface, text, font, color, pos):
    """
    Dibuja texto en la pantalla en la posición especificada.

    Args:
    - surface: Superficie de Pygame donde se dibujará el texto.
    - text: Texto a dibujar.
    - font: Fuente de Pygame para el texto.
    - color: Color del texto.
    - pos: Posición (x, y) donde se dibujará el texto.
    """
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, pos)

def main():
    """
    Función principal que inicializa el juego y comienza el bucle del juego.
    """
    game = Game()
    game.start()

if __name__ == "__main__":
    main()

pygame.quit()
