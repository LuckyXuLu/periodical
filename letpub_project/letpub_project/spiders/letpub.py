# -*- coding: utf-8 -*-
import scrapy
import urllib
import json
import re
from copy import deepcopy
from scrapy_redis.spiders import RedisSpider


# class LetpubSpider(scrapy.Spider):
class LetpubSpider(RedisSpider):
    name = 'letpub'
    allowed_domains = ['letpub.com.cn']
    # start_urls = ['https://www.letpub.com.cn/index.php?page=journalapp']
    redis_key = "letpub:start_urls"

    # 异常写入
    def read_in(self, txt_name, screen_name, url):
        with open("{}.txt".format(txt_name), "a") as e3:
            e3.write("{}; url: {}\n".format(screen_name, url))

    # 学科的url列表
    def parse_subject_url(self, subject_url):
        subject_list = [
            "./index.php?page=journalapp&fieldtag=3&firstletter=",
            "./index.php?page=journalapp&fieldtag=6&firstletter=",
            "./index.php?page=journalapp&fieldtag=1&firstletter=",
            "./index.php?page=journalapp&fieldtag=2&firstletter=",
            "./index.php?page=journalapp&fieldtag=4&firstletter=",
            "./index.php?page=journalapp&fieldtag=5&firstletter=",
            "./index.php?page=journalapp&fieldtag=7&firstletter=",
            "./index.php?page=journalapp&fieldtag=8&firstletter=",
            "./index.php?page=journalapp&fieldtag=9&firstletter=",
            "./index.php?page=journalapp&fieldtag=10&firstletter=",
            "./index.php?page=journalapp&fieldtag=11&firstletter=",
            "./index.php?page=journalapp&fieldtag=12&firstletter=",
            "./index.php?page=journalapp&fieldtag=13&firstletter=",
            "./index.php?page=journalapp&fieldtag=15&firstletter=",
            "./index.php?page=journalapp&fieldtag=14&firstletter=",
            "./index.php?page=journalapp&fieldtag=16&firstletter=",
            "./index.php?page=journalapp&fieldtag=17&firstletter=",
            "./index.php?page=journalapp&fieldtag=19&firstletter=",
            "./index.php?page=journalapp&fieldtag=18&firstletter=",
            "./index.php?page=journalapp&fieldtag=22&firstletter=",
            "./index.php?page=journalapp&fieldtag=20&firstletter=",
            "./index.php?page=journalapp&fieldtag=21&firstletter=",
            "./index.php?page=journalapp&fieldtag=23&firstletter=",
            "./index.php?page=journalapp&fieldtag=24&firstletter=",
            "./index.php?page=journalapp&fieldtag=25&firstletter=",
            "./index.php?page=journalapp&fieldtag=27&firstletter=",
            "./index.php?page=journalapp&fieldtag=28&firstletter=",
            "./index.php?page=journalapp&fieldtag=26&firstletter=",
            "./index.php?page=journalapp&fieldtag=29&firstletter=",
            "./index.php?page=journalapp&fieldtag=31&firstletter=",
            "./index.php?page=journalapp&fieldtag=33&firstletter=",
            "./index.php?page=journalapp&fieldtag=30&firstletter=",
            "./index.php?page=journalapp&fieldtag=35&firstletter=",
            "./index.php?page=journalapp&fieldtag=32&firstletter=",
            "./index.php?page=journalapp&fieldtag=52&firstletter=",
            "./index.php?page=journalapp&fieldtag=34&firstletter=",
            "./index.php?page=journalapp&fieldtag=38&firstletter=",
            "./index.php?page=journalapp&fieldtag=36&firstletter=",
            "./index.php?page=journalapp&fieldtag=39&firstletter=",
            "./index.php?page=journalapp&fieldtag=40&firstletter=",
            "./index.php?page=journalapp&fieldtag=41&firstletter=",
            "./index.php?page=journalapp&fieldtag=47&firstletter=",
            "./index.php?page=journalapp&fieldtag=37&firstletter=",
            "./index.php?page=journalapp&fieldtag=44&firstletter=",
            "./index.php?page=journalapp&fieldtag=54&firstletter=",
            "./index.php?page=journalapp&fieldtag=48&firstletter=",
            "./index.php?page=journalapp&fieldtag=56&firstletter=",
            "./index.php?page=journalapp&fieldtag=43&firstletter=",
            "./index.php?page=journalapp&fieldtag=55&firstletter=",
            "./index.php?page=journalapp&fieldtag=50&firstletter=",
            "./index.php?page=journalapp&fieldtag=51&firstletter=",
            "./index.php?page=journalapp&fieldtag=53&firstletter=",
            "./index.php?page=journalapp&fieldtag=45&firstletter=",
            # "./index.php?page=journalapp&fieldtag=49&firstletter="
        ]
        if subject_url in subject_list:
            return False
        return subject_url

    def parse(self, response):
        a_list = response.xpath('//span[@id="s1"]//td/a')[:-2]
        for a in a_list:
            subject_url = a.xpath('./@href').extract_first()
            subject_name = a.xpath('./text()').extract_first()
            # print(subject_name)

            subject_url = self.parse_subject_url(subject_url)
            print(subject_url)
            if not subject_url:
                continue

            if subject_url:
                # subject_url = urllib.parse.urljoin(response.url, subject_url)
                subject_url = "https://www.letpub.com.cn/index.php?page=journalapp&fieldtag=&firstletter=&currentpage=1#journallisttable"
                print("parse:", subject_url)
                print("parse:", subject_name)
                yield scrapy.Request(
                    subject_url,
                    callback=self.parse_1,
                    # meta={"subject_name": deepcopy(subject_name)}
                )

    def parse_1(self, response):
        print("parse_1:", response.url)
        # subject_name = response.meta["subject_name"]

        tr_list = response.xpath('//div[@id="yxyz_content"]/table[@class="table_yjfx"]/tbody/tr')[2:-1]
        print(len(tr_list))
        if len(tr_list) != 10:
            self.read_in("期刊url列表数据", "parse_1", response.url)
        if not tr_list:
            self.read_in("未获取到期刊url列表", "parse_1", response.url)
        for tr in tr_list:
            item = dict()
            item["学科"] = "1523"

            item["ISSN"] = tr.xpath('./td[1]/text()').extract_first()
            if item["ISSN"]:
                item["ISSN"] = " ".join(item["ISSN"].split())

            item["期刊"] = tr.xpath('./td[2]/a/text()').extract_first()
            if item["期刊"]:
                item["期刊"] = " ".join(item["期刊"].split())

            item["影响因子"] = tr.xpath('./td[3]/text()').extract_first()
            if item["影响因子"]:
                item["影响因子"] = " ".join(item["影响因子"].split())

            item["中科院分区"] = tr.xpath('./td[4]/text()').extract_first()
            if item["中科院分区"]:
                item["中科院分区"] = " ".join(item["中科院分区"].split())
                if item["中科院分区"] == "未录":
                    self.read_in("已录取的期刊", item["ISSN"], response.url)
                    continue

            item["大类学科"] = tr.xpath('./td[5]/text()').extract_first()
            if item["大类学科"]:
                item["大类学科"] = " ".join(item["大类学科"].split())

            item["小类学科"] = tr.xpath('./td[6]/text()').extract_first()
            if item["小类学科"]:
                item["小类学科"] = " ".join(item["小类学科"].split())

            item["SCI/SCIE"] = tr.xpath('./td[7]').xpath("string(.)").extract_first()
            if item["SCI/SCIE"]:
                item["SCI/SCIE"] = " ".join(item["SCI/SCIE"].split())

            item["是否OA"] = tr.xpath('./td[8]/text()').extract_first()
            if item["是否OA"]:
                item["是否OA"] = " ".join(item["是否OA"].split())

            item["录用比例"] = tr.xpath('./td[9]/text()').extract_first()
            if item["录用比例"]:
                item["录用比例"] = " ".join(item["录用比例"].split())

            item["审稿周期"] = tr.xpath('./td[10]/text()').extract_first()
            if item["审稿周期"]:
                item["审稿周期"] = " ".join(item["审稿周期"].split())

            item["查看数"] = tr.xpath('./td[12]/text()').extract_first()
            if item["查看数"]:
                item["查看数"] = " ".join(item["查看数"].split())

            periodical_url = tr.xpath('./td[2]/a/@href').extract_first()
            if periodical_url:
                periodical_url = urllib.parse.urljoin(response.url, periodical_url)
                yield scrapy.Request(
                    periodical_url,
                    callback=self.parse_2,
                    meta={"item": deepcopy(item)}
                )
            else:
                self.read_in("未获取的期刊url", item["ISSN"], response.url)

        nat_str = response.xpath('//a[text()="下一页"]/@href').extract_first()
        if nat_str:
            nat_str = urllib.parse.urljoin(response.url, nat_str)
            self.read_in("下一页", "parse_1", nat_str)
            print("下一页：", nat_str)
            if nat_str == response.url:
                return
            yield scrapy.Request(
                nat_str,
                callback=self.parse_1,
            )
        else:
            self.read_in("未获取到下一页", "parse_1", response.url)

    def parse_2(self, response):
        print("parse_2:", response.url)
        item = response.meta["item"]

        item['url'] = response.url
        item['网站'] = "https://www.letpub.com.cn"

        tr_all = response.xpath('//div[@id="yxyz_content"]/table[@class="table_yjfx"]/tbody[1]')

        item["自引率"] = tr_all.xpath('./tr[5]/td[2]/text()').extract_first()
        if item["自引率"]:
            item["自引率"] = " ".join(item["自引率"].split())

        item["五年影响因子"] = tr_all.xpath('./tr[6]/td[2]/text()').extract_first()
        if item["五年影响因子"]:
            item["五年影响因子"] = " ".join(item["五年影响因子"].split())

        item["期刊官方网站"] = tr_all.xpath('./tr[7]/td[2]/a/text()').extract_first()
        if item["期刊官方网站"]:
            item["期刊官方网站"] = " ".join(item["期刊官方网站"].split())

        item["期刊投稿网址"] = tr_all.xpath('./tr[8]/td[2]/a/text()').extract_first()
        if item["期刊投稿网址"]:
            item["期刊投稿网址"] = " ".join(item["期刊投稿网址"].split())

        item["通讯方式"] = tr_all.xpath('./tr[10]/td[2]/text()').extract_first()
        if item["通讯方式"]:
            item["通讯方式"] = " ".join(item["通讯方式"].split())

        item["涉及的研究方向"] = tr_all.xpath('./tr[11]/td[2]/text()').extract_first()
        if item["涉及的研究方向"]:
            item["涉及的研究方向"] = " ".join(item["涉及的研究方向"].split())

        item["出版国家或地区"] = tr_all.xpath('./tr[12]/td[2]/text()').extract_first()
        if item["出版国家或地区"]:
            item["出版国家或地区"] = " ".join(item["出版国家或地区"].split())

        item["出版周期"] = tr_all.xpath('./tr[13]/td[2]/text()').extract_first()
        if item["出版周期"]:
            item["出版周期"] = " ".join(item["出版周期"].split())

        item["出版年份"] = tr_all.xpath('./tr[14]/td[2]/text()').extract_first()
        if item["出版年份"]:
            item["出版年份"] = " ".join(item["出版年份"].split())

        item["年文章数"] = tr_all.xpath('./tr[15]/td[2]/text()').extract_first()
        if item["年文章数"]:
            item["年文章数"] = " ".join(item["年文章数"].split())

        # print(json.dumps(item, sort_keys=True, ensure_ascii=False, indent=4))
        yield item





