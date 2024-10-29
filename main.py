from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv
import logging
import json

load_dotenv()
app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

# The search_code function interacts with the GitHub Code Search API endpoint when the user inputs their code in the user function.
def github_search(query):
    url = "https://api.github.com/search/code"
    token = os.getenv('access_token')
    logging.debug(f"Token: {token}")
    headers = {"Authorization": f"token {token}"}
    params = {
        "q":query,
        "language":"python",
        "sort":"indexed",
        "order":"desc",
        "per_page":100
    }
    response = requests.get(url, headers=headers, params=params)
    if response.ok: 
        return response.json().get("items", [])
    else: 
        return("Errors: no response.")

# The user function is the entry point of the GitHub search application. It prompts the user for their code.

@app.route('/', methods=['GET', 'POST'])
def user():
  query = request.form.get("query", "")
  results = github_search(query)
  return render_template("index.html", results=results)
if __name__ == "__main__":
    app.run(debug=True)