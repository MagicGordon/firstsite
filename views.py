from django.shortcuts import render
from block.models import Block


def index(request):

    # block_infos = Block.objects.all().order_by("-id")
    block_infos = Block.objects.filter(status=0).order_by("-id")
    return render(request, "index.html", {"blocks": block_infos})
