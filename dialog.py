import pygame
import request


class Dialog:
    def __init__(self, screen, width, height, callback, callback2):
        self.callback = callback
        self.callback2 = callback2
        self.screen = screen
        self.width = width
        self.height = height
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = screen.get_rect().center
        self.input_box = pygame.Rect(0, 0, width - 20, 32)
        self.input_box.center = self.rect.center
        self.text = ""
        self.max_input_length = 10  # 最大输入长度
        self.active = False
        self.color_inactive = pygame.Color('blue')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.font = pygame.font.Font(None, 32)
        self.txt_surface = self.font.render(self.text, True, self.color)
        self.close_button = pygame.Rect(
            self.rect.right - 30, self.rect.top, 30, 30)
        self.save_button = pygame.Rect(
            self.rect.left, self.rect.bottom - 40, 100, 30)
        self.save_button.centerx = self.rect.centerx
        self.upload = False
        self.upload_text = ""
        self.tip = "Save"

    def handle_event(self, event):
        if not self.active:
            return
        if event.type == pygame.MOUSEBUTTONDOWN:
            # if self.rect.collidepoint(event.pos):
            #     self.active = not self.active
            # # else:
            # #     self.active = False
            # self.color = self.color_active if self.active else self.color_inactive
            if self.is_close_clicked(event.pos):
                self.active = False  # 关闭弹框，清除输入框文本
                self.callback(False)  # 继续游戏
                self.clear_text()
            if self.is_save_clicked(event.pos):
                self.active = False  # 关闭弹框
                self.callback(False)  # 继续游戏
                if self.upload:
                    self.upload_data()
        if event.type == pygame.KEYDOWN:
            if self.active:
                # if self.upload:
                #     if event.key == pygame.K_RETURN:
                #         self.upload_data()
                # else:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.upload_data()
                    self.active = False  # 关闭弹框
                    self.callback(False)  # 继续游戏
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if len(self.text) < self.max_input_length:
                        self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, self.color)

    def upload_data(self):
        if len(self.text) == 0 or self.text.isspace():
            self.upload_text = "unknow," + self.upload_text
        else:
            self.upload_text = self.text + "," + self.upload_text
        post_data = self.upload_text.split(",")
        print(post_data)
        request.send_post_request(post_data[0], post_data[1], self.callback2)
        # self.callback2(post_data)
        self.active = False  # 关闭弹框
        self.upload = False
        self.upload_text = ''

    def draw_upload(self, upload_text):
        self.active = True
        self.upload = True
        self.upload_text = upload_text
        self.tip = "Upload"
        self.draw()

    def draw_save(self):
        self.active = True
        self.upload = False
        self.tip = "Save"
        self.draw()

    def draw(self):
        self.callback(True)  # 暂停游戏
        self.screen.fill((155, 155, 155), self.rect)
        pygame.draw.rect(self.screen, self.color, self.input_box, 2)
        self.screen.blit(self.txt_surface, (self.input_box.x + 5, self.input_box.y + 5))
        pygame.draw.rect(self.screen, (0, 0, 0), self.input_box, 2)
        pygame.draw.rect(self.screen, (155, 155, 155), self.close_button)
        pygame.draw.rect(self.screen, (155, 155, 155), self.save_button)
        self.screen.blit(self.font.render('X', True, (255, 255, 255)), self.close_button)
        self.screen.blit(self.font.render(self.tip, True, (255, 255, 255)), self.save_button)

    def is_save_clicked(self, pos):
        return self.save_button.collidepoint(pos)

    def is_close_clicked(self, pos):
        return self.close_button.collidepoint(pos)

    def get_text(self):
        return self.text

    def clear_text(self):
        self.text = ''
        self.txt_surface = self.font.render(self.text, True, self.color)
