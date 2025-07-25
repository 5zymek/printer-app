from data_models import Job, JobStatus

# In-memory storage for jobs
_jobs = [
    Job(job_id=1, user_name="Tarik", elements=["A101"], status=JobStatus.FAILED),
    Job(job_id=2, user_name="szymon", elements=["A103", "A104"], status=JobStatus.FAILED),
    Job(job_id=3, user_name="Bart", elements=["B202"], status=JobStatus.GOOD),
    Job(job_id=4, user_name="Maciek", elements=["Braille_A101"], status=JobStatus.FAILED),
    Job(job_id=5, user_name="Bart", elements=["A101", "A102"], status=JobStatus.PRINTING),
]
_next_id = 6

# A list of available STL files to choose from when creating a new job
AVAILABLE_STL_FILES = ["A101", "Braille_A101", "A102", "A103", "A104", "B202", "C301"]

def get_all_jobs():
    """Returns all jobs, sorted by ID."""
    return sorted(_jobs, key=lambda job: job.job_id)

def add_job(job):
    """Adds a new job to the database."""
    global _next_id
    job.job_id = _next_id
    _jobs.append(job)
    _next_id += 1

def get_job_by_id(job_id):
    """Finds a job by its ID."""
    for job in _jobs:
        if job.job_id == job_id:
            return job
    return None