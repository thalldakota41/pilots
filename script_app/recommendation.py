# import all necessary libraries
from .models import Show
import pandas as pd
import sqlite3
from pprint import pp, pprint

qb = Show.objects.all()
print(qb)

# connect to database
# con = sqlite3.connect('../db.sqlite3')
# # sql_query = '''
# #         SELECT name FROM sqlite_master 
# #         WHERE type='table';

# # '''
# # cursor = con.cursor() 
# # cursor.execute(sql_query)
# # print(cursor.fetchall())

# sql = """
#     SELECT 
#         show_id,
#         tag_id
#     FROM 
#         script_app_show_tag
#     GROUP BY
#         tag_id;

# """

# df = pd.read_sql_query(sql,con)

# print (df)