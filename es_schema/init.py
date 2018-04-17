import argparse
from elasticsearch import Elasticsearch as ES

def main():
    argparser = argparse.ArgumentParser()
    group = argparser.add_mutually_exclusive_group(required=True)
    group.add_argument('-d', '--development', action='store_true')
    args = argparser.parse_args()

    if args.development:
        es = ES([{'host': '127.0.0.1', 'port': '9200'}])
        es.indices.create(index='ithome')

if __name__ == '__main__':
    main()
