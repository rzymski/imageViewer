import tkinter as tk
from PIL import Image, ImageTk
from tkinter.filedialog import asksaveasfilename, askopenfilename

from tkinter import ALL, EventType

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

    def zoom_settings(self):
        self.root.bind("<MouseWheel>", self.wheel)
        self.imscale = 1.0
        self.delta = 0.75
        self.text = self.imageSpace.create_text(0, 0, anchor='nw', text='')
        self.show_image()
        self.imageSpace.configure(scrollregion=self.imageSpace.bbox('all'))

    def wheel(self, event):
        scale = 1.0
        if event.delta == -120:
            scale *= self.delta
            self.imscale *= self.delta
        if event.delta == 120:
            scale /= self.delta
            self.imscale /= self.delta
        # Rescale all canvas objects
        x = self.imageSpace.canvasx(event.x)
        y = self.imageSpace.canvasy(event.y)
        self.imageSpace.scale(self.imageId, x, y, scale, scale)
        self.show_image()
    def show_image(self):
        if self.imageId:
            self.imageSpace.delete(self.imageId)
            self.imageId = None
            self.imageSpace.imagetk = None
        width, height = self.image.size
        new_size = int(self.imscale * width), int(self.imscale * height)
        imagetk = ImageTk.PhotoImage(self.image.resize(new_size))
        # # Use self.text object to set proper coordinates
        self.imageId = self.imageSpace.create_image(self.imageSpace.coords(self.text), anchor='nw', image=imagetk)
        self.imageSpace.lower(self.imageId)
        self.imageSpace.imagetk = imagetk
        self.movedX = 0
        self.movedY = 0

    def move_image(self, event, dx, dy):
        if self.imageId is not None:
            dx *= self.imscale
            dy *= self.imscale
            self.movedX += dx
            self.movedY += dy
            self.imageSpace.move(self.imageId, dx, dy)

    def bind_keyboard_events(self):
        self.root.bind("<Left>", lambda event: self.move_image(event, dx=10, dy=0))
        self.root.bind("<Right>", lambda event: self.move_image(event, dx=-10, dy=0))
        self.root.bind("<Up>", lambda event: self.move_image(event, dx=0, dy=10))
        self.root.bind("<Down>", lambda event: self.move_image(event, dx=0, dy=-10))

    def on_mouse_move(self, event):
        # image_coords = self.imageSpace.coords(self.imageId)
        # print(f"{image_coords} {self.image.width} {self.image.height}")
        # print(f"f{self.image}")
        if self.image is not None:
            x, y = event.x-self.movedX, event.y-self.movedY
            # print(f"x={event.x} mX={self.movedX}  y={event.y} mY={self.movedY} IX={self.image.width}  IY={self.image.height}")
            # image_x, image_y = self.imageSpace.coords(self.imageId)
            # print(f"Ob = {image_x} {image_y}")
            if (0 <= x < self.image.width * self.imscale) and (0 <= y < self.image.height * self.imscale):
                pixel_rgb = self.get_pixel_color(int(x/self.imscale), int(y/self.imscale))
                self.update_pixel_info_label(int(x/self.imscale), int(y/self.imscale), pixel_rgb)
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
        if filePath == '':
            return
        self.image = Image.open(filePath)
        if self.image is None:
            return
        self.tk_image = ImageTk.PhotoImage(self.image)
        if self.imageId is not None:
            self.imageSpace.delete(self.imageId)
            self.movedX, self.movedY = 0, 0
        self.imageId = self.imageSpace.create_image(0, 0, anchor="nw", image=self.tk_image)
        self.imageSpace.bind("<Motion>", self.on_mouse_move)
        self.bind_keyboard_events()
        self.zoom_settings()

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
        if filePath == '':
            return
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
        self.zoom_settings()

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
