import tkinter as tk
from tkinter import simpledialog, messagebox
import random

class HorseApp:
    special_horse = None  # 클래스 속성으로 이기기 쉬운 말을 정의합니다.

    def __init__(self, root):
        # 애플리케이션 초기화
        self.root = root
        self.root.title("경마 게임")
        self.canvas = tk.Canvas(root, width=800, height=600)
        self.canvas.pack()

        # 말의 이름과 말의 수
        self.horses = ["골드쉽", "키타산 블랙", "토카이 테이오", "맨하탄 카페", "하루 우라라"]
        self.num_horses = simpledialog.askinteger("Input", "몇 개의 경마를 입력하시겠습니까? (최대 5개): ")
        self.num_horses = min(self.num_horses, 5)
        self.horses = self.horses[:self.num_horses]

        # 경주 매개변수
        self.positions = [0] * self.num_horses
        self.finish_line = 500
        self.colors = ['orange', 'green', 'red', 'lightblue', 'lightpink']
        self.horse_shapes = []
        self.horse_texts = []

        # 키보드 이벤트 바인딩
        self.root.bind("<KeyPress>", self.key_press_event)

        # 경주 시작 및 재시작 버튼
        self.start_race_button = tk.Button(root, text="경주 시작", command=self.start_race)
        self.start_race_button.pack()

        self.restart_btn = tk.Button(root, text="다시하기", command=self.restart)
        self.restart_btn.pack()

        # 결승선 그리기
        self.draw_finish_line()
        self.start_race()

    def draw_finish_line(self):
        # 캔버스에 결승선 그리기
        self.canvas.create_line(self.finish_line + 50, 0, self.finish_line + 50, 600, fill="black", dash=(4, 2))
        self.canvas.create_text(self.finish_line + 50, 20, text="결승선", anchor="n")

    def start_race(self):
        # 경마 시작
        self.start_race_button.config(state=tk.DISABLED)
        self.restart_btn.config(state=tk.DISABLED)
        self.horse_shapes = []
        self.horse_texts = []
        self.positions = [0] * self.num_horses

        # 각 경주에 대해 특별한 말 선택
        for i, horse in enumerate(self.horses):
            shape = self.canvas.create_rectangle(50, i*100+50, 50, i*100+100, fill=self.colors[i])
            self.horse_shapes.append(shape)
            text_name = self.canvas.create_text(75, i*100+65, text=horse, anchor="w")
            self.horse_texts.append(text_name)
            text_distance = self.canvas.create_text(400, i*100+75, text="0m", anchor="center")
            self.horse_texts.append(text_distance)

        self.update_positions()

    def update_positions(self):
        # 승자가 결정될 때까지 말의 위치 업데이트
        if not all(pos >= self.finish_line for pos in self.positions):
            for i in range(self.num_horses):
                if self.positions[i] < self.finish_line:
                    if self.horses[i] == self.special_horse:
                        move_distance = random.randint(20, 50)  # 이기기 쉬운 말은 20에서 50 사이의 거리 이동
                    else:
                        move_distance = random.randint(10, 40)  # 다른 말들은 10에서 40 사이의 거리 이동
                    new_position = self.positions[i] + move_distance
                    if new_position > self.finish_line:
                        new_position = self.finish_line
                    self.positions[i] = new_position
                    self.canvas.coords(self.horse_shapes[i], 50, i*100+50, 50 + self.positions[i], i*100+100)
                    self.canvas.itemconfig(self.horse_texts[i*2+1], text=f"{self.positions[i]}m")

                    if self.positions[i] >= self.finish_line:
                        winner_index = i + 1
                        winner_name = self.horses[i]
                        print(f"우승한 경마는 {winner_index}번 경마, '{winner_name}'입니다!")
                        self.start_race_button.config(state=tk.NORMAL)
                        self.restart_btn.config(state=tk.NORMAL)
                        return

            self.root.after(1000, self.update_positions)

    def key_press_event(self, event):
        # 이기기 쉬운 말 선택을 위한 키보드 이벤트 처리
        key = event.char
        if key.isdigit() and int(key) in range(1, self.num_horses + 1):
            self.special_horse = self.horses[int(key) - 1]  # 선택된 말을 이기기 쉬운 말로 설정
            print(f"이기기 쉬운 말로 {self.special_horse}이(가) 선택되었습니다.")

    def restart(self):
        # 게임 재시작
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
# 화면에서 1~5사이의 숫자를 누르면 해당 번호의 말이 이기기 쉬운 말로 변경
