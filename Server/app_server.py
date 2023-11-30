import os
import functools
import getpass
import oracledb
import asyncio
import websockets
import json
# Function to receive web client input, and send database output
async def exchangeQueryData(cursor, websocket):
    data = json.loads(await websocket.recv())
    print(f"Client {websocket.remote_address[0]} said {data}")
    to_send = ""
    # Actual SQL queries are written here for each valid web client request
    match data["requestType"]:
        case "getAllTuples":
            cursor.execute("SELECT (SELECT COUNT(*) FROM PROPERTY) + \
                        (SELECT COUNT(*) FROM ARREST) + (SELECT COUNT(*) FROM TYPICALEXPENSES) + \
                        (SELECT COUNT(*) FROM MORTGAGERATES) FROM dual")
            # Get the first row, which is just the single sum
            to_send = str(cursor.fetchone()[0])
            # Temporary example for charts
        case "getDeviation":
            cursor.execute("SELECT TO_CHAR(SALE_DATE, 'Mon YYYY') as SALE_DATE, VALUE FROM (SELECT TO_DATE(SALE_MO || ' ' || SALE_YR, 'MON YYYY') as SALE_DATE, VALUE FROM (SELECT SALE_MO, SALE_YR, COUNT(PARCEL_ID) as VALUE FROM PROPERTY WHERE SALE_MO = 'January' OR SALE_MO = 'February' OR SALE_MO = 'March' OR SALE_MO = 'April' OR SALE_MO = 'May' OR SALE_MO = 'June' OR SALE_MO = 'July' OR SALE_MO = 'August' OR SALE_MO = 'September'OR SALE_MO = 'October' OR SALE_MO = 'November' OR SALE_MO = 'December' GROUP BY SALE_MO, SALE_YR) ORDER BY SALE_DATE ASC)")
            chart_data = {
                    "dates" : [],
                    "values" : []
            }
            # Convert to JSON and then to a string
            to_send = str(json.dumps(chart_data))
        case "getAgeInfluence":
            cursor.execute("SELECT TO_CHAR(SALE_DATE, 'Mon YYYY') as SALE_DATE, VALUE FROM (SELECT TO_DATE(SALE_MO || ' ' || SALE_YR, 'MON YYYY') as SALE_DATE, VALUE FROM (SELECT SALE_MO, SALE_YR, COUNT(PARCEL_ID) as VALUE FROM PROPERTY WHERE SALE_MO = 'January' OR SALE_MO = 'February' OR SALE_MO = 'March' OR SALE_MO = 'April' OR SALE_MO = 'May' OR SALE_MO = 'June' OR SALE_MO = 'July' OR SALE_MO = 'August' OR SALE_MO = 'September'OR SALE_MO = 'October' OR SALE_MO = 'November' OR SALE_MO = 'December' GROUP BY SALE_MO, SALE_YR) ORDER BY SALE_DATE ASC)")
            chart_data = {
                    "dates" : [],
                    "values" : []
            }
            # Convert to JSON and then to a string
            to_send = str(json.dumps(chart_data))
        case "getSaleLandsize":
            cursor.execute("SELECT TO_CHAR(SALE_DATE, 'Mon YYYY') as SALE_DATE, VALUE FROM (SELECT TO_DATE(SALE_MO || ' ' || SALE_YR, 'MON YYYY') as SALE_DATE, VALUE FROM (SELECT SALE_MO, SALE_YR, COUNT(PARCEL_ID) as VALUE FROM PROPERTY WHERE SALE_MO = 'January' OR SALE_MO = 'February' OR SALE_MO = 'March' OR SALE_MO = 'April' OR SALE_MO = 'May' OR SALE_MO = 'June' OR SALE_MO = 'July' OR SALE_MO = 'August' OR SALE_MO = 'September'OR SALE_MO = 'October' OR SALE_MO = 'November' OR SALE_MO = 'December' GROUP BY SALE_MO, SALE_YR) ORDER BY SALE_DATE ASC)")
            chart_data = {
                    "dates" : [],
                    "values" : []
            }
            # Convert to JSON and then to a string
            to_send = str(json.dumps(chart_data))
        case _:
            to_send = "null"

    # For each row, append the date and the count separatly to the dictionary
    for row in cursor.fetchall():
        chart_data["dates"].append(str(row[0]))
        chart_data["values"].append(str(row[1]))

    await websocket.send(str(to_send))

async def main():

    # ======= Input Oracle DB information =======
    usr = input("Enter Oracle DB username: ")
    dbdsn = "oracle.cise.ufl.edu:1521/orcl"
    pw = getpass.getpass("Enter password: ")
    connection = oracledb.connect(
    user=usr,
    password=pw,
    dsn=dbdsn)
    # ======= =======
    print("Connected to Oracle DB.")
    cursor = connection.cursor()

    # Listen to web client requests
    async with websockets.serve(
        functools.partial(exchangeQueryData, cursor), "0.0.0.0", 1337):
        await asyncio.Future()

if __name__ == '__main__':
    asyncio.run(main())
