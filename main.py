import pygame
import sys
import random

# 全局定义
SCREEN_X = 600
SCREEN_Y = 600


# 蛇类
# 点以25为单位
class Snake(object):
    # 初始化各种需要的属性 [开始时默认向右/身体块x5]
    def __init__(self):
        self.direction = pygame.K_RIGHT
        self.body = []
        for x in range(5):
            self.add_node()

    # 无论何时 都在前端增加蛇块
    def add_node(self):
        left, top = 0, 0
        if self.body:
            left, top = self.body[0].left, self.body[0].top
        node = pygame.Rect(left, top, 25, 25)
        if self.direction == pygame.K_LEFT:
            node.left -= 25
        elif self.direction == pygame.K_RIGHT:
            node.left += 25
        elif self.direction == pygame.K_UP:
            node.top -= 25
        elif self.direction == pygame.K_DOWN:
            node.top += 25
        self.body.insert(0, node)

    # 删除最后一个块
    def del_node(self):
        self.body.pop()

    # 死亡判断
    def is_dead(self):
        # 撞墙
        if self.body[0].x not in range(SCREEN_X):
            return True
        if self.body[0].y not in range(SCREEN_Y):
            return True
        # 撞自己
        if self.body[0] in self.body[1:]:
            return True
        return False

    # 移动！
    def move(self):
        self.add_node()
        self.del_node()

    # 改变方向 但是左右、上下不能被逆向改变
    def change_direction(self, cur_key):
        LR = [pygame.K_LEFT, pygame.K_RIGHT]
        UD = [pygame.K_UP, pygame.K_DOWN]
        if cur_key in LR + UD:
            if (cur_key in LR) and (self.direction in LR):
                return
            if (cur_key in UD) and (self.direction in UD):
                return
            self.direction = cur_key


# 食物类
# 方法： 放置/移除
# 点以25为单位
class Food:
    def __init__(self):
        self.rect = pygame.Rect(-25, 0, 25, 25)

    def remove(self):
        self.rect.x = -25

    def set(self):
        if self.rect.x == -25:
            all_pos = []
            # 不靠墙太近 25 ~ SCREEN_X-25 之间
            for pos in range(25, SCREEN_X - 25, 25):
                all_pos.append(pos)
            self.rect.left = random.choice(all_pos)
            self.rect.top = random.choice(all_pos)
            print(self.rect)


def show_text(screen, pos, text, color, font_bold=False, font_size=60, font_italic=False):
    # 获取系统字体，并设置文字大小
    cur_font = pygame.font.SysFont("宋体", font_size)
    # 设置是否加粗属性
    cur_font.set_bold(font_bold)
    # 设置是否斜体属性
    cur_font.set_italic(font_italic)
    # 设置文字内容
    text_fmt = cur_font.render(text, 1, color)
    # 绘制文字
    screen.blit(text_fmt, pos)


def main():
    pygame.init()
    screen_size = (SCREEN_X, SCREEN_Y)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption('Snake')
    clock = pygame.time.Clock()
    scores = 0
    is_dead = False

    # 蛇/食物
    snake = Snake()
    food = Food()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                snake.change_direction(event.key)
                # 死后按space重新
                if event.key == pygame.K_SPACE and is_dead:
                    return main()

        screen.fill((255, 255, 255))

        # 画蛇身 / 每一步+1分
        if not is_dead:
            scores += 1
            snake.move()
        for rect in snake.body:
            pygame.draw.rect(screen, (20, 220, 39), rect, 0)

        # 显示死亡文字
        is_dead = snake.is_dead()
        if is_dead:
            show_text(screen, (100, 200), 'YOU DEAD!', (227, 29, 18), False, 100)
            show_text(screen, (150, 260), 'press space to try again...', (0, 0, 22), False, 30)

        # 食物处理 / 吃到+50分
        # 当食物rect与蛇头重合,吃掉 -> Snake增加一个Node
        if food.rect == snake.body[0]:
            scores += 50
            food.remove()
            snake.add_node()

        # 食物投递
        food.set()
        pygame.draw.rect(screen, (136, 0, 21), food.rect, 0)

        # 显示分数文字
        show_text(screen, (50, 500), 'Scores: ' + str(scores), (223, 223, 223))

        pygame.display.update()
        clock.tick(10)


if __name__ == '__main__':
    main()
