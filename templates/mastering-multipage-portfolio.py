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

crsr.execute("SELECT type_ID, typename, intro_text, abbrev, icon, page_keywords, page_desc FROM TYPES")
genres = data_dict(crsr.fetchall(), "genres_data", ["nr", "typename", "intro_text", "abbrev", "icon", "page_keywords", "page_desc"])

works = {}


for curr_genre in genres:
    curr_genre_abbrev = curr_genre['abbrev']
    crsr.execute("SELECT WORKLIST.work_ID, WORKLIST.year, WORKLIST.period, CLIENTS.client_name, WORKLIST.title, WORKLIST.desc, WORKLIST.filename, WORKLIST.modal_size FROM WORKLIST, TYPES, CLIENTS WHERE TYPES.type_ID = WORKLIST.type AND CLIENTS.client_ID = WORKLIST.client AND TYPES.abbrev = (?) AND WORKLIST.show = 1 ORDER BY WORKLIST.year DESC", (curr_genre_abbrev,))
    works[curr_genre_abbrev] = data_dict(crsr.fetchall(), "works_data", ["id", "year", "period", "cust", "name", "desc", "filename", "modal_size"])
    curr_genre['count'] = (len(works[curr_genre_abbrev]))

    for curr_work in works[curr_genre_abbrev]:
        crsr.execute ("SELECT DETAILS.detail FROM DETAILS, WORKLIST WHERE DETAILS.to_work = WORKLIST.work_ID AND WORKLIST.work_id = (?) ORDER BY DETAILS.detail_ID", (str(curr_work['id']),))
        curr_desc = crsr.fetchall()
        desc_list = []
        if len(curr_desc) != 0:
            for desc_item in curr_desc:
                desc_list += list(desc_item)
        curr_work ['details'] = desc_list

crsr.execute("SELECT title, keywords, description, quota, quota_author, copyright, about, contacts, error_text FROM TEXTS where line_ID = 1")
line = crsr.fetchone()
texts = namedtuple("site_texts", ["title", "keywords", "description", "quota", "quota_author", "copyright", "about", "contacts", "error_text"])

db.close()

templateLoader = jinja2.FileSystemLoader(searchpath='x:/Development/Portfolio/templates/')
templateEnv = jinja2.Environment(loader=templateLoader)
index_tmplt = templateEnv.get_template('index_multipage_template.html')
inner_tmplt = templateEnv.get_template('itempage_multipage_template.html')
modals_tmplt = templateEnv.get_template('modals_template.html')

with open('templates/modals.html', 'wb') as dest:
    output = modals_tmplt.render(
        about = texts(*line)._asdict()['about'],
        copyright = texts(*line)._asdict()['copyright'],
        path = ''
    )
    dest.write(output.encode('utf-8'))

page_roles = ['index', '400', '401', '403', '404', '405', '408', '500', '501', '502', '503', '504']

for role in page_roles:
    with open('www/' + role + '.html', 'wb') as dest:
        output = index_tmplt.render(
            my_role = role,
            my_genres = genres,
            my_texts = texts(*line)._asdict()
        )
        dest.write(output.encode('utf-8'))

with open('templates/modals.html', 'wb') as dest:
    output = modals_tmplt.render(
        about = texts(*line)._asdict()['about'],
        copyright = texts(*line)._asdict()['copyright'],
        path = '../../'
    )
    dest.write(output.encode('utf-8'))

for c_genre in genres:
    c_genre_a = c_genre['abbrev']
    with open ('www/portfolio/'+ c_genre_a +'/index.html', 'wb') as dest:
        output = inner_tmplt.render(
            my_genres = genres,
            current_genre = c_genre,
            current_genre_name = c_genre_a,
            my_works = works[c_genre_a],
            title = texts(*line)._asdict()['title']
        )
        dest.write(output.encode('utf-8'))
