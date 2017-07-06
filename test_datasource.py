import json
import unittest

from app import create_app, db


class DatasourceTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.datasource = \
            {
                'name': 'conn1',
                'driver': 'mysql',
                'host': 'localhost',
                'port': 3306,
                'db': 'demo'
            }

        with self.app.app_context():
            db.create_all()

    def test_datasource_creation(self):
        res = self.client().post('/datasources/', data=self.datasource)
        self.assertEqual(res.status_code, 201)
        self.assertIn('jdbc:mysql//localhost:3306/demo', str(res.data))

    def test_api_can_get_all_datasources(self):
        res = self.client().post('/datasources/', data=self.datasource)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/datasources/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('jdbc:mysql//localhost:3306/demo', str(res.data))

    def test_api_can_get_datasource_by_id(self):
        rv = self.client().post('/datasources/', data=self.datasource)
        self.assertEqual(rv.status_code, 201)
        result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
        result = self.client().get(
            '/datasources/{}'.format(result_in_json['id']))
        self.assertEqual(result.status_code, 200)
        self.assertIn('jdbc:mysql//localhost:3306/demo', str(result.data))

    def test_datasource_can_be_edited(self):
        rv = self.client().post(
            '/datasources/',
            data=\
                {
                    'name': 'conn2',
                    'driver': 'mssql',
                    'host': 'msr-prod-db01',
                    'port': 1433,
                    'db': 'dqf'
                })
        self.assertEqual(rv.status_code, 201)
        rv = self.client().put(
            '/datasources/1',
            data={
                "name": "Dairy Queen Framework"
            })
        self.assertEqual(rv.status_code, 200)
        results = self.client().get('/datasources/1')
        self.assertIn('Dairy Queen', str(results.data))

    def test_datasource_deletion(self):
        rv = self.client().post(
            '/datasources/',
            data= \
                {
                    'name': 'conn3',
                    'driver': '',
                    'host': '',
                    'port': 0,
                    'db': ''
                })
        self.assertEqual(rv.status_code, 201)
        res = self.client().delete('/datasources/1')
        self.assertEqual(res.status_code, 200)
        result = self.client().get('/datasources/1')
        self.assertEqual(result.status_code, 404)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == "__main__":
    unittest.main()

