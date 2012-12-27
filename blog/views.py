from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import render_to_response

from blog.models import *


def index(request):
    posts = Post.objects.all().order_by("-created_at")
    paginator = Paginator(posts, 10)

    try: page = int(request.GET.get('page', '1'))
    except ValueError: page = 1

    try: posts = paginator.page(page)
    except (InvalidPage, EmptyPage):
        posts = paginator.page(paginator.num_pages)

    return render_to_response('blog/list.html', dict(posts=posts, user=request.user))
