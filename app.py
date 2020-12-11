import datetime
import re
from flask import Flask, render_template, request, json, Response
from modules.form import  SearchForm
app = Flask(__name__)
app.config['SECRET_KEY']="123"


# 接收关键词，返回从服务器查询得到的JSON数据
def search_from_server(keywords):
    # 从服务器查询
    # 接上es
    # 把kw的查询传到es
    # 得到es的结果:总共结果数， positive/negative， positive/negative:{datetime(yyyy-mm): num},
    # json(前20个结果)[text, pos/neg, create_at, screen_name]
    file = 'aaa.json'
    with open(file, encoding='utf-8') as f:
        data = json.load(f)
    results = data['hits']['hits']
    # print(data)
    # results = [{keywords: 'result of search ' + keywords}]
    return results


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/getSearch', methods=['GET', 'POST'])
def getSearch():
    form = SearchForm()
    search = request.args.get('query', '')
    # print(search)
    if search == "":
        # 显示提示框
        return render_template("index.html")
    else:
        results = search_from_server(search)
        # 计算以datetime聚合的positive/negative
        # correspond = search_correspond
        total = 1000
        positive = 500
        negative = 500

        return render_template("results.html", form=form, search=search, results=results)


@app.route('/getSearch_results', methods=['GET', 'POST'])
def getSearch_results():
    form = SearchForm()
    search = request.args.get('query', '')
    print('input: ', search)
    if search == "":
        # 显示提示框
        return render_template("results.html")
    else:
        results = search_from_server(search)
        # 计算以datetime聚合的positive/negative
        # correspond = search_correspond

        return render_template("results.html", form=form, search=search, results=results)


if __name__ == '__main__':
    # app.run()
    #----------------------------------------------------
    # search_from_server测试
    results = search_from_server('')
    #----------------------------------------------------