# Packages 
import pandas as pd
import datetime as dt

def clean_dataset(df): 
    """This function clean each column of the imported dataset

    Args:
        df (pd.DataFrame): Input dataframe

    Returns:
        pd.DataFrame: clean dataframe
    """
    
    # Remove the "@" and parse to datetime
    df["timestamp"] = pd.to_datetime(df["@timestamp"].str.replace("@", ""), format="%b %d, %Y %H:%M:%S.%f")
    df = df.set_index("timestamp").sort_index() # Make the timestamp the index column

    # Clean of the scalar column
    df["scalarValue"] = df["scalarValue"].dropna()
    df["scalarValue"] = df["scalarValue"] * 3.6

    # Rename the scalar colum to Hastighed
    df = df.rename(columns={"scalarValue": "Hastighed"})

    # Split the of the siteName column into KK-ID and Sitename
    df[["KK-ID", "Sitename"]] = df["siteName"].str.extract(r"(^KK\-\d{4}\-\w{2}\-\w{3}\-\d{2})\s*-\s*([^-]+)")

    # Drop columns and reorder columns
    df = df.drop(columns=["@timestamp","sensorName"])
    df = df[["KK-ID", "Sitename", "Hastighed"]]
    
    # Remove outliers  
    df = df[(df["Hastighed"] >= 5) & (df["Hastighed"] <= 31)]

    # Only look a the speed between 06:00 - 18:00
    df = df.between_time("06:00", "18:00", inclusive="left").dropna()
    return df

def metadata(df: pd.DataFrame) -> dict: 
    """This small function return the metadata of the dataframe witch will be used in the describtion of the plots produced. 

    Args:
        df pd.DateFrame: input dateframe

    Returns:
        dict: The metadata (Sitename, min-date, max-date) of the input dataframe 
    """
    meta_data = {}
    meta_data["Sitename"] = df["Sitename"].iloc[0]
    meta_data["min-date"] = df.index.min().date()
    meta_data["max-date"] = df.index.max().date()
    return meta_data

