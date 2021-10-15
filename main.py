import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser

import PIL as pil
from PIL import Image
from PIL import ImageDraw

# Defining constants
WIDTH, HEIGHT = 600, 600
CENTER = WIDTH // 2
WHITE = (255, 255, 255)


class PaintGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title = "Paint Project:"
        self.brush_width = 15
        self.current_color = "black"
        self.bg_color = "white"
        self.cnv = tk.Canvas(self.root, width=WIDTH - 10, height=HEIGHT - 10, bg=self.bg_color)
        self.cnv.pack()
        self.cnv.bind("<B1-Motion>", self.__paint)
        self.image = pil.Image.new("RGB", (WIDTH, HEIGHT), WHITE)
        self.draw = pil.ImageDraw.Draw(self.image)
        self.btn_frame = tk.Frame(self.root)
        self.btn_frame.pack(fill=tk.X)
        self.btn_frame.rowconfigure(0, weight=1)
        self.btn_frame.rowconfigure(1, weight=1)
        self.btn_frame.rowconfigure(2, weight=1)
        self.btn_frame.columnconfigure(0, weight=1)
        self.btn_frame.columnconfigure(1, weight=1)
        self.btn_frame.columnconfigure(2, weight=1)
        self.clear_btn = tk.Button(self.btn_frame, text="Clear", command=self.__clear)
        self.clear_btn.grid(row=0, column=1, sticky=tk.W + tk.E)
        self.save_btn = tk.Button(self.btn_frame, text="Save", command=self.__save)
        self.save_btn.grid(row=1, column=2, sticky=tk.W + tk.E)
        self.bplus_btn = tk.Button(self.btn_frame, text="B+", command=self.__brush_plus)
        self.bplus_btn.grid(row=0, column=0, sticky=tk.W + tk.E)
        self.b_minus_btn = tk.Button(self.btn_frame, text="B-", command=self.__brush_minus)
        self.b_minus_btn.grid(row=1, column=0, sticky=tk.W + tk.E)
        self.color_btn = tk.Button(self.btn_frame, text="Change Color", command=self.__change_color)
        self.color_btn.grid(row=1, column=1, sticky=tk.W + tk.E)
        self.root.protocol("WM_DELETE_WINDOW", self.__on_closing)
        self.root.attributes("-topmost", True)
        self.erase = tk.Button(self.btn_frame, text="Eraser", command=self.__erase)
        self.erase.grid(row=0, column=2, sticky=tk.W + tk.E)
        self.choose_image = tk.Button(self.btn_frame, text="Import Image", command=self.__open_image)
        self.choose_image.grid(row=2, column=2, sticky=tk.W + tk.E)
        self.change_background_btn = tk.Button(self.btn_frame, text="Change Background Color",
                                               command=self.__change_background_color)
        self.change_background_btn.grid(row=2, column=1, sticky=tk.W + tk.E)
        self.saved = False
        self.root.mainloop()

    def __paint(self, event):
        x1, y1 = event.x - 1, event.y - 1
        x2, y2 = event.x + 1, event.y + 1
        self.cnv.create_rectangle(x1, y1, x2, y2, outline=self.current_color, fill=self.current_color,
                                  width=self.brush_width)
        self.draw.rectangle([x1, y1, x2 + self.brush_width, y2 + self.brush_width], outline=self.current_color,
                            fill=self.current_color, width=self.brush_width)
        print(x1, y1)

    def __clear(self):
        self.cnv.delete("all")
        self.draw.rectangle([0, 0, 1000, 1000], fill="white")

    def __save(self):
        file_name = filedialog.asksaveasfilename(initialfile="untitled.png", defaultextension="png",
                                                 filetypes=[("PNG", "JPG",), (".png", ".jpg",)])
        if file_name != "":
            self.image.save(file_name)
            self.saved = True
            return 1
        else:
            messagebox.showerror("An error has occurred trying to save the file. Please try again",
                                 "An error has occurred trying to save the file. Please try again")

    def __brush_plus(self):
        if self.brush_width < 25:
            self.brush_width += 1

    def __brush_minus(self):
        if self.brush_width > 1:
            self.brush_width -= 1

    def __change_color(self):
        _, self.current_color = colorchooser.askcolor(title="Choose a color")

    def __on_closing(self):
        if not self.saved:
            answer = messagebox.askyesno("Quit", "Do you want to save your work first?", parent=self.root)
            if answer is not None:
                if answer:
                    for i in range(3):
                        ans = self.__save()
                        if ans == 1:
                            break
        self.root.destroy()
        exit()

    def __open_image(self):
        self.root.file_name = filedialog.askopenfilename(title="Select an image to import",
                                                         filetypes=[("PNG", "JPG",), (".png", ".jpg",)])
        if self.root.file_name != '':
            pass

    def __erase(self):
        self.current_color = self.bg_color

    def __change_background_color(self):
        _, self.bg_color = colorchooser.askcolor(title="Choose a color")
        self.cnv.config(bg=self.bg_color)


def main():
    PaintGUI()


if __name__ == '__main__':
    main()
