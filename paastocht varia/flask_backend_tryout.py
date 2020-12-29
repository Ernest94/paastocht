from flask import Flask, render_template, request
import mysql.connector;
import base64
import json

app = Flask(__name__)

@app.route('/tiles', methods=['GET'])
def getTiles():
    if request.method == "GET":
        db_mysql = mysql.connector.connect(host="127.0.0.1",user="root",password="laRForeAUshIel",database="paastocht")
        c_mysql = db_mysql.cursor()

        sql = "SELECT * FROM tiles"
        c_mysql.execute(sql)
        myresult = c_mysql.fetchall()

        # ##CREATE ONE LARGE STRING
        tiles_string = ""
        for tile_row in myresult:
            tiles_string+="sAndErnEstrow"
            for value in tile_row:
                try:
                    tiles_string+="sAndErnEstcol" + base64.b64encode(value).decode('utf-8')
                except:
                    tiles_string+="sAndErnEstcol" + str(value)

        c_mysql.close()
        db_mysql.close()
        return json.dumps(tiles_string)
        
@app.route('/metadata', methods=['GET'])
def getMetadata():
    if request.method == "GET":
        db_mysql = mysql.connector.connect(host="127.0.0.1",user="root",password="laRForeAUshIel",database="paastocht")
        c_mysql = db_mysql.cursor()

        sql = "SELECT * FROM metadata"
        c_mysql.execute(sql)
        myresult = c_mysql.fetchall()

        # ##CREATE ONE LARGE STRING
        metadata_string = ""
        for metadata_row in myresult:
            metadata_string+="sAndErnEstrow"
            for value in metadata_row:
                try:
                    metadata_string+="sAndErnEstcol" + str(value)
                except:
                    pass

        c_mysql.close()
        db_mysql.close()
        return json.dumps(metadata_string)


@app.route('/route/info', methods=['GET'])
def getRouteInfo():
    if request.method == "GET":
        db_mysql = mysql.connector.connect(host="127.0.0.1",user="root",password="laRForeAUshIel",database="paastocht")
        c_mysql = db_mysql.cursor()

        sql = "SELECT * FROM route_info"
        c_mysql.execute(sql)
        myresult = c_mysql.fetchall()

        # ##CREATE ONE LARGE STRING
        route_info_string = ""
        for route_info_row in myresult:
            route_info_string+="sAndErnEstrow"
            for value in route_info_row:
                try:
                    route_info_string+="sAndErnEstcol" + str(value)
                except:
                    pass

        c_mysql.close()
        db_mysql.close()
        return json.dumps(route_info_string)

@app.route('/route/coordinates', methods=['GET'])
def getRouteCoordinates():
    if request.method == "GET":
        db_mysql = mysql.connector.connect(host="127.0.0.1",user="root",password="laRForeAUshIel",database="paastocht")
        c_mysql = db_mysql.cursor()

        sql = "SELECT * FROM route_coordinates"
        c_mysql.execute(sql)
        myresult = c_mysql.fetchall()

        # ##CREATE ONE LARGE STRING
        route_coordinates_string = ""
        for route_coordinates_row in myresult:
            route_coordinates_string+="sAndErnEstrow"
            for value in route_coordinates_row:
                try:
                    route_coordinates_string+="sAndErnEstcol" + str(value)
                except:
                    pass

        c_mysql.close()
        db_mysql.close()
        return json.dumps(route_coordinates_string)

@app.route('/')
def hello_name():
    return "Hello!"

if __name__ == '__main__':
    app.run(host='0.0.0.0')