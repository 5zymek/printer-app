import enum

class JobStatus(enum.Enum):
    """Enumeration for the status of a print job."""
    PRINTING = "Printing"
    GOOD = "Good"
    FAILED = "Failed"

class Job:
    """Represents a single print job."""
    def __init__(self, job_id, user_name, elements, status=JobStatus.PRINTING):
        self.job_id = job_id
        self.user_name = user_name
        self.elements = elements
        self.status = status

    def __repr__(self):
        return f"Job(ID={self.job_id}, User='{self.user_name}', Status='{self.status.value}')"