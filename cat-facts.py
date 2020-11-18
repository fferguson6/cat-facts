import requests
import json
import sqlite3
import pprint
from flask import Flask, jsonify


app = Flask(__name__)
app.config["DEBUG"] = True


cat_facts_api = "https://cat-fact.herokuapp.com/facts"
alphabet = "abcdefghijklmnopqrstuvwxyz"
create_sql = "CREATE TABLE IF NOT EXISTS catfacts (id varchar(3), data json)"



def init_sqlite(db_file, create_sql):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute(create_sql)
    return {"conn": conn, "cursor": cursor}


def get_all_cat_facts(api_url):
    cat_facts_raw = requests.get(api_url)
    cat_facts = cat_facts_raw.json()["all"]

    return cat_facts


def filter_cat_facts(cat_facts_raw, matching_chars):
    filtered_facts = []

    [
        filtered_facts.append(fact) for fact in cat_facts_raw 
        if "user" in fact.keys() 
        and fact["user"]["name"]["first"][0].lower() in matching_chars
    ]

    return filtered_facts

def load_db(conn, cursor, data, matching_chars):
    for fact in data:
        cursor.execute("insert into catfacts values (?, ?)", [fact['_id'], json.dumps(fact)])
    
    conn.commit()
    conn.close()



@app.route('/', methods=['GET'])
def main():
    alpha_slice = list(alphabet[::2])

    conn = init_sqlite("cat-facts.db", create_sql)

    cat_facts = get_all_cat_facts(cat_facts_api)

    valid_cat_facts = filter_cat_facts(cat_facts, alpha_slice)

    load_db(conn["conn"], conn["cursor"], valid_cat_facts ,alpha_slice)


    return jsonify(valid_cat_facts)



if __name__ == "__main__":
    app.run()
