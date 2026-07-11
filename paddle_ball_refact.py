import tkinter as tk
import random


class Ball:
    def __init__(self, canvas, paddle, color):
        self.canvas = canvas
        self.paddle = paddle
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color)
        self.canvas.move(self.id, 245, 100)

        starts = [-3, -2, -1, 1, 2, 3]
        random.shuffle(starts)
        self.x = starts[0]
        self.y = -3

        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.hit_bottom = False

    def hit_paddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                return True
        return False

    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)

        if pos[1] <= 0:
            self.y = 3
        if pos[3] >= self.canvas_height:
            self.hit_bottom = True
        if self.hit_paddle(pos):
            self.y = -3
        if pos[0] <= 0:
            self.x = 3
        if pos[2] >= self.canvas_width:
            self.x = -3


class Paddle:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)
        self.canvas.move(self.id, 200, 300)
        self.x = 0
        self.canvas_width = self.canvas.winfo_width()

        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        self.canvas.bind_all('<KeyRelease-Left>', self.stop)
        self.canvas.bind_all('<KeyRelease-Right>', self.stop)

    def draw(self):
        pos = self.canvas.coords(self.id)
        # Bug Fix: Allow movement but prevent the paddle from slipping off-screen
        if pos[0] + self.x >= 0 and pos[2] + self.x <= self.canvas_width:
            self.canvas.move(self.id, self.x, 0)

    def turn_left(self, evt):
        self.x = -3

    def turn_right(self, evt):
        self.x = 3

    def stop(self, evt):
        self.x = 0


class Game:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Game")
        self.root.resizable(0, 0)
        self.root.wm_attributes("-topmost", 1)

        self.canvas = tk.Canvas(self.root, width=500,
                                height=400, bd=0, highlightthickness=0)
        self.canvas.pack()
        self.root.update()

        self.paddle = Paddle(self.canvas, 'blue')
        self.ball = Ball(self.canvas, self.paddle, 'red')

        self.game_loop()

    def game_loop(self):
        if not self.ball.hit_bottom:
            self.ball.draw()
            self.paddle.draw()
            self.root.update_idletasks()
            self.root.update()
            # Loop safely using Tkinter's internal clock (10ms interval)
            self.root.after(10, self.game_loop)
        else:
            self.canvas.create_text(
                250, 200, text="GAME OVER", font=("Arial", 20), fill="black")


if __name__ == "__main__":
    game = Game()
    game.root.mainloop()
