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

    def __init__(self) -> None:
        self.position = (
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2
        )
        self.body_color = None

    def draw(self) -> None:
        """Метод отрисовки, который будет переопределен в дочерних классах"""
        raise NotImplementedError

    def draw_cell(
        self, position: tuple[int, int],
        body_color: tuple[int, int, int]
    ) -> None:
        """Основной метод отрисовки обьектов"""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, body_color, rect)
        if body_color == self.body_color:
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Содержит основные атрибуты и методы змейки"""

    def __init__(self) -> None:
        super().__init__()
        self.reset()
        self.body_color = SNAKE_COLOR       # Цвет змейки
        self.direction = RIGHT              # Начальное направление змейки
        self.next_direction = None          # Следующее направление змейки
        self.last = self.positions[-1]      # Хвост змейки

    def get_head_position(self) -> tuple[int, int]:
        """Возвращает положение головы змейки"""
        return self.positions[0]

    def move(self) -> None:
        """Метод, отвечающий за движение змейки на игровом поле"""
        head_position_x, head_position_y = self.get_head_position()
        # Рассчитываем новую позицию головы змейки
        new_head_position = (
            (head_position_x + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
            (head_position_y + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT
        )
        self.positions.insert(0, new_head_position)
        if len(self.positions) - 1 > self.length:
            # Удаляем и возвращаем хвост змейки:
            self.last = self.positions.pop()

    def draw(self) -> None:
        """Отрисовка змейки"""
        # Отрисовка тела змейки
        for position in self.positions[:-1]:
            self.draw_cell(position, self.body_color)

        # Отрисовка головы змейки
        self.draw_cell(self.get_head_position(), self.body_color)

        # Затирание последнего сегмента
        if self.last:
            self.draw_cell(self.last, BOARD_BACKGROUND_COLOR)

    def update_direction(self) -> None:
        """Передает новое направление змейке"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def reset(self) -> None:
        """Проверка и сброс результата при столкновении змейки"""
        self.length = START_SNAKE_LENGTH
        self.positions = [self.position]
        self.direction = choice((RIGHT, LEFT, UP, DOWN))


class Apple(GameObject):
    """Содержит основные методы и атрибуты яблока"""

    def __init__(self) -> None:
        super().__init__()               # Наследуем атрибуты базового класса
        self.body_color = APPLE_COLOR    # Задаем цвет яблока

    def randomize_position(self, snake_object: Snake) -> None:
        """Метод отвечает за случайное положение яблока на игровом поле"""
        while True:
            self.position = (
                randint(0, int(SCREEN_WIDTH / GRID_SIZE) - 1) * GRID_SIZE,
                randint(0, int(SCREEN_HEIGHT / GRID_SIZE) - 1) * GRID_SIZE
            )
            if self.position not in snake_object.positions:
                break

    def draw(self) -> None:
        """Отрисовка яблока на игровом поле"""
        self.draw_cell(self.position, self.body_color)


def handle_keys(snake_object: Snake) -> None:
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


def main() -> None:
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
        # Проверка, съела ли змейка яблоко:
        if snake.get_head_position() == apple.position:
            apple.randomize_position(snake)
            snake.length += 1
        # Сброс змейки при столкновении:
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
        pygame.display.update()             # Обновление содержимого экрана
        clock.tick(SPEED)                   # Установка ограничения FPS


if __name__ == '__main__':
    main()
