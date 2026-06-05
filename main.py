import tkinter as tk
from tkinter import filedialog, messagebox

class PDFReader:
    def __init__(self, root):
        self.root = root
        self.root.title("My Own PDF Reader Pro 2.0")
        self.root.geometry("1000x700")

        self.dark_mode = False

        # Toolbar
        toolbar = tk.Frame(root)
        toolbar.pack(fill="x")

        tk.Button(toolbar, text="Open PDF", command=self.open_pdf).pack(side="left", padx=5, pady=5)
        tk.Button(toolbar, text="Dark/Light", command=self.toggle_theme).pack(side="left", padx=5)

        tk.Button(toolbar, text="About", command=self.about).pack(side="right", padx=5)

        # Main area
        self.text = tk.Text(root, wrap="word")
        self.text.pack(fill="both", expand=True)

        self.apply_light()

    def open_pdf(self):
        file = filedialog.askopenfilename(
            filetypes=[("PDF Files", "*.pdf")]
        )

        if file:
            self.text.delete("1.0", tk.END)
            self.text.insert(tk.END,
                f"PDF Selected:\n\n{file}\n\n"
                "Version 2.0 PDF Engine coming next step."
            )

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode

        if self.dark_mode:
            self.apply_dark()
        else:
            self.apply_light()

    def apply_dark(self):
        self.text.config(bg="#1e1e1e", fg="white")
        self.root.config(bg="#1e1e1e")

    def apply_light(self):
        self.text.config(bg="white", fg="black")
        self.root.config(bg="white")

    def about(self):
        messagebox.showinfo(
            "About",
            "My Own PDF Reader Pro 2.0\n\nCreated by Alvee Al Rishad"
        )

root = tk.Tk()
app = PDFReader(root)
root.mainloop()
