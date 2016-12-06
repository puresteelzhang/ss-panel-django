from django.shortcuts import render, redirect
from django.views.decorators.http import require_safe
from django.db.models import Sum
from django.contrib.auth.views import logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.forms import AdminAuthenticationForm

from .models import In, Out


@require_safe
def index_main(request):
    """可以将此页加为主站点的首页.

    可以将以下语句加入工程的 urls.py:

    import panel.views

    urlpatterns 内添加:

    url(r'^$', panel.views.index_main),
    url(r'^accounts/', include('django.contrib.auth.urls', namespace='auth')),
    """
    if request.user.is_authenticated():
        return redirect('panel:index')
    else:
        c = {
            'title': '首页',
            'info': '欢迎光临, 请登录.',
            'link_url': 'auth:login',
            'link_text': '登录',
        }
        return render(request, 'panel/info.html', c)


@require_safe
def quit(request):
    """logout"""
    logout(request)
    c = {
        'title': '退出成功',
        'info': '感谢您的使用, 再见.',
        'link_url': 'panel:index',
        'link_text': '重新登录',
    }
    return render(request, 'panel/info.html', c)


@require_safe
@login_required
def index(request):
    c = {
        'title': '首页',
        'user': request.user,
    }
    return render(request, 'panel/index.html', c)


@require_safe
@login_required
def status(request):
    """统计服务器状态, 属于管理页面."""
    c = {
        'title': '服务器状态',
    }
    return render(request, 'panel/status.html', c)


@require_safe
@login_required
def gold(request):
    """统计资金收支状态, 属于管理页面."""
    gold_in = In.objects.all().aggregate(Sum('num'))['num__sum']
    gold_out = Out.objects.all().aggregate(Sum('num'))['num__sum']
    gold_sum = gold_in + gold_out

    c = {
        'title': '资金状态',
        'gold_sum': gold_sum,
        'gold_in': gold_in,
        'gold_out': gold_out,
    }
    return render(request, 'panel/gold.html', c)


@require_safe
@login_required
def gold_method(request, method):
    """统计资金收支明细, 属于管理页面."""
    title = ''
    gold_sum = 0.0
    gold_list = []

    if method == 'in':
        title = '收入明细'
        gold_sum = In.objects.all().aggregate(Sum('num'))['num__sum']
        gold_list = In.objects.all().order_by('-date')
    elif method == 'out':
        title = '支出明细'
        gold_sum = Out.objects.all().aggregate(Sum('num'))['num__sum']
        gold_list = Out.objects.all().order_by('-date')

    c = {
        'title': title,
        'gold_sum': gold_sum,
        'gold_list': gold_list,
        'method': method,
    }
    return render(request, 'panel/gold_method.html', c)
