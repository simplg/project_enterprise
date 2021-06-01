from os import path
import pandas as pd
import re
from enum import Enum
from sqlalchemy import create_engine


class EnumDatabases(Enum):
    MS_SQL_SERVER = 'microsoft sql server|ms sql server|ssrs'
    MS_APS = 'parallel data ?warehouse|pdw|aps|azure dw|azure data ?warehouse'
    POSTGRE_SQL = 'postgresql|enterprisedb'
    AZURE_DATA_LAKE = 'data lake'
    AZURE_SQL_DB = 'azure'
    MICROSOFT_ACCESS = 'microsoft access'
    ORACLE = 'oracle'
    MYSQL = 'mysql/mariadb'
    AMAZON_RDS = 'amazon rds (any flavor)'
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
    for key, database in enumerate(EnumDatabases):
        if re.search('(?:' + database.value + ')',
                     db) or database.value.find(db) != -1:
            return key + 1
    # to check what was missed
    print(db)
    return len(EnumDatabases)


df = pd.read_csv("project_enterprise/Data_Professional.csv", delimiter=";")
df.index += 1
other_databases_filtered = df['OtherDatabases'].dropna().astype(str).apply(
    lambda x: re.split(r'(?:[-/,]| and )', x.lower()))
primary_databases = df['PrimaryDatabase'].drop_duplicates()

other_db = []
database = pd.DataFrame(
    {"db_name": [enum.name for enum in list(EnumDatabases)]})
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
    other_databases_filtered[key] = diff

df['OtherDatabases'] = other_databases_filtered
database.index += 1
database = database.rename_axis(index="db_id")

sondage_item = df[[
    "CompanyEmployeesOverall", "DatabaseServers", "EducationIsComputerRelated",
    "Gender", "HoursWorkedPerWeek", "ManageStaff", "NewestVersionInProduction",
    "OldestVersionInProduction", "OtherPeopleOnYourTeam", "PostalCode",
    "SalaryUSD", "Timestamp", "TelecommuteDaysPerWeek",
    "YearsWithThisTypeOfJob", "YearsWithThisDatabase"
]]
sondage_item = sondage_item.rename(columns={
    "CompanyEmployeesOverall": "company_employee",
    "DatabaseServers": "database_servers",
    "EducationIsComputerRelated": "education_compute",
    "Gender": "gender",
    "HoursWorkedPerWeek": "hours_worked", "ManageStaff": "manage_staff",
    "NewestVersionInProduction": "newest_version",
    "OldestVersionInProduction": "oldest_version", "OtherPeopleOnYourTeam": "other_people",
    "PostalCode": "postal_code",
    "SalaryUSD": "salary_usd", "Timestamp": "timestamp", "TelecommuteDaysPerWeek": "telecommute",
    "YearsWithThisTypeOfJob": "years_with_job", "YearsWithThisDatabase": "years_with_db"
})

print(sondage_item)

#print(database.to_sql('database', if_exists='append', con=db))
#print(pd.DataFrame(other_database).to_sql('other_database', if_exists='append', con=db, index=False))
