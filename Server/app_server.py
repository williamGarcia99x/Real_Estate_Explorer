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
        case "getDeviation":
            if data["options"]["county"] == "default":
                cursor.execute("SELECT TO_CHAR(SALE_DATE, 'Mon YYYY') as SALE_DATE, VALUE \
                        FROM (SELECT TO_DATE(SALE_MO || ' ' || SALE_YR, 'MON YYYY') as SALE_DATE, VALUE \
                        FROM (SELECT SALE_MO, SALE_YR, AVG(((SALE_PRC / MARKET_VALUE) - 1) * 100) as VALUE \
                        FROM PROPERTY \
                        WHERE MARKET_VALUE != 0 AND (SALE_PRC / MARKET_VALUE) - 1 >= 0 \
                        AND(SALE_PRC / MARKET_VALUE) - 1 <= 10 \
                        AND (SALE_MO = 'January' OR SALE_MO = 'February' OR SALE_MO = 'March' \
                        OR SALE_MO = 'April' OR SALE_MO = 'May' OR SALE_MO = 'June' \
                        OR SALE_MO = 'July' OR SALE_MO = 'August' OR SALE_MO = 'September'\
                        OR SALE_MO = 'October' OR SALE_MO = 'November' OR SALE_MO = 'December') \
                        GROUP BY SALE_MO, SALE_YR) \
                        ORDER BY SALE_DATE ASC)")
            else:
                cursor.execute(f"SELECT TO_CHAR(SALE_DATE, 'Mon YYYY') as SALE_DATE, VALUE \
                        FROM (SELECT TO_DATE(SALE_MO || ' ' || SALE_YR, 'MON YYYY') as SALE_DATE, VALUE \
                        FROM (SELECT SALE_MO, SALE_YR, AVG(((SALE_PRC / MARKET_VALUE) - 1) * 100) as VALUE \
                        FROM PROPERTY \
                        WHERE MARKET_VALUE != 0 AND (SALE_PRC / MARKET_VALUE) - 1 >= 0 \
                        AND COUNTY_CODE = {data['options']['county']} AND (SALE_PRC / MARKET_VALUE) - 1 <= 10 \
                        AND (SALE_MO = 'January' OR SALE_MO = 'February' OR SALE_MO = 'March' \
                        OR SALE_MO = 'April' OR SALE_MO = 'May' OR SALE_MO = 'June' \
                        OR SALE_MO = 'July' OR SALE_MO = 'August' OR SALE_MO = 'September'\
                        OR SALE_MO = 'October' OR SALE_MO = 'November' OR SALE_MO = 'December') \
                        GROUP BY SALE_MO, SALE_YR) \
                        ORDER BY SALE_DATE ASC) \
                        WHERE SALE_DATE BETWEEN TO_DATE('{data['options']['startDate']}', 'YYYY-MM') AND TO_DATE('{data['options']['endDate']}', 'YYYY-MM')")
                        

            chart_data = {
                    "dates" : [],
                    "values" : []
            }

            # For each row, append the date and the count separatly to the dictionary
            for row in cursor.fetchall():
                chart_data["dates"].append(str(row[0]))
                chart_data["values"].append(str(row[1]))

            # Convert to JSON and then to a string
            to_send = str(json.dumps(chart_data))
        case "getAgeInfluence":
            min_year = 0
            max_year = 0
            if data["options"]["propertyAge"] == "0-9":
                min_year = 0
                max_year = 9
            elif data["options"]["propertyAge"] == "10-19":
                min_year = 10
                max_year = 19
            elif data["options"]["propertyAge"] == "20-29":
                min_year = 20
                max_year = 29
            elif data["options"]["propertyAge"] == "30-39":
                min_year = 30
                max_year = 39
            elif data["options"]["propertyAge"] == "40":
                min_year = 40
                max_year = 999
            if data["options"]["county"] == "default":
                cursor.execute(f"SELECT TO_CHAR(SALE_DATE, 'Mon YYYY') as SALE_DATE, VALUE \
                        FROM (SELECT TO_DATE(SALE_MO || ' ' || SALE_YR, 'MON YYYY') as SALE_DATE, VALUE \
                        FROM (SELECT SALE_MO, SALE_YR, COUNT(PARCEL_ID) as VALUE \
                        FROM PROPERTY \
                        WHERE (2023 - BUILT_YEAR) >= 0 AND (2023 - BUILT_YEAR) <= 1000 \
                        AND (SALE_MO = 'January' OR SALE_MO = 'February' OR SALE_MO = 'March' \
                        OR SALE_MO = 'April' OR SALE_MO = 'May' OR SALE_MO = 'June' \
                        OR SALE_MO = 'July' OR SALE_MO = 'August' OR SALE_MO = 'September' \
                        OR SALE_MO = 'October' OR SALE_MO = 'November' OR SALE_MO = 'December') \
                        GROUP BY SALE_MO, SALE_YR) \
                        ORDER BY SALE_DATE ASC) \
                        ")
            else:
                cursor.execute(f"SELECT TO_CHAR(SALE_DATE, 'Mon YYYY') as SALE_DATE, VALUE \
                        FROM (SELECT TO_DATE(SALE_MO || ' ' || SALE_YR, 'MON YYYY') as SALE_DATE, VALUE \
                        FROM (SELECT SALE_MO, SALE_YR, COUNT(PARCEL_ID) as VALUE \
                        FROM PROPERTY \
                        WHERE (2023 - BUILT_YEAR) >= {min_year} AND (2023 - BUILT_YEAR) <= {max_year} \
                        AND COUNTY_CODE = {data['options']['county']} \
                        AND (SALE_MO = 'January' OR SALE_MO = 'February' OR SALE_MO = 'March' \
                        OR SALE_MO = 'April' OR SALE_MO = 'May' OR SALE_MO = 'June' \
                        OR SALE_MO = 'July' OR SALE_MO = 'August' OR SALE_MO = 'September' \
                        OR SALE_MO = 'October' OR SALE_MO = 'November' OR SALE_MO = 'December') \
                        GROUP BY SALE_MO, SALE_YR) \
                        ORDER BY SALE_DATE ASC) \
                        WHERE SALE_DATE BETWEEN TO_DATE('{data['options']['startDate']}', 'YYYY-MM') AND TO_DATE('{data['options']['endDate']}', 'YYYY-MM')")
            chart_data = {
                    "dates" : [],
                    "values" : []
            }
            
            # For each row, append the date and the count separatly to the dictionary
            for row in cursor.fetchall():
                chart_data["dates"].append(str(row[0]))
                chart_data["values"].append(str(row[1]))
                
            # Convert to JSON and then to a string
            to_send = str(json.dumps(chart_data))
        case "getSaleLandsize":
            min_size = 0
            max_size = 0
            if data["options"]["landSize"] == "0-999":
                min_size = 0
                max_size= 999
            elif data["options"]["landSize"] == "1000-4999":
                min_size = 1000
                max_size = 4999
            elif data["options"]["landSize"] == "5000-9999":
                min_size = 29999
                max_size = 9999
            elif data["options"]["landSize"] == "20000-29999":
                min_size = 20000
                max_size = 29999
            elif data["options"]["landSize"] == "30000":
                min_size = 30000
                max_size = 99999999

            if data["options"]["county"] == "default":
                cursor.execute(f"SELECT TO_CHAR(SALE_DATE, 'Mon YYYY') as SALE_DATE, VALUE \
                        FROM (SELECT TO_DATE(SALE_MO || ' ' || SALE_YR, 'MON YYYY') as SALE_DATE, VALUE \
                        FROM (SELECT SALE_MO, SALE_YR, COUNT(PARCEL_ID) as VALUE \
                        FROM PROPERTY \
                        WHERE LANDSIZE >= 0 AND LANDSIZE <= 99999999 \
                        AND (SALE_MO = 'January' OR SALE_MO = 'February' OR SALE_MO = 'March' \
                        OR SALE_MO = 'April' OR SALE_MO = 'May' OR SALE_MO = 'June' \
                        OR SALE_MO = 'July' OR SALE_MO = 'August' OR SALE_MO = 'September' \
                        OR SALE_MO = 'October' OR SALE_MO = 'November' OR SALE_MO = 'December') \
                        GROUP BY SALE_MO, SALE_YR) \
                        ORDER BY SALE_DATE ASC) \
                        ")
            else:
                cursor.execute(f"SELECT TO_CHAR(SALE_DATE, 'Mon YYYY') as SALE_DATE, VALUE \
                        FROM (SELECT TO_DATE(SALE_MO || ' ' || SALE_YR, 'MON YYYY') as SALE_DATE, VALUE \
                        FROM (SELECT SALE_MO, SALE_YR, COUNT(PARCEL_ID) as VALUE \
                        FROM PROPERTY \
                        WHERE LANDSIZE >= {min_size} AND LANDSIZE <= {max_size} \
                        AND COUNTY_CODE = {data['options']['county']} \
                        AND (SALE_MO = 'January' OR SALE_MO = 'February' OR SALE_MO = 'March' \
                        OR SALE_MO = 'April' OR SALE_MO = 'May' OR SALE_MO = 'June' \
                        OR SALE_MO = 'July' OR SALE_MO = 'August' OR SALE_MO = 'September' \
                        OR SALE_MO = 'October' OR SALE_MO = 'November' OR SALE_MO = 'December') \
                        GROUP BY SALE_MO, SALE_YR) \
                        ORDER BY SALE_DATE ASC) \
                        WHERE SALE_DATE BETWEEN TO_DATE('{data['options']['startDate']}', 'YYYY-MM') AND TO_DATE('{data['options']['endDate']}', 'YYYY-MM')")
            chart_data = {
                    "dates" : [],
                    "values" : []
            }

            # For each row, append the date and the count separately to the dictionary
            for row in cursor.fetchall():
                chart_data["dates"].append(str(row[0]))
                chart_data["values"].append(str(row[1]))

            # Convert to JSON and then to a string
            to_send = str(json.dumps(chart_data))
        case "getSafety":
            chart_data = {
                    "datesarrests" : [],
                    "valuesarrests" : [],
                    "datessales" : [],
                    "valuessales" : []
            }
            # Arrests Chart
            if data["options"]["county"] == "default":
                cursor.execute(f"SELECT ARREST_DATE, AVG(VALUE) VALUE \
                        FROM (SELECT TO_CHAR(ARRESTDATE, 'Mon YYYY') as ARREST_DATE, COUNT(CHARGEID) as VALUE \
                        FROM ARREST \
                        WHERE ARRESTDATE >= TO_DATE('2022-01', 'YYYY-MM') \
                        GROUP BY ARRESTDATE \
                        ORDER BY ARRESTDATE ASC) \
                        GROUP BY ARREST_DATE \
                        ORDER BY TO_DATE(ARREST_DATE, 'Mon YYYY') ASC")
                for row in cursor.fetchall():
                    chart_data["datesarrests"].append(str(row[0]))
                    chart_data["valuesarrests"].append(str(row[1]))
            else:
                cursor.execute(f"SELECT ARREST_DATE, AVG(VALUE) VALUE \
                        FROM (SELECT TO_CHAR(ARRESTDATE, 'Mon YYYY') as ARREST_DATE, COUNT(CHARGEID) as VALUE \
                        FROM ARREST \
                        WHERE COUNTYCODE = {data['options']['county']} \
                        AND ARRESTDATE BETWEEN TO_DATE('{data['options']['startDate']}', 'YYYY-MM')  \
                        AND TO_DATE('{data['options']['endDate']}', 'YYYY-MM') \
                        GROUP BY ARRESTDATE \
                        ORDER BY ARRESTDATE ASC) \
                        GROUP BY ARREST_DATE \
                        ORDER BY TO_DATE(ARREST_DATE, 'Mon YYYY') ASC")
                for row in cursor.fetchall():
                    chart_data["datesarrests"].append(str(row[0]))
                    chart_data["valuesarrests"].append(str(row[1]))
            # Sales Chart
            if data["options"]["county"] == "default":
                cursor.execute(f"SELECT TO_CHAR(SALE_DATE, 'Mon YYYY') as SALE_DATE, VALUE \
                        FROM (SELECT TO_DATE(SALE_MO || ' ' || SALE_YR, 'MON YYYY') as SALE_DATE, VALUE \
                        FROM (SELECT SALE_MO, SALE_YR, AVG(SALE_PRC) as VALUE \
                        FROM PROPERTY \
                        WHERE (SALE_MO = 'January' OR SALE_MO = 'February' OR SALE_MO = 'March' \
                        OR SALE_MO = 'April' OR SALE_MO = 'May' OR SALE_MO = 'June' \
                        OR SALE_MO = 'July' OR SALE_MO = 'August' OR SALE_MO = 'September' \
                        OR SALE_MO = 'October' OR SALE_MO = 'November' OR SALE_MO = 'December') \
                        GROUP BY SALE_MO, SALE_YR) \
                        ORDER BY SALE_DATE ASC)")
                for row in cursor.fetchall():
                    chart_data["datessales"].append(str(row[0]))
                    chart_data["valuessales"].append(str(row[1]))
            else:
                cursor.execute(f"SELECT TO_CHAR(SALE_DATE, 'Mon YYYY') as SALE_DATE, VALUE \
                        FROM (SELECT TO_DATE(SALE_MO || ' ' || SALE_YR, 'MON YYYY') as SALE_DATE, VALUE \
                        FROM (SELECT SALE_MO, SALE_YR, AVG(SALE_PRC) as VALUE \
                        FROM PROPERTY \
                        WHERE MARKET_VALUE != 0 AND (SALE_PRC / MARKET_VALUE) - 1 >= 0 \
                        AND COUNTY_CODE = {data['options']['county']} AND (SALE_PRC / MARKET_VALUE) - 1 <= 10 \
                        AND (SALE_MO = 'January' OR SALE_MO = 'February' OR SALE_MO = 'March' \
                        OR SALE_MO = 'April' OR SALE_MO = 'May' OR SALE_MO = 'June' \
                        OR SALE_MO = 'July' OR SALE_MO = 'August' OR SALE_MO = 'September'\
                        OR SALE_MO = 'October' OR SALE_MO = 'November' OR SALE_MO = 'December') \
                        GROUP BY SALE_MO, SALE_YR) \
                        ORDER BY SALE_DATE ASC) \
                        WHERE SALE_DATE BETWEEN TO_DATE('{data['options']['startDate']}', 'YYYY-MM') AND TO_DATE('{data['options']['endDate']}', 'YYYY-MM')")
                        
                for row in cursor.fetchall():
                    chart_data["datessales"].append(str(row[0]))
                    chart_data["valuessales"].append(str(row[1]))
            to_send = str(json.dumps(chart_data))
        case "getAffordability":
            chart_data = {
                    "datesafford" : [],
                    "valuesafford" : []
            }
            # Affordability Chart
            cursor.execute(f"SELECT SALE_DATE, \
                    (((VALUE * ( (PERCENTAGE/100) / 12)) / (1 - POWER((1 + (PERCENTAGE/100) / 12), - 12 * 30)) * 12) \
                    -  (SELECT {data['options']['householdSize']} FROM TYPICALEXPENSES WHERE COUNTYCODE = {data['options']['county']})) as VALUE \
                    FROM (SELECT TO_CHAR(SALE_DATE, 'Mon YYYY') as SALE_DATE, VALUE \
                    FROM (SELECT TO_DATE(SALE_MO || ' ' || SALE_YR, 'MON YYYY') as SALE_DATE, VALUE \
                    FROM (SELECT SALE_MO, SALE_YR, AVG(SALE_PRC) as VALUE \
                    FROM PROPERTY, MORTGAGERATES \
                    WHERE MARKET_VALUE != 0 AND (SALE_PRC / MARKET_VALUE) - 1 >= 0 \
                    AND COUNTY_CODE = {data['options']['county']} AND (SALE_PRC / MARKET_VALUE) - 1 <= 10 \
                    AND (SALE_MO = 'January' OR SALE_MO = 'February' OR SALE_MO = 'March' \
                    OR SALE_MO = 'July' OR SALE_MO = 'August' OR SALE_MO = 'September' \
                    OR SALE_MO = 'October' OR SALE_MO = 'November' OR SALE_MO = 'December') \
                    GROUP BY SALE_MO, SALE_YR) \
                    ORDER BY SALE_DATE ASC) \
                    WHERE SALE_DATE BETWEEN TO_DATE('{data['options']['startDate']}', 'YYYY-MM') AND TO_DATE('{data['options']['endDate']}', 'YYYY-MM')) \
                    NATURAL JOIN \
                    (SELECT SALE_DATE, AVG(PERCENTAGE) as PERCENTAGE \
                    FROM (SELECT TO_CHAR(RATEDATE, 'Mon YYYY') as SALE_DATE, PERCENTAGE \
                    FROM MORTGAGERATES \
                    WHERE RATEDATE BETWEEN TO_DATE('{data['options']['startDate']}', 'YYYY-MM') AND TO_DATE('{data['options']['endDate']}', 'YYYY-MM'))  \
                    GROUP BY SALE_DATE)")
            for row in cursor.fetchall():
                chart_data["datesafford"].append(str(row[0]))
                chart_data["valuesafford"].append(str(row[1]))
            to_send = str(json.dumps(chart_data))
        case _:
            to_send = "null"

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
