import tkinter as tk
from PIL import Image, ImageTk
from tkinter.filedialog import asksaveasfilename, askopenfilename

from tkinter import messagebox

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

        self.loadPPM3Button = tk.Button(self.frame, text="Load PPM FILE", command=self.loadFile, padx=20, pady=20)
        self.loadPPM3Button.grid(row=0, column=2)

        self.savePPMButton = tk.Button(self.frame, text="Save as PPM P3", command=self.savePPM, padx=20, pady=20)
        self.savePPMButton.grid(row=0, column=3)

        self.linearScaleButton = tk.Button(self.frame, text="Linear Scale", command=self.linearScale, padx=20, pady=20)
        self.linearScaleButton.grid(row=0, column=4)

        self.pixel_info_label = tk.Label(self.frame, text="", padx=10, pady=10)
        self.pixel_info_label.grid(row=0, column=6)

        self.imageSpace = tk.Canvas(self.root, bg="white")
        self.imageSpace.pack(fill="both", expand=True)
        self.image = None
        self.imageId = None
        self.movedX = 0
        self.movedY = 0
        self.ppm = False
        self.jpg = False

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

    def settingsAfterLoad(self):
        if self.imageId is not None:
            self.imageSpace.delete(self.imageId)
            self.movedX, self.movedY = 0, 0
        self.imageId = self.imageSpace.create_image(0, 0, anchor="nw", image=self.tk_image)
        self.imageSpace.bind("<Motion>", self.on_mouse_move)
        self.bind_keyboard_events()
        self.zoom_settings()

    def measureTime(self, startEnd):
        if startEnd == "start":
            self.start_time = time.time()
        elif startEnd == "end":
            self.end_time = time.time()
            execution_time = self.end_time - self.start_time
            print(f"Czas wykonania funkcji: {execution_time} sekundy")

    def loadJPG(self):
        filePath = askopenfilename()
        if filePath == '':
            return
        self.image = Image.open(filePath)
        if self.image is None:
            return
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.settingsAfterLoad()
        self.ppm = False
        self.jpg = True

    def saveJPG(self):
        if self.image and self.jpg:
            compression_quality = tk.simpledialog.askinteger("Compression Quality", "Enter compression quality (0-100):", minvalue=0, maxvalue=100)
            if compression_quality is not None:
                file_path = asksaveasfilename(initialfile='Untitled.jpg', defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")])
                if file_path:
                    self.image.save(file_path, "JPEG", quality=compression_quality)
                    print(f"Image saved as {file_path} with compression quality {compression_quality}")

    def loadFile(self):
        filePath = askopenfilename(filetypes=[("PPM P3/P6 files", "*.ppm")])
        if filePath == '':
            return
        print(filePath)
        with open(filePath, "rb") as ppm_file:
            firstLine = ppm_file.readline().decode("ansi").strip()
        #print(firstLine)
        if firstLine == "P3":
            self.loadPPMP3(filePath)
        elif firstLine == "P6":
            self.loadPPMP6(filePath)
        else:
            raise ValueError("To nie jest ani plik PPM P3, ani plik PPM P6")

    def getValuesFromLine(self, line):
        # Usuń komentarze i białe znaki z początku i końca linii
        cleaned_line = line.split('#')[0].strip()
        # Pomijaj puste linie
        if not cleaned_line:
            return None
        values = cleaned_line.split()
        return values

    def loadPPMP3(self, filePath):
        self.measureTime("start")
        allValues = []
        with open(filePath, "r") as ppm_file:
            for line in ppm_file:
                values = self.getValuesFromLine(line)
                if values:
                    allValues.extend(values)

        self.header = allValues[0]
        self.width = int(allValues[1])
        self.height = int(allValues[2])
        self.maxColor = int(allValues[3])

        if self.header != "P3":
            raise ValueError("To nie jest plik PPM P3")

        if self.maxColor <= 256:
            self.pixels = [int(x) for x in allValues[4:]]
        else:
            self.pixels = [int(x)//256 for x in allValues[4:]]
        # print(f"MAX VALUE RED: {max(pixels[0::3])}")
        # print(f"MAX VALUE GREEN: {max(pixels[1::3])}")
        # print(f"MAX VALUE BLUE: {max(pixels[2::3])}")
        self.image = Image.frombytes("RGB", (self.width, self.height), bytes(self.pixels))
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.measureTime("end")
        self.settingsAfterLoad()
        self.ppm = True
        self.jpg = False

    def decodeSkipCommentsEmptyLines(self, file):
        while True:
            line = file.readline().decode("ansi").strip()
            cleaned_line = line.split('#')[0].strip()
            if cleaned_line:
                return cleaned_line

    def readBinaryDataInChunks(self, file, chunk_size=4096):
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            for byte in chunk:
                yield int(byte)

    def loadPPMP6(self, filePath):
        self.measureTime("start")
        with open(filePath, "rb") as ppm_file:
            parameters = [self.decodeSkipCommentsEmptyLines(ppm_file)]
            while len(parameters) < 4:
                line = self.decodeSkipCommentsEmptyLines(ppm_file)
                lineValues = map(int, line.split())
                parameters.extend(lineValues)
            # print(parameters)

            self.header = parameters[0]
            self.width = parameters[1]
            self.height = parameters[2]
            self.maxColor = parameters[3]

            if self.header != "P6":
                raise ValueError("To nie jest plik PPM P6")

            self.pixels = list(self.readBinaryDataInChunks(ppm_file))

        self.image = Image.frombytes("RGB", (self.width, self.height), bytes(self.pixels))
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.measureTime("end")
        self.settingsAfterLoad()
        self.ppm = True
        self.jpg = False

    def linearScale(self):
        if self.ppm:
            redMax = max(self.pixels[0::3])
            greenMax = max(self.pixels[1::3])
            blueMax = max(self.pixels[2::3])
            changeScale = tk.messagebox.askyesno(title="Linear scale", message=f"Actual max RGB = ({redMax},{greenMax},{blueMax}). Do you want rescale it?")
            if changeScale:
                redScale = self.maxColor / redMax
                greenScale = self.maxColor / greenMax
                blueScale = self.maxColor / blueMax
                scaledPixels = []
                # print(self.pixels[:10])
                for i, pixel in enumerate(self.pixels):
                    if i % 3 == 0:
                        pixel *= redScale
                    elif i % 3 == 1:
                        pixel *= greenScale
                    else:
                        pixel *= blueScale
                    scaledPixels.append(int(pixel))
                # print(scaledPixels[:10])
                self.imageSpace.delete(self.imageId)
                self.movedX, self.movedY = 0, 0
                self.image = Image.frombytes("RGB", (self.width, self.height), bytes(scaledPixels))
                self.tk_image = ImageTk.PhotoImage(self.image)
                self.imageId = self.imageSpace.create_image(0, 0, anchor="nw", image=self.tk_image)
                self.imageSpace.bind("<Motion>", self.on_mouse_move)
                self.bind_keyboard_events()
                self.zoom_settings()

    def savePPM(self):
        if self.image and self.ppm:
            file_path = asksaveasfilename(initialfile='Untitled.ppm', defaultextension=".ppm",
                                          filetypes=[("PPM P3 files", "*.ppm")])
            if file_path:
                self.savePPMP3(file_path)
                print(f"Image saved as {file_path}")

    def savePPMP3(self, file_path):
        if self.image and self.ppm:
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
