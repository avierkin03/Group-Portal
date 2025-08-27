import pygame
pygame.init()

#створюємо фон та ігрове вікно
back = (200,255,255)
mw = pygame.display.set_mode((500, 500))
mw.fill(back)

clock = pygame.time.Clock()

#змінні що відповідають за координати платформи
platform_x = 200
platform_y = 330

#змінні що відповідають за переміщення м'яча
dx = 3
dy = 3

#змінні що відповідають за рух платформи
move_right = False
move_left = False

#Клас, що визначає прямокутну область навколо спрайта
class Area():
    def __init__(self, x=0, y=0, width=10, height=10, color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.fill_color = back
        if color:
            self.fill_color = color

    def color(self, new_color):
        self.self.fill_color = new_color
    
    def fill(self):
        pygame.draw.rect(mw, self.fill_color, self.rect)
    
    def collidepoint(self, x, y):
        return self.rect.collidepoint(x,y)
    
    def colliderect(self, rect):
        return self.rect.colliderect(rect)

#Клас для об'єктів-картинок
class Picture(Area):
    def __init__(self, filename, x=0, y=0, width=10, height=10):
        Area.__init__(self, x=x, y=y, width=width, height=height, color=None)
        self.image = pygame.image.load(filename)

    def draw(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))

#Клас написів "You Win" та "You Lose"
class Label(Area):
  def set_text(self, text, fsize=12, text_color=(0, 0, 0)):
      self.image = pygame.font.SysFont('verdana', fsize).render(text, True, text_color)
  def draw(self, shift_x=0, shift_y=0):
      self.fill()
      mw.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))

#створення м'яча та платформи
ball = Picture('hero.png', 160, 200, 50, 50)
platform = Picture('platform.png', platform_x, platform_y, 100, 30)

#створення ворогів
start_x = 5
start_y = 5
count = 9
monsters = []
for j in range(3):
    y = start_y + (55*j)
    x = start_x + (27.5*j)
    for i in range(count):
        monster = Picture('pixil-frame-0.png', x, y, 50, 50)
        monsters.append(monster)
        x += 55
    count -= 1

#змінні що відповідає за закінчення гри
game_over = False
finish = False
monsters_destroyed =0

#Ігровий цикл
while not game_over:
    ball.fill()
    platform.fill()
    #перевіряємо яка кнопка натиснута
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finish = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                move_right = True
            if event.key == pygame.K_LEFT:
                move_left = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                move_right = False
            if event.key == pygame.K_LEFT:
                move_left = False
    #умова руху вправо
    if move_right:
        platform.rect.x += 3
    #умова руху вліво
    if move_left:
        platform.rect.x -= 3
    #додаємо постійне прискорення м'ячу
    ball.rect.x += dx
    ball.rect.y += dy
    #якщо м'яч досягає меж екрану, міняємо напрямок руху
    if ball.rect.y < 0:
        dy *= -1
    if ball.rect.x > 450 or ball.rect.x < 0:
        dx *= -1
    #умова програшу (м'яч знаходиться нижче платформи)
    if ball.rect.y > 350:
        time_text = Label(150,150,50,50,back)
        time_text.set_text('YOU LOSE',60, (255,0,0))
        time_text.draw(10, 10)
        game_over = True
    #умова виграшу (не залишилося монстрів)
    if len(monsters) == 0:
        time_text = Label(150,150,50,50,back)
        time_text.set_text('YOU WIN',60, (0,200,0))
        time_text.draw(10, 10)
        game_over = True
    #якщо м'яч торкнувся платформи, міняємо напрямок руху
    if ball.rect.colliderect(platform.rect):
        dy *= -1
    #малюємо монстрів
    for m in monsters:
        m.draw()
        #якщо монстра торкнувся м'яч, видаляємо монстра зі списку та міняємо напрямок руху м'яча
        if m.rect.colliderect(ball.rect):
            monsters.remove(m)
            m.fill()
            monsters_destroyed += 1
            dy *= -1
    #виводимо рахунок
    # font = pygame.font.Font(None, 35)
    # text = font.render(f"{monsters_destroyed}", True, (255, 0, 0))
    # p=mw.copy()
    # mw.blit(p, (0, 0))  # Відобразити попередній фон
    # mw.blit(text, (10, 10))  # Відобразити новий текст
    #малюємо платформу та м'яч
    platform.draw()
    ball.draw()
    pygame.display.update()
    clock.tick(40)