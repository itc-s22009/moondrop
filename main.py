from tkinter import *

from ball import Ball
from paddle import Paddle
from block import Block
from PIL import Image, ImageTk

class Game:
    """ ゲームのメインクラス
    このクラスで、ゲーム全体のコントロールをします。
    処理の流れとして、全体像が把握できるように作る。
    """

    def __init__(self):
        """ 基本的な初期化をします。
        Tk オブジェクトの生成や初期設定をします。
        ゲームに必要なオブジェクトの準備をします。
        """

        # tkinter を使用するときの基本部分
        self.tk = Tk()
        self.tk.title("MOON DROP")                       # Tk本体(GUIのウィンドウ)
        self.tk.resizable(False, False)             # ウィンドウのサイズ変更を許可するかどうか。横・縦
        self.tk.wm_attributes("-topmost", True)     # ウィンドウを常に前面に。
        self.img1 = Image.open('space.png')
        self.img1 = ImageTk.PhotoImage(self.img1)
        # 図形描画に使う Canvas オブジェクトの準備
        self.canvas = Canvas(self.tk, width=1024, height=768, bd=False, bg="black")
        self.canvas.pack()      # canvas をメインウィンドウ(tk)に組み込んで表示
        self.canvas.create_image(0, 0, image=self.img1, anchor=NW)
        

        #self.canvas.create_image(0,0, imag=img)

        self.tk.update()        # tk の状態を更新

        # ゲームの準備
        self.block = Block(self.canvas, "blue")
        self.paddle = Paddle(self.canvas, "white")
        self.ball = Ball(self.canvas, "yellow", self.paddle, self.block)

        #self.block = Block(self.canvas, "Blue", self.ball)

        # イベントハンドラ設定(キー入力の反映)
        self.canvas.bind_all("<KeyPress-a>", self.paddle.turn_left)
        self.canvas.bind_all("<KeyPress-d>", self.paddle.turn_right)
        self.canvas.bind_all("<KeyPress-space>", self.ball.start)

        self.canvas.bind_all("<KeyRelease-a>", self.paddle.slip_left)
        self.canvas.bind_all("<KeyRelease-d>", self.paddle.slip_right)

        self.canvas.bind_all("<KeyPress-Shift_L>",self.paddle.stop)
        self.canvas.bind_all("<KeyRelease-Shift_L>",self.paddle.accelerator)

        #self.canvas.bind_all("<KeyPress-w>",self.paddle.up)
        #self.canvas.bind_all("<KeyPress-s>",self.paddle.down)

    



    def main(self):
        """ ゲームを動かすための関数
        必ず初期化後に呼び出す。
        """
        self.update()       # 更新処理の関数
        self.tk.mainloop()  # Tk 使うときに、プログラムが一瞬で終了しないようにする。
    def update(self):
        # ボールの更新処理
        self.ball.draw()
        # パドルの更新処理
        self.paddle.draw()

        # 次回 update の呼び出し予約
        self.canvas.after(1000 // 60, self.update)
        

game = Game()
game.main()