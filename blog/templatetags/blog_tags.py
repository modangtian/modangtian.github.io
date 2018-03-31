# coding=utf-8
#这个文件存放自定义的模板标签代码
#{% get_recent_articles %} 的语法在模板中调用这个函数，
# 必须按照 Django 的规定注册这个函数为模板标签，方法如下：#
from django import template
from ..models import Article, Category


register = template.Library()

#获取最近文章
@register.simple_tag()
def get_recent_articles(num=5):
    return Article.objects.all().order_by('-create_time')[:num]


'''这里我们首先导入 template 这个模块，然后实例化了一个 template.Library 类，
并将函数 get_recent_articles 装饰为 register.simple_tag。
这样就可以在模板中使用语法 {% get_recent_posts %} 调用这个函数了。
注意 Django 1.9 后才支持 simple_tag 模板标签，
如果你使用的 Django 版本小于 1.9，
你将得到一个错误。Django 1.9 以前的版本如何自定义模板标签这里不再赘述。'''


#归档模板标签
@register.simple_tag()
def archives():
    return Article.objects.dates('create_time', 'month', order='DESC')

'''这里 dates 方法会返回一个列表，列表中的元素为每一篇文章（Post）的创建时间，
且是 Python 的 date 对象，精确到月份，降序排列。接受的三个参数值表明了这些含义，一个是 created_time ，
即 Post 的创建时间，month 是精度，order='DESC' 表明降序排列（即离当前越近的时间越排在前面）。
例如我们写了 3 篇文章，分别发布于 2017 年 2 月 21 日、2017 年 3 月 25 日、2017 年 3 月 28 日，
那么 dates 函数将返回 2017 年 3 月 和 2017 年 2 月这样一个时间列表，且降序排列，从而帮助我们实现按月归档的目的。'''

#分类模板标签
@register.simple_tag
def get_categories():
    return Category.objects.all()

'''尽管侧边栏有 4 项内容（还有一个标签云），但是这里我们只实现最新文章、归档和分类数据的显示，
还有一个标签云没有实现。因为标签云的实现稍有一点不同，所以将在接下来的教程中专门介绍。
这里你也可以尝试着自己解决，如果遇到问题，可以通过官方文档或者搜索引擎求助。
独立思考并寻求解决方案以及善用搜索引擎是一个开发者必须培养的能力，
只有这样你才能成为一个独立的开发者，独立地解决别人可能从来没有遇到过的问题。'''


