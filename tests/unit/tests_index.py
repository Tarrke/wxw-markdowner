""" Unit tests for wxw_markdowner module """

import unittest

from src.wxw_markdowner import WXWMarkdowner

class IndexTests(unittest.TestCase):
    """ Tests for the index thingy. """
    def setUp(self):
        self.filename = "test"
        self.title = "Dummy Storie"
        self.author = "Me"

    def test_generate_filenames(self):
        """ test generate filename """
        my_markdowner = WXWMarkdowner(self.filename, self.title,
                                      "https://www.wuxiaworld.com/novel/martial-world", self.author)
        my_markdowner.generate_filenames()


    def test_index_dl(self):
        """ test index download """
        my_markdowner = WXWMarkdowner(self.filename, self.title,
                                      "https://www.wuxiaworld.com/novel/martial-world", self.author)
        my_markdowner.generate_filenames()
        my_markdowner.generate_metadata()
        my_markdowner.download_index(["Chapter", "MW", "Afterword"], ["Chapters"])
        self.assertEqual(my_markdowner.chaps[-1],
                         (2277, 'http://wuxiaworld.com/novel/martial-world/mw-chapter-2256',
                          'Afterword'), "Comment")

    def test_chapter_generation(self):
        """ test chapter generation """
        my_markdowner = WXWMarkdowner(self.filename, self.title,
                                      "https://www.wuxiaworld.com/novel/martial-world", self.author)
        my_markdowner.get_chapter_from_index("./tests/unit/test_index.html",
                                             starts=["Chapter", "MW", "Afterword"],
                                             nostarts=["Chapters"])
        # print(my_markdowner.chaps[-1])
        self.assertEqual(my_markdowner.chaps[-1],
                         (738, 'http://wuxiaworld.com/novel/martial-world/mw-chapter-2256',
                          'Afterword'), "Comment")

if __name__ == '__main__':
    unittest.main()
