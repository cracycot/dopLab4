import pygame
import sys
import math

pygame.init()

# Определение цветов
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

FONT = pygame.font.Font(None, 32)

class InputBox:

    def __init__(self, x, y, w, h, text='', label=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.label = label
        self.txt_surface = FONT.render(text, True, BLACK)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Проверяем, была ли нажата мышь на поле ввода
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
            # Изменяем цвет поля в зависимости от активности
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    # По желанию можно добавить действие при нажатии Enter
                    self.active = False
                    self.color = COLOR_INACTIVE
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    # Допускаем только цифры, точку и минус
                    if event.unicode.isdigit() or event.unicode in '.-':
                        self.text += event.unicode
                # Обновляем текстовую поверхность
                self.txt_surface = FONT.render(self.text, True, BLACK)

    def update(self):
        # Изменяем ширину поля, если текст слишком длинный
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Отображаем метку поля
        label_surface = FONT.render(self.label, True, BLACK)
        screen.blit(label_surface, (self.rect.x - label_surface.get_width() - 10, self.rect.y + 5))
        # Отображаем текст
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Отображаем рамку поля
        pygame.draw.rect(screen, self.color, self.rect, 2)

def main():
    # Фиксированные размеры окна
    width = 800
    height = 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Ввод параметров")

    clock = pygame.time.Clock()

    input_boxes = []

    # Создаём поля ввода для параметров
    input_boxes.append(InputBox(300, 50, 140, 32, label='Масса тела 1:'))
    input_boxes.append(InputBox(300, 100, 140, 32, label='Масса тела 2:'))

    input_boxes.append(InputBox(300, 150, 140, 32, label='Скорость тела 1:'))
    input_boxes.append(InputBox(300, 200, 140, 32, label='Угол тела 1:'))

    input_boxes.append(InputBox(300, 250, 140, 32, label='Скорость тела 2:'))
    input_boxes.append(InputBox(300, 300, 140, 32, label='Угол тела 2:'))

    input_boxes.append(InputBox(300, 350, 140, 32, label='Радиус тела 1:'))
    input_boxes.append(InputBox(300, 400, 140, 32, label='Радиус тела 2:'))

    # Кнопка для начала симуляции
    start_button_rect = pygame.Rect(350, 500, 100, 50)

    done = False
    start_simulation = False

    while not done:
        for event in pygame.event.get():
            for box in input_boxes:
                box.handle_event(event)
            if event.type == pygame.QUIT:
                done = True
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    # Проверяем, заполнены ли все поля
                    start_simulation = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                    pygame.quit()
                    sys.exit()
        for box in input_boxes:
            box.update()

        screen.fill(WHITE)
        for box in input_boxes:
            box.draw(screen)

        # Отрисовка кнопки "Старт"
        pygame.draw.rect(screen, (0, 255, 0), start_button_rect)
        start_text = FONT.render('Старт', True, BLACK)
        screen.blit(start_text, (start_button_rect.x + 20, start_button_rect.y + 15))

        pygame.display.flip()
        clock.tick(30)

        if start_simulation:
            # Проверяем, что все поля заполнены
            all_filled = all(box.text.strip() != '' for box in input_boxes)
            if all_filled:
                # Получаем значения из полей ввода
                try:
                    mass1 = float(input_boxes[0].text)
                    mass2 = float(input_boxes[1].text)
                    speed1 = float(input_boxes[2].text)
                    angle1 = float(input_boxes[3].text)
                    speed2 = float(input_boxes[4].text)
                    angle2 = float(input_boxes[5].text)
                    radius1 = float(input_boxes[6].text)
                    radius2 = float(input_boxes[7].text)
                except ValueError:
                    # Если введены некорректные данные
                    start_simulation = False
                    error_text = FONT.render('Ошибка: Некорректные данные', True, (255, 0, 0))
                    screen.blit(error_text, (300, 450))
                    pygame.display.flip()
                    pygame.time.wait(2000)
                    continue

                # Добавляем проверки на корректность значений
                if mass1 <= 0 or mass2 <= 0:
                    start_simulation = False
                    error_text = FONT.render('Ошибка: Масса должна быть положительной', True, (255, 0, 0))
                    screen.blit(error_text, (300, 450))
                    pygame.display.flip()
                    pygame.time.wait(2000)
                    continue

                if radius1 <= 0 or radius2 <= 0:
                    start_simulation = False
                    error_text = FONT.render('Ошибка: Радиус тела должен быть положительным', True, (255, 0, 0))
                    screen.blit(error_text, (300, 450))
                    pygame.display.flip()
                    pygame.time.wait(2000)
                    continue

                # Проверяем, что радиусы не слишком большие
                max_radius = min(width, height) / 4
                if radius1 > max_radius or radius2 > max_radius:
                    start_simulation = False
                    error_text = FONT.render('Ошибка: Радиус тела слишком большой', True, (255, 0, 0))
                    screen.blit(error_text, (300, 450))
                    pygame.display.flip()
                    pygame.time.wait(2000)
                    continue

                # Переходим к симуляции
                done = True
                break
            else:
                # Если не все поля заполнены
                start_simulation = False
                error_text = FONT.render('Пожалуйста, заполните все поля', True, (255, 0, 0))
                screen.blit(error_text, (300, 450))
                pygame.display.flip()
                pygame.time.wait(2000)

    # Переходим к симуляции с введёнными параметрами
    try:
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Абсолютно упругое столкновение")

        # Конвертация углов из градусов в радианы
        angle1_rad = math.radians(angle1)
        angle2_rad = math.radians(angle2)

        # Преобразование модулей и направлений в компоненты скоростей по x и y
        # Инвертируем y-компоненту из-за особенностей системы координат Pygame
        velocity1 = [speed1 * math.cos(angle1_rad), -speed1 * math.sin(angle1_rad)]
        velocity2 = [speed2 * math.cos(angle2_rad), -speed2 * math.sin(angle2_rad)]

        # Начальные позиции тел
        pos1 = [width * 0.25, height * 0.5]
        pos2 = [width * 0.75, height * 0.5]

        # Цвета
        RED = (255, 0, 0)
        BLUE = (0, 0, 255)

        # Вспомогательная функция для расчёта скоростей после столкновения
        def calculate_velocity(v1, v2, m1, m2):
            v1_new = ((m1 - m2) / (m1 + m2)) * v1 + ((2 * m2) / (m1 + m2)) * v2
            v2_new = ((2 * m1) / (m1 + m2)) * v1 + ((m2 - m1) / (m1 + m2)) * v2
            return v1_new, v2_new

        # Основной цикл симуляции
        running = True
        clock = pygame.time.Clock()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Обновление позиций тел
            pos1[0] += velocity1[0]
            pos1[1] += velocity1[1]
            pos2[0] += velocity2[0]
            pos2[1] += velocity2[1]

            # Проверка столкновений с границами окна (абсолютно упругие)
            if pos1[0] - radius1 <= 0 or pos1[0] + radius1 >= width:
                velocity1[0] = -velocity1[0]
            if pos1[1] - radius1 <= 0 or pos1[1] + radius1 >= height:
                velocity1[1] = -velocity1[1]

            if pos2[0] - radius2 <= 0 or pos2[0] + radius2 >= width:
                velocity2[0] = -velocity2[0]
            if pos2[1] - radius2 <= 0 or pos2[1] + radius2 >= height:
                velocity2[1] = -velocity2[1]

            # Проверка столкновения между телами
            dx = pos2[0] - pos1[0]
            dy = pos2[1] - pos1[1]
            distance = math.hypot(dx, dy)

            if distance <= radius1 + radius2:
                # Вычисление нормали и касательной
                if distance == 0:
                    # Избегаем деления на ноль
                    distance = 0.01
                normal = [dx / distance, dy / distance]
                tangent = [-normal[1], normal[0]]

                # Проекция скоростей на нормаль и касательную
                v1_normal = normal[0] * velocity1[0] + normal[1] * velocity1[1]
                v2_normal = normal[0] * velocity2[0] + normal[1] * velocity2[1]

                v1_tangent = tangent[0] * velocity1[0] + tangent[1] * velocity1[1]
                v2_tangent = tangent[0] * velocity2[0] + tangent[1] * velocity2[1]

                # Обновление нормальных скоростей после столкновения
                v1_normal_new, v2_normal_new = calculate_velocity(v1_normal, v2_normal, mass1, mass2)

                # Преобразование обратно в векторы скоростей
                velocity1[0] = v1_normal_new * normal[0] + v1_tangent * tangent[0]
                velocity1[1] = v1_normal_new * normal[1] + v1_tangent * tangent[1]
                velocity2[0] = v2_normal_new * normal[0] + v2_tangent * tangent[0]
                velocity2[1] = v2_normal_new * normal[1] + v2_tangent * tangent[1]

                # Сдвигаем объекты, чтобы избежать застревания
                overlap = radius1 + radius2 - distance + 1
                pos1[0] -= overlap * normal[0] / 2
                pos1[1] -= overlap * normal[1] / 2
                pos2[0] += overlap * normal[0] / 2
                pos2[1] += overlap * normal[1] / 2

            # Отрисовка
            screen.fill(WHITE)
            pygame.draw.circle(screen, RED, (int(pos1[0]), int(pos1[1])), int(radius1))
            pygame.draw.circle(screen, BLUE, (int(pos2[0]), int(pos2[1])), int(radius2))
            pygame.display.flip()

            # Ограничение FPS
            clock.tick(60)

    except Exception as e:
        print("An error occurred during the simulation:", e)
        error_text = FONT.render('Ошибка: ' + str(e), True, (255, 0, 0))
        screen.blit(error_text, (50, 50))
        pygame.display.flip()
        pygame.time.wait(5000)
        pygame.quit()
        sys.exit()

    pygame.quit()

if __name__ == '__main__':
    main()
