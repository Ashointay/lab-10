import psycopg2
import pygame
import random

conn = psycopg2.connect(
    dbname="snake_db",
    user="postgres",
    password="Zhasminchik6",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

def get_or_create_user(username):
    cur.execute("SELECT id FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    if user:
        user_id = user[0]
    else:
        cur.execute("INSERT INTO users (username) VALUES (%s) RETURNING id", (username,))
        user_id = cur.fetchone()[0]
        conn.commit()

    cur.execute("SELECT level, score FROM user_score WHERE user_id = %s", (user_id,))
    score_data = cur.fetchone()
    if not score_data:
        cur.execute("INSERT INTO user_score (user_id) VALUES (%s)", (user_id,))
        conn.commit()
        return user_id, 1, 0
    else:
        return user_id, score_data[0], score_data[1]

def save_progress(user_id, level, score):
    cur.execute(
        "UPDATE user_score SET level = %s, score = %s WHERE user_id = %s",
        (level, score, user_id)
    )
    conn.commit()

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

username = input("Enter your username: ")
user_id, level, score = get_or_create_user(username)
print(f"Welcome back, {username}! Level: {level}, Score: {score}")

snake = [(100, 100)]
snake_dir = (20, 0)
food = (300, 300)
paused = False

speed = 3 + level
walls = []
if level >= 2:
    walls = [(200, 200), (220, 200), (240, 200)]
if level >= 3:
    walls += [(100, 300), (120, 300), (140, 300)]

def draw_text(text, x, y):
    screen.blit(font.render(text, True, (255, 255, 255)), (x, y))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_progress(user_id, level, score)
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused
                if paused:
                    print("Paused. Progress saved.")
                    save_progress(user_id, level, score)
            elif event.key == pygame.K_UP and snake_dir != (0, 20):
                snake_dir = (0, -20)
            elif event.key == pygame.K_DOWN and snake_dir != (0, -20):
                snake_dir = (0, 20)
            elif event.key == pygame.K_LEFT and snake_dir != (20, 0):
                snake_dir = (-20, 0)
            elif event.key == pygame.K_RIGHT and snake_dir != (-20, 0):
                snake_dir = (20, 0)

    if not paused:
        screen.fill((0, 0, 0))
        draw_text(f"Score: {score}", 10, 10)
        draw_text(f"Level: {level}", 10, 40)

        new_head = (snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1])
        if new_head in snake or new_head in walls or not (0 <= new_head[0] < 640 and 0 <= new_head[1] < 480):
            print("Game Over! Progress saved.")
            save_progress(user_id, level, score)
            break

        snake.insert(0, new_head)
        if new_head == food:
            score += 1
            if score % 5 == 0:
                level += 1
                speed = 5 + level  # Increase speed slowly
            food = (random.randint(0, 31)*20, random.randint(0, 23)*20)
        else:
            snake.pop()

        for part in snake:
            pygame.draw.rect(screen, (0, 255, 0), (*part, 20, 20))
        pygame.draw.rect(screen, (255, 0, 0), (*food, 20, 20))
        for wall in walls:
            pygame.draw.rect(screen, (100, 100, 100), (*wall, 20, 20))

        pygame.display.flip()
        clock.tick(speed)

pygame.quit()
cur.close()
conn.close()
