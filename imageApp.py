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

        self.frameImage = tk.LabelFrame(self.root, labelanchor="n")
        self.frameImage.pack()
        self.imageLabel = None

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
