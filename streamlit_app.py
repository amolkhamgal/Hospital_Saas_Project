"""
Streamlit Authentication & Authorization App
Hospital SaaS Project - MS-SQL Server Backend
"""

import streamlit as st
import pyodbc
import bcrypt
import os
import pandas as pd

# ─────────────────────────────────────────────
# Database configuration (MS-SQL Server)
# Override via environment variables for production
# ─────────────────────────────────────────────
DB_SERVER   = os.environ.get("DB_SERVER",   "localhost")
DB_NAME     = os.environ.get("DB_NAME",     "HospitalSaasDB")
DB_USER     = os.environ.get("DB_USER",     "sa")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")   # must be set via env var
DB_DRIVER   = os.environ.get("DB_DRIVER",   "ODBC Driver 17 for SQL Server")

# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────

@st.cache_resource
def get_connection_pool():
    """
    Return a shared pyodbc connection.
    Cached at the resource level so it is reused across Streamlit reruns
    (pyodbc also enables driver-level connection pooling by default).
    """
    conn_str = (
        f"DRIVER={{{DB_DRIVER}}};"
        f"SERVER={DB_SERVER};"
        f"DATABASE={DB_NAME};"
        f"UID={DB_USER};"
        f"PWD={DB_PASSWORD};"
        "TrustServerCertificate=yes;"
    )
    return pyodbc.connect(conn_str, autocommit=False)


def get_connection():
    """Return the cached pyodbc connection."""
    return get_connection_pool()


def hash_password(password: str) -> bytes:
    """Return a bcrypt hash of the given password."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def check_password(password: str, hashed: bytes) -> bool:
    """Verify a plaintext password against its bcrypt hash."""
    if isinstance(hashed, str):
        hashed = hashed.encode()
    return bcrypt.checkpw(password.encode(), hashed)


def init_db():
    """Create the users table if it does not already exist."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            IF NOT EXISTS (
                SELECT * FROM INFORMATION_SCHEMA.TABLES
                WHERE TABLE_NAME = 'streamlit_users'
            )
            BEGIN
                CREATE TABLE streamlit_users (
                    id          INT IDENTITY(1,1) PRIMARY KEY,
                    username    NVARCHAR(150) NOT NULL UNIQUE,
                    email       NVARCHAR(254) NOT NULL UNIQUE,
                    password    NVARCHAR(128) NOT NULL,
                    role        NVARCHAR(20)  NOT NULL DEFAULT 'patient',
                    is_active   BIT           NOT NULL DEFAULT 1,
                    created_at  DATETIME      NOT NULL DEFAULT GETDATE()
                )
            END
        """)
        conn.commit()
        return True, None
    except Exception as exc:
        return False, str(exc)


def register_user(username: str, email: str, password: str, role: str):
    """Insert a new user; return (success, message)."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM streamlit_users WHERE username = ? OR email = ?",
            (username, email)
        )
        if cursor.fetchone()[0] > 0:
            return False, "Username or email already exists."

        pw_hash = hash_password(password).decode()
        cursor.execute(
            """
            INSERT INTO streamlit_users (username, email, password, role)
            VALUES (?, ?, ?, ?)
            """,
            (username, email, pw_hash, role)
        )
        conn.commit()
        return True, "Registration successful! You can now log in."
    except Exception as exc:
        return False, str(exc)


def authenticate_user(username: str, password: str):
    """Return user dict on success, or None on failure."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, username, email, role, is_active, password
            FROM   streamlit_users
            WHERE  username = ?
            """,
            (username,)
        )
        row = cursor.fetchone()
        if row and check_password(password, row[5]):
            return {
                "id":        row[0],
                "username":  row[1],
                "email":     row[2],
                "role":      row[3],
                "is_active": bool(row[4]),
            }
        return None
    except Exception as exc:
        st.error(f"Database error: {exc}")
        return None


