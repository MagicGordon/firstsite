from django.shortcuts import render
from django.shortcuts import redirect
from block.models import Block
from .models import Article
from .forms import ArticleForm

from django.views.generic import View, DetailView
from django.core.paginator import Paginator


def article_list(request, block_id):
    block_id = int(block_id)
    block = Block.objects.get(id=block_id)
    all_articles = Article.objects.filter(block=block, status=0).order_by("-id")

# 分页制作部分
    ARTICLE_CNT_1PAGE = 1
    page_no = int(request.GET.get("page_no", "1"))
    p = Paginator(all_articles, ARTICLE_CNT_1PAGE)
# 得出一页显示的内容
    page = p.page(page_no)
    articles_objs = page.object_list
# 目录用到的变量
    page_cnt = p.num_pages  # 总页数
    current_no = page_no  # 当前页码
    page_links = [i for i in range(page_no - 1, page_no + 1) if i > 0 and i <= p.num_pages]  # 当前页左右两边都不超过5页的页码list
    previous_link = page_links[0] - 1
    next_link = page_links[-1] + 1
    previous = (current_no - 1) if (current_no - 1) > 0 else 1
    next = (current_no + 1) if (current_no + 1) <= page_cnt else page_cnt
    has_previous = previous_link > 0
    has_next = next_link <= page_cnt
    page_data = {
            "page_cnt": page_cnt,
            "current_no": current_no,
            "page_links": page_links,
            "has_previous": has_previous,
            "has_next": has_next,
            "previous": previous,
            "next": next}
    return render(request, "article_list.html", {"articles": articles_objs, "b": block, "page_data": page_data})


class ArticleCreateView(View):
    template_name = "article_create.html"

    def init_data(self, block_id):
        self.block_id = block_id
        self.block = Block.objects.get(id=block_id)

    def get(self, request, block_id):
        self.init_data(block_id)
        return render(request, self.template_name, {"b": self.block})

    def post(self, request, block_id):
        self.init_data(block_id)
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.block = self.block
            article.status = 0
            article.save()
            return redirect("/article/list/%s" % self.block_id)
        else:
            return render(request, self.template_name, {"b": self.block, "form": form})


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_detail.html'
    context_object_name = 'a'
