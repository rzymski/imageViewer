import tkinter as tk
from PIL import Image, ImageTk
from tkinter.filedialog import asksaveasfilename, askopenfilename

import time

class ImageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image viewer Piotr Szumowski")
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()
        self.root.geometry(f"{self.screen_width}x{self.screen_height}")

        self.frame = tk.LabelFrame(self.root, padx=10, pady=10, labelanchor="n")
        self.frame.pack(side="top", fill="both")

        self.loadJPGButton = tk.Button(self.frame, text="Load JPG", command=self.loadJPG, padx=20, pady=20)
        self.loadJPGButton.grid(row=0, column=0)

        self.saveJPGButton = tk.Button(self.frame, text="Save JPG", command=self.saveJPG, padx=20, pady=20)
        self.saveJPGButton.grid(row=0, column=1)

        self.loadPPMButton = tk.Button(self.frame, text="Load PPM P3", command=self.loadPPM, padx=20, pady=20)
        self.loadPPMButton.grid(row=0, column=2)

        self.savePPMButton = tk.Button(self.frame, text="Save PPM P3", command=self.savePPM, padx=20, pady=20)
        self.savePPMButton.grid(row=0, column=3)

        self.pixel_info_label = tk.Label(self.frame, text="", padx=10, pady=10)
        self.pixel_info_label.grid(row=0, column=4)

        self.imageSpace = tk.Canvas(self.root, bg="white")
        self.imageSpace.pack(fill="both", expand=True)
        self.image = None
        self.imageId = None

        self.movedX = 0
        self.movedY = 0

    def move_image(self, dx, dy):
        if self.imageId is not None:
            self.movedX += dx
            self.movedY += dy
            self.imageSpace.move(self.imageId, dx, dy)

    def move_image_left(self, event):
        self.move_image(10, 0)

    def move_image_right(self, event):
        self.move_image(-10, 0)

    def move_image_up(self, event):
        self.move_image(0, 10)

    def move_image_down(self, event):
        self.move_image(0, -10)

    def bind_keyboard_events(self):
        self.root.bind("<Left>", self.move_image_left)
        self.root.bind("<Right>", self.move_image_right)
        self.root.bind("<Up>", self.move_image_up)
        self.root.bind("<Down>", self.move_image_down)

    def on_mouse_move(self, event):
        # image_coords = self.imageSpace.coords(self.imageId)
        # print(f"{image_coords} {self.image.width} {self.image.height}")
        # print(f"f{self.image}")
        if self.image is not None:
            x, y = event.x-self.movedX, event.y-self.movedY
            # print(f"x={event.x} mX={self.movedX}  y={event.y} mY={self.movedY} IX={self.image.width}  IY={self.image.height}")
            # image_x, image_y = self.imageSpace.coords(self.imageId)
            # print(f"Ob = {image_x} {image_y}")
            if (0 <= x < self.image.width) and (0 <= y < self.image.height):
                pixel_rgb = self.get_pixel_color(x, y)
                self.update_pixel_info_label(x, y, pixel_rgb)
            else:
                self.pixel_info_label.config(text="")

    def get_pixel_color(self, x, y):
        if self.image is not None:
            try:
                pixel = self.image.getpixel((x, y))
                return pixel
            except Exception as e:
                print(f"Error getting pixel color: {e}")
        return None

    def update_pixel_info_label(self, x, y, pixel_rgb):
        if pixel_rgb is not None:
            r, g, b = pixel_rgb
            info_text = f"X: {x}, Y: {y}, R: {r}, G: {g}, B: {b}"
            self.pixel_info_label.config(text=info_text)

    def loadJPG(self):
        filePath = askopenfilename()
        self.image = Image.open(filePath)
        self.tk_image = ImageTk.PhotoImage(self.image)
        if self.imageId is not None:
            self.imageSpace.delete(self.imageId)
            self.movedX, self.movedY = 0, 0
        self.imageId = self.imageSpace.create_image(0, 0, anchor="nw", image=self.tk_image)
        self.imageSpace.bind("<Motion>", self.on_mouse_move)
        self.bind_keyboard_events()

    def saveJPG(self):
        if self.image:
            compression_quality = tk.simpledialog.askinteger("Compression Quality", "Enter compression quality (0-100):", minvalue=0, maxvalue=100)
            if compression_quality is not None:
                file_path = asksaveasfilename(initialfile='Untitled.jpg', defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")])
                if file_path:
                    self.image.save(file_path, "JPEG", quality=compression_quality)
                    print(f"Image saved as {file_path} with compression quality {compression_quality}")

    def getValuesFromLine(self, line):
        # Usuń komentarze i białe znaki z początku i końca linii
        cleaned_line = line.split('#')[0].strip()
        # Pomijaj puste linie
        if not cleaned_line:
            return None
        values = cleaned_line.split()
        return values

    def loadPPM(self):
        filePath = askopenfilename(filetypes=[("PPM P3 files", "*.ppm")])
        print(filePath)

        start_time = time.time()

        allValues = []
        with open(filePath, "r") as ppm_file:
            for line in ppm_file:
                values = self.getValuesFromLine(line)
                if values:
                    allValues.extend(values)

        header = allValues[0]
        width = int(allValues[1])
        height = int(allValues[2])
        maxColor = int(allValues[3])

        if header != "P3":
            raise ValueError("To nie jest plik PPM P3")

        if maxColor <= 256:
            pixels = [int(x) for x in allValues[4:]]
        else:
            pixels = [int(x)//256 for x in allValues[4:]]

        self.image = Image.frombytes("RGB", (width, height), bytes(pixels))
        self.tk_image = ImageTk.PhotoImage(self.image)
        if self.imageId is not None:
            self.imageSpace.delete(self.imageId)
            self.movedX, self.movedY = 0, 0
        self.imageId = self.imageSpace.create_image(0, 0, anchor="nw", image=self.tk_image)
        self.imageSpace.bind("<Motion>", self.on_mouse_move)
        self.bind_keyboard_events()

        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Czas wykonania funkcji: {execution_time} sekundy")

    def savePPM(self):
        if self.image:
            file_path = asksaveasfilename(initialfile='Untitled.ppm', defaultextension=".ppm",
                                          filetypes=[("PPM P3 files", "*.ppm")])
            if file_path:
                self.save_ppm(file_path)
                print(f"Image saved as {file_path}")

    def save_ppm(self, file_path):
        if self.image:
            width, height = self.image.size
            max_color = 255

            with open(file_path, "w") as ppm_file:
                ppm_file.write("P3\n")
                ppm_file.write(f"{width} {height}\n")
                ppm_file.write(f"{max_color}\n")

                pixels = self.image.tobytes()
                pixels = [pixels[i:i + 3] for i in range(0, len(pixels), 3)]

                for i, pixel in enumerate(pixels):
                    ppm_file.write(" ".join(map(str, pixel)) + " ")
                    if (i + 1) % (width * 3) == 0:
                        ppm_file.write("\n")
