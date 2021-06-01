from datetime import datetime
from enum import Enum
from models import Gender
import re
from typing import Tuple, Union
import pandas as pd
from pandas.core.frame import DataFrame
from pandas.core.series import Series
from sqlalchemy import create_engine

# Dictionnaires associant les noms de chaque champs du fichier Excel
# au nom de la table dans laquelle il sera extrapôlé et ses champs dans la bdd
# Seulement les associations 1..n:1 (sauf pour PrimaryDatabase)
KEYS_DICT: dict[str, dict[str, Union[str, Tuple[str,str]]]] = {
    "Certifications": {
        "tablename": "certification",
        "rows": ("cert_id", "cert_name"),
    },
    "LookingForAnotherJob": {
        "tablename": "looking_job",
        "rows": ("look_id", "look_job"),
    },
    "Education": {
        "tablename": "education",
        "rows": ("edu_id", "edu_title"),
    },
    "EmploymentStatus": {
        "tablename": "employment_status",
        "rows": ("emp_id", "emp_status"),
    },
    "EmploymentSector": {
        "tablename": "employment_sector",
        "rows": ("sec_id", "sec_name"),
    },
    "HowManyCompanies": {
        "tablename": "how_many_companies",
        "rows": ("mcp_id", "mcp_many_companies"),
    },
    "CareerPlansThisYear": {
        "tablename": "career_plan",
        "rows": ("cap_id", "cap_plan"),
    },
    "Country": {
        "tablename": "country",
        "rows": ("ctr_id", "ctr_name"),
    },
    "Survey Year": {
        "tablename": "sondage",
        "rows": ("sdg_id", "sdg_year"),
    },
    "JobTitle": {
        "tablename": "job",
        "rows": ("job_id", "job_name")
    },
}

