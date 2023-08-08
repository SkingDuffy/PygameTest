import pygame
import random

# 初始化Pygame
pygame.init()

# 设置窗口大小和标题
window_width = 1200
window_height = 1000
window_title = "坦克大战游戏"

# 创建游戏窗口
screen = pygame.display.set_mode((window_width, window_height), pygame.DOUBLEBUF)
pygame.display.set_caption(window_title)

# 加载坦克图像
tank_image = pygame.image.load('/Users/fmq/GolandProjects/PygameTest/tank.png')
# 加载子弹图像
bullet_image = pygame.image.load('/Users/fmq/GolandProjects/PygameTest/bullet.png')
# 加载敌人图像
enemy_image = pygame.image.load('/Users/fmq/GolandProjects/PygameTest/enemy.png')

# 加载射击声音效
shoot_sound = pygame.mixer.Sound('/Users/fmq/GolandProjects/PygameTest/launch.wav')
# 加载爆炸声音效
explosion_sound = pygame.mixer.Sound('/Users/fmq/GolandProjects/PygameTest/score.wav')

# 设置坦克的初始位置
tank_x = window_width // 2
tank_y = window_height // 2

# 设置坦克的移动速度
tank_speed = 5

# 设置子弹的尺寸和移动速度
bullet_width = 100
bullet_height = 100
bullet_speed = 10

# 自定义子弹类
class Bullet:
	def __init__(self, x, y, direction):
		# self.original_image = bullet_image  # 保留原始图像
		# self.image = pygame.transform.scale(self.original_image, (bullet_width, bullet_height))
		self.rect = bullet_image.get_rect(center=(x, y))
		self.direction = direction

	def move(self):
		if self.direction == "UP":
			self.rect.y -= bullet_speed
		elif self.direction == "DOWN":
			self.rect.y += bullet_speed
		elif self.direction == "LEFT":
			self.rect.x -= bullet_speed
		elif self.direction == "RIGHT":
			self.rect.x += bullet_speed
		# 如果子弹移出窗口，将其从 bullets 列表中移除
		if self.rect.right < 0 or self.rect.left > window_width or self.rect.bottom < 0 or self.rect.top > window_height:
			bullets.remove(self)
	
	def draw(self, surface):
		surface.blit(bullet_image, self.rect)

# 子弹列表
bullets = []

# 上一次的方向
last_direction = "UP"

# 定义敌人类
class Enemy:
	def __init__(self, x, y, speed_x, speed_y):
		# self.image = pygame.Surface((80, 80))
		# self.image.fill((255, 0, 0))  # 红色表示敌人
		self.image = enemy_image
		self.rect = self.image.get_rect(center=(x, y))
		self.speed_x = speed_x
		self.speed_y = speed_y

	def move(self):
		self.rect.x += self.speed_x
		self.rect.y += self.speed_y
		# 如果子弹移出窗口，将其从 bullets 列表中移除
		if self.rect.right < 0 or self.rect.left > window_width or self.rect.bottom < 0 or self.rect.top > window_height:
			enemies.remove(self)

# 创建敌人列表
enemies = []

# 创建 Clock 对象
clock = pygame.time.Clock()

