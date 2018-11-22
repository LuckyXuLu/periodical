# -*- coding: utf-8 -*-
import scrapy
import urllib
import json
from copy import deepcopy
from scrapy_redis.spiders import RedisSpider
import re


# class SpringerSpider(scrapy.Spider):
class SpringerSpider(RedisSpider):
    name = 'springer'
    allowed_domains = []
    # start_urls = ['https://www.springer.com/cn']
    redis_key = 'springer:start_urls'

    def __init__(self):
        self.repair_parameters = False  # True修复, False不修复
        self.url_list = self.repair_url() if self.repair_parameters else list()
        pass

    # 手动添加url
    def repair_url(self):
        url_str = """"""
        url_list = url_str.split("\n")
        url_list_2 = list()
        for url_ in url_list:
            url_list_2.append(" ".join(url_.split()))
        return url_list_2

    # 异常写入
    def read_in(self, txt_name, anomaly, screen_name, url):
        with open("{}.txt".format(txt_name), "a") as e3:
            e3.write("{}: {}; url: {}\n".format(anomaly, screen_name, url))

    # 学科的url列表
    def parse__(self, subject_url):
        subject_list = [
            '/cn/astronomy',  # 已爬取
            '/cn/behavioral-sciences',  # 已爬取
            '/cn/biomedical-sciences',  # 已爬取
            '/cn/business-management',  # 已爬取
            '/cn/chemistry',  # 已爬取
            '/cn/climate',  # 无数据
            '/cn/computer-science',  # 已爬取
            '/cn/earth-sciences',  # 已爬取
            '/cn/economics',  # 已爬取
            '/cn/education-language',  # 已爬取  待确认
            '/cn/energy',  # 已爬取  待确认
            '/cn/engineering',  # 已爬取
            '/cn/environmental-sciences',  # 已爬取
            '/cn/food-science-nutrition',
            '/cn/geography',  # 已爬取
            '/cn/law',  # 已爬取
            '/cn/life-sciences',  # 已爬取
            '/cn/materials',  # 已爬取
            '/cn/mathematics',  # 已爬取
            '/cn/medicine',  # 已爬取
            '/cn/philosophy',  # 已爬取
            '/cn/physics',  # 已爬取
            '/cn/popular-science',  # 大众学科
            '/cn/public-health',  # 已爬取
            '/cn/social-sciences',  # 已爬取
            '/cn/statistics',  # 已爬取
            # '/cn/water'
        ]

        # if [i for i in subject_list if i in subject_url]:
        #     return False
        if subject_url in subject_list:
            return False
        return subject_url

    # 获取学科的url列表
    def parse(self, response):
        print("开始:", response.url)
        a_url = response.xpath('//ul[@class="cms-col cms-link-list"]/li/a')
        for a_ in a_url:
            subject_url = a_.xpath("./@href").extract_first()
            subject_name = a_.xpath('./span/text()').extract_first()

            subject_url = self.parse__(subject_url)
            if not subject_url:
                continue

            if subject_url:
                subject_url = urllib.parse.urljoin(response.url, subject_url)
                print("parse:", subject_url)
                yield scrapy.Request(
                    subject_url,
                    callback=self.parse_1,
                    meta={"subject_name": deepcopy(subject_name)}
                )
                break

    # 获取期刊总链接url
    def parse_1(self, response):
        subject_name = response.meta["subject_name"]

        print("parse_1:", response.url)

        civil_url = response.xpath(
            "//*[contains(text(), 'Featured journals')]/../..//a[contains(text(), 'see all')]/@href").extract_first()

        if not civil_url:
            civil_url = response.xpath("//*[contains(text(), 'Featured journals')]/../..//a/@href").extract_first()
        if civil_url:
            civil_url = urllib.parse.urljoin(response.url, civil_url)
            # print("parse_1_1: ", civil_url)
            yield scrapy.Request(
                civil_url,
                callback=self.periodical_2,
                meta={"subject_name": subject_name}
            )
            self.read_in("成功获取期刊总链接", "成功获取期刊总链接", subject_name, response.url)
        else:
            self.read_in("未获取期刊总链接", "未获取期刊总链接", subject_name, response.url)

    # 获取期刊的url列表
    def periodical_2(self, response):
        subject_name = response.meta["subject_name"]

        div_list = response.xpath('//div[@id="result-list"]/div')
        if not div_list:
            div_list = response.xpath('//div[@class="product-information"]/h3')
        if div_list:
            div_list = div_list[:-1]
        else:
            self.read_in("未获取期刊的url", "未获取期刊的url_2", subject_name, response.url)

        for div in div_list:
            periodical_url = div.xpath('./a/@href').extract_first()
            # periodical = div.xpath('./h4/a/text()').extract_first()
            # if not periodical:
            #     periodical = div.xpath('./a/text()').extract_first()

            if periodical_url:
                periodical_url = urllib.parse.urljoin(response.url, periodical_url)
                yield scrapy.Request(
                    periodical_url,
                    callback=self.periodical_3,
                    meta={"subject_name": subject_name,
                          # "periodical": deepcopy(periodical),
                          }
                )
                if self.repair_parameters:
                    break
            else:
                self.read_in("未获取期刊的url", "未获取期刊的url_1", subject_name, response.url)
            print("periodical_2: ", periodical_url)
            # break  # 测试时使用

        if self.repair_parameters:
            return
        next_url = response.xpath('//a[@title="next"]/@href').extract_first()
        if next_url:
            next_url = urllib.parse.urljoin(response.url, next_url)
            print("periodical_2_1 下一页: ", next_url)
            yield scrapy.Request(
                next_url,
                callback=self.periodical_2,
                meta={"subject_name": subject_name}
            )

    # 获取所有问卷的url
    def periodical_3(self, response):
        # periodical = response.meta["periodical"]
        subject_name = response.meta["subject_name"]

        answer_url = response.xpath('//span[text()="All Volumes & Issues"]/../@href').extract_first()
        if not answer_url:
            answer_url = response.xpath('//span[text()="Alle Bände & Ausgaben"]/../@href').extract_first()

        if answer_url:
            # 判断 url里是否有volumesAndIssues子字符
            if answer_url.find("volumesAndIssues"):
                answer_url = answer_url.replace("/volumesAndIssues/", "/")

            print("periodical_3: ", answer_url)
            yield scrapy.Request(
                answer_url,
                callback=self.periodical_4,
                meta={"subject_name": subject_name,
                      # "periodical": periodical,
                      }
            )
        else:
            self.read_in("未获取问卷的url", "未获取问卷的url", subject_name, response.url)

    # 获取全部文章的url
    def periodical_4(self, response):
        # periodical = response.meta["periodical"]
        subject_name = response.meta["subject_name"]

        if self.repair_parameters:
            for all_articles_url in self.url_list:
                print("手动添加数据")
                print(all_articles_url)
                yield scrapy.Request(
                    all_articles_url,
                    callback=self.periodical_5,
                    meta={"subject_name": subject_name}
                )
            return

        print("periodical_4", response.url)
        all_articles_url = response.xpath('//div[@class="show-all"]/a/@href').extract_first()
        if not all_articles_url:
            all_articles_url = response.xpath('//a[@class="c-button c-button--secondary"]/@href').extract_first()

        if all_articles_url:
            all_articles_url = urllib.parse.urljoin(response.url, all_articles_url)

            yield scrapy.Request(
                all_articles_url,
                callback=self.periodical_5,
                meta={"subject_name": subject_name}
            )
        else:
            self.read_in("未获取文章的url", "未获取文章的url", "->", response.url)

    # 获取文章的url列表
    def periodical_5(self, response):
        subject_name = response.meta["subject_name"]
        print("periodical_5: ", response.url)

        # 文章详情url列表
        li_list = response.xpath('//ol[@data-test="results-list"]/a/text()')
        if not li_list:
            li_list = response.xpath('//ol[@id="results-list"]/li')

        for li in li_list:
            data_str = li.xpath('.//span[@class="year"]/text()').extract_first()
            if not data_str:
                data_str = li.xpath('.//span[@itemprop="datePublished"]/text()').extract_first()
            if data_str:
                data_str = data_str.replace("(", "").replace(")", "")
                data_str = re.findall('[0-9]{4}', data_str)[0] if re.findall('[0-9]{4}', data_str) else None

                if not data_str:
                    data_str = "2010"
                try:
                    if int(data_str) < 2010:
                        self.read_in("期刊时间过长", "期刊时间过长", "->", response.url)
                        return
                except Exception:
                    data_str = "2010"
            else:
                data_str = "2010"

            article_details_url = li.xpath('./h2/a/@href').extract_first()
            if not article_details_url:
                article_details_url = li.xpath('.//h3[@itemprop="name"]'
                                               '/a/@href').extract_first()
            if not article_details_url:
                article_details_url = li.xpath('./div[1]/h3/a/@href').extract_first()
            if not article_details_url:
                article_details_url = li.xpath('./article/div/h3/a/@href').extract_first()

            if article_details_url:
                article_details = urllib.parse.urljoin(response.url, article_details_url)
                yield scrapy.Request(
                    article_details,
                    callback=self.periodical_6,
                    meta={"subject_name": subject_name,
                          "data_str": data_str}
                )
                # break  # 测试时使用
                # return  # 测试时使用

        # 下一页
        next_url = response.xpath('//a[@data-test="next-page"]/@href').extract_first()
        if not next_url:
            next_url = response.xpath('//a[@title="next"]/@href').extract_first()
        if next_url:
            next_url = urllib.parse.urljoin(response.url, next_url)
            yield scrapy.Request(
                next_url,
                callback=self.periodical_5,
                meta={"subject_name": subject_name}
            )

    def periodical_6(self, response):
        subject_name = response.meta["subject_name"]
        data_str = response.meta["data_str"]
        # periodical = response.meta["periodical"]

        print("periodical_6  url: ", response.url)
        item = dict()
        item["期刊"] = None
        item["出版日期"] = data_str
        item["网站"] = "https://www.springer.com/cn"
        item["学科"] = subject_name
        item["url"] = response.url
        item["name"] = None
        item["E_mail"] = None
        item["biography"] = None
        item["标题"] = None
        item["关键词"] = None
        item["resume"] = None
        item["判断"] = "1"

        period_str = response.xpath('//div[@id="enumeration"]/p/a/span/text()').extract_first()
        if not period_str:
            period_str = response.xpath('//div[@id="journalTitle"]/a/text ()').extract_first()
        if not period_str:
            period_str = response.xpath('//span[@class="JournalTitle"]/a/text()').extract_first()
        if not period_str:
            period_str = response.xpath('//div[@id="journalTitle"]/a/span/text()').extract_first()
        if period_str:
            item["期刊"] = " ".join(period_str.split())
        # print("期刊: ", item["期刊"])

        headline = response.xpath('//div[@class="MainTitleSection"]/h1'). \
            xpath('string(.)').extract()
        if headline:
            item["标题"] = " ".join(headline[0].replace("\\n", "").split())
        # print("标题: ", item["标题"])

        antistop_list = response.xpath('//div[@class="KeywordGroup"]/span'). \
            xpath('string(.)').extract()
        if not antistop_list:
            antistop_list = response.xpath('//div[@id="Keywords"]/ul/li') \
                .xpath('string(.)').extract()
        if not antistop_list:
            antistop_list = response.xpath('//div[@id="Keyword"]/ul/li'). \
                xpath('string(.)').extract()
        antistop = list()
        for antistop_str in antistop_list:
            antistop_str = " ".join(antistop_str.replace("\\n", "").split())
            antistop.append(antistop_str)
        if antistop:
            item["关键词"] = str(antistop)
        # print("关键词: ", item["关键词"])

        abstract = response.xpath('//*[@id="Par1"]').xpath('string(.)').extract()
        if not abstract:
            abstract = response.xpath('//section[@id="Abs1"]/p').xpath('string(.)').extract()
        if not abstract:
            abstract = response.xpath('//div[@id="ASec1"]/p').xpath('string(.)').extract()
        if not abstract:
            abstract = response.xpath('//div[@id="Abs1"]/div/p').xpath('string(.)').extract()
        if not abstract:
            abstract = response.xpath('//div[@id="Abstract"]/div[1]/p').xpath('string(.)').extract()
        if not abstract:
            abstract = response.xpath('//div[@id="Abstract"]/p').xpath('string(.)').extract()
        if not abstract:  # 额外添加
            abstract = response.xpath('//*[@class="Para"]').xpath('string(.)').extract()

        if abstract:
            item["resume"] = " ".join(str(abstract[0]).split()).replace("−", "-").replace("\n", "").replace("\\n", "")

        div_list = response.xpath('//*[@id="authorsandaffiliations"]/div')
        em_list = list()
        if div_list:
            serial_number_list = list()
            li_list = div_list.xpath('./ul/li')
            for li_ in li_list:
                ul_serial_number = li_.xpath('./ul/li/text()').extract_first()
                ul_name = li_.xpath('./span[@itemprop="name"]/text()').extract_first()
                ul_mail = li_.xpath('./span[@class="author-information"]//a[@itemprop="email"]/@href').extract_first()

                if ul_mail and ul_name and ul_serial_number:
                    serial_number_list.append((ul_serial_number, ul_name, ul_mail))

            if not serial_number_list:
                return

            oi_list = div_list.xpath('./ol/li')
            for oi_ in oi_list:
                oi_brief = oi_.xpath('./span[@class="affiliation__item"]').xpath("string(.)").extract_first()
                oi_serial_number = oi_.xpath('./span[@class="affiliation__count"]/text()').extract_first()
                oi_serial_number = oi_serial_number.replace('.', '') if oi_serial_number else None
                for serial_number_str in serial_number_list:
                    if serial_number_str[0] == oi_serial_number:
                        em_list.append((serial_number_str[1], serial_number_str[2], oi_brief))
                    elif serial_number_str[0] in oi_brief:
                        pass
        else:
            li_str2 = response.xpath('//ul[@class="u-listReset"]/li/a[@title="Email author"]')
            for li_ in li_str2:
                brief_number = li_.xpath('../sup/a/@href').extract_first()
                brief_number = brief_number.replace("#", "").replace(" ", "")
                brief_str = response.xpath('//*[@id="{}"]/div/text()'.format(brief_number)).extract_first()
                li_mail = li_.xpath('./@href').extract_first()
                li_name = li_.xpath('./../span/text()').extract_first()
                if li_mail and li_name:
                    em_list.append((li_name, li_name, brief_str))

        for em in em_list:
            item["name"] = " ".join(em[0].split())
            item["E_mail"] = " ".join(em[1].replace("mailto:", "").split())
            item["biography"] = " ".join(em[2].split()) if em[2] else None
            # print(json.dumps(item, sort_keys=True, ensure_ascii=False, indent=4))
            yield item

