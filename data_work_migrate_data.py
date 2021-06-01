# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from re import I
import sqlalchemy
from sqlalchemy import Column, String, Integer, VARCHAR, SMALLINT, DATETIME, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import Boolean, Enum
import enum
import json
import pandas as pd


# %%
data = pd.read_excel('Data_Professional_Salary_Survey_Responses_1.xlsx')
data.head()


# %%
data_feuille_1 = pd.read_excel('Data_Professional_Salary_Survey_Responses_1.xlsx',sheet_name=1)
data_feuille_1

# %% [markdown]
# ## création du dataframe data_Certifications pour le mapping vert la table certification

# %%
Certifications = data.Certifications
data_Certifications = pd.DataFrame({"cert_name":Certifications})
data_Certifications = data_Certifications.drop_duplicates()
data_Certifications = data_Certifications.reset_index()
data_Certifications = data_Certifications.drop(columns=["index"])
data_Certifications = data_Certifications.reset_index()
data_Certifications = data_Certifications.rename(columns={"index":"cert_id"})
#data_Certifications.cert_id = data_Certifications.cert_id*25
data_Certifications.cert_id = data_Certifications.cert_id+1

data_Certifications

# %% [markdown]
# ## création du dataframe data_LookingForAnotherJob pour le mapping vert la table looking_job

# %%
LookingForAnotherJob = data.LookingForAnotherJob
data_LookingForAnotherJob = pd.DataFrame({"look_job":LookingForAnotherJob})
data_LookingForAnotherJob = data_LookingForAnotherJob.drop_duplicates()
data_LookingForAnotherJob = data_LookingForAnotherJob.reset_index()
data_LookingForAnotherJob = data_LookingForAnotherJob.drop(columns=["index"])
data_LookingForAnotherJob = data_LookingForAnotherJob.reset_index()
data_LookingForAnotherJob = data_LookingForAnotherJob.rename(columns={"index":"look_id"})
#data_LookingForAnotherJob.look_id = data_LookingForAnotherJob.look_id*25
data_LookingForAnotherJob.look_id = data_LookingForAnotherJob.look_id+1

data_LookingForAnotherJob

# %% [markdown]
# ## création du dataframe data_Education pour le mapping vert la table education

# %%
Education = data.Education
data_Education = pd.DataFrame({"edu_title":Education})
data_Education = data_Education.drop_duplicates()
data_Education = data_Education.reset_index()
data_Education = data_Education.drop(columns=["index"])
data_Education = data_Education.reset_index()
data_Education = data_Education.rename(columns={"index":"edu_id"})
#data_Education.edu_id = data_Education.edu_id*25
data_Education.edu_id = data_Education.edu_id+1

data_Education

# %% [markdown]
# ## création du dataframe data_EmploymentStatus pour le mapping vert la table employment_status

# %%
EmploymentStatus = data.EmploymentStatus
data_EmploymentStatus = pd.DataFrame({"emp_status":EmploymentStatus})
data_EmploymentStatus = data_EmploymentStatus.drop_duplicates()
data_EmploymentStatus = data_EmploymentStatus.reset_index()
data_EmploymentStatus = data_EmploymentStatus.drop(columns=["index"])
data_EmploymentStatus = data_EmploymentStatus.reset_index()
data_EmploymentStatus = data_EmploymentStatus.rename(columns={"index":"emp_id"})
#data_EmploymentStatus.emp_id = data_EmploymentStatus.emp_id*25
data_EmploymentStatus.emp_id = data_EmploymentStatus.emp_id+1

data_EmploymentStatus

# %% [markdown]
# ## création du dataframe data_EmploymentSector pour le mapping vert la table employment_sector

# %%
EmploymentSector = data.EmploymentSector
data_EmploymentSector = pd.DataFrame({"sec_name":EmploymentSector})
data_EmploymentSector = data_EmploymentSector.drop_duplicates()
data_EmploymentSector = data_EmploymentSector.reset_index()
data_EmploymentSector = data_EmploymentSector.drop(columns=["index"])
data_EmploymentSector = data_EmploymentSector.reset_index()
data_EmploymentSector = data_EmploymentSector.rename(columns={"index":"sec_id"})
#data_EmploymentSector.sec_id = data_EmploymentSector.sec_id*25
data_EmploymentSector.sec_id = data_EmploymentSector.sec_id+1
data_EmploymentSector

# %% [markdown]
# ## création du dataframe data_HowManyCompanies pour le mapping vert la table how_many_companies

