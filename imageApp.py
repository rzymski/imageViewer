import tkinter as tk
from PIL import Image, ImageTk
from tkinter.filedialog import asksaveasfilename, askopenfilename

class ImageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image viewer Piotr Szumowski")

        self.frame = tk.LabelFrame(root, padx=50, pady=50)
        self.frame.pack(padx=10, pady=10)

        self.loadJPGButton = tk.Button(self.frame, text="Load JPG", command=self.loadJPG, padx=20, pady=20)
        self.loadJPGButton.grid(row=0, column=0)

        self.saveJPGButton = tk.Button(self.frame, text="Save JPG", command=self.saveJPG, padx=20, pady=20)
        self.saveJPGButton.grid(row=0, column=1)

        self.imageLabel = None

    def loadJPG(self):
        filePath = askopenfilename()
        self.image = Image.open(filePath)
        self.tk_image = ImageTk.PhotoImage(self.image)
        if self.imageLabel is not None:
            self.imageLabel.pack_forget()
        self.imageLabel = tk.Label(self.root, image=self.tk_image)
        self.imageLabel.pack()

    def saveJPG(self):
        if hasattr(self, 'image'):
            file_path = asksaveasfilename(initialfile='Untitled.jpg', defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")])
            if file_path:
                self.image.save(file_path, "JPEG")
                print(f"Image saved as {file_path}")