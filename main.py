import pygame
import random
import math
import os
import time

# Ініціалізація Pygame
pygame.init()
sound = pygame.mixer.Sound("so.mp3")

# Налаштування екрану
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Рулетка зі стрілочкою вниз")
background = pygame.image.load("wheel.png")
background = pygame.transform.scale(background, (width, height))
# Перевірка шляху до зображення
image_path = 'wheel_image.png'  # Вкажіть правильний шлях до вашого зображення
if os.path.exists(image_path):
    print("Файл зображення знайдено")
else:
    print("Файл зображення не знайдено. Малюємо замість колеса фігуру.")

try:
    # Завантаження зображення колеса
    wheel_image = pygame.image.load(image_path).convert_alpha()
    wheel_rect = wheel_image.get_rect(center=(width // 2, height // 2))
except Exception as e:
    print(f"Помилка при завантаженні зображення: {e}")
    wheel_image = None

# Функція для малювання сегментів колеса
def draw_fallback_wheel(surface, center, radius, segments, colors):
    angle_step = 360 / segments
    for i in range(segments):
        start_angle = math.radians(i * angle_step)
        end_angle = math.radians((i + 1) * angle_step)

        x1 = center[0] + radius * math.cos(start_angle)
        y1 = center[1] - radius * math.sin(start_angle)
        x2 = center[0] + radius * math.cos(end_angle)
        y2 = center[1] - radius * math.sin(end_angle)

        pygame.draw.polygon(surface, colors[i % len(colors)], [(center[0], center[1]), (x1, y1), (x2, y2)])

# Розмір рулетки
radius = 250

# Кольори сегментів та текст
segment_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0), (128, 0, 128)]
segment_texts = ["Перемога", "Поразка", "Поразка", "Перемога", "Поразка", "Перемога"]
num_segments = len(segment_colors)

# Положення стрілки над "Призом 1"
arrow_image = pygame.Surface((20, 100), pygame.SRCALPHA)
pygame.draw.polygon(arrow_image, (255, 0, 0), [(10, 100), (20, 0), (0, 0)])
arrow_rect = arrow_image.get_rect(center=(width // 2, height // 2 - radius - 20))

# Основна логіка
running = True
angle = 0
velocity = 0
message = ""
font = pygame.font.SysFont(None, 30)  # Зменшений розмір шрифту для тексту
result_font = pygame.font.SysFont(None, 55)

# Зміщення для "Призу 1" під стрілкою
initial_offset = 360 / num_segments / 2

# Функція для генерації випадкового кольору
def get_random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# Ініціалізація випадкових кольорів для текстів
text_colors = [get_random_color() for _ in segment_texts]
last_color_change_time = time.time()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            sound.play()
            velocity = random.uniform(5, 15)
            message = "обертання завершено!"

    # Оновлення кольорів тексту кожні 0.5 секунди
    if time.time() - last_color_change_time > 0.5:
        text_colors = [get_random_color() for _ in segment_texts]
        last_color_change_time = time.time()

    screen.fill((255, 255, 255))

    # Обертання колеса
    current_angle = angle + initial_offset
    if wheel_image:
        rotated_wheel = pygame.transform.rotate(wheel_image, current_angle)
        new_rect = rotated_wheel.get_rect(center=(width // 2, height // 2))
        screen.blit(rotated_wheel, new_rect.topleft)
    else:
        draw_fallback_wheel(screen, (width // 2, height // 2), radius, num_segments, segment_colors)

    screen.blit(arrow_image, arrow_rect.topleft)

    # Додавання різнокольорового тексту по центру сегментів
    for i, text in enumerate(segment_texts):
        text_angle = (360 / num_segments) * i - current_angle % 360
        radian_angle = math.radians(text_angle)
        text_x = width // 2 + math.cos(radian_angle) * (radius // 1.5)
        text_y = height // 2 - math.sin(radian_angle) * (radius // 1.5)
        text_surface = font.render(text, True, text_colors[i])
        screen.blit(text_surface, (text_x - text_surface.get_width() // 2, text_y - text_surface.get_height() // 2))

    pygame.display.flip()

    angle += velocity
    velocity *= 0.94
    if velocity < 0.1:
        velocity = 0
        message = "Обертання завершено"

    pygame.time.delay(50)

# Виведення повідомлення "Обертання завершено" та сердечка
if message:
    completion_text = result_font.render(message, True, (0, 0, 0))
    screen.blit(completion_text, (width // 2 - completion_text.get_width() // 2, height // 2))
    screen.blit(background, (0, 0))
    heart_color = (255, 0, 0)
    pygame.draw.circle(screen, heart_color, (width // 2 - 50, height // 2 + 100), 50)
    pygame.draw.circle(screen, heart_color, (width // 2 + 50, height // 2 + 100), 50)
    pygame.draw.polygon(screen, heart_color, [(width // 2 - 100, height // 2 + 100), (width // 2 + 100, height // 2 + 100), (width // 2, height // 2 + 200)])

    thank_you_text = result_font.render("Дякую за увагу", True, (0, 0, 0))
    screen.blit(thank_you_text, (width // 2 - thank_you_text.get_width() // 2, height // 2 + 250))

    pygame.display.flip()
    pygame.time.delay(3000)
    pygame.quit()
