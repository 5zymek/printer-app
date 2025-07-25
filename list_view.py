import tkinter as tk
from data_models import JobStatus
import database
from status_info_view import StatusInfoView


class ListView(tk.Frame):
    """The main view displaying the list of print jobs."""

    def __init__(self, master, show_add_new_view):
        super().__init__(master)
        self.show_add_new_view = show_add_new_view
        self.master = master

        # --- UI Elements ---
        tk.Label(self, text="DRUKARKA NR 1 LIST VIEW", font=("Arial", 16, "bold")).pack(pady=10)

        tk.Button(self, text="Add Job", command=self.show_add_new_view).pack(pady=10, anchor="ne", padx=20)

        self.job_list_frame = tk.Frame(self)
        self.job_list_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Add event button is shown on the diagram but has no clear action
        # It could refresh the list or perform another action. Here, it refreshes.
        tk.Button(self, text="Add Event (Refresh List)", command=self.redraw_job_list).pack(pady=10, side="left",
                                                                                            padx=20)

        # Save print job button seems out of place on list view, but following diagram
        tk.Button(self, text="Save Print Job", state="disabled").pack(pady=10, side="right", padx=20)

        self.redraw_job_list()

    def redraw_job_list(self):
        """Clears and redraws the list of jobs from the database."""
        for widget in self.job_list_frame.winfo_children():
            widget.destroy()

        jobs = database.get_all_jobs()

        for job in jobs:
            self.create_job_row(job)

    def create_job_row(self, job):
        """Creates a single row widget for a job."""
        row_frame = tk.Frame(self.job_list_frame, borderwidth=1, relief="solid")
        row_frame.pack(fill="x", pady=2, padx=5)

        tk.Label(row_frame, text=f"JOB ID: {job.job_id}", width=10).pack(side="left", padx=5)
        tk.Label(row_frame, text=job.user_name, width=15).pack(side="left", padx=5)

        status_color = {
            JobStatus.GOOD: "green",
            JobStatus.FAILED: "red",
            JobStatus.PRINTING: "orange"
        }.get(job.status, "grey")

        status_button = tk.Button(
            row_frame,
            text=job.status.value,
            fg="white",
            bg=status_color,
            command=lambda j=job: self.open_status_info(j)
        )
        status_button.pack(side="right", padx=5, pady=5)

    def open_status_info(self, job):
        """Opens the status info window for a specific job."""
        StatusInfoView(self.master, job, on_close_callback=self.redraw_job_list)