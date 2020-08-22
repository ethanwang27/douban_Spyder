# -*-coding:utf-8-*-

"""
@Author: ethan
@Email: ethanwang279@gmail.com
@Datetime: 2020/8/22 23:17
@File: doubanBookRankFetcher.py
@Project: douban_Spyder
@Description: None
"""

from datetime import datetime
from helper.logHepler import LogHelper
from utils.WebRequest import WebRequest

import config
import time
import random


class DoubanBookRankFetcher(object):

    def __init__(self):
        self.name = "DoubanBookRankFetcher"
        self.log = LogHelper(self.name)

    @staticmethod
    def get_weekly_rank() -> list:

        book_rank_infos = []
        url_list = config.DOUBAN_BOOK_RANK_URL

        for book_type, url in url_list.items():
            tree = WebRequest().get(url).tree
            week_num = datetime.now().isocalendar()[:2]
            # 图书排行信息
            rank_info = {'date': datetime.now().strftime('%Y-%m-%d'),
                         'week_num': str(week_num[0]) + "-" + str(week_num[1]),
                         'book_type': book_type,
                         'rank_info': []}

            rank_num = tree.xpath('//div[@class="media__img"]/strong[@class="fleft green-num-box"]/text()')
            books_links = tree.xpath('//h2[@class="clearfix"]/a[@class="fleft"]/@href')
            books_name = tree.xpath('//h2[@class="clearfix"]/a[@class="fleft"]/text()')
            books_star = tree.xpath('//p[@class="clearfix w250"]/span[@class="font-small color-red fleft"]/text()')

            for num, book_url, name, star in zip(rank_num, books_links, books_name, books_star):
                rank_info['rank_info'].append({'rank_num': num,
                                               'book_name': name,
                                               'book_subject_id': url.split('/')[-2],
                                               'star': star})

            time.sleep(random.randint(12, 20))
            book_rank_infos.append(rank_info)

        return book_rank_infos

    @staticmethod
    def get_book_info(book_url: str) -> dict:
        book_tree = WebRequest().get(book_url).tree

        # 获取书籍名称
        book_name = book_tree.xpath('//span[@property="v:itemreviewed"]/text()')
        # 获取作者
        author = book_tree.xpath('//*[@id="book_info"]/span[1]/a/text()')
        # 获取书籍对应出版信息标题（每本书包含的出版信息可能不同，故连标题一起抓取）
        publication_titles = book_tree.xpath('//*[@id="book_info"]/span[@class="pl"]/text()')
        # 获取书籍对应出版信息
        publication_infos = book_tree.xpath('//div[@id="book_info"]/text()')
        # Xpath获取到的书籍信息中会有很多换行和空格的无用信息，直接过滤掉
        publication_infos = [item.replace('\xa0', '') for item in publication_infos if
                             item.replace("\n", "").replace(" ", "") != ""]
        # 获取书籍内容简介
        content_summary = book_tree.xpath('//*[@id="link-report"]//div[@class="intro"]/p/text()')
        # 获取书籍作者简介（作者简介可能会抓取出隐藏的相同简介，故存储前应该去重）
        author_summary = book_tree.xpath('//*[@class="indent "]//p/text()')
        # 获取书籍标签
        book_tags = book_tree.xpath('//*[@id="db-tags-section"]/div/span/a/text()')
        # subject_id 豆瓣书籍ID
        book_douban_subject_id = book_url.strip('/').split('/')[-1]

        book_info = {'name': book_name[0], 'author': ';'.join(author)}
        # 出版信息
        isbn = ""
        for title, publication_info in zip(publication_titles, publication_infos):
            title = title.strip(':')
            if len(book_info) > 0:
                book_info[title] = publication_info
            if title.lower() == "isbn":
                isbn = publication_info

        # 书籍内容简介
        if isinstance(content_summary, list):
            book_info["content_summay"] = "\n".join(content_summary)
        else:
            book_info["content_summay"] = content_summary

        # 作者简介
        if isinstance(author_summary, list):
            author_summary = list(set(author_summary))
            book_info["author_summary"] = '\n'.join(author_summary)
        else:
            book_info["author_summary"] = author_summary
        book_info["tags"] = book_tags
        book_info["subject_id"] = book_douban_subject_id

        return book_info


if __name__ == '__main__':
    print(DoubanBookRankFetcher().get_weekly_rank())


