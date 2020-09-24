import sqlite3
import jinja2
from collections import namedtuple

db = sqlite3.connect("portfolio-data.db3")
crsr = db.cursor()

crsr.execute("SELECT typename, intro_text, abbrev, icon FROM TYPES")
genres_raw = crsr.fetchall()

genres = []

for genre in genres_raw:
  genres_named = namedtuple("genres_data", ["typename", "intro_text", "abbrev", "icon"])
  genres.append(genres_named(*genre)._asdict())

works = {}

for genre_item in genres:
  works[genre_item['abbrev']] = []
  crsr.execute("SELECT WORKLIST.work_ID, WORKLIST.year, WORKLIST.period, CLIENTS.client_name, WORKLIST.title, WORKLIST.desc, WORKLIST.filename FROM WORKLIST, TYPES, CLIENTS WHERE TYPES.type_ID = WORKLIST.type AND CLIENTS.client_ID = WORKLIST.client AND TYPES.abbrev = (?) AND WORKLIST.show = 1 ORDER BY WORKLIST.year DESC", (genre_item['abbrev'],))
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
      works[genre_item['abbrev']].append(tmpline)

crsr.execute("SELECT title, keywords, description, quota, quota_author, copyright, about, contacts FROM TEXTS where line_ID = 1")
line = crsr.fetchone()

texts = namedtuple("site_texts", ["title", "keywords", "description", "quota", "quota_author", "copyright", "about", "contacts"])

db.close()

templateLoader = jinja2.FileSystemLoader(searchpath='x:/Development/Portfolio/templates/')
templateEnv = jinja2.Environment(loader=templateLoader)
tmplt = templateEnv.get_template('index_template.html')

with open('www/index_new.html', 'wb') as dest:
    output = tmplt.render(
        my_genres = genres,
        my_works = works,
        my_texts = texts(*line)._asdict()
    )
    dest.write(output.encode('utf-8'))

