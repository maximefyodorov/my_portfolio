import sqlite3
import jinja2

db = sqlite3.connect("portfolio-data.db3")

crsr = db.cursor()

crsr.execute("SELECT typename, intro_text, abbrev, icon FROM TYPES")
genres = crsr.fetchall()

works = {
  'posters': [],
  'logos': [],
  'advert': [],
  'pack': [],
  'calend': [],
  'sites': [],
  'photo': [],
  'misc': []
}

for i in range (8):
  crsr.execute("SELECT WORKLIST.work_ID, WORKLIST.desc, WORKLIST.year, WORKLIST.period, WORKLIST.filename FROM WORKLIST, TYPES WHERE TYPES.type_ID = WORKLIST.type AND TYPES.type_ID = (?) ORDER BY WORKLIST.year DESC", str(i+1))
  curworks = crsr.fetchall()
  if len(curworks) !=0:
    for current in curworks:
      tmpline = []
      tmpline += current
      crsr.execute ("SELECT DETAILS.detail FROM DETAILS, WORKLIST WHERE DETAILS.to_work = WORKLIST.work_ID AND WORKLIST.work_id = (?)", str(current[0]))
      curdesc = crsr.fetchall()
      if len(curdesc) !=0:
        for descitem in curdesc:
          tmpline += descitem
      works[genres[i][2]].append(tmpline)


db.close()

# templateLoader = jinja2.FileSystemLoader(searchpath='x:/Development/Portfolio/templates/')
# templateEnv = jinja2.Environment(loader=templateLoader)
# tmplt = templateEnv.get_template('index_template.html')

# with open('www/index_new.html', 'wb') as dest:
#     output = tmplt.render(
#         my_genres = genres
#     )
#     dest.write(output.encode('utf-8'))

for item in (works['pack']):
  print (item)

# print("posters -- {}".format(works['posters']))
# print("logos -- {}".format(works['logos']))
# print("advert -- {}".format(works['advert']))
# print("pack -- {}".format(works['pack']))
# print("calend -- {}".format(works['calend']))
# print("sites -- {}".format(works['sites']))
# print("photo -- {}".format(works['photo']))
# print("misc -- {}".format(works['misc']))
