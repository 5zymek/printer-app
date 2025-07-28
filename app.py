import streamlit as st
import database
from data_models import Job, JobStatus, FACULTIES
import os
import re

# --- Page Configuration ---
st.set_page_config(page_title="Printer Management App", layout="wide")

# --- Initialize Database & Directories ---
database.init_db()
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# --- Session State Management ---
if 'page' not in st.session_state:
    st.session_state.page = 'list'
if 'editing_job_id' not in st.session_state:
    st.session_state.editing_job_id = None


# --- Helper Functions ---

def sanitize_foldername(name):
    """Replaces spaces with underscores and removes special characters to make a valid folder name."""
    return re.sub(r'[^a-zA-Z0-9_]', '', name.replace(' ', '_'))


def get_stl_files_for_faculty(faculty):
    """Scans the directory for a given faculty and returns a list of STL files."""
    faculty_dir = os.path.join("uploads", sanitize_foldername(faculty))
    if not os.path.exists(faculty_dir):
        return []

    return [f for f in os.listdir(faculty_dir) if f.lower().endswith('.stl')]


# --- VIEWS / PAGES ---

def show_list_view():
    """Displays the main list of jobs with search and filtering."""
    st.title("Printer Job Dashboard")

    # --- Sidebar for Navigation and Filtering ---
    with st.sidebar:
        st.header("Navigation")
        if st.button("Job Dashboard"):
            st.session_state.page = 'list'
            st.rerun()
        if st.button("Add New Job"):
            st.session_state.page = 'add_new'
            st.session_state.editing_job_id = None  # Clear any previous edit
            st.rerun()
        if st.button("Bulk File Upload"):
            st.session_state.page = 'bulk_upload'
            st.rerun()

        st.header("Search & Filter")
        search_query = st.text_input("Search by User or Filename")
        selected_faculties = st.multiselect("Filter by Faculty", options=FACULTIES)
        selected_statuses = st.multiselect("Filter by Status", options=[s.value for s in JobStatus])

    # Fetch and display jobs
    jobs = database.search_jobs(query=search_query, faculties=selected_faculties, statuses=selected_statuses)

    col_headers = st.columns((1, 2, 1, 2, 1, 2))
    headers = ["Job ID", "User Name", "Printer ID", "Faculty", "Status", "Actions"]
    for col, header in zip(col_headers, headers):
        col.markdown(f"**{header}**")

    for job in jobs:
        col_data = st.columns((1, 2, 1, 2, 1, 2))
        col_data[0].write(job.job_id)
        col_data[1].write(job.user_name)
        col_data[2].write(job.printer_id)
        col_data[3].write(job.faculty)
        col_data[4].write(job.status.value)
        if col_data[5].button("Edit", key=f"edit_{job.job_id}"):
            st.session_state.page = 'edit'
            st.session_state.editing_job_id = job.job_id
            st.rerun()


def show_bulk_upload_view():
    """A dedicated page for uploading multiple STL files to a faculty's library."""
    st.title("Bulk File Upload to Library")

    st.info(
        "Here you can upload many STL files at once and assign them to a faculty. These files will then be available when creating a new job.")

    selected_faculty = st.selectbox("Select Faculty to upload files for:", FACULTIES)

    uploaded_files = st.file_uploader(
        "Upload STL files",
        type=["stl"],
        accept_multiple_files=True,
        key="bulk_uploader"
    )

    if st.button("Upload to Library", type="primary"):
        if uploaded_files and selected_faculty:
            faculty_dir = os.path.join("uploads", sanitize_foldername(selected_faculty))
            os.makedirs(faculty_dir, exist_ok=True)

            success_count = 0
            for uploaded_file in uploaded_files:
                with open(os.path.join(faculty_dir, uploaded_file.name), "wb") as f:
                    f.write(uploaded_file.getbuffer())
                success_count += 1
            st.success(f"Successfully uploaded {success_count} files to the {selected_faculty} library!")
        else:
            st.warning("Please select a faculty and choose at least one file.")


def show_add_or_edit_view(job_id=None):
    """View for adding or editing a job, now with library selection AND status editing."""
    is_edit_mode = job_id is not None

    if is_edit_mode:
        job = database.get_job_by_id(job_id)
        if not job:
            st.error("Job not found!");
            st.session_state.page = 'list';
            st.rerun()
        page_title = f"Editing Job ID: {job.job_id}"
    else:
        # For new jobs, default to Pending. The form will reflect this.
        job = Job(user_name="", printer_id=1, faculty=FACULTIES[0], elements=[], status=JobStatus.PENDING)
        page_title = "DRUKARKA NR 1 ADD NEW"

    st.title(page_title)

    with st.form(key="job_form"):
        user_name = st.text_input("User Name", value=job.user_name)

        # We'll put all the selects in columns for a cleaner layout
        col1, col2, col3 = st.columns(3)
        with col1:
            printer_id = st.selectbox("Select Printer ID", options=list(range(1, 9)), index=job.printer_id - 1)
        with col2:
            faculty = st.selectbox("Select Faculty", options=FACULTIES,
                                   index=FACULTIES.index(job.faculty) if job.faculty in FACULTIES else 0)

        # --- NEW ---: Add the status editor here
        with col3:
            status_options = [s.value for s in JobStatus]
            current_status_index = status_options.index(job.status.value)
            status_str = st.selectbox("Job Status", options=status_options, index=current_status_index)
        # --- END NEW ---

        st.markdown("---")
        st.subheader("Select Files for Job")

        available_stls = get_stl_files_for_faculty(faculty)
        if not available_stls:
            st.info(f"No files found in the {faculty} library. Use 'Bulk File Upload' to add some.")
            selected_from_library = []
        else:
            selected_from_library = st.multiselect(
                f"Select from {faculty} Library:",
                options=available_stls,
                default=job.elements if is_edit_mode else []
            )

        uploaded_on_the_fly = st.file_uploader(
            "Or upload new, one-off STL files for this job:",
            type=["stl"],
            accept_multiple_files=True
        )

        submit_button = st.form_submit_button(label="SAVE JOB" if not is_edit_mode else "SAVE CHANGES")

        if submit_button:
            newly_uploaded_filenames = []
            for uploaded_file in uploaded_on_the_fly:
                faculty_dir = os.path.join("uploads", sanitize_foldername(faculty))
                os.makedirs(faculty_dir, exist_ok=True)
                with open(os.path.join(faculty_dir, uploaded_file.name), "wb") as f:
                    f.write(uploaded_file.getbuffer())
                newly_uploaded_filenames.append(uploaded_file.name)

            final_elements = sorted(list(set(selected_from_library + newly_uploaded_filenames)))

            if not user_name or not final_elements:
                st.error("User name and at least one STL file are required.")
            else:
                # --- NEW ---: Update the job's status from the form
                job.status = JobStatus(status_str)
                # --- END NEW ---

                job.user_name, job.printer_id, job.faculty, job.elements = user_name, printer_id, faculty, final_elements
                if is_edit_mode:
                    database.update_job(job);
                    st.success("Job updated successfully!")
                else:
                    database.add_job(job);
                    st.success("Job saved successfully!")

                st.session_state.page = 'list';
                st.session_state.editing_job_id = None;
                st.rerun()

    if st.button("< Back to Dashboard"):
        st.session_state.page = 'list';
        st.session_state.editing_job_id = None;
        st.rerun()