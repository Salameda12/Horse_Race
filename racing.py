import tkinter as tk
from tkinter import simpledialog, messagebox
import random

class HorseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Horse Race Game")
        self.canvas = tk.Canvas(root, width=800, height=600)
        self.canvas.pack()

        self.horses = ["골드쉽", "키타산 블랙", "토카이 테이오", "맨하탄 카페", "하루 우라라"]
        self.num_horses = simpledialog.askinteger("Input", "몇 개의 경마를 입력하시겠습니까? (최대 5개): ")
        self.num_horses = min(self.num_horses, 5)
        self.horses = self.horses[:self.num_horses]

        self.positions = [0] * self.num_horses
        self.finish_line = 500
        self.colors = ['orange', 'green', 'red', 'lightblue', 'lightpink']
        self.horse_shapes = []
        self.horse_texts = []

        self.start_race_button = tk.Button(root, text="Start Race", command=self.start_race)
        self.start_race_button.pack()

        self.restart_btn = tk.Button(root, text="다시하기", command=self.restart)
        self.restart_btn.pack()

        self.draw_finish_line()
        self.start_race()

    def draw_finish_line(self):
        self.canvas.create_line(self.finish_line + 50, 0, self.finish_line + 50, 600, fill="black", dash=(4, 2))
        self.canvas.create_text(self.finish_line + 50, 20, text="Finish Line", anchor="n")

    def start_race(self):
        self.start_race_button.config(state=tk.DISABLED)
        self.restart_btn.config(state=tk.DISABLED)
        for i, horse in enumerate(self.horses):
            shape = self.canvas.create_rectangle(50, i*100+50, 50, i*100+100, fill=self.colors[i])
            self.horse_shapes.append(shape)
            # 말의 이름을 사각형 위에 표시
            text_name = self.canvas.create_text(75, i*100+65, text=horse, anchor="w")
            self.horse_texts.append(text_name)
            # 거리 표시
            text_distance = self.canvas.create_text(400, i*100+75, text="0m", anchor="center")
            self.horse_texts.append(text_distance)

        self.update_positions()

    def update_positions(self):
        if not all(pos >= self.finish_line for pos in self.positions):
            for i in range(self.num_horses):
                if self.positions[i] < self.finish_line:
                    move_distance = random.randint(10, 40)  # 이동 거리를 10에서 40 사이의 랜덤값으로 설정
                    new_position = self.positions[i] + move_distance
                    if new_position > self.finish_line:  # 500m를 넘어가면 500m로 고정
                        new_position = self.finish_line
                    self.positions[i] = new_position
                    self.canvas.coords(self.horse_shapes[i], 50, i*100+50, 50 + self.positions[i], i*100+100)  # 말의 이동 거리를 반영하여 좌표 업데이트
                    self.canvas.itemconfig(self.horse_texts[i*2+1], text=f"{self.positions[i]}m")  # 말의 위치를 미터(m) 단위로 표시

                    if self.positions[i] >= self.finish_line:
                        winner_index = i + 1  # 0이 아닌 1부터 시작하도록 인덱스에 1을 더해줍니다.
                        winner_name = self.horses[i]
                        self.canvas.create_text(400, 300, text=f"우승한 경마는 {winner_index}번 경마, '{winner_name}'입니다!", font=('Helvetica', 24), fill='black')
                        self.start_race_button.config(state=tk.NORMAL)
                        self.restart_btn.config(state=tk.NORMAL)
                        return  # 경주가 끝났으므로 함수를 종료합니다.

            self.root.after(1000, self.update_positions)  # 1초마다 update_positions() 호출하여 이동 거리 갱신

    def restart(self):
        self.canvas.delete("all")
        self.horse_shapes.clear()
        self.horse_texts.clear()
        self.draw_finish_line()
        self.num_horses = simpledialog.askinteger("Input", "몇 개의 경마를 입력하시겠습니까? (최대 5개): ")
        self.num_horses = min(self.num_horses, 5)
        self.horses = ["골드쉽", "키타산 블랙", "토카이 테이오", "맨하탄 카페", "하루 우라라"][:self.num_horses]
        self.positions = [0] * self.num_horses
        self.start_race()

if __name__ == "__main__":
    root = tk.Tk()
    app = HorseApp(root)
    root.mainloop()
