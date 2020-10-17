import unittest
from scripts import captura_con_filtros as captura


class MyTestCase(unittest.TestCase):
    #prueba unitaria valida la url de Mongo
    def test_hostMongo(self):
        self.assertEqual(captura.MONGO_HOST, 'mongodb://localhost/twitterdb')

if __name__ == '__main__':
    unittest.main()

