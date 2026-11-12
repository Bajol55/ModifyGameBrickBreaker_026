import tkinter as tk


class GameObject(object):
    def __init__(self, canvas, item):
        self.canvas = canvas
        self.item = item

    def get_position(self):
        return self.canvas.coords(self.item)

    def move(self, x, y):
        self.canvas.move(self.item, x, y)

    def delete(self):
        self.canvas.delete(self.item)


class Ball(GameObject):
    def __init__(self, canvas, x, y):
        self.radius = 10
        self.direction = [1, -1]
        self.speed = 10
        # Warna bola diubah menjadi hijau terang (#2ecc71)
        item = canvas.create_oval(
            x - self.radius,
            y - self.radius,
            x + self.radius,
            y + self.radius,
            fill='#2ecc71',
            outline='#27ae60',
        )
        super(Ball, self).__init__(canvas, item)

    def update(self):
        coords = self.get_position()
        width = self.canvas.winfo_width()
        if coords[0] <= 0 or coords[2] >= width:
            self.direction[0] *= -1
        if coords[1] <= 0:
            self.direction[1] *= -1
        x = self.direction[0] * self.speed
        y = self.direction[1] * self.speed
        self.move(x, y)

    def collide(self, game_objects):
        coords = self.get_position()
        x = (coords[0] + coords[2]) * 0.5
        if len(game_objects) > 1:
            self.direction[1] *= -1
        elif len(game_objects) == 1:
            game_object = game_objects[0]
            coords = game_object.get_position()
            if x > coords[2]:
                self.direction[0] = 1
            elif x < coords[0]:
                self.direction[0] = -1
            else:
                self.direction[1] *= -1

        for game_object in game_objects:
            if isinstance(game_object, Brick):
                game_object.hit()


class Paddle(GameObject):
    def __init__(self, canvas, x, y):
        self.width = 80
        self.height = 10
        self.ball = None
        item = canvas.create_rectangle(
            x - self.width / 2,
            y - self.height / 2,
            x + self.width / 2,
            y + self.height / 2,
            fill='#f1c40f',  # Kuning keemasan
        )
        super(Paddle, self).__init__(canvas, item)

    def set_ball(self, ball):
        self.ball = ball

    def move(self, offset):
        coords = self.get_position()
        width = self.canvas.winfo_width()
        if coords[0] + offset >= 0 and coords[2] + offset <= width:
            super(Paddle, self).move(offset, 0)
            if self.ball is not None:
                self.ball.move(offset, 0)
class Brick(GameObject):
    # Warna blok kustom berdasarkan sisa hits (1: Pink, 2: Oranye, 3: Ungu)
    COLORS = {1: '#ff7675', 2: '#fab1a0', 3: '#a29bfe'}

    def __init__(self, canvas, x, y, hits, game):
        self.width = 75
        self.height = 20
        self.hits = hits
        self.game = game  # Referensi ke objek Game untuk menambah skor
        color = Brick.COLORS[hits]
        item = canvas.create_rectangle(
            x - self.width / 2,
            y - self.height / 2,
            x + self.width / 2,
            y + self.height / 2,
            fill=color,
            tags='brick',
        )
        super(Brick, self).__init__(canvas, item)

    def hit(self):
           self.hits -= 1
           # Tambah skor setiap kali brick terkena (misal: 10 poin per hit)
           self.game.add_score(10)
   
           if self.hits == 0:
               self.delete()
           else:
               self.canvas.itemconfig(self.item, fill=Brick.COLORS[self.hits])
   
   
class Game(tk.Frame):
       def __init__(self, master):
           super(Game, self).__init__(master)
           self.lives = 3
           self.score = 0
           self.width = 610
           self.height = 400
           self.canvas = tk.Canvas(
               self, bg='#2d3436', width=self.width, height=self.height
           )  # Background agak gelap agar warna bola & blok lebih kontras
           self.canvas.pack()
           self.pack()
   
           self.items = {}
           self.ball = None
           self.paddle = Paddle(self.canvas, self.width / 2, 326)
           self.items[self.paddle.item] = self.paddle
           for x in range(5, self.width - 5, 75):
               self.add_brick(x + 37.5, 50, 2)
               self.add_brick(x + 37.5, 70, 1)
               self.add_brick(x + 37.5, 90, 1)
   
           self.hud = None
           self.score_hud = None
           self.setup_game()
           self.canvas.focus_set()
           self.canvas.bind('<Left>', lambda _: self.paddle.move(-10))
           self.canvas.bind('<Right>', lambda _: self.paddle.move(10))
   
       def setup_game(self):
                  self.add_ball()
                  self.update_hud_text()
                  self.text = self.draw_text(300, 200, 'Press Space to start')
                  self.canvas.bind('<space>', lambda _: self.start_game())
          
def add_ball(self):
                  if self.ball is not None:
                      self.ball.delete()
                  paddle_coords = self.paddle.get_position()
                  x = (paddle_coords[0] + paddle_coords[2]) * 0.5
                  self.ball = Ball(self.canvas, x, 310)
                  self.paddle.set_ball(self.ball)
          
def add_brick(self, x, y, hits):
                  brick = Brick(self.canvas, x, y, hits, self)
                  self.items[brick.item] = brick
          
