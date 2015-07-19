#/usr/bin/env python2.7

import argparse
import csv
import sqlite3

SQLITE_INSERT_STRING = ("INSERT INTO 'results' ('semester', 'semester_num', "
    "'code', 'subject', 'mark', 'grade', 'cp') VALUES (?, ?, ?, ?, ?, ?, ?);")

DROP_OLD_TABLE = """
DROP TABLE IF EXISTS results;
"""
SQLITE_SCHEMA = """
CREATE TABLE results (semester TEXT, semester_num INTEGER, code TEXT, subject TEXT, mark REAL, grade TEXT, cp INTEGER);
"""

class Course(object):
    """
    Useful class which represents a course taken, and can be converted into an
    SQL statement
    """
    def __init__(self, semester_text, semester_num, subj_code, subj_name, grade, mark, cp):
        self.text = semester_text
        self.sem_num = int(semester_num)
        self.code = subj_code
        self.name = subj_name
        self.grade = grade
        self.mark = float(mark)
        self.cp = int(cp)

    def toSQLRow(self):
        return (SQLITE_INSERT_STRING, (self.text, self.sem_num, self.code,
            self.name, self.mark, self.grade, self.cp))

def parse_csv(path_to_csv):
    """
    Given a path to a CSV file with the expected structure, this function
    returns a list of Course objects with each course the user has taken
    """
    print "Parsing CSV file..."
    courses = []
    try:
        with open(path_to_csv, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            courses = [ Course(
                row['semester'], row['semester_num'], row['code'], row['name'],
                row['grade'], row['mark'], row['cp']
            ) for row in reader ]
    except KeyError as e:
        print "Missing required key!"
        raise
    except IOError as e:
        print "Error reading CSV file"
        raise

    return courses

def init_sqlite(path_to_sqlite, courses):
    """
    Given a path to a SQLite file, this creates the SQLite file, this
    initialises the DB with the schema from the file, and inserts each course
    into the DB
    """
    print "Creating database..."
    conn = sqlite3.connect(path_to_sqlite);
    c = conn.cursor()
    c.execute(DROP_OLD_TABLE)
    c.execute(SQLITE_SCHEMA);

    print "Loading data..."
    for course in courses:
        query, params = course.toSQLRow()
        c.execute(query, params)

    conn.commit()
    conn.close()
    print "Done. Open %s in sqlite3 to browse your data!" % path_to_sqlite



def main():
    parser = argparse.ArgumentParser(description='USyd Marks Analysis')
    parser.add_argument('-c' '--csvfile', default='results.csv',
            help='Path to the CSV file', dest='csvfile')
    parser.add_argument('-s' '--sqlite-file', default='results.sqlite',
            help='Path to output SQLite file', dest='sqlitefile')

    args = parser.parse_args()

    courses = parse_csv(args.csvfile)

    init_sqlite(args.sqlitefile, courses)


if __name__ == '__main__':
    main()
