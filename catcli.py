import argparse
import requests

my_api_url = "http://localhost:5000"


def query_all(my_api_url):

    api_output = requests.get(my_api_url)

    return api_output.json()


# Needs DB Conn for query + delete

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--all", help="Show All facts", action='store_true')
    parser.add_argument("--query", help="Query For a Fact")
    parser.add_argument("--delete", help="Delete a Fact")

    args = parser.parse_args()

    if args.all:
        print(query_all(my_api_url))
    elif args.query:
        print("query")
    elif args.delete:
        print("delete")