import sqlite3
import jinja2
from collections import namedtuple

def data_dict(input, name, list):
    result = []
    for item in input:
        current = namedtuple(name, list)
        result.append(current(*item)._asdict())
    return result

db = sqlite3.connect("portfolio-data.db3")
crsr = db.cursor()

crsr.execute("SELECT type_ID, typename, intro_text, abbrev, icon FROM TYPES")
genres = data_dict(crsr.fetchall(), "genres_data", ["nr", "typename", "intro_text", "abbrev", "icon"])

works = {}

for curr_genre in genres:
    curr_genre_abbrev = curr_genre['abbrev']
    crsr.execute("SELECT WORKLIST.work_ID, WORKLIST.year, WORKLIST.period, CLIENTS.client_name, WORKLIST.title, WORKLIST.desc, WORKLIST.filename, WORKLIST.modal_size FROM WORKLIST, TYPES, CLIENTS WHERE TYPES.type_ID = WORKLIST.type AND CLIENTS.client_ID = WORKLIST.client AND TYPES.abbrev = (?) AND WORKLIST.show = 1 ORDER BY WORKLIST.year DESC", (curr_genre_abbrev,))
    works[curr_genre_abbrev] = data_dict(crsr.fetchall(), "works_data", ["id", "year", "period", "cust", "name", "desc", "filename", "modal_size"])

    for curr_work in works[curr_genre_abbrev]:
        crsr.execute ("SELECT DETAILS.detail FROM DETAILS, WORKLIST WHERE DETAILS.to_work = WORKLIST.work_ID AND WORKLIST.work_id = (?) ORDER BY DETAILS.detail_ID", (str(curr_work['id']),))
        curr_desc = crsr.fetchall()
        desc_list = []
        if len(curr_desc) != 0:
            for desc_item in curr_desc:
                desc_list += list(desc_item)
        curr_work ['details'] = desc_list

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

