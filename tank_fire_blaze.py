import pygame
import sys

# 初始化Pygame
pygame.init()

# 设置窗口大小和标题
window_width = 800
window_height = 600
window_title = "连发子弹示例"

# 创建游戏窗口
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption(window_title)

# 子弹列表
bullets = []

# 设置子弹的尺寸和移动速度
bullet_width = 10
bullet_height = 5
bullet_speed = 5

# 创建 Clock 对象
clock = pygame.time.Clock()

# 游戏主循环
running = True
fire_bullet = False  # 用于控制是否发射子弹
fire_delay = 200  # 子弹发射延迟，单位为毫秒
last_fire_time = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # 按下空格键开始连发子弹
            if event.key == pygame.K_SPACE:
                fire_bullet = True

        elif event.type == pygame.KEYUP:
            # 松开空格键停止连发子弹
            if event.key == pygame.K_SPACE:
                fire_bullet = False

    # 当按下空格键且满足发射延迟条件时，创建新的子弹
    if fire_bullet and pygame.time.get_ticks() - last_fire_time > fire_delay:
        last_fire_time = pygame.time.get_ticks()
        new_bullet = pygame.Rect(0, 0, bullet_width, bullet_height)
        new_bullet.midtop = (window_width // 2, window_height - 30)
        bullets.append(new_bullet)

    # 移动子弹
    for bullet in bullets:
        bullet.y -= bullet_speed
        if bullet.bottom < 0:
            bullets.remove(bullet)

    # 绘制背景
    screen.fill((255, 255, 255))

    # 绘制子弹
    for bullet in bullets:
        pygame.draw.rect(screen, (0, 0, 0), bullet)

    # 更新屏幕
    pygame.display.flip()

    # 控制帧率
    clock.tick(60)  # 设置刷新帧率为 60 帧/秒

# 退出Pygame
pygame.quit()
sys.exit()
