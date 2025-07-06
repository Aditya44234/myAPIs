from email import message
import errno
import json
from math import degrees, e
from flask import Flask,request,jsonify

import random

from werkzeug.exceptions import RequestURITooLarge 

app=Flask(__name__)

@app.route("/")
def home():
    return "Hello Boss"

@app.route("/echo")
def echo():
    mssg=request.args.get("mssg")

    return jsonify({
        "mssg":f"Your message {mssg}"
    })


@app.route("/add")
def add():
    data=request.json

    if not data:
        return jsonify({
            "error":"No data"
        })
    else:
        a=data.get('a')
        b=data.get('b')

        return jsonify({
            "Addition":add()
        })
        




@app.route("/login")
def login():
    data=request.json
    if not data:
        return jsonify({
            "error":"No data provided"
        })



    username=data.get('username')
    password=data.get('password')

    if username=="admin" and password=="secret":
        return jsonify({
            "Mssg":"Login Successfull"
        })
    
    return jsonify({
        "mssg":"Invalid credentials"
    })

#   Random Quote API

QUOTE=[
    "Be yourself",
    "If PLAN is not working , change the PLAN never the GOAL",
    "You don't need TIME, you need FOCUS",
    "Give RESPECT take RESPECT",
    "Don't let your comfort destroy your carrier"
]

@app.route("/quote")
def quote():
    return jsonify(random.choice(QUOTE))

#  Add a new QUOTE
@app.route("/quote")
def add_quote():
    data=request.json
    quote=data.get('quote') if data else None
    if quote:
        QUOTE.append(quote)
        return jsonify(message="Quote added")

    return jsonify(error="No Quote Added")


dicts={
    'api':'Application programming Interface',
    'ram':'Random Access Memory',
    'html':'HyperText Markup Language',
    'css':'Casceding Style Sheet'
}
@app.route("/define",methods=['GET'])
def define():
    word=request.args.get('word', '').lower()
    meaning=dicts.get(word)

    if meaning:
        return meaning
    return jsonify(error="No Such Word")

# Number of routes

@app.route("/routes")
def routes():
    """List all available routes"""

    output=[]

    for rule in app.url_map.iter_rules():
        output.append(str(rule))
    return jsonify(Routes=output)
















if __name__=="__main__":
    app.run(debug=True)
