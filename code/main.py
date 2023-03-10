from prefect import task, flow
import pandas as pd
from ingest_pyspark import main as ingest
from gcs_to_bq_pyspark import execute

from prefect_dbt.cloud import DbtCloudJob
from prefect_dbt.cloud.jobs import run_dbt_cloud_job


@flow()
def pipeline(year: int, months: list, days=None):
    
    for month in months:
        if type(days) == int:
            ingest(year, month, days)
            execute(year, month)
        elif type(days) == list:
            for day in days:
                ingest(year, month, day)
                execute(year, month)
        else:
            num_of_days = pd.Period(f"{year}-{month:02}").days_in_month
            
            for day in range(1,num_of_days+1):
                ingest(year, month, day)
                execute(year, month)

    #run dbt cloud

if __name__=="__main__":
    year = 2015
    month = [i for i in range(1,2)]
    day = [i for i in range(3,4)]
    pipeline(year, month, day)