import datetime
import re
from flask import Flask, render_template, request, json, Response
from modules.form import  SearchForm
app = Flask(__name__)
app.config['SECRET_KEY']="123"


# 接收关键词，返回从服务器查询得到的JSON数据
def search_from_server(keywords):
    # 从服务器查询
    results = [{keywords: 'result of search ' + keywords}]
    return results


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/getSearch', methods=['GET', 'POST'])
def getSearch():
    form = SearchForm()
    search = request.args.get('query', '')

    if search=="":
        # 显示提示框
        return render_template("index.html")
    else:
        results = search_from_server(search)
        print(results)
        return render_template("result.html", results=results)


if __name__ == '__main__':
    app.run(port=8080)
