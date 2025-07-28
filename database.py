import sqlite3
from data_models import Job, JobStatus

DB_FILE = "jobs.db"


def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initializes the database and creates the jobs table if it doesn't exist."""
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT NOT NULL,
            printer_id INTEGER NOT NULL,
            faculty TEXT NOT NULL,
            status TEXT NOT NULL,
            elements TEXT NOT NULL -- Storing filenames as a comma-separated string
        );
    ''')
    conn.commit()
    conn.close()


def add_job(job: Job):
    """Adds a new job to the database."""
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO jobs (user_name, printer_id, faculty, status, elements) VALUES (?, ?, ?, ?, ?)',
        (job.user_name, job.printer_id, job.faculty, job.status.value, ",".join(job.elements))
    )
    conn.commit()
    conn.close()


def get_job_by_id(job_id: int) -> Job:
    """Retrieves a single job by its ID."""
    conn = get_db_connection()
    job_row = conn.execute('SELECT * FROM jobs WHERE id = ?', (job_id,)).fetchone()
    conn.close()
    if job_row:
        return Job(
            job_id=job_row['id'],
            user_name=job_row['user_name'],
            printer_id=job_row['printer_id'],
            faculty=job_row['faculty'],
            status=JobStatus(job_row['status']),
            elements=job_row['elements'].split(',')
        )
    return None


def update_job(job: Job):
    """Updates an existing job in the database."""
    conn = get_db_connection()
    conn.execute(
        'UPDATE jobs SET user_name = ?, printer_id = ?, faculty = ?, status = ?, elements = ? WHERE id = ?',
        (job.user_name, job.printer_id, job.faculty, job.status.value, ",".join(job.elements), job.job_id)
    )
    conn.commit()
    conn.close()


def search_jobs(query="", faculties=None, statuses=None):
    """Searches and filters jobs from the database."""
    conn = get_db_connection()

    sql_query = "SELECT * FROM jobs WHERE 1=1"
    params = []

    if query:
        sql_query += " AND (user_name LIKE ? OR elements LIKE ?)"
        params.extend([f"%{query}%", f"%{query}%"])

    if faculties:
        sql_query += f" AND faculty IN ({','.join(['?'] * len(faculties))})"
        params.extend(faculties)

    if statuses:
        sql_query += f" AND status IN ({','.join(['?'] * len(statuses))})"
        params.extend(statuses)

    sql_query += " ORDER BY id DESC"

    cursor = conn.execute(sql_query, params)
    jobs_rows = cursor.fetchall()
    conn.close()

    jobs = []
    for row in jobs_rows:
        jobs.append(Job(
            job_id=row['id'],
            user_name=row['user_name'],
            printer_id=row['printer_id'],
            faculty=row['faculty'],
            status=JobStatus(row['status']),
            elements=row['elements'].split(',') if row['elements'] else []
        ))
    return jobs