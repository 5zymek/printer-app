import enum

class JobStatus(enum.Enum):
    """Enumeration for the status of a print job."""
    PRINTING = "Printing"
    GOOD = "Good"
    FAILED = "Failed"
    PENDING = "Pending" # New status for newly created jobs

# List of faculties for categorization
FACULTIES = [
    "Faculty of Architecture",
    "Faculty of Mechanical Engineering",
    "Faculty of Civil Engineering",
    "Faculty of Electronics",
    "Faculty of Chemistry",
    "Faculty of Arts",
    "Faculty of Medicine",
    "Other"
]

class Job:
    """Represents a single print job, now with more details."""
    def __init__(self, user_name, printer_id, faculty, elements, status=JobStatus.PENDING, job_id=None):
        self.job_id = job_id
        self.user_name = user_name
        self.printer_id = printer_id
        self.faculty = faculty
        self.elements = elements  # This will now store filenames
        self.status = status

    def __repr__(self):
        return (f"Job(ID={self.job_id}, User='{self.user_name}', Printer={self.printer_id}, "
                f"Faculty='{self.faculty}', Status='{self.status.value}')")