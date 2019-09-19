import unittest

from src.wxwMarkdowner import WXWMarkdowner

class indexTests(unittest.TestCase):
    def setUp(self):
        self.filename = "test"
        self.title = "Dummy Storie"
        self.author = "Me"

    def test_generate_filenames(self):
        myMarkdowner = WXWMarkdowner(self.filename, self.title, "https://www.wuxiaworld.com/novel/martial-world", self.author)
        myMarkdowner.generate_filenames()


    def test_index_dl(self):
        myMarkdowner = WXWMarkdowner(self.filename, self.title, "https://www.wuxiaworld.com/novel/martial-world", self.author)
        myMarkdowner.generate_filenames()
        myMarkdowner.generate_metadata()
        myMarkdowner.download_index(["Chapter", "MW", "Afterword"], ["Chapters"])
        self.assertEqual(myMarkdowner.chaps[-1], (2277, 'http://wuxiaworld.com/novel/martial-world/mw-chapter-2256', 'Afterword'), "Comment")

    def test_chapter_generation(self):
        myMarkdowner = WXWMarkdowner(self.filename, self.title, "https://www.wuxiaworld.com/novel/martial-world", self.author)
        myMarkdowner.get_chapter_from_index("./tests/unit/test_index.html", starts = ["Chapter", "MW", "Afterword"], nostarts = ["Chapters"])
        # print(myMarkdowner.chaps[-1])
        self.assertEqual(myMarkdowner.chaps[-1], (738, 'http://wuxiaworld.com/novel/martial-world/mw-chapter-2256', 'Afterword'), "Comment")

if __name__ == '__main__':
    unittest.main()