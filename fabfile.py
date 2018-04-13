from fabric.api import local
def InstallDB(user):
    local(" psql " +user+" -c 'CREATE DATABASE mrm_d'")

def Run_Migration():
    local("alembic revision --autogenerate ")
    local("alembic upgrade head ")

def Run_App():
    local("python app.py")

def prepare_to_host(user):
    InstallDB(user)
    Run_Migration()
    Run_App()

