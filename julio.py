import pymongo
import argparse
import drought_factor
import season_factor
import json

from datetime import datetime


ALLOWED_POLICIES = [
    'tolerance_raise',
    'tolerance_ignore'
]


GENERAL = (17.6653, 1.1692, -0.4387, 0.3473, 18.6882, -0.2664)
ZONE1 = (39.9622, 0.6125, -0.7252, 0.7459, 25.7198, 0)

METHOD_MAP = {
    'general': GENERAL,
    'zone1': ZONE1
}


def clamp(x, m, M):
    if x < m:
        return m
    elif x > M:
        return M
    else:
        return x


def calculate(x1, x2, x3, x4, x5, i, x1f, x2f, x3f, x4f, x5f):
    return i+x1f*x1+x2f*x2+x3f*x3+x4f*x4+x5f*x5


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mongo', default='localhost',
                        help='mongo DB connection string, default: localhost')
    parser.add_argument('-d', '--db', default='dmc',
                        help='mongo DB database name, default: dmc')
    parser.add_argument('-c', '--coll', default='data',
                        help='mongo DB database collection, default: data')
    parser.add_argument('--phony', action='store_true',
                        help='Use all data, even if it has completed fields, default: False')
    parser.add_argument('-t', '--tolerance', type=int,
                        default=20, help='delta tolerance from julio result, default: 20')
    parser.add_argument('-p', '--policies', default='tolerance_raise',
                        help='program policies, defaults: tolerance_raise;')
    parser.add_argument('--verbose', action='store_true',
                        help='display warnings')
    parser.add_argument('-o', '--output', default='',
                        help='[database:]collection|file.json to write output inside mongo DB, if database is not specified, --db is used; if this argument is not passed, no output is generated')
    parser.add_argument('--variant', choices=['general', 'zone1'],
                        default='general', help="julio's index variant, default: general")

    args = parser.parse_args()

    args.mongo = 'mongodb://{uri}'.format(
        uri=args.mongo.replace('mongodb://', ''))

    o = args.output.split(':')
    if len(o) > 2:
        print('ERROR: expected output format is [database:]collection')
    try:
        output_db, output_collection = o
    except ValueError:
        output_db = args.db
        output_collection = o[0]

    policies = args.policies.split(',')
    tolerance_policy_ignore = 'tolerance_ignore' in policies

    cl = pymongo.MongoClient(args.mongo)

    last_rain_day = datetime(2013, 1, 1)
    drought = drought_factor.MIN

    m = None
    M = None

    g = 0
    l = 0

    i = 0
    ds = 0

    ok = 0

    mongo_data = []

    for doc in cl[args.db][args.coll].find({}):
        if not args.phony and\
                (doc['tmp_ts'] != doc['ts'] or
                 doc['hum_ts'] != doc['ts'] or
                 doc['wnd_ts'] != doc['ts'] or
                 # if precipitation information is older than one day, discard
                 abs((doc['prc_ts']-doc['ts']).days) > 1):
            if args.verbose:
                print(
                    'WRN: Ignoring document with missing data @ {ts}'.format(ts=doc['ts']))
            i += 1
            continue

        days = (doc['prc_ts']-last_rain_day).days

        if doc['prc'] == 0:
            drought = drought_factor.calculate(drought, days)
        elif drought == drought_factor.MIN:
            drought = doc['prc']
        else:
            drought = doc['prc'] + drought_factor.calculate(drought, days)

        try:
            season = season_factor.calculate(1, doc['ts'])
            season_default = False
        except ValueError:
            ds += 1
            if args.verbose:
                print('WRN: Next value is issued with default season factor')
            season = 1
            season_default = True

        julio = calculate(doc['tmp'], doc['hum'], doc['wnd'],
                          season, drought, *METHOD_MAP[args.variant])

        upper_diff = 100-julio
        if upper_diff < 0 and -upper_diff > args.tolerance:
            if not tolerance_policy_ignore:
                print(
                    'ERROR: Got value greater than 100+{tol} ({val})'.format(tol=args.tolerance, val=julio))
                return
        if julio < 0 and -julio > args.tolerance:
            if not tolerance_policy_ignore:
                print(
                    'ERROR: Got value lesser than 100-{tol} ({val})'.format(tol=args.tolerance, val=julio))
                return

        ok += 1

        if m == None or julio < m:
            m = julio
        if M == None or julio > M:
            M = julio

        delta = 0

        if julio > 100:
            delta = -upper_diff
            g += 1
        if julio < 0:
            delta = julio
            l += 1

        if output_collection != '':
            mongo_data.append({
                'ts': doc['ts'],
                'julio': clamp(julio, 0, 100),
                'tmp': doc['tmp'],
                'hum': doc['hum'],
                'wnd': doc['wnd'],
                'season': season,
                'seasonDefault': season_default,
                'drought': drought,
                'delta': delta
            })

        if doc['prc'] > 0:
            last_rain_day = doc['prc_ts']

    if output_collection != '':
        if output_collection.endswith('.json'):
            with open(output_collection, 'w') as f:
                json.dump(mongo_data, f, default=lambda x: str(x))
        else:
            cl[output_db][output_collection].insert_many(mongo_data)
    elif args.verbose:
        print('WRN: no output specified')

    print('Max julio : {f}'.format(f=M))
    print('Min julio : {f}'.format(f=m))
    print()
    print('Less than 0 count    : {c}'.format(c=l))
    print('Greater than 0 count : {c}'.format(c=g))
    print()
    print('Ignored document count      : {c}'.format(c=i))
    print('Default season factor count : {c}'.format(c=ds))
    print()
    print('OK count : {c}'.format(c=ok))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()
