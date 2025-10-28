import unittest
import sqlite3

def merge_sort(arr):
    if len(arr) < 2:
        return arr
    mid = len(arr)//2
    left, right = merge_sort(arr[:mid]), merge_sort(arr[mid:])
    i = j = 0
    res = []
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            res.append(left[i]); i += 1
        else:
            res.append(right[j]); j += 1
    res.extend(left[i:])
    res.extend(right[j:])
    return res

def db():
    conn = sqlite3.connect(':memory:')
    conn.executescript('''
        CREATE TABLE s(id INTEGER PRIMARY KEY, name);
        CREATE TABLE c(id INTEGER PRIMARY KEY, title);
        CREATE TABLE sc(sid INTEGER, cid INTEGER,
            FOREIGN KEY(sid) REFERENCES s(id),
            FOREIGN KEY(cid) REFERENCES c(id));
    ''')
    return conn

def add_student(conn, name): conn.execute('INSERT INTO s(name) VALUES(?)', (name,))
def add_course(conn, title): conn.execute('INSERT INTO c(title) VALUES(?)', (title,))
def add_student_course(conn, sid, cid): conn.execute('INSERT INTO sc(sid, cid) VALUES(?,?)', (sid, cid))
def delete_student(conn, sid):
    conn.execute('DELETE FROM sc WHERE sid=?', (sid,))
    conn.execute('DELETE FROM s WHERE id=?', (sid,))

class TestAll(unittest.TestCase):
    def test_merge_sort(self):
        self.assertEqual(merge_sort([4,2,5,1,3]), [1,2,3,4,5])
        self.assertEqual(merge_sort([]), [])
        self.assertEqual(merge_sort([3]), [3])
        self.assertEqual(merge_sort([2,2,1]), [1,2,2])

    def test_student_course(self):
        conn = db()
        add_student(conn, "Анна")
        add_course(conn, "Python")
        sid = conn.execute('SELECT id FROM s').fetchone()[0]
        cid = conn.execute('SELECT id FROM c').fetchone()[0]
        add_student_course(conn, sid, cid)
        self.assertIsNotNone(conn.execute(
            'SELECT * FROM sc WHERE sid=? AND cid=?', (sid, cid)
        ).fetchone())
        delete_student(conn, sid)
        self.assertIsNone(conn.execute('SELECT * FROM s WHERE id=?', (sid,)).fetchone())
        self.assertIsNone(conn.execute('SELECT * FROM sc WHERE sid=?', (sid,)).fetchone())

if __name__ == '__main__':
    unittest.main()
