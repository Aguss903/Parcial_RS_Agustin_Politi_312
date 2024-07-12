"""
Este módulo define la clase Player que representa al jugador en el juego Aniquilador.

Importa los siguientes módulos:
- pygame: para la creación de la interfaz gráfica y la lógica del juego.
- math: para operaciones matemáticas, como cálculos trigonométricos.
"""

import pygame
import math

class Player(pygame.sprite.Sprite):
    """
    Clase que representa al jugador en el juego.

    Atributos:
    - rect (pygame.Rect): Rectángulo que delimita al jugador.
    - speed (int): Velocidad de movimiento del jugador.
    - health (int): Salud actual del jugador.
    - shielded (bool): Indica si el jugador está protegido por un escudo.
    - shield_time (int): Tiempo restante de duración del escudo.
    - shield_duration (int): Duración total del escudo en segundos.
    - shield_cooldown (int): Tiempo de enfriamiento entre usos del escudo en segundos.
    - last_shield_time (int): Marca de tiempo del último uso del escudo.
    """

    def __init__(self, screen_size):
        """
        Inicializa al jugador en la posición central de la pantalla.

        Args:
        - screen_size (tuple): Dimensiones de la pantalla (ancho, alto).
        """
        super().__init__()
        self.image = pygame.Surface((40, 40))  # Imagen del jugador (rectángulo azul)
        self.image.fill((0, 128, 255))
        self.rect = self.image.get_rect()  # Rectángulo que delimita al jugador
        self.rect.center = (screen_size[0] // 2, screen_size[1] // 2)  # Posición inicial centrada
        self.health = 3  # Salud inicial del jugador
        self.alive = True  # Estado de vida del jugador
        self.speed = 300  # Velocidad de movimiento del jugador en píxeles por segundo
        self.movementVector = [0, 0]  # Vector de movimiento actual del jugador
        self.shielded = False  # Indica si el jugador está protegido por un escudo
        self.shield_time = 0  # Tiempo restante de duración del escudo
        self.shield_duration = 3  # Duración total del escudo en segundos
        self.shield_cooldown = 15  # Tiempo de enfriamiento entre usos del escudo en segundos
        self.last_shield_time = 0  # Marca de tiempo del último uso del escudo

    def move(self, screen_size, timeDelta):
        """
        Mueve al jugador según las teclas presionadas y el tiempo transcurrido.

        Args:
        - screen_size (tuple): Dimensiones de la pantalla (ancho, alto).
        - timeDelta (float): Tiempo transcurrido desde el último frame en segundos.
        """
        self.rect.x += self.movementVector[0] * self.speed * timeDelta
        self.rect.y += self.movementVector[1] * self.speed * timeDelta

        # Limita al jugador dentro de los límites de la pantalla
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_size[0]:
            self.rect.right = screen_size[0]
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > screen_size[1]:
            self.rect.bottom = screen_size[1]

    def shoot(self, target_pos):
        """
        Dispara un proyectil hacia la posición objetivo.

        Args:
        - target_pos (tuple): Posición (x, y) del objetivo.

        Returns:
        - pygame.sprite.Sprite: Proyectil creado si se puede disparar, None si no.
        """
        if self.alive:
            angle = math.atan2(target_pos[1] - self.rect.centery, target_pos[0] - self.rect.centerx)
            return self.Projectile(self.rect.center, angle)

    def activate_shield(self):
        """
        Activa el escudo protector del jugador si ha pasado el tiempo de enfriamiento.
        """
        if pygame.time.get_ticks() - self.last_shield_time > self.shield_cooldown * 1000:
            self.shielded = True
            self.shield_time = pygame.time.get_ticks()
            self.last_shield_time = pygame.time.get_ticks()

    def update_shield(self):
        """
        Actualiza el estado del escudo protector del jugador y lo desactiva cuando expira.
        """
        if self.shielded and pygame.time.get_ticks() - self.shield_time > self.shield_duration * 1000:
            self.shielded = False

    def render(self, screen):
        """
        Renderiza al jugador en la superficie especificada.

        Args:
        - screen (pygame.Surface): Superficie de Pygame donde se renderizará al jugador.
        """
        if self.shielded:
            pygame.draw.circle(screen, (0, 255, 0), self.rect.center, 30, 2)  # Dibuja el escudo
        screen.blit(self.image, self.rect)  # Dibuja al jugador en la pantalla

    class Projectile(pygame.sprite.Sprite):
        """
        Clase interna que representa el proyectil disparado por el jugador.

        Atributos:
        - rect (pygame.Rect): Rectángulo que delimita al proyectil.
        - speed (int): Velocidad de movimiento del proyectil.
        """
        def __init__(self, pos, angle):
            """
            Inicializa el proyectil en una posición inicial y con un ángulo de movimiento.

            Args:
            - pos (tuple): Posición inicial del proyectil (x, y).
            - angle (float): Ángulo de dirección del proyectil en radianes.
            """
            super().__init__()
            self.image = pygame.Surface((10, 10))  # Imagen del proyectil (rectángulo rojo)
            self.image.fill((255, 0, 0))
            self.rect = self.image.get_rect(center=pos)  # Rectángulo que delimita al proyectil
            self.angle = angle  # Ángulo de dirección del proyectil
            self.speed = 600  # Velocidad de movimiento del proyectil en píxeles por segundo

        def update(self, timeDelta):
            """
            Actualiza la posición del proyectil basado en el tiempo transcurrido.

            Args:
            - timeDelta (float): Tiempo transcurrido desde el último frame en segundos.
            """
            self.rect.x += math.cos(self.angle) * self.speed * timeDelta
            self.rect.y += math.sin(self.angle) * self.speed * timeDelta

            # Elimina el proyectil si sale de la pantalla
            if self.rect.right < 0 or self.rect.left > 1800 or self.rect.bottom < 0 or self.rect.top > 1000:
                self.kill()  # Elimina el proyectil del grupo de sprites
