from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Article, Category
import markdown#markdown格式的文本渲染成标准的 HTML 文档是一个复杂的工作
from comments.forms import CommentsForm#引入评论表单

"""
请使用下方的模板引擎方式。
def index(request):
    return HttpResponse("欢迎访问我的博客首页！")
"""

"""
请使用下方真正的首页视图函数
def index(request):
    return render(request, 'blog/index.html', context={
        'title': '我的博客首页',
        'welcome': '欢迎访问我的博客首页'
    })
"""


def index(request):
    article_list = Article.objects.all()
    context = {'article_list': article_list}
    return render(request, 'blog/index.html', context)

'''获取数据库中文章 id 为该值的记录，然后传递给模板。
注意这里我们用到了从 django.shortcuts 模块导入的 get_object_or_404 方法，
其作用就是当传入的 pk 对应的 Post 在数据库存在时，就返回对应的 post，
如果不存在，就给用户返回一个 404 错误，表明用户请求的文章不存在。'''


def detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.context = markdown.markdown(article.context,
                                  extensions=[
                                      'markdown.extensions.extra',#extra 本身包含很多拓展，
                                      'markdown.extensions.codehilite',#而 codehilite 是语法高亮拓展，这为我们后面的实现代码高亮功能提供基础，
                                      #代码高亮，且换行，在引用```时，要在大写情况下才生效！！！
                                      #代码高亮，且换行，在引用```时，要在大写情况下才生效！！！
                                      'markdown.extensions.toc',#而 toc 则允许我们自动生成目录（在以后会介绍）。
                                  ])
    form = CommentsForm()
    # 获取这篇 post 下的全部评论
    comment_list = article.comment_set.all()
    context = {'article': article,
               'comment_list': comment_list,
               'form': form,

               }
    return render(request, 'blog/detail.html', context)

'''这样我们在模板中展示 {{ post.body }} 的时候，就不再是原始的 Markdown 文本了，
而是渲染过后的 HTML 文本。注意这里我们给 markdown 渲染函数传递了额外的参数 extensions，
它是对 Markdown 语法的拓展，这里我们使用了三个拓展，分别是 extra、codehilite、toc。extra 本身包含很多拓展，
而 codehilite 是语法高亮拓展，这为我们后面的实现代码高亮功能提供基础，而 toc 则允许我们自动生成目录（在以后会介绍）。
来测试一下效果，进入后台，这次我们发布一篇用 Markdown 语法写的测试文章看看，
你可以使用以下的 Markdown 测试代码进行测试，也可以自己书写你喜欢的 Markdown 文本。
假设你是 Markdown 新手参考一下这些教程，一定学一下，保证你可以在 5 分钟内掌握常用的语法格式，
而以后对你写作受用无穷。可谓充电五分钟，通话 2 小时。以下是我学习中的一些参考资料：
https://www.appinn.com/markdown/    https://www.jianshu.com/p/1e402922ee32/ 
'''


def archives(request, year, month):
    article_list = Article.objects.filter(create_time__year=year,
                                          create_time__month=month).order_by('-create_time')#create_time中的属性是两个下划线,注意
    context = {'article_list': article_list}
    return render(request, 'blog/index.html', context)
'''这里我们使用了模型管理器（objects）的 filter 函数来过滤文章。
由于是按照日期归档，因此这里根据文章发表的年和月来过滤。
具体来说，就是根据 created_time 的 year 和 month 属性过滤，
筛选出文章发表在对应的 year 年和 month 月的文章。
注意这里 created_time 是 Python 的 date 对象，其有一个 year 和 month 属性，
我们在 页面侧边栏：使用自定义模板标签 使用过这个属性。Python 中类实例调用属性的方法通常是 created_time.year，
但是由于这里作为函数的参数列表，所以 Django 要求我们把点替换成了两个下划线，即 created_time__year。
同时和 index 视图中一样，我们对返回的文章列表进行了排序。
此外由于归档的下的文章列表的显示和首页是一样的，因此我们直接渲染了index.html 模板。'''


def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    article_list = Article.objects.filter(category=cate)
    context = {'article_list': article_list}
    return render(request, 'blog/index.html', context)

'''这里我们首先根据传入的 pk 值（也就是被访问的分类的 id 值）从数据库中获取到这个分类。
get_object_or_404 函数和 detail 视图中一样，其作用是如果用户访问的分类不存在，
则返回一个 404 错误页面以提示用户访问的资源不存在。
然后我们通过 filter 函数过滤出了该分类下的全部文章。
同样也和首页视图中一样对返回的文章列表进行了排序。'''