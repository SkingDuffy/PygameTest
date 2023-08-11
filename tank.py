#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pygame
import random
import os
import sys
from dialog import Dialog


# 初始化Pygame
pygame.init()

# 设置窗口大小和标题
window_width = 1800
window_height = 1000
window_title = "坦克大战游戏"

# 创建游戏窗口
screen = pygame.display.set_mode((window_width, window_height), pygame.DOUBLEBUF)
pygame.display.set_caption(window_title)

# 获取当前文件所在的绝对路径
current_path = os.path.dirname(__file__)
current_path2 = os.path.dirname(os.path.abspath(__file__))
current_path3 = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
# current_path = 'C:/Users/fmq/Documents/HBuilderProjects/PygameTest'
print("当前文件所在路径:", current_path, ", path2 = ", current_path2, ", path3 = ", current_path3)
# 加载坦克图像
# tank_image = pygame.image.load(os.path.join(current_path, 'tank.png'))
# 加载子弹图像
# bullet_image = pygame.image.load(os.path.join(current_path, 'bullet.png'))
# # 加载敌人图像
# enemy_image = pygame.image.load(os.path.join(current_path, 'enemy.png'))
# # 加载背景图像
# bg_image = pygame.image.load(os.path.join(current_path, 'map.png'))

# # 加载射击声音效
# shoot_sound = pygame.mixer.Sound(os.path.join(current_path, 'launch.wav'))
# # 加载爆炸声音效
# score_sound = pygame.mixer.Sound(os.path.join(current_path, 'score.wav'))
# # 加载坦克阵亡音效
# dead_sound = pygame.mixer.Sound(os.path.join(current_path, 'dead.wav'))

tank_image = pygame.image.load('tank.png')
bullet_image = pygame.image.load('bullet.png')
enemy_image = pygame.image.load('enemy.png')
bg_image = pygame.image.load('map.png')
shoot_sound = pygame.mixer.Sound('launch.wav')
score_sound = pygame.mixer.Sound('score.wav')
dead_sound = pygame.mixer.Sound('dead.wav')

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

def rotate_tank(tank_image, tank_angle, tank_x, tank_y):
    # 旋转坦克图像
    rotated_tank = pygame.transform.rotate(tank_image, tank_angle)
    rotated_tank_rect = rotated_tank.get_rect(center=(tank_x, tank_y))
    return rotated_tank_rect
tank_angle = 0

# 设置字体
font_path = "/System/Library/Fonts/PingFang.ttc"  # 选择一个支持中文的字体文件路径
font = pygame.font.Font(font_path, 36)  # 使用默认字体和字号

# 初始化得分
score = 0
level = 0
dead = 0
rank_list = ""


# 游戏主循环
running = True
paused = False  # 添加暂停状态变量

def update_x(new_paused):
	global paused  # 使用global关键字，指示使用全局变量
	paused = new_paused
	print("Updated x = ", paused)

# 创建一个用于存储每行渲染文本的列表
rendered_lines = []

def update_y(new_rank):
	global rank_list, rendered_lines
	rendered_lines = []
	rendered_line0 = font.render('超级排行榜', True, (255, 255, 255))
	rendered_lines.append(rendered_line0)
	for i, user in enumerate(new_rank, start=1):
		# rank_list += '\n' + user.user_name
		# print("rank_list = ", user.user_name)
		line_text = f"第{i}名：{user['user_name']} - 得分：{user['score']}"
		rendered_line = font.render(line_text, True, (255, 255, 255))
		rendered_lines.append(rendered_line)

# 创建弹框实例,,把函数 update_x 作为参数传入
dialog = Dialog(screen, 300, 200, update_x, update_y)

