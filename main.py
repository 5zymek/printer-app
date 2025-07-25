import tkinter as tk
from list_view import ListView
from add_new_view import AddNewView


class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Printer Management App")
        self.geometry("500x600")

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.current_frame = None
        self.show_list_view()

    def show_frame(self, frame_class, *args, **kwargs):
        """Destroys current frame and replaces it with a new one."""
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = frame_class(self.container, *args, **kwargs)
        self.current_frame.pack(fill="both", expand=True)

    def show_list_view(self):
        """Shows the main job list view."""
        self.show_frame(ListView, show_add_new_view=self.show_add_new_view)

    def show_add_new_view(self):
        """Shows the view for adding a new job."""
        self.show_frame(AddNewView, show_list_view=self.show_list_view)


if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()