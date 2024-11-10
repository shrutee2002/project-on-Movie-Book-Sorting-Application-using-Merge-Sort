import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import font as tkFont

class Item:
    def __init__(self, title, genre, creator, year):
        self.title = title
        self.genre = genre
        self.creator = creator
        self.year = year
    
    def __repr__(self):
        return f"{self.title} ({self.year}) by {self.creator} - {self.genre}"

def merge(left, right, key):
    sorted_list = []
    while left and right:
        if getattr(left[0], key).lower() < getattr(right[0], key).lower():
            sorted_list.append(left.pop(0))
        else:
            sorted_list.append(right.pop(0))
    sorted_list.extend(left if left else right)
    return sorted_list

def merge_sort(items, key):
    if len(items) <= 1:
        return items
    mid = len(items) // 2
    left = merge_sort(items[:mid], key)
    right = merge_sort(items[mid:], key)
    return merge(left, right, key)

class SimpleSorterApp:
    def __init__(self, root):
        self.root = root
        self.items = []
        
        # Setting up styles and fonts
        self.root.configure(bg="#f0f0f5")
        self.root.title("Movie & Book Sorter")
        title_font = tkFont.Font(family="Helvetica", size=14, weight="bold")
        
        # Title label
        tk.Label(root, text="Movie & Book Sorter", font=title_font, bg="#f0f0f5").grid(row=0, column=0, columnspan=3, pady=(10, 5))

        # Entry fields with tooltips
        fields = ["Title", "Genre", "Creator", "Year"]
        self.entries = {}
        for idx, field in enumerate(fields):
            tk.Label(root, text=f"{field}:", bg="#f0f0f5").grid(row=idx+1, column=0, padx=10, pady=2, sticky="e")
            entry = tk.Entry(root, width=25)
            entry.grid(row=idx+1, column=1, padx=10, pady=2)
            self.entries[field.lower()] = entry

        # Buttons
        tk.Button(root, text="Add Item", command=self.add_item, bg="#0066cc", fg="white").grid(row=5, column=0, pady=5)
        tk.Button(root, text="Sort & Display", command=self.sort_and_display, bg="#4CAF50", fg="white").grid(row=5, column=1, pady=5)
        tk.Button(root, text="Save to File", command=self.save_to_file, bg="#FF5733", fg="white").grid(row=5, column=2, pady=5)

        # Sort options with radio buttons
        self.sort_var = tk.StringVar(value="title")
        tk.Radiobutton(root, text="Title", variable=self.sort_var, value="title", bg="#f0f0f5").grid(row=6, column=0, pady=2)
        tk.Radiobutton(root, text="Genre", variable=self.sort_var, value="genre", bg="#f0f0f5").grid(row=6, column=1, pady=2)
        tk.Radiobutton(root, text="Creator", variable=self.sort_var, value="creator", bg="#f0f0f5").grid(row=7, column=0, pady=2)
        tk.Radiobutton(root, text="Year", variable=self.sort_var, value="year", bg="#f0f0f5").grid(row=7, column=1, pady=2)

        # Display area
        self.display_area = tk.Text(root, height=10, width=50, wrap="word", state="disabled", bg="#f7f7fa")
        self.display_area.grid(row=8, column=0, columnspan=3, pady=10, padx=10)
        
    def add_item(self):
        # Collect data from entries
        title = self.entries["title"].get()
        genre = self.entries["genre"].get()
        creator = self.entries["creator"].get()
        year = self.entries["year"].get()
        
        # Validate entries
        if not title or not genre or not creator or not year:
            messagebox.showerror("Input Error", "Please fill all fields.")
            return
        
        try:
            year = int(year)
        except ValueError:
            messagebox.showerror("Input Error", "Year must be a number.")
            return
        
        # Add item to the list and clear entries
        item = Item(title, genre, creator, year)
        self.items.append(item)
        
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        
        messagebox.showinfo("Success", "Item added successfully!")

    def sort_and_display(self):
        if not self.items:
            messagebox.showerror("No Items", "No items to sort.")
            return
        
        sorted_items = merge_sort(self.items, self.sort_var.get())
        
        # Display sorted items
        self.display_area.config(state="normal")
        self.display_area.delete(1.0, tk.END)
        for item in sorted_items:
            self.display_area.insert(tk.END, f"{item}\n")
        self.display_area.config(state="disabled")

    def save_to_file(self):
        if not self.items:
            messagebox.showerror("No Items", "No items to save.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                for item in self.items:
                    file.write(f"{item}\n")
            messagebox.showinfo("Success", f"Data saved to {file_path}")

# Initialize the application
root = tk.Tk()
app = SimpleSorterApp(root)
root.mainloop()
