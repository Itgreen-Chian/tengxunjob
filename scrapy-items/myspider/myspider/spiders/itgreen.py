import scrapy
import json, time

from myspider.items import MyspiderItem


class ItgreenSpider(scrapy.Spider):
    name = 'itgreen'
    allowed_domains = ['tencent.com']

    # 时间戳
    t = int(time.time()*1000)
    print('时间戳', t)

    # 实际url
    start_urls = ['https://careers.tencent.com/tencentcareer/api/post/Query?timestamp='+str(t)+'&countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=&attrId=&keyword=&pageIndex=1&pageSize=10&language=zh-cn&area=cn']

    # 重写start_request方法-携带cookie
    def start_requests(self):
        # t = int(time.time())
        # print('时间戳', t)

        # cookie处理
        temp = 'pgv_pvid=3056923520; pgv_pvi=9424708608; _ga=GA1.2.1460148958.1599101891; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22007cb2e21159523c214e3329d3f637b0%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fcn.bing.com%2F%22%2C%22%24latest_utm_medium%22%3A%22cpc%22%7D%2C%22%24device_id%22%3A%2217451e66f7b1a1-02e5443e58d1c5-71415a3b-728320-17451e66f7c61%22%7D; _gcl_au=1.1.496817875.1620115640; Hm_lvt_eaa57ca47dacb4ad4f5a257001a3457c=1621684314,1621749232; Hm_lpvt_eaa57ca47dacb4ad4f5a257001a3457c=1621751899'
        cookie = {data.split("=")[0]: data.split("=")[-1]for data in temp.split("; ")}

        # 返回请求方法和回调函数
        url = self.start_urls[0]
        yield scrapy.FormRequest(url=url, cookies=cookie, callback=self.parse)

    def parse(self, response,):
        # 解析数据，定义对于网站的相关操作
        # with open('job.html', 'wb')as f:
        #     f.write(response.body)

        # 初始化模型对象
        items = MyspiderItem()

        # 获取所有职位节点列表
        json_text = json.loads(response.text)
        # print(json_text)
        # print(type(json_text))

        # 获取一页所有职位数据数据列表
        dict_data = json_text["Data"]["Posts"]
        # print(dict_data)

        # 总页数提取
        page_number = json_text["Data"]["Count"]//10+1
        print('总页数：', page_number)

        # 遍历获取职位信息
        # for data in dict_data[0:1]:  # Debug使用
        for data in dict_data[0:2]:
            items["PostName"] = data["RecruitPostName"]
            items["PostURL"] = data["PostURL"]
            items["CategoryType"] = data["CategoryName"]
            items["LocationName"] = data["LocationName"]
            items["LastUpdateTime"] = data["LastUpdateTime"]

            print(items["PostName"])
            print(items["PostURL"])
            print(items["CategoryType"])
            print(items["LocationName"])
            print(items["LastUpdateTime"])
            # break

            # 获取详情页-重组详情页url（由于访问详情页url发生重定向）
            PostId = items["PostURL"].split('postId=')[-1]
            PostURL = 'https://careers.tencent.com/tencentcareer/api/post/ByPostId?timestamp='+str(self.t)+'&postId='+PostId+'&language=zh-cn'
            yield scrapy.Request(
                url=PostURL,
                callback=self.parse_detile,
                meta={"items": items},

            )

    def parse_detile(self, response):

        # 获取详情页数据
        dict_detail = json.loads(response.text)
        # print(dict_detail)

        # 接收items
        items = response.meta["items"]

        # 提取岗位职责和岗位要求，并过替换掉多余字符串
        items['Requirement'] = dict_detail['Data']['Requirement'].replace('\\n', '')
        items['Responsibility'] = dict_detail['Data']['Responsibility'].replace('\\n', '')
        print(items['Requirement'])
        print(items['Responsibility'])

        yield items
