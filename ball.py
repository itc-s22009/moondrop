import random
import math
from paddle import Paddle
from tkinter import messagebox


class Ball:
    """ ボールクラス
    円を描く関数を使って表現する。
    """
    
    def __init__(self, canvas, color, paddle, block):
        """ 初期化処理
        メイン側から Canvas を受け取る。
        ボールの色も str 型で受け取る。
        衝突判定に使うパドルを受け取る。
        """
        self.canvas = canvas
        self.paddle = paddle
        self.block = block
        
        # 楕円を描く関数できれいな円を描画する。識別番号を保持しておく。
        self.id = self.canvas.create_oval(45, 45, 90, 90, fill=color)
        # 画面サイズ(縦/横)を取得しておく。
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        # ボールの初期位置を計算で決める。リセット時のことを考えて保存しておく。
        self.init_x = self.canvas_width / 2 - 7.5
        self.init_y = self.canvas_height / 6 - 7.5
        # ボールの移動スピードをとりあえず0で作っておく
        self.speed = 0
        # ボールのx/yのスピードを0でとりあえず初期化
        self.x = 0
        self.y = 0

        self.score = 0

        self.speedif = 0



    def start(self, evt):
        # ボール移動中なら何もしない
        if self.speed != 0:
            return
        
        # 初期位置へ移動(絶対座標)
        self.canvas.moveto(self.id, self.init_x, self.init_y)
        self.speed = 8  # 移動スピード
        """ 発射角度のリストを生成(angle の処理内容)
            1 - range() で 20 - 60 のデータを作成
            2 - list() でリスト型に変換
            3 - random.choice() でリストから1個をランダムで選択
            4 - math.radians() で度数法から弧度法(ラジアン)に変換
        """
        angle = math.radians(random.choice(list(range(20, 65, 5))))
        direction = random.choice([1, -1])  # xの向きをランダムに。
        # 三角関数をつかって、x軸y軸それぞれの移動速度を求める。
        self.x = math.cos(angle) * self.speed * direction
        self.y = math.sin(angle) * self.speed
    
    def draw(self):
        self.stop_paddle = self.paddle.stop_paddle

        self.canvas.create_text(950, 50, text=f'{self.score} SHOT', fill="white", font=("System", 20), tag="text")
        # ボールを移動させる
        self.canvas.move(self.id, self.x, self.y)

        # 移動したあとの座標(左上xy,右下xy)を取得する
        pos = self.canvas.coords(self.id)

        # 左に当たった(pos[0]が越えた)かどうか
        if pos[0] <= 0:
            self.fix(pos[0] - 0, 0)

        # 上に当たった(pos[1]が越えた)かどうか
        if pos[1] <= 0:
            self.fix(0, pos[1])
            if self.speedif == 1:
                self.speedif = 0
                self.x /= 2.5
                self.y /= 2.5

        # 右に当たった(pos[2]が越えた)かどうか
        if pos[2] >= self.canvas_width:
            self.fix(pos[2] - self.canvas_width, 0)

        # 下に当たった(pos[3]が越えた)かどうか
        if pos[3] >= self.canvas_height:
            self.fix(0, pos[3] - self.canvas_height)
            self.failed()  #プレイヤーのミスを処理する関数を呼ぶ

            #self.gameOver()#

        # パドルとの衝突判定
        paddle_pos = self.canvas.coords(self.paddle.id)
        # b.x2 >= p.x1
        # b.x1 <= p.x2
        # p.y1 <= b.y2 <= p.y2
        
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2] \
           and paddle_pos[1] <= pos[3] <= paddle_pos[3]:
            self.fix(0, pos[3] - paddle_pos[1])
            self.canvas.delete('text')
            self.score += 1
            if self.stop_paddle == 0:
                self.x *= 2.5
                self.y *= 2.5
                self.speedif = 1
                #self.block.setblock()
            
        block_pos = self.canvas.coords(self.block.id)
        
        if pos[2] >= block_pos[0] and pos[0] <= block_pos[2] \
           and pos[1] <= block_pos[3] and pos[3] >= block_pos[1]:
            if pos[0] <=  block_pos[2] and pos[0] >= block_pos[0]:
                self.x *= -1
            if pos[1] <= block_pos[3] and pos[1] >= block_pos[1]:
                self.y *= -1
            if pos[2] >= block_pos[0] and pos[2] <= block_pos[2]:
                self.x *= -1
            
            if pos[3] >= block_pos[1] and pos[3] <= block_pos[3]:
                self.y *= -1
            self.canvas.delete("Block")
            self.block.setblock()
            self.score += 5
            self.canvas.delete("text")
        
    def fix(self, diff_x, diff_y):
        # x/y の差分を受け取って、2倍した数を逆に移動する。
        self.canvas.move(self.id, -(diff_x * 2), -(diff_y * 2))

        # 差分があったら(0でなければ)跳ね返ったとして向きを反転させる。
        if diff_x != 0:
            self.x = -self.x
            
        if diff_y != 0:
            self.y = -self.y 

    def failed(self):
        # 動きを止める
        self.x = 0
        self.y = 0
        self.speed = 0
        messagebox.showinfo("Infomation","GAME OVER!!")
        self.score = 0
        self.canvas.delete('text')
'''''
    def gameOver():
        messagebox.showinfo("Infomation","GAME OVER!!")
'''''