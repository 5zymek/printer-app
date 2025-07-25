import tkinter as tk
from tkinter import ttk, messagebox
import database
from data_models import Job


class AddNewView(tk.Frame):
    """The view for creating a new print job."""

    def __init__(self, master, show_list_view):
        super().__init__(master)
        self.show_list_view = show_list_view
        self.current_job_elements = []

        tk.Label(self, text="DRUKARKA NR 1 ADD NEW", font=("Arial", 16, "bold")).pack(pady=10)

        # --- Filters Frame ---
        filters_frame = tk.LabelFrame(self, text="Filters")
        filters_frame.pack(pady=10, padx=20, fill="x")

        # Simplified search from diagram
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self.update_search_results)
        search_entry = tk.Entry(filters_frame, textvariable=self.search_var, relief="solid")
        search_entry.pack(pady=5, padx=5, fill="x")

        self.search_results_listbox = tk.Listbox(filters_frame, height=8)
        self.search_results_listbox.pack(pady=5, padx=5, fill="x")
        self.update_search_results()

        tk.Label(self, text="DLA KOGO JEST TEN STL (Who is this STL for?)").pack(pady=(10, 0))
        self.user_name_entry = tk.Entry(self, relief="solid")
        self.user_name_entry.pack(pady=5, padx=20, fill="x")

        tk.Button(self, text="ADD ELEMENT to JOB", bg="#ff4d4d", fg="white", font=("Arial", 10, "bold"),
                  command=self.add_element_to_job).pack(pady=10)

        # --- Current Job Frame ---
        job_frame = tk.LabelFrame(self, text="JOB")
        job_frame.pack(pady=10, padx=20, fill="x")
        self.job_elements_label = tk.Label(job_frame, text="No elements added", wraplength=350, justify="left")
        self.job_elements_label.pack(pady=10, padx=10, fill="x")

        # --- ACTION BUTTONS ---
        # --- THIS IS THE NEW BUTTON ---
        tk.Button(self, text="< Back to List", command=self.show_list_view).pack(pady=(20, 5))

        tk.Button(self, text="SAVE JOB", bg="#ff4d4d", fg="white", font=("Arial", 10, "bold"),
                  command=self.save_job).pack(pady=5)

    def update_search_results(self, *args):
        """Filters the available STL files based on search entry."""
        search_term = self.search_var.get().lower()
        self.search_results_listbox.delete(0, tk.END)
        for item in database.AVAILABLE_STL_FILES:
            if search_term in item.lower():
                self.search_results_listbox.insert(tk.END, item)

    def add_element_to_job(self):
        """Adds the selected element from search results to the current job."""
        selected_indices = self.search_results_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Warning", "Please select an element from the list.")
            return

        selected_element = self.search_results_listbox.get(selected_indices[0])
        self.current_job_elements.append(selected_element)
        self.job_elements_label.config(text=", ".join(self.current_job_elements))

    def save_job(self):
        """Saves the new job and returns to the list view."""
        user_name = self.user_name_entry.get()
        if not user_name or not self.current_job_elements:
            messagebox.showerror("Error", "User name and at least one element are required.")
            return

        new_job = Job(job_id=None, user_name=user_name, elements=self.current_job_elements)
        database.add_job(new_job)

        # Clear form for next time
        self.user_name_entry.delete(0, tk.END)
        self.current_job_elements = []
        self.job_elements_label.config(text="No elements added")

        messagebox.showinfo("Success", "Job saved successfully!")
        self.show_list_view()