def list_users():
    """Return all users (admin only)."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, username, email, role, is_active, created_at FROM streamlit_users"
        )
        return cursor.fetchall()
    except Exception as exc:
        st.error(f"Database error: {exc}")
        return []


# ─────────────────────────────────────────────
# Page renderers
# ─────────────────────────────────────────────

def show_login_page():
    st.subheader("🔐 Login")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

    if submitted:
        if not username or not password:
            st.error("Please enter both username and password.")
            return
        user = authenticate_user(username, password)
        if user is None:
            st.error("Invalid username or password.")
        elif not user["is_active"]:
            st.warning("Your account is inactive. Please contact an administrator.")
        else:
            st.session_state["user"] = user
            st.success(f"Welcome back, {user['username']}! (Role: {user['role']})")
            st.rerun()


def show_register_page():
    st.subheader("📝 Register")
    with st.form("register_form"):
        username = st.text_input("Username")
        email    = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm  = st.text_input("Confirm Password", type="password")
        role     = st.selectbox("Register as", ["patient", "hospital"])
        submitted = st.form_submit_button("Register")

    if submitted:
        if not username or not email or not password or not confirm:
            st.error("All fields are required.")
            return
        if password != confirm:
            st.error("Passwords do not match.")
            return
        if len(password) < 8:
            st.error("Password must be at least 8 characters long.")
            return
        ok, msg = register_user(username, email, password, role)
        if ok:
            st.success(msg)
        else:
            st.error(msg)


def show_admin_dashboard(user: dict):
    st.subheader("🛡️ Admin Dashboard")
    st.write(f"Logged in as **{user['username']}** | Role: `{user['role']}`")

    st.markdown("---")
    st.markdown("### 👥 All Registered Users")
    rows = list_users()
    if rows:
        df = pd.DataFrame(
            rows,
            columns=["ID", "Username", "Email", "Role", "Active", "Created At"]
        )
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No users found.")


def show_hospital_dashboard(user: dict):
    st.subheader("🏥 Hospital Dashboard")
    st.write(f"Logged in as **{user['username']}** | Role: `{user['role']}`")

    st.markdown("---")
    st.markdown("### Hospital Features")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Patients", "—")
    with col2:
        st.metric("Appointments Today", "—")
    with col3:
        st.metric("Pending Approvals", "—")

    st.info("Connect this dashboard to the Django REST API to populate live data.")


def show_patient_dashboard(user: dict):
    st.subheader("🧑‍⚕️ Patient Dashboard")
    st.write(f"Logged in as **{user['username']}** | Role: `{user['role']}`")

    st.markdown("---")
    st.markdown("### Patient Features")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("My Appointments", "—")
    with col2:
        st.metric("My Documents", "—")

    st.info("Connect this dashboard to the Django REST API to populate live data.")


# ─────────────────────────────────────────────
# Main app
# ─────────────────────────────────────────────

def main():
    st.set_page_config(
        page_title="Hospital SaaS – Auth",
        page_icon="🏥",
        layout="centered",
    )

    st.title("🏥 Hospital SaaS Platform")

    # Initialise session state
    if "user" not in st.session_state:
        st.session_state["user"] = None

    # Initialise database
    ok, err = init_db()
    if not ok:
        st.error(
            f"⚠️ Could not connect to the MS-SQL Server database.\n\n"
            f"Error: {err}\n\n"
            "Please check your database settings (DB_SERVER, DB_NAME, DB_USER, "
            "DB_PASSWORD, DB_DRIVER) and ensure the server is running."
        )
        st.stop()

    # ── Logged-in view ──────────────────────────────
    if st.session_state["user"] is not None:
        user = st.session_state["user"]

        with st.sidebar:
            st.markdown(f"**User:** {user['username']}")
            st.markdown(f"**Role:** `{user['role']}`")
            st.markdown("---")
            if st.button("Logout"):
                st.session_state["user"] = None
                st.rerun()

        role = user["role"]
        if role == "admin":
            show_admin_dashboard(user)
        elif role == "hospital":
            show_hospital_dashboard(user)
        else:
            show_patient_dashboard(user)

    # ── Guest view ──────────────────────────────────
    else:
        tab_login, tab_register = st.tabs(["Login", "Register"])
        with tab_login:
            show_login_page()
        with tab_register:
            show_register_page()


if __name__ == "__main__":
    main()
