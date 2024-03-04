from typing import Union,List, Optional
from fastapi import FastAPI, HTTPException, Query, Body, Path
from pydantic import BaseModel
import mysql.connector
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta



app = FastAPI()
# Configure CORS
origins = [
    "http://localhost:9906",
    "http://localhost:3000",  # Adjust this to match your front-end's address
    "http://localhost:3001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
host = "localhost"
port = 9906 
user = "root"
password = "MYSQL_ROOT_PASSWORD"
db = "test"
db2 = "AXIS_test"


class CountRecord(BaseModel):
    Lot_id: str
    Direction: str
    Timestamp: str
    Machine_ID: int
    Substrate: int
    TTL: int
    badmark: int
    ASSY_input: int
    NG: int
    Good: int
    Machine_name: str


@app.get("/api/countrecords_counttray")
def read():
    mydb = mysql.connector.connect(host=host, port=port, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)
    sql = """
    SELECT cr.*, st.Machine_name 
    FROM countrecords_counttray cr
    LEFT JOIN station st ON cr.Machine_ID = st.Machine_ID
    """
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return myresult

@app.get("/api/business")
def read():
    mydb = mysql.connector.connect(host=host, port=port, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("SELECT * FROM business")
    myresult = mycursor.fetchall()
    return myresult

@app.get("/api/business/countrecords_counttray/{Business_id}")
def read_count_records(Business_id: int):
    try:
        # Connect to the database
        mydb = mysql.connector.connect(host=host, port=port, user=user, password=password, db=db)
        mycursor = mydb.cursor(dictionary=True)

        # Fetch count records by Business_id
        query = "SELECT * FROM countrecords_counttray WHERE Business_id = %s"
        mycursor.execute(query, (Business_id,))
        results = mycursor.fetchall()

        # Close database connection
        mycursor.close()
        mydb.close()

        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/countrecords")
def read():
    mydb = mysql.connector.connect(host=host, port=port, user=user, password=password, db=db2)
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("SELECT * FROM countrecords")
    myresult = mycursor.fetchall()
    return myresult

@app.get("/api/countrecords_counttray/{Lot_id}")
def read_by_id(Lot_id: str):
    mydb = mysql.connector.connect(host=host, port=port, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)
    # Adjusted SQL query to perform a LEFT JOIN to include Machine_name
    sql = """
    SELECT cr.*, st.Machine_name 
    FROM countrecords_counttray cr
    LEFT JOIN station st ON cr.Machine_ID = st.Machine_ID
    WHERE cr.Lot_id = %s
    """
    val = (Lot_id,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    return myresult

@app.get("/api/countrecords/{Lot_id}")
def read_by_id(Lot_id: str):
    mydb = mysql.connector.connect(host=host, port=port, user=user, password=password, db=db2)
    mycursor = mydb.cursor(dictionary=True)
    # Adjusted SQL query to perform a LEFT JOIN to include Machine_name
    sql = """
    SELECT cr.*, st.Machine_name 
    FROM countrecords cr
    LEFT JOIN station st ON cr.Machine_ID = st.Machine_ID
    WHERE cr.Lot_id = %s
    """
    val = (Lot_id,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    return myresult

@app.post("/api/countrecords_counttray")
def create_records(data: list[CountRecord]):
    mydb = mysql.connector.connect(host=host, port=port, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)

    for item in data:
        sql = "INSERT INTO countrecords_counttray (Lot_id, Direction, Timestamp, Machine_ID, Substrate, TTL, badmark, ASSY_input, NG, Good) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (
            item.Lot_id,
            item.Direction,
            item.Timestamp,
            item.Machine_ID,
            item.Substrate,
            item.TTL,
            item.badmark,
            item.ASSY_input,
            item.NG,
            item.Good
        )

        mycursor.execute(sql, val)
        mydb.commit()

    return {"message": "Data inserted successfully"}

@app.post("/api/countrecords")
def create_records(data: list[CountRecord]):
    mydb = mysql.connector.connect(host=host, port=port, user=user, password=password, db=db2)
    mycursor = mydb.cursor(dictionary=True)

    for item in data:
        sql = "INSERT INTO countrecords (Lot_id, Direction, Timestamp, Machine_ID, Substrate, TTL, badmark, ASSY_input, NG, Good) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (
            item.Lot_id,
            item.Direction,
            item.Timestamp,
            item.Machine_ID,
            item.Substrate,
            item.TTL,
            item.badmark,
            item.ASSY_input,
            item.NG,
            item.Good
        )

        mycursor.execute(sql, val)
        mydb.commit()

    return {"message": "Data inserted successfully"}


@app.delete("/api/countrecords_counttray/{Lot_id}")
def delete_record(Lot_id: str):
    mydb = mysql.connector.connect(host=host, port=port, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)
    sql = "DELETE FROM countrecords_counttray WHERE Lot_id = %s"
    val = (Lot_id,)
    mycursor.execute(sql, val)
    mydb.commit()
    return {"rowcount": mycursor.rowcount}

@app.get("/api/countrecords_counttray/Position/{Machine_ID}/{Direction}/{Lot_id}")
def get_newest_data_by_direction_with_lot_id(Machine_ID: int, Direction: str, Lot_id: str):
    return get_newest_data(Machine_ID, Direction, Lot_id)

@app.get("/api/countrecords_counttray/Position/{Machine_ID}/{Direction}/")
def get_newest_data_by_direction_without_lot_id(Machine_ID: int, Direction: str):
    return get_newest_data(Machine_ID, Direction)

@app.get("/api/countrecords_counttray/Position/{Machine_ID}/{Direction}/")
def get_newest_data_by_direction(Machine_ID: int, Direction: str, Lot_id: str = None):
    mydb = mysql.connector.connect(host=host, port=port, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)

    try:
        # Include Lot_id in the SQL query if provided
        if Lot_id:
            sql = "SELECT Good, Direction FROM countrecords_counttray WHERE Machine_ID = %s AND Direction = %s AND Lot_id = %s ORDER BY Timestamp DESC LIMIT 1"
            val = (Machine_ID, Direction, Lot_id)
        else:
            sql = "SELECT Good, Direction FROM countrecords_counttray WHERE Machine_ID = %s AND Direction = %s ORDER BY Timestamp DESC LIMIT 1"
            val = (Machine_ID, Direction)

        mycursor.execute(sql, val)
        data = mycursor.fetchone()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        mycursor.close()
        mydb.close()

@app.get("/api/countrecords_counttray/PositionCBM/{Machine_ID}/{Direction}/{Lot_id}")
def get_newest_data_by_direction_with_lot_id(Machine_ID: int, Direction: str, Lot_id: str):
    return get_newest_data(Machine_ID, Direction, Lot_id)

@app.get("/api/countrecords_counttray/PositionCBM/{Machine_ID}/{Direction}/")
def get_newest_data_by_direction_without_lot_id(Machine_ID: int, Direction: str):
    return get_newest_data(Machine_ID, Direction)

def get_newest_data(Machine_ID: int, Direction: str, Lot_id: str = None):
    mydb = mysql.connector.connect(host=host, port=port, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)
    try:
        # Include Lot_id in the SQL query if provided
        if Lot_id:
            sql = "SELECT Substrate, TTL, badmark, ASSY_input, NG, Good FROM countrecords_counttray WHERE Machine_ID = %s AND Direction = %s AND Lot_id = %s ORDER BY Timestamp DESC LIMIT 1"
            val = (Machine_ID, Direction, Lot_id)
        else:
            sql = "SELECT Lot_id, Substrate, TTL, badmark, ASSY_input, NG, Good FROM countrecords_counttray WHERE Machine_ID = %s AND Direction = %s ORDER BY Timestamp DESC LIMIT 1"
            val = (Machine_ID, Direction)
        
        mycursor.execute(sql, val)
        data = mycursor.fetchone()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        mycursor.close()
        mydb.close()

@app.get("/api/countrecords_counttray/Lot_id/")
def get_unique_lot_ids():
    mydb = mysql.connector.connect(host=host, port=port, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)

    try:
        # Use DISTINCT in the SQL query to get unique Lot_ids
        mycursor.execute("SELECT DISTINCT Lot_id FROM countrecords_counttray")
        myresult = mycursor.fetchall()
        return JSONResponse(content=myresult)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        mycursor.close()
        mydb.close()


@app.get("/api/countrecords_counttray/datetime_range/{start_timestamp}/{end_timestamp}")
def get_records_by_datetime_range(start_timestamp: str, end_timestamp: str):
    mydb = mysql.connector.connect(host=host, port=port, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)
    
    try:
        # Handle the case where start_timestamp equals end_timestamp
        if start_timestamp == end_timestamp:
            start_date = datetime.strptime(start_timestamp, "%Y-%m-%d %H:%M:%S")
            end_date = start_date + timedelta(days=1)
            end_timestamp = end_date.strftime("%Y-%m-%d %H:%M:%S")

        # Build the SQL query based on the provided datetime range
        sql = "SELECT * FROM countrecords_counttray WHERE Timestamp BETWEEN %s AND %s"
        val = (start_timestamp, end_timestamp)
        mycursor.execute(sql, val)
        data = mycursor.fetchall()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        mycursor.close()
        mydb.close()

@app.get("/api/countrecords_counttray/{Business_id}/datetime_range/{start_timestamp}/{end_timestamp}")
def get_records_by_datetime_range_and_business(Business_id: int, start_timestamp: str, end_timestamp: str):
    mydb = mysql.connector.connect(host=host, port=port, user=user, password=password, db=db)
    mycursor = mydb.cursor(dictionary=True)
    
    try:
        # Handle the case where start_timestamp equals end_timestamp
        if start_timestamp == end_timestamp:
            start_date = datetime.strptime(start_timestamp, "%Y-%m-%d %H:%M:%S")
            end_date = start_date + timedelta(days=1)
            end_timestamp = end_date.strftime("%Y-%m-%d %H:%M:%S")

        # Build the SQL query based on the provided datetime range and Business_id
        sql = "SELECT * FROM countrecords_counttray WHERE Business_id = %s AND Timestamp BETWEEN %s AND %s"
        val = (Business_id, start_timestamp, end_timestamp)
        mycursor.execute(sql, val)
        data = mycursor.fetchall()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        mycursor.close()
        mydb.close()
