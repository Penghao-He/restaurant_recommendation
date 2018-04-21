import app
import unittest
import sqlite3 as sqlite

class testDataRetrival(unittest.TestCase):

    def testMake_new_search(self):
        name_list = app.main.make_new_search('Chinese', 'Ann Arbor')
        conn = sqlite.connect('final_project.sqlite')
        cur = conn.cursor()
        self.assertEqual(type(name_list), list)
        cur.execute('SELECT * FROM Google WHERE Type = "{}" AND City = "{}"'.format('Chinese', 'Ann Arbor'))
        a = cur.fetchone()
        with self.assertRaises(IndexError):
            a[8]
        self.assertTrue(type(a) != None)
        self.assertTrue(type(a) == tuple)
        cur.execute('SELECT * FROM Yelp WHERE Type = "{}" AND City = "{}"'.format('Chinese', 'Ann Arbor'))
        b = cur.fetchone()
        with self.assertRaises(IndexError):
            b[8]
        self.assertTrue(type(b) != None)
        self.assertTrue(type(b) == tuple)
        cur.execute('SELECT Zomato.Name FROM Zomato lEFT OUTER JOIN Google ON Zomato.Name = Google.Name LEFT OUTER JOIN Yelp ON Zomato.Name = Yelp.Name WHERE Google.Type = "{}" AND Google.City = "{}" OR Yelp.Type = "{}" AND Yelp.City = "{}"'.format('Chinese', 'Ann Arbor', 'Chinese', 'Ann Arbor'))
        c = cur.fetchone()
        self.assertTrue(type(c) != None)
        self.assertTrue(type(c) == tuple)

class testDataStorage(unittest.TestCase):

    def testGoogle(self):
        conn = sqlite.connect('final_project.sqlite')
        cur = conn.cursor()
        cur.execute('SELECT * FROM Google')
        a = cur.fetchone()
        self.assertTrue(type(a[0]) == int)
        self.assertTrue(type(a[1]) == str)
        self.assertTrue(type(a[2]) == str)
        self.assertTrue(type(a[3]) == str)
        self.assertTrue(type(a[4]) == float)
        self.assertTrue(type(a[5]) == str)
        self.assertTrue(type(a[6]) == str)
        self.assertTrue(type(a[7]) == int)

    def testYelp(self):
        conn = sqlite.connect('final_project.sqlite')
        cur = conn.cursor()
        cur.execute('SELECT * FROM Yelp')
        a = cur.fetchone()
        self.assertTrue(type(a[0]) == int)
        self.assertTrue(type(a[1]) == str)
        self.assertTrue(type(a[2]) == str)
        self.assertTrue(type(a[3]) == str)
        self.assertTrue(type(a[4]) == float)
        self.assertTrue(type(a[5]) == str)
        self.assertTrue(type(a[6]) == str)
        self.assertTrue(type(a[7]) == int)

    def testZomato(self):
        conn = sqlite.connect('final_project.sqlite')
        cur = conn.cursor()
        cur.execute('SELECT * FROM Zomato')
        a = cur.fetchone()
        self.assertTrue(type(a[0]) == int)
        self.assertTrue(type(a[1]) == str)
        self.assertTrue(type(a[2]) == str)
        self.assertTrue(type(a[3]) == str)
        self.assertTrue(type(a[4]) == str)

    def testMain(self):
        conn = sqlite.connect('final_project.sqlite')
        cur = conn.cursor()
        cur.execute('SELECT * FROM Main')
        a = cur.fetchone()
        self.assertTrue(type(a[0]) == int)
        self.assertTrue(type(a[1]) == str)
        self.assertTrue(type(a[2]) == int)
        self.assertTrue(type(a[3]) == int or a[3] == None)
        self.assertTrue(type(a[4]) == int or a[4] == None)

class testDataProcessing(unittest.TestCase):

    def testMakeTitle(self):
        a = app.main.make_title("Chinese", "Ann Arbor")
        self.assertEqual(type(a), str)

    def testCreateObject(self):
        obj_list = app.main.create_obj("Chinese", "Ann Arbor")
        self.assertEqual(type(obj_list[0]), app.main.Rest)
        self.assertTrue(len(obj_list) != 0)

if __name__ == "__main__":
    unittest.main()