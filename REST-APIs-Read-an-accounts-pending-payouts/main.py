'''
Hello World! by Polkadot!
[ADVANCED CHALLENGE] REST APIs - Read An Account's Pending Payouts
Gitcoin: https://gitcoin.co/issue/Polkadot-Network/hello-world-by-polkadot/5/100023931

usage: main.py [-h] [-d DEPTH] [-e ERA] [-a] [-s SIDECAR_URL] account

positional arguments:
  account

optional arguments:
  -h, --help            show this help message and exit
  -d DEPTH, --depth DEPTH
  -e ERA, --era ERA
  -a, --all
  -s SIDECAR_URL, --sidecar-url SIDECAR_URL
'''

import argparse
import sys

import requests


DEFAULT_SIDECAR_URL = 'http://127.0.0.1:8080'
DEFAULT_DEPTH = 5
DEFAULT_ERA = -1
DEFAULT_ALL = False
COIN_DECIMAL = 12


def get_stacking_payout(args):
    url = f'{args.sidecar_url}/accounts/{args.account}/staking-payouts?'
    params = dict(depth=args.depth, unclaimedOnly=str(not args.all).lower())

    if args.era != -1:
        params['era'] = args.era

    resp = requests.get(url, params=params)

    if resp.status_code != 200:
        print(resp.json())
        sys.exit(resp.status_code)
    
    return resp.json()['erasPayouts']


def calculate_payouts(data):
    total = 0
    for era in data:
        for payout in era['payouts']:
            total += int(payout['nominatorStakingPayout'])
    
    total = total / 10 ** COIN_DECIMAL
    return total
            

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get Pending Payouts')
    parser.add_argument('account', type=str)
    parser.add_argument('-d', '--depth', type=int, default=DEFAULT_DEPTH)
    parser.add_argument('-e', '--era', type=int, default=DEFAULT_ERA)
    parser.add_argument('-a', '--all', action='store_true', default=DEFAULT_ALL)
    parser.add_argument('-s', '--sidecar-url', type=str, default=DEFAULT_SIDECAR_URL)

    args = parser.parse_args()

    print(f'Getting account info: {args.account}...')
    data = get_stacking_payout(args)
    total_payouts = calculate_payouts(data)
    print(f'Pending Payouts: {total_payouts}')
