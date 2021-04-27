from typing import List
import yaml

class DAO:

    def __init__(self) -> None:
        pass

    def get_parameters(self, popid, component_number) -> List:
        query = 'SELECT'
        return []

    def get_fake_parameters(self, popid) -> List:
        with open('data/mock_request.yml') as f:
            r = yaml.safe_load(f)['data']        
        params = list(filter(lambda x: x['popid'] == popid, r))[0]
        return params['components']

    def get_parameters_full(self, popid):
        pass

    def save_results(self):
        query = 'INSERT INTO'
        pass


if __name__ == '__main__':
    d = DAO()
    p = d.get_fake_parameters('111111')
    print(p['components'])