# Enumeration servant à remplacer les valeurs dans OtherDatabase et PrimaryDatabase
# par des valeurs uniformizé (le nom de l'enum)
# la valeur de l'enum étant un pattern regex pour le remplacement
class EnumDatabases(Enum):
    MS_SQL_SERVER = 'microsoft sql server|ms sql server|ssrs'
    MS_APS = 'parallel data ?warehouse|pdw|aps|azure dw|azure data ?warehouse'
    POSTGRE_SQL = 'postgresql|enterprisedb'
    AZURE_DATA_LAKE = 'data lake'
    AZURE_SQL_DB = 'azure'
    MICROSOFT_ACCESS = 'microsoft access'
    ORACLE = 'oracle'
    MYSQL = 'mysql/mariadb'
    AMAZON_RDS = 'amazon rds'
    MONGO_DB = 'mongodb'
    IBM_DB2 = 'db2|udb|as ?400'
    IBM_NETEZZA = 'netezza'
    CASSANDRA = 'cassandra'
    SQLITE = 'sqlite|db3'
    SAP = 'sap'
    TERADATA = 'teradata'
    ELASTIC_SEARCH = 'elasticsearch'
    COSMO_DB = 'cosmosdb'
    RAVEN_DB = 'raven ?db'
    SNOWFLAKE = 'snowflake'
    HADOOP = 'hadoop|hdfs'
    FIREBIRD = 'firebird'
    FIREBOLT = 'firebolt'
    BIGQUERY = 'big ?query|gbq'
    REDIS = 'redis'
    AMAZON_REDSHIFT = 'redshift'
    AMAZON_AURORA = 'aurora|aws'
    COUCH_DB = 'co[a|u]chdb'
    INFORMIX = 'informix'
    PROGRESS = 'progress|4gl|open ?edge'
    SYBASE = 'sybase'
    INGRES = 'ingres|actian'
    PROVIDEX = 'providex'
    APACHE_MAPR = 'mapr'
    TIBCO_GRAPH_DB = 'tibco'
    VECTOR_WISE = 'informatica'
    ORACLE_BERKELEY = 'berkeley'
    QLIK_SENSE = 'qix'
    ADABAS = 'adabas'
    COUCHBASE = 'couch ?base'
    FOXPRO = 'foxpro'
    EXASOL = 'exasol'
    INTERBASE = 'interbase'
    PERVASIVE = 'pervasive'
    RIAK = 'riak'
    DATACOM = 'datacom'
    GREENPLUM = 'greenplum'
    VERTICA = 'vertica'
    SAP_HANA = 'hana'
    PARADOX = 'paradox'
    GRUPTA_SQLBASE = 'sql ?base'
    DYNAMO_DB = 'dynamo'
    MULTICS_RDS = 'multics'
    CITRIX = 'citrix'
    ALPHAFOUR = 'alpha ?four'
    ROCKET_UNIDATA = 'unidata'
    ROCKET_UNIVERSE = 'universe'
    RAIMA_DBVISTA = 'raima|dbvista'
    AMAZON_DOCUMENT_DB = 'documentdb'
    NEO4J = 'neo4j'
    PICK_OS = 'pick'
    ADS_DB = 'advantage|ads'
    IBM_NOTES_DOMINO = 'domino'
    IBM_IMS = 'ims'
    H2_DB = 'h2'
    FOURD_DB = '4d'
    DATAEASE = 'dataease'
    GRAPH_DB = 'graphdb'
    MONET_DB = 'monetdb'
    MARKLOGIC = 'marklogic'
    KYLIN = 'kylin'
    HPCC = 'hpcc'
    LITE_DB = 'litedb'
    APACHE_IMPALA = 'impala'
    PERVASIVE_BTRIEVE = 'btrieve'
    MEMSQL = 'memsql|singlestore'
    UNISYS = 'unisys'
    INFLUX_DB = 'i[n|m]flux'
    SQL_ANYWHERE = 'sql ?anywhere'
    SPARK = 'spark'
    COCKROACH = 'cockroach'
    GOOGLE_SPANNER = 'spanner'
    GOOGLE_CLOUD_SQL = 'google|gcp'
    SCADA = 'scada'
    GPU_DB = 'kinetica'
    EXTREME_DB = 'extremedb'
    ARANGO_DB = 'arango'
    ROCKS_DB = 'rocks'
    CLIPPER = 'clipper'
    DRUID = 'druid'
    PRESTO_DB = 'presto'
    CLOUDERA_OP_DB = 'cloudera'
    FILEMAKER = 'filemaker'
    APACHE_SOLR = 'solr'
    APACHE_KAFKA = 'kafka'
    APACHE_IGNITE = 'ignite'
    APACHE_HBASE = 'hbase'
    APACHE_PARQUET = 'parquet'
    APACHE_KUDU = 'kudu'
    ALTIBASE = 'altibase'
    SPLUNK = 'splunk'
    SALESFORCE = 'salesforce'
    APACHE_DELTA = 'delta lake'
    APACHE_DERBY = 'derby'
    DATABRICKS = 'databricks'
    CLICKHOUSE = 'clickhouse'
    ORACLE_ESSBASE = 'essbase|hyperion'
    ORIENT_DB = 'orientdb'
    INTERSYSTEMS_CACHE = 'intersystems|cach.'
    IBM_COGNOS = 'tm1'
    IBM_REDBRICK = 'red ?brick'
    IBM_FOCUS = 'focus'
    DB4O = 'db4'
    MUMPS = 'mumps'
    HIVE = 'hive|llap|hdinsight'
    NONSTOP_SQL = 'hp tandem'
    CISCO = 'cisco'
    JADE = 'jade'
    CLUSTRIX = 'clustrix'
    RDB = 'rdb'
    MS_COSMOS_DB = 'cosmo'
    IDMS = 'idms'
    SAS = 'sas'
    DBASE = 'dbase'
    OTHER = 'other'


def uniformize_database(db: str):
    """Fonction qui retourne pour un nom de base de données, un index (int) correspondant à l'enum

    Args:
        db (str): Nom d'une base de données

    Returns:
        int: Index de l'enum
    """
    for key, database in enumerate(EnumDatabases):
        if re.search('(?:' + database.value + ')',
                     db, flags=re.IGNORECASE) or database.value.find(db) != -1:
            return key + 1
    # to check what was missed
    # print(db)
    return len(EnumDatabases)

def remove_not_asked(ligne):
    """Remplace les Not Asked par None

    Args:
        ligne (Series): Ligne a remplacer dans le dataframe

    Returns:
        Series: Retourne la ligne remplacée
    """
    for key, col in enumerate(ligne):
        if col == "Not Asked":
            ligne[key] = None
    return ligne


