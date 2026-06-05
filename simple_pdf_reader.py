
import tkinter as tk
from tkinter import filedialog
import fitz  # PyMuPDF
from PIL import Image, ImageTk

class PDFReader:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple PDF Reader")
        self.doc = None
        self.page_num = 0
        self.zoom = 1.5

        top = tk.Frame(root)
        top.pack(fill="x")

        tk.Button(top, text="Open PDF", command=self.open_pdf).pack(side="left")
        tk.Button(top, text="Previous", command=self.prev_page).pack(side="left")
        tk.Button(top, text="Next", command=self.next_page).pack(side="left")

        self.zoom_scale = tk.Scale(
            top, from_=50, to=300, orient="horizontal",
            label="Zoom %", command=self.change_zoom
        )
        self.zoom_scale.set(150)
        self.zoom_scale.pack(side="left")

        self.canvas = tk.Canvas(root, bg="gray")
        self.canvas.pack(fill="both", expand=True)

        self.start_x = None
        self.start_y = None
        self.rect = None

        self.canvas.bind("<Button-1>", self.highlight_start)
        self.canvas.bind("<B1-Motion>", self.highlight_drag)
        self.canvas.bind("<ButtonRelease-1>", self.highlight_end)

    def open_pdf(self):
        path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if path:
            self.doc = fitz.open(path)
            self.page_num = 0
            self.show_page()

    def show_page(self):
        if not self.doc:
            return

        page = self.doc[self.page_num]
        mat = fitz.Matrix(self.zoom, self.zoom)
        pix = page.get_pixmap(matrix=mat)

        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        self.tk_img = ImageTk.PhotoImage(img)

        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_img)
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def prev_page(self):
        if self.doc and self.page_num > 0:
            self.page_num -= 1
            self.show_page()

    def next_page(self):
        if self.doc and self.page_num < len(self.doc) - 1:
            self.page_num += 1
            self.show_page()

    def change_zoom(self, value):
        self.zoom = int(value) / 100
        self.show_page()

    def highlight_start(self, event):
        self.start_x, self.start_y = event.x, event.y
        self.rect = self.canvas.create_rectangle(
            event.x, event.y, event.x, event.y,
            outline="yellow", fill="yellow", stipple="gray25"
        )

    def highlight_drag(self, event):
        if self.rect:
            self.canvas.coords(
                self.rect,
                self.start_x, self.start_y,
                event.x, event.y
            )

    def highlight_end(self, event):
        pass

root = tk.Tk()
root.geometry("1000x700")
PDFReader(root)
root.mainloop()
