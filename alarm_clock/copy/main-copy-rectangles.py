import tkinter as tk
from tkinter import ttk
# Alarm clock that I wanted to create based on android alam clock but for windows


class AlarmApp(tk.Tk):
    def __init__(self, height, width, title):
        super().__init__()
        self.title(title)
        self.height = height
        self.width = width
        self.geometry(f'{self.height}x{self.width}')
        self.config(bg='gray')
        self.update_idletasks()
        self.canvas = None

    def alarm_event(self, b):
        def fn(*arg):
            print(b)
        return fn

    def draw_buttons_ui_alarm(self, canvas):
        print('kekw')
        label = tk.Label(canvas, text="Click the Button to Exit", font=('Helvetica 17 bold')).pack()
        ttk.Button(
            canvas,
            text="+",
            command=self.alarm_event('add')
        ).pack(side="left")
        ttk.Button(
            canvas,
            text="-",
            command=self.alarm_event('delete')
        ).pack()

    def create_scrollbar_to_canvas(self, canvas):
        scrollbar = ttk.Scrollbar(canvas, orient="vertical", command=canvas.yview)
        scrollbar.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack()
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def draw_alarm_boxes(self, count, width, height, margin_left=25, margin_top=25):
        self.canvas = tk.Canvas(
            self,
            height=self.winfo_height() + (height * count),
            width=self.winfo_width(),
            bg="blue"
        )

        for x in range(margin_left, width, width):
            for y in range(margin_top, (count * height), height):
                self.canvas.create_rectangle(x, y, x + width, y + height, fill="green", outline='black')
            tag = f"kekw{x}"
            self.canvas.tag_bind(tag, "<Button-1>", self.alarm_event(tag))
        self.create_scrollbar_to_canvas(self.canvas)
        self.draw_buttons_ui_alarm(self.canvas)

def run_program():
    alarm = AlarmApp(1366, 768, 'Alarm Clock')

    alarm.draw_alarm_boxes(44, 250, 50)

    alarm.mainloop()



if __name__ == "__main__":
    run_program()


# window = tk.Tk()
# window.title("Alarm clock")
#label = tk.Label(window, text="Wassup")
#label.pack()




