# coding: utf-8
from scrapy import Selector

res = u"""<div class="zh-summary summary clearfix" style="display:none;">

	一、你国人 人格发展不健全，没有能力为自己负责。二，你国人 人格上不是成年人，是幼儿，需要别人提供不仅仅情感关爱，而且要提供物质供给。三。你国人 思想不健康，希望别人以自残的方式来表达对自己的爱。大咕咕鸡发明这个词，真乃智者也，ヾ（´▽｀…

	<a href="/question/30503452/answer/96791511" class="toggle-expand">显示全部</a>

	</div>"""


if __name__ =='__main__':
	selector = Selector(text=res)
	print selector.css('div.zh-summary.summary').re_first('<div.*?>([\S\s]+)<\/div>')
