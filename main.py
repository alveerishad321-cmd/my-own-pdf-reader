import tkinter as tk
from tkinter import filedialog
import fitz
from PIL import Image, ImageTk

class PDFReader:
    def __init__(self, root):
        self.root = root
        self.root.title("My Own PDF Reader Pro 2.1")
        self.root.geometry("1000x700")

        self.doc = None
        self.page_num = 0
        self.zoom = 1.5

        toolbar = tk.Frame(root)
        toolbar.pack(fill="x")

        tk.Button(toolbar, text="Open PDF", command=self.open_pdf).pack(side="left")
        tk.Button(toolbar, text="Previous", command=self.prev_page).pack(side="left")
        tk.Button(toolbar, text="Next", command=self.next_page).pack(side="left")
        tk.Button(toolbar, text="Zoom +", command=self.zoom_in).pack(side="left")
        tk.Button(toolbar, text="Zoom -", command=self.zoom_out).pack(side="left")

        self.page_label = tk.Label(toolbar, text="Page: 0")
        self.page_label.pack(side="right", padx=10)

        self.canvas = tk.Canvas(root, bg="gray")
        self.canvas.pack(fill="both", expand=True)

    def open_pdf(self):
        path = filedialog.askopenfilename(
            filetypes=[("PDF Files", "*.pdf")]
        )

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

        img = Image.frombytes(
            "RGB",
            [pix.width, pix.height],
            pix.samples
        )

        self.tk_img = ImageTk.PhotoImage(img)

        self.canvas.delete("all")
        self.canvas.create_image(
            0, 0,
            anchor="nw",
            image=self.tk_img
        )

        self.page_label.config(
            text=f"Page: {self.page_num + 1}/{len(self.doc)}"
        )

    def prev_page(self):
        if self.doc and self.page_num > 0:
            self.page_num -= 1
            self.show_page()

    def next_page(self):
        if self.doc and self.page_num < len(self.doc) - 1:
            self.page_num += 1
            self.show_page()

    def zoom_in(self):
        self.zoom += 0.2
        self.show_page()

    def zoom_out(self):
        if self.zoom > 0.4:
            self.zoom -= 0.2
            self.show_page()

root = tk.Tk()
PDFReader(root)
root.mainloop()
