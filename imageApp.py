import tkinter as tk
from PIL import Image, ImageTk
from tkinter.filedialog import asksaveasfilename, askopenfilename

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

        self.frameImage = tk.LabelFrame(self.root, labelanchor="n")
        self.frameImage.pack()
        self.imageLabel = None
        self.image = None

    def loadJPG(self):
        filePath = askopenfilename()
        self.image = Image.open(filePath)
        self.tk_image = ImageTk.PhotoImage(self.image)
        if self.imageLabel is not None:
            self.imageLabel.pack_forget()
        self.imageLabel = tk.Label(self.frameImage, image=self.tk_image)
        self.imageLabel.pack(side="top")

    def saveJPG(self):
        if hasattr(self, 'image'):
            file_path = asksaveasfilename(initialfile='Untitled.jpg', defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")])
            if file_path:
                self.image.save(file_path, "JPEG")
                print(f"Image saved as {file_path}")

    def loadPPM(self):
        filePath = askopenfilename(filetypes=[("PPM P3 files", "*.ppm")])
        if filePath:
            with open(filePath, "r") as ppm_file:
                self.image = self.load_ppm(ppm_file)
                self.tk_image = ImageTk.PhotoImage(self.image)
                if self.imageLabel is not None:
                    self.imageLabel.pack_forget()
                self.imageLabel = tk.Label(self.frameImage, image=self.tk_image)
                self.imageLabel.pack(side="top")

    def get_parameters(self, ppm_lines):
        count = 0
        values = []
        for line in ppm_lines[1:]:
            s = ""
            for char in line:
                if char == "#":
                    break
                if char.isdigit():
                    s += char
                else:
                    if s.isnumeric():
                        values.append(int(s))
                        count += 1
                        if count == 3:
                            return values[0], values[1], values[2]
                    s = ""
            if s != "" and s.isnumeric():
                values.append(int(s))
                count += 1
                if count == 3:
                    return values[0], values[1], values[2]
    def load_ppm(self, ppm_file):
        ppm_data = ppm_file.read()
        ppm_lines = ppm_data.split("\n")
        ppm_lines = [line.split('#')[0].strip() for line in ppm_lines]
        if ppm_lines[0] != "P3":
            raise ValueError("Not a PPM P3 file")

        width, height, max_color = self.get_parameters(ppm_lines)

        values = []
        for line in ppm_lines[1:]:
            s = ""
            for char in line:
                if char == "#":
                    break
                if char.isdigit():
                    s += char
                else:
                    if s.isnumeric():
                        if max_color > 255:
                            values.append(int(s) // 256)
                        else:
                            values.append(int(s))
                    s = ""
            if s != "" and s.isnumeric():
                if max_color > 255:
                    values.append(int(s) // 256)
                else:
                    values.append(int(s))
        pixels = []
        for value in values[3:]:
            pixels.append(value)
        return Image.frombytes("RGB", (width, height), bytes(pixels))

    def savePPM(self):
        if hasattr(self, 'image'):
            file_path = asksaveasfilename(initialfile='Untitled.ppm', defaultextension=".ppm",
                                          filetypes=[("PPM P3 files", "*.ppm")])
            if file_path:
                self.save_ppm(file_path)
                print(f"Image saved as {file_path}")

    def save_ppm(self, file_path):
        if hasattr(self, 'image'):
            width, height = self.image.size
            max_color = 255  # Adjust this as needed

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
