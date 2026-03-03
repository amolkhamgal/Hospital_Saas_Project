# Hospital_Saas_Project


1. #steps to use:

git clone https://github.com/amolkhamgal/Hospital_Saas_Project.git
cd Hospital_Saas_Project

python -m venv venv
venv\Scripts\activate  # Windows

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

2. #Auth Endpoints:
POST /auth/register/ – Register user

POST /auth/login/ – Login user

3.  #Main Endpoints
/hospitals/ – Manage hospitals

/patients/ – Manage patients

/documents/ – Manage documents

/approvals/ – Approve hospital access

/api/sidebars/ – Dynamic sidebar

---

## Streamlit Authentication & Authorization UI

A standalone Streamlit app (`streamlit_app.py`) provides a simple browser-based
login / registration interface backed by **Microsoft SQL Server**.

### Prerequisites

* Python 3.9+
* [Microsoft ODBC Driver 17 for SQL Server](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server)
  installed on the machine that runs the app.
* A running SQL Server instance (local or remote).

### Configuration (environment variables)

| Variable      | Default                          | Description                        |
|---------------|----------------------------------|------------------------------------|
| `DB_SERVER`   | `localhost`                      | SQL Server hostname or IP          |
| `DB_NAME`     | `HospitalSaasDB`                 | Database name                      |
| `DB_USER`     | `sa`                             | SQL Server login username          |
| `DB_PASSWORD` | `YourStrong@Passw0rd`            | SQL Server login password          |
| `DB_DRIVER`   | `ODBC Driver 17 for SQL Server`  | ODBC driver name                   |

Set these before running the app, for example on Windows:

```
set DB_SERVER=my-sql-server
set DB_NAME=HospitalSaasDB
set DB_USER=sa
set DB_PASSWORD=MySecret123!
```

Or on Linux / macOS:

```bash
export DB_SERVER=my-sql-server
export DB_NAME=HospitalSaasDB
export DB_USER=sa
export DB_PASSWORD=MySecret123!
```

### Running the Streamlit app

```bash
streamlit run streamlit_app.py
```

The app will open in your browser at `http://localhost:8501`.

### Roles

| Role       | Description                                    |
|------------|------------------------------------------------|
| `patient`  | Can view their own appointments and documents  |
| `hospital` | Can manage patients and appointments           |
| `admin`    | Full access – can view all registered users    |

> **Note:** The `admin` role must be assigned directly in the database.
> New users registering through the UI may choose `patient` or `hospital`.

### Django backend – MS-SQL Server

To run the Django REST API with MS-SQL Server instead of SQLite, set:

```
DB_ENGINE=mssql
DB_SERVER=...
DB_NAME=...
DB_USER=...
DB_PASSWORD=...
```

Then run migrations as usual:

```bash
python manage.py migrate
```