# %%
HowManyCompanies = data.HowManyCompanies
data_HowManyCompanies = pd.DataFrame({"mcp_many_companies":HowManyCompanies})
data_HowManyCompanies = data_HowManyCompanies.drop_duplicates()
data_HowManyCompanies = data_HowManyCompanies.reset_index()
data_HowManyCompanies = data_HowManyCompanies.drop(columns=["index"])
data_HowManyCompanies = data_HowManyCompanies.reset_index()
data_HowManyCompanies = data_HowManyCompanies.rename(columns={"index":"mcp_id"})
#data_HowManyCompanies.mcp_id = data_HowManyCompanies.mcp_id*25
data_HowManyCompanies.mcp_id = data_HowManyCompanies.mcp_id+1
data_HowManyCompanies

# %% [markdown]
# ## création du dataframe data_CareerPlansThisYear pour le mapping vert la table carreer_plan

# %%
CareerPlansThisYear = data.CareerPlansThisYear
data_CareerPlansThisYear = pd.DataFrame({"cap_plan":CareerPlansThisYear})
data_CareerPlansThisYear = data_CareerPlansThisYear.drop_duplicates()
data_CareerPlansThisYear = data_CareerPlansThisYear.reset_index()
data_CareerPlansThisYear = data_CareerPlansThisYear.drop(columns=["index"])
data_CareerPlansThisYear = data_CareerPlansThisYear.reset_index()
data_CareerPlansThisYear = data_CareerPlansThisYear.rename(columns={"index":"cap_id"})
#data_CareerPlansThisYear.cap_id = data_CareerPlansThisYear.cap_id*25
data_CareerPlansThisYear.cap_id = data_CareerPlansThisYear.cap_id+1
data_CareerPlansThisYear

# %% [markdown]
# ## création du dataframe data_Country pour le mapping vert la table country

# %%
Country = data.Country
data_Country = pd.DataFrame({"ctr_name":Country})
data_Country = data_Country.drop_duplicates()
data_Country = data_Country.reset_index()
data_Country = data_Country.drop(columns=["index"])
data_Country = data_Country.reset_index()
data_Country = data_Country.rename(columns={"index":"ctr_id"})
#data_Country.ctr_id = data_Country.ctr_id*25
data_Country.ctr_id = data_Country.ctr_id+1
data_Country

# %% [markdown]
# ## création du dataframe data_Survey_Year pour le mapping vert la table sondage

# %%
Survey_Year = data["Survey Year"]
data_Survey_Year = pd.DataFrame({"sdg_year":Survey_Year})
data_Survey_Year = data_Survey_Year.drop_duplicates()
data_Survey_Year = data_Survey_Year.reset_index()
data_Survey_Year = data_Survey_Year.drop(columns=["index"])
data_Survey_Year = data_Survey_Year.reset_index()
data_Survey_Year = data_Survey_Year.rename(columns={"index":"sdg_id"})
#data_Survey_Year.sdg_id = data_Survey_Year.sdg_id*25
data_Survey_Year.sdg_id = data_Survey_Year.sdg_id+1

data_Survey_Year


# %%
sondage_item = data_Survey_Year
sondage_item = sondage_item.reset_index()
sondage_item = sondage_item.rename(columns={"index":"sgi_id"})
#sondage_item.sgi_id = sondage_item.sgi_id*25
sondage_item.sgi_id = sondage_item.sgi_id+1
sondage_item


# %%
## création du dataframe data_KindsOfTasksPerformed pour le mapping vert la table task


# %%
KindsOfTasksPerformed = data_feuille_1.KindsOfTasksPerformed
data_KindsOfTasksPerformed = pd.DataFrame({"tas_name":KindsOfTasksPerformed})
data_KindsOfTasksPerformed = data_KindsOfTasksPerformed.drop_duplicates()
data_KindsOfTasksPerformed = data_KindsOfTasksPerformed.reset_index()
data_KindsOfTasksPerformed = data_KindsOfTasksPerformed.drop(columns=["index"])
data_KindsOfTasksPerformed = data_KindsOfTasksPerformed.reset_index()
data_KindsOfTasksPerformed = data_KindsOfTasksPerformed.rename(columns={"index":"tas_id"})
data_KindsOfTasksPerformed.tas_id = data_KindsOfTasksPerformed.tas_id+1
data_KindsOfTasksPerformed

# %% [markdown]
# ## création du dataframe data_JobTitle pour le mapping vert la table job

# %%
JobTitle = data.JobTitle
data_JobTitle = pd.DataFrame({"job_name":JobTitle})
data_JobTitle = data_JobTitle.drop_duplicates()
data_JobTitle = data_JobTitle.reset_index()
data_JobTitle = data_JobTitle.drop(columns=["index"])
data_JobTitle = data_JobTitle.reset_index()
data_JobTitle = data_JobTitle.rename(columns={"index":"job_id"})
data_JobTitle.job_id = data_JobTitle.job_id+1
data_JobTitle