while running:

	level = score // 10

	for event in pygame.event.get():
		dialog.handle_event(event)
		if event.type == pygame.QUIT:
			running = False
		# if event.type == pygame.MOUSEBUTTONDOWN:
		# 	if dialog.is_save_clicked(event.pos):
				# print("Save Clicked")
				# rank_list = dialog.get_text()
				# print("Input Text:", rank_list)
				# dialog.clear_text()
		if event.type == pygame.KEYDOWN:
			# if event.key == pygame.K_RETURN:
			# 	rank_list = dialog.get_text()
			# 	dialog.clear_text()
			# 	print("Input Text:", rank_list)

			# if event.key == pygame.K_1:
			# 	dialog.draw_save()

			if event.key == pygame.K_p:
				paused = not paused
			# 按下空格键发射子弹
			if event.key == pygame.K_SPACE and not paused:
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
	
	if paused:
		if dialog.active:  # 是否绘制弹框
			dialog.draw()
		# 控制帧率
		clock.tick(60)  # 设置刷新帧率为 60 帧/秒
		# 更新屏幕
		pygame.display.flip()
		continue
	
	# 获取按键状态
	keys = pygame.key.get_pressed()
	# 根据按键状态移动坦克
	if keys[pygame.K_LEFT]:
		tank_x_speed = -tank_speed
		last_direction = "LEFT"
		tank_angle = 90
	elif keys[pygame.K_RIGHT]:
		tank_x_speed = tank_speed
		last_direction = "RIGHT"
		tank_angle = 270
	else:
		tank_x_speed = 0

	if keys[pygame.K_UP]:
		tank_y_speed = -tank_speed
		last_direction = "UP"
		tank_angle = 0
	elif keys[pygame.K_DOWN]:
		tank_y_speed = tank_speed
		last_direction = "DOWN"
		tank_angle = 180
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
	if random.randint(1, 100) < 2 + level:  # 控制生成敌人的频率
		side = random.choice(['top', 'bottom', 'left', 'right'])
		if side == 'top':
			x = random.randint(0, window_width)
			y = 0
			speed_x = 0
			speed_y = random.randint(1, 3 + level)
		elif side == 'bottom':
			x = random.randint(0, window_width)
			y = window_height
			speed_x = 0
			speed_y = random.randint(-3 - level, -1)
		elif side == 'left':
			x = 0
			y = random.randint(0, window_height)
			speed_x = random.randint(1, 3 + level)
			speed_y = 0
		elif side == 'right':
			x = window_width
			y = random.randint(0, window_height)
			speed_x = random.randint(-3 - level, -1)
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
				score += 1  # 更新得分
				bullets_to_remove.append(bullet)
				enemies_to_remove.append(enemy)
				score_sound.play()
	# print("enemies size:", len(enemies), "bullets size:", len(bullets))
		
	# 坦克rect
	tank_rect = pygame.Rect(tank_x, tank_y, tank_image.get_width(), tank_image.get_height())
		
	# 坦克与敌人之间的碰撞检测
	for enemy in enemies:
		if tank_rect.colliderect(enemy.rect):
			# 在这里可以处理坦克与敌人碰撞的情况，比如游戏结束等
			print("坦克撞击敌人")
			dead += 1  # 更新得分
			enemies_to_remove.append(enemy)
			dead_sound.play()
			if dead == 1:
				dialog.draw_upload(str(score))
			pass
			
	# 移除碰撞的子弹和敌人
	for bullet in bullets_to_remove:
		try:
			bullets.remove(bullet)
		except ValueError:
			print("not find bullet id = ", id(bullet))
			for b in bullets_to_remove: print("need remove bullet id = ", id(b))
			pass
	
	for enemy in enemies_to_remove:
		try:
			enemies.remove(enemy)
		except ValueError:
			print("not find enemy id = ", id(enemy))
			for e in enemies_to_remove: print("need remove enemy id = ", id(e))
			pass

	# 绘制背景
	screen.fill((0, 0, 0))
	scale = max(window_width / bg_image.get_width(), window_height / bg_image.get_height())  # 计算缩放比例
	scaled_bg = pygame.transform.scale(bg_image, (int(bg_image.get_width() * scale), int(bg_image.get_height() * scale)))  # 缩放图像
	screen.blit(scaled_bg, scaled_bg.get_rect(center=(window_width // 2, window_height // 2)))
	
	# 旋转坦克图像
	rotated_tank = pygame.transform.rotate(tank_image, tank_angle)
	rotated_tank_rect = rotated_tank.get_rect(topleft=(tank_x, tank_y))

	# 绘制坦克
	# screen.blit(tank_image, (tank_x, tank_y))
	screen.blit(rotated_tank, rotated_tank_rect)
		
	# 绘制敌人
	for enemy in enemies:
		screen.blit(enemy.image, enemy.rect)

	# 绘制子弹
	for bullet in bullets:
		bullet.draw(screen)
		
	# 渲染得分文本
	score_text = font.render(f"Score: {score}", True, (255, 255, 255))  # 白色字体
	score_rect = score_text.get_rect()
	score_rect.topleft = (10, 10)  # 文本位置在窗口左上角
	screen.blit(score_text, score_rect)



	level_text = font.render(f"Level: {level}", True, (255, 255, 255))  # 白色字体
	level_rect = score_text.get_rect()
	level_rect.topleft = (10, 10 + score_rect.bottom)  # 文本位置在窗口左上角
	screen.blit(level_text, level_rect)
	dead_text = font.render(f"Dead: {dead}", True, (255, 255, 255))  # 白色字体
	dead_rect = dead_text.get_rect()
	dead_rect.topleft = (10, 10 + level_rect.bottom)  # 文本位置在窗口右上角
	screen.blit(dead_text, dead_rect)

	# rank_text = font.render(f"Rank Board: {rank_list}", True, (255, 255, 255))  # 白色字体
	# rank_rect = dead_text.get_rect()
	# rank_rect.topleft = (window_width - rank_text.get_width() - 10, 10)  # 文本位置在窗口右上角
	# screen.blit(rank_text, rank_rect)

	# 计算总文本高度
	total_text_height = sum(rendered.get_height() for rendered in rendered_lines)
	# 绘制每行文本
	y_pos = (window_height - total_text_height) // 2
	for rendered in rendered_lines:
		screen.blit(rendered, ((window_width - rendered.get_width()) // 2, y_pos))
		y_pos += rendered.get_height()

	if dialog.active:  # 是否绘制弹框
		dialog.draw()

	# 控制帧率
	clock.tick(60)  # 设置刷新帧率为 60 帧/秒
	# 更新屏幕
	pygame.display.flip()
	# 刷新窗口
	# pygame.display.update()

# 退出Pygame
pygame.quit()