def export_to_table(data: Series,
                    row_names: Tuple[str, str]) -> Tuple[DataFrame, DataFrame]:
    """Exporte une colonne du dataframe avec une table d'association 1..n:1

    Args:
        data (Series): La colonne du dataframe a extraire
        row_names (Tuple[str, str]): Un tuple des noms que prennent les champs id et valeurs dans la nouvelle table

    Returns:
        Tuple[DataFrame, DataFrame]: Retourne un tuple de dataframe, le premier correspondant à la nouvelle table et
        et le deuxième correspondant au dataframe original modifié  
    """
    id, name = row_names
    data = data.dropna().rename(name)
    unique_values = pd.DataFrame(data.drop_duplicates())
    unique_values = unique_values.reset_index(drop=True).rename_axis(index=id)
    unique_values.index += 1
    return unique_values, data.apply(lambda x: unique_values.index[
        unique_values[name] == x][0] if x is not None else x)

def extract_tasks(data: Series):
    """Extrait les taches réalisés du fichier excel dans une table d'association 1..n:1..n

    Args:
        data (Series): La colonne à extraire

    Returns:
        Tuple[DataFrame, DataFrame]: Un tuple correspondans à une table task et une table task_performed
    """
    data = data.dropna().apply(lambda x: x.split(', '))
    unique_task = pd.DataFrame(set([v for d in data for v in d]), columns=["tas_name"]).rename_axis(index="tas_id")
    unique_task.index += 1
    tasks_performed = []
    for index, tasks in data.iteritems():
        for task in tasks:
            tasks_performed.append({"sgi_id": index, "tas_id": unique_task.index[unique_task['tas_name'] == task][0] })
    return unique_task, pd.DataFrame(tasks_performed)

def extract_jobs(data: Series, unique_jobs):
    """Extrait les métiers du fichier excel

    Args:
        data (Series): La colonne à extraire
        unique_jobs (DataFrame): Les métiers uniques présents dans la table job 

    Returns:
        DataFrame: Un dataframe correpondant à la table other_jobs 
    """
    unique_jobs_with_comma = unique_jobs[unique_jobs['job_name'].str.find(',') != -1]
    other_jobs = []
    for i, job in unique_jobs_with_comma["job_name"].iteritems():
        data = data.str.replace(job, str(i), regex=False)
    for index, jobs in data.dropna().iteritems():
        for job in jobs.split(", "):
            other_jobs.append({"sgi_id": index, "job_id": unique_jobs.index[unique_jobs['job_name'] == job][0] if not job.isnumeric() else int(job) })
    return pd.DataFrame(other_jobs)

def extract_other_database(data: Series):
    """Extrait les autres base de données utilisés du fichier excel

    Args:
        data (Series): La colonne à extraire

    Returns:
        DataFrame: Retourne un dataframe correspondant à la table other_database
    """
    other_databases_filtered = data.dropna().astype(str).apply(
    lambda x: re.split(r'(?:[-/,]| and )', x.lower()))
    other_database = []
    for key, db_list in other_databases_filtered.iteritems():
        diff = []
        for db in db_list:
            db: str = db.strip()
            db = re.sub(r'\([^\s]+\)', '', db)
            db = re.sub(r'[\(\)\]\[]*', '', db)
            u = uniformize_database(db)
            if not u in diff:
                diff.append(u)
                other_database.append({"db_id": u, "sgi_id": key})
    return pd.DataFrame(other_database)

def get_gender(gender):
    """Retourne la valeur de l'enum genre pour un genre donné

    Args:
        gender (Gender): Un élément de l'énumération genre

    Returns:
        str: La valeur associée à l'énumériation genre dans la bdd
    """
    if gender == Gender.male:
        return 'male'
    elif gender == Gender.female:
        return 'female'
    elif gender == Gender.other:
        return 'other'
    elif gender == Gender.na:
        return 'na'
    return None

def cmp_to_int(n):
    """Converti le nombre d'employé en valeur exploitable, certains sont des intervalles dans le fichier excel

    Args:
        n (str | int): Le nombre d'employés dans l'entreprise

    Returns:
        int: Le nombre d'employés uniformisé
    """
    if isinstance(n, int) or n is None:
        return n
    if n.isnumeric():
        return int(n)
    else:
        match = re.search("(\d+).+", n)
        return int(match.group(1))

def telecommute_to_int(n):
    """Converti le champs telecommute en int

    Args:
        n (str | int): La fréquence de télécommute

    Returns:
        int: Une fréquence converti en int
    """
    if isinstance(n, int) or n is None:
        return n
    if n.isnumeric():
        return int(n)
    elif n == 'None, or less than 1 day per week':
        return 0
    elif n == '5 or more':
        return 5