# %% [markdown]
# ## Creation de la connexion vers la DATABASE

# %%
## IMPORT DU CONFIG.JSON
# assignation de la config.json à fichierConfig
fichierConfig = "config.json"
# ouverture et chargement des donnée contenu dans fichierConfig
with open(fichierConfig) as fichier:
    config = json.load(fichier)["mysql"]


class SqlORM():
    def __init__(self,config):
        self.config = config
        self.connector = self._connect_db()
    def _connect_db(self):
        connector = create_engine('mysql+' + config["connector"] + '://' + config["user"] + ":" + config["password"] + "@" + config["host"] + ":" + config["port"] + "/" + config["bdd"], echo=True)
        return connector




testclass = SqlORM(config)

print(10 * "*")
print("test de la connection", '\n')
connection = testclass.connector
print(connection , '\n')

# %% [markdown]
# ## Insertion dans la table certification

# %%
data_Certifications


# %%
data_Certifications.to_sql('certification', if_exists='append', con=connection, index=False)
print("executed")


# %%
pd.read_sql_query("SELECT * FROM certification",connection)

# %% [markdown]
# ## Insertion dans la table looking_job

# %%
data_LookingForAnotherJob


# %%
data_LookingForAnotherJob.to_sql('looking_job', if_exists='append', con=connection, index=False)
print("executed")


# %%
pd.read_sql_query("SELECT * FROM looking_job",connection)

# %% [markdown]
# ## Insertion dans la table education

# %%
data_Education


# %%
data_Education.to_sql('education', if_exists='append', con=connection, index=False)
print("executed")


# %%
pd.read_sql_query("SELECT * FROM education",connection)

# %% [markdown]
# ## Insertion dans la table employment_status

# %%
data_EmploymentStatus


# %%
for i in data_EmploymentStatus.emp_status:
    print(len(i))


# %%
data_EmploymentStatus.to_sql('employment_status', if_exists='append', con=connection, index=False)
print("executed")


# %%
pd.read_sql_query("SELECT * FROM employment_status",connection)

# %% [markdown]
# ## Insertion dans la table employment_sector

# %%
data_EmploymentSector


# %%
data_EmploymentSector.to_sql('employment_sector', if_exists='append', con=connection, index=False)
print("executed")


# %%
pd.read_sql_query("SELECT * FROM employment_sector",connection)

# %% [markdown]
# ## Insertion dans la table how_many_companies

# %%
data_HowManyCompanies


# %%
data_HowManyCompanies.mcp_many_companies = data_HowManyCompanies.mcp_many_companies.astype(str)


# %%
for i in data_HowManyCompanies.mcp_many_companies:
    print(len(i))


# %%
data_HowManyCompanies.to_sql('how_many_companies', if_exists='append', con=connection, index=False)
print("executed")


# %%
pd.read_sql_query("SELECT * FROM how_many_companies",connection)

# %% [markdown]
# ## Insertion dans la table carreer_plan

# %%
data_CareerPlansThisYear


# %%
data_CareerPlansThisYear.to_sql('carrerr_plan', if_exists='append', con=connection, index=False)
print("executed")


# %%
pd.read_sql_query("SELECT * FROM carrerr_plan",connection)

# %% [markdown]
# ## Insertion dans la table country

# %%
data_Country


# %%
data_Country.to_sql('country', if_exists='append', con=connection, index=False)
print("executed")


# %%
pd.read_sql_query("SELECT * FROM country",connection)

# %% [markdown]
# ## Insertion dans la table sondage

# %%
data_Survey_Year


# %%
data_Survey_Year.to_sql('sondage', if_exists='append', con=connection, index=False)
print("executed")


# %%
pd.read_sql_query("SELECT * FROM sondage",connection)

# %% [markdown]
# ## Insertion dans la table task

# %%
data_KindsOfTasksPerformed


# %%
data_KindsOfTasksPerformed.to_sql('task', if_exists='append', con=connection, index=False)
print("executed")


# %%
pd.read_sql_query("SELECT * FROM task",connection)

# %% [markdown]
# ## Insertion dans la table job

# %%
data_JobTitle


# %%
data_JobTitle.job_name = data_JobTitle.job_name.astype(str)
for i in data_JobTitle.job_name:
    print(len(i))


# %%
data_JobTitle.to_sql('job', if_exists='append', con=connection, index=False)
print("executed")


# %%
pd.read_sql_query("SELECT * FROM job",connection)


# %%



