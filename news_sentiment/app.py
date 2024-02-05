from flask import Flask, render_template, request, jsonify
import mysql.connector
import pandas as pd
from datetime import datetime
import subprocess
from fetch import fetching

app = Flask(__name__)

fetching()

def query_database(a, b, c):
    # Connection to  mysql 
    db = mysql.connector.connect(
        host="mysql",
        user="root",
        port="3306",
        database="news_data_db"
        
    )
    print("1")
    cursor = db.cursor()
    print("1")
    senti=','.join(['%s' for _ in c])
    query = f"SELECT * FROM news_articles WHERE publishedAt >=%s  AND publishedAt<=%s AND sentiment IN ({senti});"
    values=(a,b) + tuple(c)
    print(query)
    # sentiment_tuple = tuple(sentiments)
    print("1")
    # print("THis is sentiment " , sentiment_tuple)
    # values=(a,b) + tuple(c)
    cursor.execute(query, values)
    print("1")
    results = cursor.fetchall()
    # print(results)
    cursor.close()
    db.close()

    return results

@app.route('/' , methods = ['GET', 'POST'])
def get_page():
    return render_template('index.html')
@app.route('/getData' , methods = ['POST'])
# def getData():
#     date_from = request.form['date_from']
#     date_too = request.form['date_too']
#     sentiments = request.form['sentiment']
#     print("Date" , date_from , date_too , sentiments)
#     return request.data
@app.route('/get_news', methods=['POST', 'GET'])
def get_news():
    if request.method == 'POST':
        date_from = request.form['date_from']
        date_too = request.form['date_too']
        sentiments = request.form.getlist('sentiment')
        # sentiments="Negative"
        print(date_from, date_too)
        print(sentiments)
        # preferences = (date_from , date_too )+ tuple(sentiments)
        # print(preferences)
        # if not preferences:
        #     return jsonify({"message": "No preferences provided"}), 400
        # print("THis is type of " , type(preferences))
        # preferences = str(preferences)
        # print("THis is type of " , type(preferences))
        news_links = query_database(date_from, date_too, sentiments)
        print("news_links" ,news_links)

        return jsonify({"news_links": news_links})

@app.route('/run_fetch', methods=['GET'])
def run_fetch():
    subprocess.run(["python", "fetch.py"])

if __name__ == '__main__':
    app.run(debug=True , host="0.0.0.0", port = 8000)



