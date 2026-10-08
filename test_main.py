import unittest,json
from pathlib import Path
from main import *
class Tests(unittest.TestCase):
    def sample(self):return json.loads(Path(__file__).with_name('sample-input.json').read_text(encoding='utf-8'))

    def test_units_and_dangling(self):
        o=run(self.sample());self.assertEqual(o['normalized_properties'][0]['value'],30);self.assertEqual(o['normalized_properties'][1]['value'],0.85)
        self.assertEqual({e['reason'] for e in o['errors']},{'value_out_of_range','dangling_connection'})
    def test_duplicate_semantic(self):
        d=self.sample();d['assets'][0]['properties'].append(d['assets'][0]['properties'][0].copy())
        self.assertIn('duplicate_semantic_id',[e['reason'] for e in run(d)['errors']])
    def test_missing_and_wrong_unit(self):
        d=self.sample();d['assets'][0]['properties']=[]
        self.assertIn('required_property_missing',[e['reason'] for e in run(d)['errors']])
        d=self.sample();d['assets'][0]['properties'][0]['unit']='A'
        self.assertIn('incompatible_unit',[e['reason'] for e in run(d)['errors']])
    def test_duplicate_asset_and_nan(self):
        d=self.sample();d['assets'][1]['id']='oht-1'
        with self.assertRaises(ValueError):run(d)
        d=self.sample();d['assets'][0]['properties'][0]['value']=float('nan')
        self.assertIn('nonfinite_value',[e['reason'] for e in run(d)['errors']])

if __name__=="__main__":unittest.main()
