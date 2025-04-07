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
