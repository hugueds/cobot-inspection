from typing import List
import yaml

WORKPLACE_ID = ''       # Not defined yet
CIMI_CONTRACT_ID = ''   # Not defined yet

class DAO:

    def __init__(self) -> None:
        pass

    def get_parameters(self, popid) -> list:
        query = f'SELECT FROM WHERE POPID = {popid} and W.ID = {WORKPLACE_ID}'
        return []

    def get_fake_parameters(self, popid) -> list:
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
    p = d.get_fake_parameters('999999')
    print(p)