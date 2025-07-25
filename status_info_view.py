import tkinter as tk
from tkinter import messagebox
from data_models import JobStatus


class StatusInfoView(tk.Toplevel):
    """A window to display job information and update its status."""

    def __init__(self, master, job, on_close_callback):
        super().__init__(master)
        self.title("Status / Info")
        self.geometry("300x250")
        self.job = job
        self.on_close_callback = on_close_callback

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        tk.Label(self, text=f"Job ID: {self.job.job_id}", font=("Arial", 12)).pack(pady=5)
        tk.Label(self, text=f"User: {self.job.user_name}", font=("Arial", 12)).pack(pady=5)

        self.status_label = tk.Label(self, text=f"Status: {self.job.status.value}", font=("Arial", 12, "bold"))
        self.status_label.pack(pady=10)

        # Placeholder for a photo
        photo_frame = tk.Frame(self, width=150, height=100, bg="lightgrey")
        photo_frame.pack(pady=10)
        tk.Label(photo_frame, text="Photo", fg="grey").pack(expand=True)

        # Status change buttons
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Set to Good", command=lambda: self.update_status(JobStatus.GOOD)).pack(side=tk.LEFT,
                                                                                                          padx=5)
        tk.Button(btn_frame, text="Set to Failed", command=lambda: self.update_status(JobStatus.FAILED)).pack(
            side=tk.LEFT, padx=5)

    def update_status(self, new_status):
        self.job.status = new_status
        self.status_label.config(text=f"Status: {self.job.status.value}")
        messagebox.showinfo("Success", "Job status updated.")
        self.on_close()

    def on_close(self):
        self.on_close_callback()
        self.destroy()