def uniformize_ydb(n):
    """Uniformise le nombre d'années passé à utiliser une bdd

    Args:
        n (int): Le nombre d'année ou l'année à laquelle on a commencé à utiliser la bdd

    Returns:
        int: Le nombre d'années
    """
    current_year = datetime.now().year
    if n > 1900 and n <= current_year:
        return current_year - n
    elif n < 150:
        return n
    else:
        return None

df = pd.read_excel("Data_Professional_Salary_Survey_Responses_1.xlsx")
df.index += 1
# On remplace les Not Asked par None
df = df.apply(remove_not_asked, axis=1)

unique_jobs = None
db = create_engine('mysql://akuma06:sdfsdf23@localhost/simplon', echo='debug')

with db.connect() as connexion: 
    with connexion.begin():
        # for 1n:1 associations sauf database
        for _, col in enumerate(KEYS_DICT):
            table, data = export_to_table(df[col], KEYS_DICT[col]["rows"])
            df[KEYS_DICT[col]["rows"][0]] = data.astype(pd.Int64Dtype())
            if col == "JobTitle":
                unique_jobs = table

            table.to_sql(KEYS_DICT[col]["tablename"], if_exists='append', con=connexion)

        # for n:n associations
        unique_tasks, tasks_performed = extract_tasks(df["KindsOfTasksPerformed"])
        other_jobs = extract_jobs(df["OtherJobDuties"], unique_jobs)

        df["primary_db_id"] = df["PrimaryDatabase"].apply(uniformize_database)
        database = pd.DataFrame({"db_name": [enum.name for enum in list(EnumDatabases)]})
        database.index += 1
        database = database.rename_axis(index="db_id")
        other_database = extract_other_database(df["OtherDatabases"])
        database.to_sql('database', if_exists='append', con=connexion)
        unique_tasks.to_sql('task', if_exists='append', con=connexion)

        indices = [
            "CompanyEmployeesOverall", "DatabaseServers", "EducationIsComputerRelated",
            "Gender", "HoursWorkedPerWeek", "ManageStaff", "NewestVersionInProduction",
            "OldestVersionInProduction", "OtherPeopleOnYourTeam", "PostalCode",
            "SalaryUSD", "Timestamp", "TelecommuteDaysPerWeek",
            "YearsWithThisTypeOfJob", "YearsWithThisDatabase",
        ] + [KEYS_DICT[key]["rows"][0] for key in KEYS_DICT]
        sondage_item = df[indices]
        sondage_item = sondage_item.rename(columns={
            "CompanyEmployeesOverall": "company_employee",
            "DatabaseServers": "database_servers",
            "EducationIsComputerRelated": "education_computer",
            "Gender": "gender",
            "HoursWorkedPerWeek": "hours_worked", "ManageStaff": "manage_staff",
            "NewestVersionInProduction": "newest_version",
            "OldestVersionInProduction": "oldest_version", "OtherPeopleOnYourTeam": "other_people",
            "PostalCode": "postal_code",
            "SalaryUSD": "salary_usd", "Timestamp": "timestamp", "TelecommuteDaysPerWeek": "telecommute",
            "YearsWithThisTypeOfJob": "years_with_job", "YearsWithThisDatabase": "years_with_db"
        })

        sondage_item["manage_staff"] = sondage_item["manage_staff"] == "Yes"
        sondage_item["education_computer"] = sondage_item["education_computer"] == "Yes"
        sondage_item["other_people"] = sondage_item["other_people"].apply(lambda x: 0 if x == 'None' else (5 if x == 'More than 5' else x))
        sondage_item["gender"] = sondage_item["gender"].apply(get_gender)
        sondage_item["company_employee"] = sondage_item["company_employee"].apply(cmp_to_int)
        sondage_item["telecommute"] = sondage_item["telecommute"].apply(telecommute_to_int)
        sondage_item["years_with_db"] = sondage_item["years_with_db"] .apply(uniformize_ydb)

        sondage_item = sondage_item.rename_axis(index="sgi_id")
        sondage_item.to_sql('sondage_item', if_exists='append', con=connexion)

        other_database.to_sql('other_database', if_exists='append', con=connexion, index=False)
        tasks_performed.to_sql('task_performed', if_exists='append', con=connexion, index=False)
        other_jobs.to_sql("other_duties", if_exists='append', con=connexion, index=False)
