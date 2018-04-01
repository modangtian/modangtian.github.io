# coding=utf-8
#这个文件存放自定义的模板标签代码
#{% get_recent_articles %} 的语法在模板中调用这个函数，
# 必须按照 Django 的规定注册这个函数为模板标签，方法如下：#
from django import template
from ..models import Article, Category, Tag
from django.db.models.aggregates import Count


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
    # Count 计算分类下的文章数，其接受的参数为需要计数的模型的名称
    return Category.objects.annotate(num_articles=Count('article')).filter(num_articles__gt=0) #gt小于号


@register.simple_tag
def get_tags():
    # Count 计算分类下的文章数，其接受的参数为需要计数的模型的名称
    return Tag.objects.annotate(num_articles=Count('article')).filter(num_articles__gt=0) #gt小于号


# Count 计算分类下的文章数，其接受的参数为需要计数的模型的名称
# article_list = Tag.objects,annotate(num_articles=Count(Article))
'''这个 Category.objects.annotate 方法和 Category.objects.all 有点类似，它会返回数据库中全部 Category 的记录，
但同时它还会做一些额外的事情，在这里我们希望它做的额外事情就是去统计返回的 Category 记录的集合中每条记录下的文章数。
代码中的 Count 方法为我们做了这个事，它接收一个和 Categoty 相关联的模型参数名（这里是 Post，通过 ForeignKey 关联的），
然后它便会统计 Category 记录的集合中每条记录下的与之关联的 Post 记录的行数，也就是文章数，最后把这个值保存到 num_posts 属性中。
此外，我们还对结果集做了一个过滤，使用 filter 方法把 num_posts 的值小于 1 的分类过滤掉。
因为 num_posts 的值小于 1 表示该分类下没有文章，没有文章的分类我们不希望它在页面中显示。
关于 filter 函数以及查询表达式（双下划线）在之前已经讲过'''

'''尽管侧边栏有 4 项内容（还有一个标签云），但是这里我们只实现最新文章、归档和分类数据的显示，
还有一个标签云没有实现。因为标签云的实现稍有一点不同，所以将在接下来的教程中专门介绍。
这里你也可以尝试着自己解决，如果遇到问题，可以通过官方文档或者搜索引擎求助。
独立思考并寻求解决方案以及善用搜索引擎是一个开发者必须培养的能力，
只有这样你才能成为一个独立的开发者，独立地解决别人可能从来没有遇到过的问题。'''


