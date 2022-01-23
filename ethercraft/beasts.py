from ethercraft.scraping import Extractor

class Bestiary():

    def __init__(self, extractor):
        self.beasts = []
        self.populated = False
        self.extractor = extractor

    def load_from_extractor(self):
        try:
            self.beasts = self.extractor.load_db_from_js('bestiaryDB.js')

            self.populated = True
        except Exception as err:
            print(f"error while populating item database:\n{str(err)}")

        return self.populated


if __name__ == '__main__':
    extractor = Extractor('https://ethercraft.io/kovan_v46/')

    beasts = Bestiary()
    beasts.load_from_extractor(extractor)

    print(beasts.beasts)