import sqlite3;

filename = "paastocht2020.mbtiles"
db = sqlite3.connect(filename)
c = db.cursor()

# ## PRINT METADATA FROM MBTILES FILE
# metadata = dict(c.execute("SELECT * FROM metadata"))
# print(metadata)


# ##PRINT ALL TABLE NAMES SQLITE DATABASE
# results = c.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%' ORDER BY 1;")
# all_tables = results.fetchall()
# print(all_tables)

# ##PRINT THE NUMBER OF TILES FROM MBTILES FILE
# results = c.execute("SELECT count(*) FROM tiles")
# nr_rows = results.fetchall()
# print(nr_rows)

# ##PRINT ALL COLUMN NAME OF THE TILES TABLE
# results = c.execute("SELECT name FROM PRAGMA_TABLE_INFO('metadata');")
# collumn_names = results.fetchall()
# print(collumn_names)

# ##EXPORT MBTILES TO CSV FILE TO UNDERSTAND THE STRUCTURE
# import pandas as pd
# conn = sqlite3.connect(filename, isolation_level=None,
#                        detect_types=sqlite3.PARSE_COLNAMES)
# db_df = pd.read_sql_query("SELECT * FROM tiles", conn)
# db_df.to_csv('database.csv', index=False)


#PRINT ALL TILES FROM MBTILES FILE
results = c.execute("SELECT * FROM tiles;")
all_tiles = results.fetchall() ##creates a list with tuples 0:zoom_level 1:tile_column 2:tile_row 3:tile_data
print(all_tiles[0])

# ##CREATE ONE LARGE STRING
# tiles_string = ""
# for tile in all_tiles:
#     tiles_string+="sAndErnEst"+str(tile)
# # print(tiles_string)

# ##Strip the long string
# list_tiles_strings = tiles_string.split("sAndErnEst")
# print(len(list_tiles_strings[-1]))