# 游戏主循环
running = True
while running:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.KEYDOWN:
			# 按下空格键发射子弹
			if event.key == pygame.K_SPACE:
				print("tank_x_speed = ", tank_x_speed, "tank_y_speed = ", tank_y_speed, "last_direction = ", last_direction)
				# 添加新子弹到子弹列表，根据坦克的移动方向设置子弹的射击方向
				if last_direction == "LEFT":
					last_bullet = Bullet(tank_x, tank_y + tank_image.get_height() // 2, "LEFT")
				elif last_direction == "RIGHT":
					last_bullet = Bullet(tank_x + tank_image.get_width(), tank_y + tank_image.get_height() // 2, "RIGHT")
				elif last_direction == "UP":
					last_bullet = Bullet(tank_x + tank_image.get_width() // 2, tank_y, "UP")
				elif last_direction == "DOWN":
					last_bullet = Bullet(tank_x + tank_image.get_width() // 2, tank_y + tank_image.get_height(), "DOWN")
				bullets.append(last_bullet)
				# 播放射击声音效
				shoot_sound.play()	
	
	# 获取按键状态
	keys = pygame.key.get_pressed()
	# 根据按键状态移动坦克
	if keys[pygame.K_LEFT]:
		tank_x_speed = -tank_speed
		last_direction = "LEFT"
	elif keys[pygame.K_RIGHT]:
		tank_x_speed = tank_speed
		last_direction = "RIGHT"
	else:
		tank_x_speed = 0

	if keys[pygame.K_UP]:
		tank_y_speed = -tank_speed
		last_direction = "UP"
	elif keys[pygame.K_DOWN]:
		tank_y_speed = tank_speed
		last_direction = "DOWN"
	else:
		tank_y_speed = 0

	# 移动坦克，如果超出窗口则不移动
	tank_x += tank_x_speed
	tank_y += tank_y_speed
	if tank_x < 0:
		tank_x = 0
	if tank_x > window_width - tank_image.get_width():
		tank_x = window_width - tank_image.get_width()
	if tank_y < 0:
		tank_y = 0
	if tank_y > window_height - tank_image.get_height():
		tank_y = window_height - tank_image.get_height()

	 # 移动子弹
	for bullet in bullets:
		bullet.move()
		
	# 随机生成新敌人
	if random.randint(1, 100) < 2:  # 控制生成敌人的频率
		side = random.choice(['top', 'bottom', 'left', 'right'])
		if side == 'top':
			x = random.randint(0, window_width)
			y = 0
			speed_x = 0
			speed_y = random.randint(1, 3)
		elif side == 'bottom':
			x = random.randint(0, window_width)
			y = window_height
			speed_x = 0
			# speed_y = random.randint(-3, -1)
			speed_y = -1
		elif side == 'left':
			x = 0
			y = random.randint(0, window_height)
			# speed_x = random.randint(1, 3)
			speed_x = 1
			speed_y = 0
		elif side == 'right':
			x = window_width
			y = random.randint(0, window_height)
			# speed_x = random.randint(-3, -1)
			speed_x = -1
			speed_y = 0

		new_enemy = Enemy(x, y, speed_x, speed_y)
		enemies.append(new_enemy)

	# 移动敌人
	for enemy in enemies:
		enemy.move()
		
	# 子弹与敌人之间的碰撞检测
	bullets_to_remove = []
	enemies_to_remove = []
	
	for bullet in bullets:
		for enemy in enemies:
			if bullet.rect.colliderect(enemy.rect):
				print("子弹击中敌人")
				bullets_to_remove.append(bullet)
				enemies_to_remove.append(enemy)
				explosion_sound.play()
	# print("enemies size:", len(enemies), "bullets size:", len(bullets))
		
	# 坦克rect
	tank_rect = pygame.Rect(tank_x, tank_y, tank_image.get_width(), tank_image.get_height())
		
	# 坦克与敌人之间的碰撞检测
	for enemy in enemies:
		if tank_rect.colliderect(enemy.rect):
			# 在这里可以处理坦克与敌人碰撞的情况，比如游戏结束等
			print("坦克撞击敌人")
			enemies_to_remove.append(enemy)
			explosion_sound.play()
			pass
			
	# 移除碰撞的子弹和敌人
	for bullet in bullets_to_remove:
		bullets.remove(bullet)
	
	for enemy in enemies_to_remove:
		try:
			enemies.remove(enemy)
		except ValueError:
			print("not find id = ", id(enemy))
			for e in enemies_to_remove: print("need remove id = ", id(e))
			pass

	# 绘制背景
	screen.fill((155, 155, 155))

	# 绘制坦克
	screen.blit(tank_image, (tank_x, tank_y))
		
	# 绘制敌人
	for enemy in enemies:
		screen.blit(enemy.image, enemy.rect)

	# 绘制子弹
	for bullet in bullets:
		bullet.draw(screen)

	# 控制帧率
	clock.tick(60)  # 设置刷新帧率为 60 帧/秒
	# 更新屏幕
	pygame.display.flip()
	# 刷新窗口
	# pygame.display.update()

# 退出Pygame
pygame.quit()

