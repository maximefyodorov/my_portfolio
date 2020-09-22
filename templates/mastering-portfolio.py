import sqlite3
import jinja2

db = sqlite3.connect("portfolio-data.db3")

crsr = db.cursor()

crsr.execute("SELECT typename, intro_text, abbrev, icon FROM TYPES")
genres = crsr.fetchall()

works = {}

for i in range (8):
  works[genres[i][2]] = []
  crsr.execute("SELECT WORKLIST.work_ID, WORKLIST.year, WORKLIST.period, CLIENTS.client_name, WORKLIST.title, WORKLIST.desc, WORKLIST.filename FROM WORKLIST, TYPES, CLIENTS WHERE TYPES.type_ID = WORKLIST.type AND CLIENTS.client_ID = WORKLIST.client AND TYPES.type_ID = (?) AND WORKLIST.show = 1 ORDER BY WORKLIST.year DESC", str(i+1))
  curworks = crsr.fetchall()
  if len(curworks) !=0:
    for current in curworks:
      tmpline = []
      tmpline += current
      crsr.execute ("SELECT DETAILS.detail FROM DETAILS, WORKLIST WHERE DETAILS.to_work = WORKLIST.work_ID AND WORKLIST.work_id = (?) ORDER BY DETAILS.detail_ID", str(current[0]))
      curdesc = crsr.fetchall()
      if len(curdesc) !=0:
        for descitem in curdesc:
          tmpline += descitem
      works[genres[i][2]].append(tmpline)

db.close()

templateLoader = jinja2.FileSystemLoader(searchpath='x:/Development/Portfolio/templates/')
templateEnv = jinja2.Environment(loader=templateLoader)
tmplt = templateEnv.get_template('index_template.html')

with open('www/index_new.html', 'wb') as dest:
    output = tmplt.render(
        my_genres = genres,
        my_works = works
    )
    dest.write(output.encode('utf-8'))

