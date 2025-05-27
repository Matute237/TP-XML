import os
import unittest
from sqlalchemy import text
from app import create_app, db
from xml.etree import ElementTree as ET

# Modelo de ejemplo
class ExampleModel(db.Model):
    __tablename__ = 'example'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    value = db.Column(db.String(50))

class XMLImportTestCase(unittest.TestCase):

    def setUp(self):
        os.environ['FLASK_CONTEXT'] = 'testing'
        os.environ['TEST_DATABASE_URI'] = 'sqlite:///:memory:'

        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()

        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_import_xml_to_db(self):
        # Simulamos un archivo XML
        xml_data = """
        <data>
            <item>
                <name>Item1</name>
                <value>Value1</value>
            </item>
            <item>
                <name>Item2</name>
                <value>Value2</value>
            </item>
        </data>
        """

        # Parseamos el XML
        root = ET.fromstring(xml_data)
        for item in root.findall('item'):
            name = item.find('name').text
            value = item.find('value').text

            # Insertamos en la base de datos
            new_entry = ExampleModel(name=name, value=value)
            db.session.add(new_entry)

        db.session.commit()

        # Verificamos que los datos se hayan insertado correctamente
        results = ExampleModel.query.all()
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].name, 'Item1')
        self.assertEqual(results[0].value, 'Value1')
        self.assertEqual(results[1].name, 'Item2')
        self.assertEqual(results[1].value, 'Value2')

if __name__ == '__main__':
    unittest.main()