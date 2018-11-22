# -*- coding: utf-8 -*-
import scrapy
import urllib
import re
import time
from copy import deepcopy
from scrapy_redis.spiders import RedisSpider
from copy import deepcopy

class TandfonlineSpider(RedisSpider):
    # class TandfonlineSpider(scrapy.Spider):
    name = 'tandfonline'
    allowed_domains = ["tandfonline.com"]
    redis_key = "tandfonline:start_urls"

    # start_urls = ["https://www.tandfonline.com"]

    def __init__(self):

        self.headers = {
            ':authority': 'www.tandfonline.com',
            ':method': 'GET',
            ':path': '',
            ':scheme': 'https',
            'accept': 'text/html, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'Cookie': 'I2KBRCK=1; MAID=qpjDL3P3KgN+3WidZgMn4A==; displayMathJaxFormula=true; _gcl_au=1.1.581131978.1537845583; _ga=GA1.2.1503691299.1537845584; visitor_id111042=883298955; visitor_id111042-hash=ad4dd1e4d9793fb4fcdac921111501d9fa285f4fed5552a20d9859d4c078fdbd43e8c55687b3d4ddda56540c2f17782b30430b83; MAID=eq9bOu/kQG8iUwV3sTsB0w==; MACHINE_LAST_SEEN=2018-09-24T20%3A23%3A50.443-07%3A00; cookiePolicy=accept; timezone=480; _gid=GA1.2.1663335771.1540276740; SERVER=WZ6myaEXBLEUAmK1OYt0wg==; MACHINE_LAST_SEEN=2018-10-23T01%3A17%3A57.688-07%3A00; JSESSIONID=aaaiDLgPz8KNzba_nKtAw; __atuvc=1%7C39%2C0%7C40%2C16%7C41%2C1%7C42%2C2%7C43; __atuvs=5bceda104777031d000; _gat_UA-3062505-5=1',
            'X-Requested-With:': 'XMLHttpRequest'
        }

        self.headers_2 = {
            ':authority': 'www.tandfonline.com',
            ':method': 'GET',
            ':path': '',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'Cookie': 'I2KBRCK=1; MAID=PC0Jpxp9zvx+1hNZe9K65A==; _gcl_au=1.1.895568112.1537961011; _ga=GA1.2.1836440912.1537961012; displayMathJaxFormula=true; visitor_id111042=884542313; visitor_id111042-hash=549dbf345424fa63bcc9c8209104e0a8d86968876b164e435e65f951dae3d95dbcd20e5b708c9af3e5581b934244e27c1c1be9b5; cookiePolicy=accept; _gid=GA1.2.283319798.1540819996; timezone=480; __atuvc=0%7C40%2C0%7C41%2C0%7C42%2C1%7C43%2C5%7C44; SERVER=WZ6myaEXBLE0r6Bgisb3Fw==; MACHINE_LAST_SEEN=2018-10-31T07%3A29%3A23.933-07%3A00; JSESSIONID=aaauTv-aCjTqQ7Xpf33Aw'
        }

    def read_in(self, txt_name, anomaly, screen_name, url):
        with open("{}.txt".format(txt_name), "a") as e3:
            e3.write("{}: {}; url: {}\n".format(anomaly, screen_name, url))

    def parse__(self, subject_url):
        subject_list = [
            '/topic/4251?target=topic',
            '/topic/4250?target=topic',
            '/topic/4252?target=topic',
            '/topic/4253?target=topic',
            '/topic/4254?target=topic',  #建筑与环境
            '/topic/4256?target=topic',
            '/topic/4255?target=topic',
            '/topic/4257?target=topic',
            '/topic/4258?target=topic',
            '/topic/4259?target=topic',
            '/topic/4261?target=topic',
            '/topic/4260?target=topic',  # 工程与技术
            # '/topic/4248?target=topic',  # 环境与农业
            '/topic/4262?target=topic',  # 环境与可持续发展
            '/topic/4263?target=topic',
            '/topic/4264?target=topic',
            '/topic/4266?target=topic',
            '/topic/4267?target=topic',
            '/topic/4268?target=topic',
            '/topic/4269?target=topic',
            '/topic/4270?target=topic',
            '/topic/4271?target=topic',
            '/topic/4272?target=topic',
            '/topic/4249?target=topic',
            '/topic/4273?target=topic',
            '/topic/4274?target=topic',
            '/topic/4278?target=topic',
            '/topic/4277?target=topic',
            '/topic/4279?target=topic',
            '/topic/4280?target=topic'
        ]

        if subject_url in subject_list:
            return False
        return subject_url

    # 获取学科的url列表
    def parse(self, response):
        print("开始:", response.url)
        li_list = response.xpath('//div[contains(@class, "unit ")]/ul/li/a')

        for li in li_list:
            subject_url = li.xpath("./@href").extract_first()
            subject_name = li.xpath('./text()').extract_first()

            subject_url = self.parse__(subject_url)
            if not subject_url:
                continue

            if subject_url and subject_name:
                subject_str = "&pageSize=50&subjectTitle=&startPage=0"
                subject_url = urllib.parse.urljoin(response.url, subject_url) + subject_str
                print("parse:", subject_url)
                yield scrapy.Request(
                    # subject_url,
                    "https://www.tandfonline.com/topic/4248?target=topic&pageSize=50&subjectTitle=&startPage=2000",
                    callback=self.parse_1,
                    meta={"subject_name": deepcopy(subject_name)}
                )
                break  # 测试使用
            else:
                self.read_in("未获取学科的url", "未获取学科的url", subject_name, response.url)

    # 获取文章的url列表
    def parse_1(self, response):
        subject_name = response.meta["subject_name"]
        print("parse_1:", response.url)

        self.read_in("成功获取学科的url", "成功获取学科的url", subject_name, response.url)

        article_list = response.xpath('//article[@class="searchResultItem"]')
        for article in article_list:
            item = dict()
            item["出版日期"] = None
            item["学科"] = subject_name

            volume = article.xpath('.//div[@class="searchentryright"]//a[contains(text(), "Volume")]/text()').extract_first()
            if volume:
                volume = re.findall(r".+([0-9]{4})", volume)
                volume = int(volume[0]) if volume else None

            if volume and volume > 2009:
                item["出版日期"] = str(volume)
                periodical_url = article.xpath('.//a[@class="ref nowrap"]/@href').extract_first()
                if periodical_url:
                    periodical_url = urllib.parse.urljoin(response.url, periodical_url)
                    print("parse_1_1:", periodical_url)

                    headers = deepcopy(self.headers_2)
                    headers[':path'] = periodical_url.replace('https://www.tandfonline.com', '')
                    yield scrapy.Request(
                        periodical_url,
                        callback=self.parse_2,
                        headers=headers,
                        meta={"item": item}
                    )
                    # break  # 测试使用
                else:
                    self.read_in("未获取文章的url", "未获取文章的url", subject_name, response.url)
            else:
                self.read_in("未获取出版日期的url", "未获取出版日期的url", subject_name, response.url)

        if not article_list:
            self.read_in("未获取任何文章的url", "未获取任何文章的url", subject_name, response.url)

        next_url = response.xpath('//a[@class="nextPage  js__ajaxSearchTrigger"]/@href').extract_first()
        if next_url:
            next_url = urllib.parse.urljoin(response.url, next_url)

            if next_url == "https://www.tandfonline.com/topic/4248?target=topic&pageSize=50&subjectTitle=&startPage=2110":
                return
            print("下一页: ", next_url)
            self.read_in("下一页的url", "下一页的url", subject_name, response.url)

            # headers = deepcopy(self.headers)
            # headers[':path'] = next_url.replace('https://www.tandfonline.com', '')
            yield scrapy.Request(
                next_url,
                # headers=headers,
                callback=self.parse_1,
                meta={"subject_name": subject_name}
            )
        else:
            self.read_in("未获取下一页的url", "未获取下一页的url", subject_name, response.url)

    # 获取数据
    def parse_2(self, response):
        item = response.meta["item"]
        print("parse_2:", response.url)

        item["url"] = response.url
        item["姓名"] = None
        item["邮箱"] = None
        item["标题"] = None
        item["作者简介"] = None
        item["关键词"] = None
        item["摘要"] = None
        item["期刊"] = None
        item["网站"] = "https://www.tandfonline.com/"
        item["判断"] = "1"

        item["期刊"] = response.xpath('//div[@class="title-container"]/h1/a/text()').extract_first()
        if item["期刊"]:
            item["期刊"] = " ".join(item["期刊"].split())
        # print("期刊: ", item["期刊"])

        antistop_list = response.xpath('//div[@class="hlFld-KeywordText"]/a/text()').extract()
        if antistop_list:
            item["关键词"] = str(antistop_list)

        abstract = response.xpath('//div[@class="abstractSection abstractInFull"]/p').xpath('string(.)').extract()
        if abstract:
            item["摘要"] = " ".join(str(abstract[0]).split())

        div_str = response.xpath(
            '//div[@id="fa57727f-b942-4eb8-9ed2-ecfe11ac03f5"]//span[@class="NLM_article-title hlFld-title"]/text()').extract_first()
        if div_str:
            item["标题"] = " ".join(div_str.split())
            # print("标题: ", item["标题"])

        a_list = response.xpath('.//span[@class="contribDegrees corresponding "]/a')
        for a in a_list:
            item["姓名"] = a.xpath('./text()').extract_first()
            if item["姓名"]:
                item["姓名"] = " ".join(item["姓名"].split())

            item["作者简介"] = a.xpath('.//span[@class="overlay"]/text()').extract_first()
            if item["作者简介"]:
                item["作者简介"] = " ".join(item["作者简介"].split())

                item["邮箱"] = a.xpath('.//span[@class="corr-email"]/@data-mailto').extract_first()

            if item["邮箱"]:

                item["邮箱"] = " ".join(item["邮箱"].split()).replace("mailto:", "")

            if not item["邮箱"]:
                self.read_in("未获取到邮箱", "未获取到邮箱", item["学科"], response.url)
                return

            # print(json.dumps(item, sort_keys=True, ensure_ascii=False, indent=4))
            yield item
