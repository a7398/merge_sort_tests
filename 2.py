import unittest, sqlite3

def merge_sort(a):
    if len(a) < 2: return a
    m = len(a)//2
    l, r = merge_sort(a[:m]), merge_sort(a[m:])
    i = j = 0
    res = []
    while i < len(l) and j < len(r):
        if l[i] <= r[j]:
            res.append(l[i]); i += 1
        else:
            res.append(r[j]); j += 1
    return res + l[i:] + r[j:]


def db():
    c = sqlite3.connect(':memory:')
    c.executescript('''
        create table s(id integer primary key, name);
        create table c(id integer primary key, title);
        create table sc(sid int, cid int,
            foreign key(sid) references s(id),
            foreign key(cid) references c(id));
    ''')
    return c

def add_student(conn, name): conn.execute('insert into s(name) values(?)', (name,))
def add_course(conn, title): conn.execute('insert into c(title) values(?)', (title,))
def add_student_course(conn, sid, cid): conn.execute('insert into sc values(?,?)', (sid, cid))
def delete_student(conn, sid):
    conn.execute('delete from sc where sid=?', (sid,))
    conn.execute('delete from s where id=?', (sid,))


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
        sid = conn.execute('select id from s').fetchone()[0]
        cid = conn.execute('select id from c').fetchone()[0]
        add_student_course(conn, sid, cid)
        self.assertIsNotNone(conn.execute('select * from sc where sid=? and cid=?',(sid,cid)).fetchone())
        delete_student(conn, sid)
        self.assertIsNone(conn.execute('select * from s where id=?',(sid,)).fetchone())
        self.assertIsNone(conn.execute('select * from sc where sid=?',(sid,)).fetchone())

if __name__ == '__main__':
    unittest.main()
