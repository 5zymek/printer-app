import streamlit as st
import database  # Your existing database file
from data_models import Job, JobStatus  # Your existing data models

# --- Page Configuration ---
# This should be the first Streamlit command in your app
st.set_page_config(
    page_title="Printer Management App",
    layout="centered"
)

# --- Session State Management ---
# This is how Streamlit remembers information between user interactions.
# We use it to know which page to show ("list" or "add_new").
if 'page' not in st.session_state:
    st.session_state.page = 'list'


# --- Functions to display different views ---

def show_list_view():
    """
    This function replaces your list_view.py.
    It displays the main list of jobs.
    """
    st.title("DRUKARKA NR 1 LIST VIEW")

    if st.button("Add Job", type="primary"):
        # When "Add Job" is clicked, we change the page state and rerun the app
        st.session_state.page = 'add_new'
        st.rerun()

    st.markdown("---")

    # Get all jobs from your database file
    jobs = database.get_all_jobs()

    # Display each job
    for job in jobs:
        # st.columns creates a nice layout, similar to your Tkinter frames
        col1, col2, col3 = st.columns([1, 2, 1.5])

        with col1:
            st.write(f"**Job ID: {job.job_id}**")

        with col2:
            st.write(f"User: {job.user_name}")

        with col3:
            # The status button now opens a pop-up dialog
            if st.button(job.status.value, key=f"status_{job.job_id}"):
                show_status_info_dialog(job)

        st.divider()  # A nice horizontal line between jobs


@st.experimental_dialog("Status / Info")
def show_status_info_dialog(job):
    """
    This function replaces your status_info_view.py.
    It shows a pop-up dialog for a specific job.
    """
    st.write(f"**Job ID:** {job.job_id}")
    st.write(f"**User:** {job.user_name}")
    st.write(f"**Current Status:** {job.status.value}")

    # Placeholder for the photo
    st.image("https://via.placeholder.com/150", caption="Photo Placeholder")

    # Buttons to change the status
    if st.button("Set to Good"):
        job.status = JobStatus.GOOD
        st.rerun()

    if st.button("Set to Failed"):
        job.status = JobStatus.FAILED
        st.rerun()


def show_add_new_view():
    """
    This function replaces your add_new_view.py.
    It displays a form to add a new job.
    """
    st.title("DRUKARKA NR 1 ADD NEW")

    # Using st.form is the best practice for inputs. It groups them together
    # and only submits when the "Save Job" button is clicked.
    with st.form(key="add_job_form"):
        # Instead of a searchable listbox, a multiselect is more web-friendly
        available_files = database.AVAILABLE_STL_FILES
        selected_elements = st.multiselect("Select STL files for the job:", available_files)

        st.markdown("### DLA KOGO JEST TEN STL? (Who is this STL for?)")
        user_name = st.text_input("User Name")

        # The submit button for the form
        submit_button = st.form_submit_button(label="SAVE JOB", type="primary")

        if submit_button:
            if not user_name or not selected_elements:
                st.error("Error: User name and at least one element are required.")
            else:
                new_job = Job(job_id=None, user_name=user_name, elements=selected_elements)
                database.add_job(new_job)
                st.success("Job saved successfully!")

                # Switch back to the list view after saving
                st.session_state.page = 'list'
                st.rerun()

    # A button to go back without saving
    if st.button("< Back to List"):
        st.session_state.page = 'list'
        st.rerun()


# --- Main App Router ---
# This part of the code checks the session state and calls the
# correct function to display the right page.

if st.session_state.page == 'list':
    show_list_view()
elif st.session_state.page == 'add_new':
    show_add_new_view()