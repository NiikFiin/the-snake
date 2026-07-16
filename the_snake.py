from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки:
BORDER_COLOR = (93, 216, 228)

# Цвет яблока:
APPLE_COLOR = (255, 0, 0)

# Цвет змейки:
SNAKE_COLOR = (0, 255, 0)

# Начальная длина змейки:
START_SNAKE_LENGTH = 1

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс с основными атрибутами для игровых объектов"""

    def __init__(self):
        self.position = (
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2
        )                         # Позиция объекта
        self.body_color = None    # Цвет объекта

    def draw(self):
        """Отрисовка обьектов"""
        pass


class Apple(GameObject):
    """Содержит основные методы и атрибуты яблока"""

    def __init__(self):
        super().__init__()               # Наследуем атрибуты базового класса
        self.body_color = APPLE_COLOR    # Задаем цвет яблока

    def randomize_position(self):
        """Метод отвечает за случайное положение яблока на игровом поле"""
        self.position = (
            randint(0, int(SCREEN_WIDTH / GRID_SIZE)) * GRID_SIZE,
            randint(0, int(SCREEN_HEIGHT / GRID_SIZE)) * GRID_SIZE
        )

    def draw(self):
        """Отрисовка яблока на игровом поле"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Содержит основные атрибуты и методы змейки"""

    def __init__(self):
        super().__init__()
        self.body_color = SNAKE_COLOR       # Цвет змейки
        self.length = START_SNAKE_LENGTH    # Начальная длина змейки
        self.positions = [self.position]    # Список сегментов змейки
        self.direction = RIGHT              # Начальное направление змейки
        self.next_direction = None          # Следующее направление змейки
        self.last = self.positions[-1]      # Хвост змейки

    def get_head_position(self):
        """Возвращает положение головы змейки"""
        return self.positions[0]

    def move(self):
        """Метод, отвечающий за движение змейки на игровом поле"""
        head_position = self.get_head_position()
        # Рассчитываем новую позицию головы змейки
        new_head_position = (
            (head_position[0] + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
            (head_position[1] + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT
        )
        self.positions.insert(0, new_head_position)
        if len(self.positions) - 1 > self.length:
            # Удаляем и возвращаем хвост змейки:
            self.last = self.positions.pop()

    def draw(self):
        """Отрисовка змейки"""
        # Отрисовка тела змейки
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def if_eat_apple(self, apple_object):
        """Проверка, сьела ли змейка яблоко"""
        if self.get_head_position() == apple_object.position:
            apple_object.randomize_position()
            self.length += 1

    def update_direction(self):
        """Передает новое направление змейке"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def reset(self):
        """Проверка и сброс результата при столкновении змейки"""
        for position in self.positions[1:]:
            if self.get_head_position() == position:
                self.length = START_SNAKE_LENGTH
                self.positions = [(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)]
                self.direction = choice((RIGHT, LEFT, UP, DOWN))


def handle_keys(snake_object):
    """Принимает и обрабатывает действия пользователя"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_object.direction != DOWN:
                snake_object.next_direction = UP
            elif event.key == pygame.K_DOWN and snake_object.direction != UP:
                snake_object.next_direction = DOWN
            elif (event.key == pygame.K_LEFT
                  and snake_object.direction != RIGHT):
                snake_object.next_direction = LEFT
            elif (event.key == pygame.K_RIGHT
                  and snake_object.direction != LEFT):
                snake_object.next_direction = RIGHT


def main():
    """Точка входа в программу"""
    pygame.init()                    # Инициализация pygame
    apple = Apple()                  # Создание обьектов
    snake = Snake()
    while True:                      # Игровой цикл
        handle_keys(snake)
        snake.update_direction()
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        snake.move()
        snake.if_eat_apple(apple)    # Проверка, съела ли змейка яблоко
        snake.reset()                # Сброс змейки при столкновении
        pygame.display.update()      # Обновление содержимого экрана
        clock.tick(SPEED)            # Установка ограничения FPS


if __name__ == '__main__':
    main()
