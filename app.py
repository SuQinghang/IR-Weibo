import datetime
import copy
from flask import Flask, render_template, request, json, Response
from modules.form import  SearchForm
from elasticsearch import Elasticsearch
app = Flask(__name__)
app.config['SECRET_KEY']="123"

#elasticsearch集群服务器地址
ES = [
    '10.10.110.117:9200'
]
#创建elasticsearch客户端
es = Elasticsearch(
    ES,
    sniff_on_start = True,
    sniff_on_connection_fail = True,
    sniffer_timeout = 60
)
# 接收关键词，返回从服务器查询得到的JSON数据
from elasticsearch import Elasticsearch

# elasticsearch集群服务器地址
ES = [
    '10.10.110.117:9200'
]
# 创建elasticsearch客户端
es = Elasticsearch(
    ES,
    sniff_on_start=True,
    sniff_on_connection_fail=True,
    sniffer_timeout=60
)


def fun(x):
    return datetime.date(*([int(i) for i in x.split('-')]), day=1)


# 接收关键词，返回从服务器查询得到的JSON数据
def search_from_server(keywords):
    # 从服务器查询
    # 接上es
    # 把kw的查询传到es
    # 得到es的结果:总共结果数， positive/negative， positive/negative:{datetime(yyyy-mm): num},
    # json(前20个结果)[text, pos/neg, create_at, screen_name]

    # 返回前50个文档信息；与关键字相关的标签聚合
    body1 = {
        'size': 10000,
        'query': {
            'match': {
                'text': keywords
            }
        },
        "aggs": {
            "all_sentiment": {
                "terms": {
                    "field": "sentiment"

                }
            }
        }
    }
    data = es.search(index='weiboooo', doc_type='docccc', body=body1)
    #todo 记录data1中的总数以及聚合datetime
    # 获得num_total, num_positive and num_negative
    num_negative = data['aggregations']['all_sentiment']['buckets'][0]['doc_count']
    num_positive = data['aggregations']['all_sentiment']['buckets'][1]['doc_count']
    num_total = num_negative + num_positive

    items = copy.copy(data['hits']['hits'])
    num_datetime = {}
    # 处理data1
    for item in items:
        date = item['_source']['created_at']
        date_time = datetime.datetime.strptime(date, '%Y/%m/%d %H:%M:%S')
        date_str = str(date_time.year)+'-'+str(date_time.month)
        if date_str not in num_datetime.keys():
            num_datetime[date_str] = [0, 0]
        if item['_source']['sentiment']==1:
            item['_source']['sentiment'] = 'Positive'
            num_datetime[date_str][1]+=1
        else:
            item['_source']['sentiment'] = 'Negative'
            num_datetime[date_str][0]+=1
        item['_source']['created_at'] = date_str

    datetime_sorted = sorted(num_datetime, key=fun)
    positive_datetime_sorted = []
    negative_datetime_sorted = []
    for i in sorted(datetime_sorted, key=fun):
        positive_datetime_sorted.append(num_datetime[i][1])
        negative_datetime_sorted.append(num_datetime[i][0])



    return items[:50], num_total, num_negative, num_positive, \
                        (datetime_sorted, negative_datetime_sorted, positive_datetime_sorted)
'''
def search_from_server(keywords):
    # 从服务器查询
    # 接上es
    # 把kw的查询传到es
    # 得到es的结果:总共结果数， positive/negative， positive/negative:{datetime(yyyy-mm): num},
    # json(前20个结果)[text, pos/neg, create_at, screen_name]
    #--------------------------------------------------
   file = 'aaa.json'
    with open(file, encoding='utf-8') as f:
        data = json.load(f)
    results = data['hits']['hits']
    # print(data)
    # results = [{keywords: 'result of search ' + keywords}]
    for result in results:
        date = result['_source']['created_at']
        date_time = datetime.datetime.strptime(date, '%Y/%m/%d %H:%M:%S')
        date_str = str(date_time.year)+'/'+str(date_time.month)
        if result['_source']['sentiment']==1:
            result['_source']['sentiment']='Positive'
        else:
            result['_source']['sentiment'] = 'Negative'
        result['_source']['created_at'] = date_str
    return results
'''



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
        items, num_total, num_negative, num_positive, num_datetime_sorted = search_from_server(search)

        return render_template("results.html", form=form, search=search,
                            results=items, num_total=num_total, num_negative=num_negative, num_positive=num_positive,
                               num_datetime_sorted=num_datetime_sorted)


@app.route('/getSearch_results', methods=['GET', 'POST'])
def getSearch_results():
    form = SearchForm()
    search = request.args.get('query', '')
    if search == "":
        # 显示提示框
        return render_template("results.html")
    else:
        items, num_total, num_negative, num_positive, num_datetime_sorted = search_from_server(search)
        print('positve', num_datetime_sorted[2])
        print('negative', num_datetime_sorted[1])
        return render_template("results.html", form=form, search=search,
                            results=items, num_total=num_total, num_negative=num_negative, num_positive=num_positive,
                               num_datetime_sorted=num_datetime_sorted)


if __name__ == '__main__':
    app.run()
    #----------------------------------------------------
    # search_from_server测试
    # items, num_total, num_negative, num_positive, num_datetime_sorted = search_from_server('钟南山')
    #----------------------------------------------------