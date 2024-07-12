"""
Este módulo define la clase Enemy que representa a los enemigos en el juego Aniquilador.

Importa los siguientes módulos:
- pygame: para la creación de la interfaz gráfica y la lógica del juego.
"""

import pygame
import random
import math

class Enemy(pygame.sprite.Sprite):
    """
    Clase que representa a un enemigo en el juego.

    Atributos:
    - rect (pygame.Rect): Rectángulo que delimita al enemigo.
    - speed (int): Velocidad de movimiento del enemigo.
    - health (int): Salud actual del enemigo.
    """
    def __init__(self, pos):
        """
        Inicializa al enemigo en una posición inicial aleatoria.

        Args:
        - position (tuple): Posición inicial del enemigo (x, y).
        """
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=pos)
        self.speed = 150

    def move(self, enemies, target_pos, timeDelta):
        """
        Mueve al enemigo hacia la posición del jugador.

        Args:
        - all_enemies (pygame.sprite.Group): Grupo que contiene a todos los enemigos en pantalla.
        - player_pos (tuple): Posición (x, y) actual del jugador.
        - dt (float): Tiempo transcurrido desde el último frame en segundos.
        """
        angle = math.atan2(target_pos[1] - self.rect.centery, target_pos[0] - self.rect.centerx)
        self.rect.x += math.cos(angle) * self.speed * timeDelta
        self.rect.y += math.sin(angle) * self.speed * timeDelta

    def shoot(self, target):
        """
        Dispara un proyectil hacia la posición objetivo.

        Args:
        - target_pos (tuple): Posición (x, y) del objetivo.

        Returns:
        - pygame.sprite.Sprite: Proyectil creado si se puede disparar, None si no.
        """
        if random.random() < 0.01:  # Probabilidad de disparo de los enemigos
            angle = math.atan2(target[1] - self.rect.centery, target[0] - self.rect.centerx)
            return self.Projectile(self.rect.center, angle)

    class Projectile(pygame.sprite.Sprite):
        """
        Clase interna que representa el proyectil disparado por el enemigo.

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
            self.image = pygame.Surface((5, 5))
            self.image.fill((0, 255, 0))
            self.rect = self.image.get_rect(center=pos)
            self.angle = angle
            self.speed = 300

        def update(self, timeDelta):
            """
            Actualiza la posición del proyectil basado en el tiempo transcurrido.

            Args:
            - timeDelta (float): Tiempo transcurrido desde el último frame en segundos.
            """
            self.rect.x += math.cos(self.angle) * self.speed * timeDelta
            self.rect.y += math.sin(self.angle) * self.speed * timeDelta

            if self.rect.right < 0 or self.rect.left > 1800 or self.rect.bottom < 0 or self.rect.top > 1000:
                self.kill()

