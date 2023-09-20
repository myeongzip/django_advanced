from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from django.http import Http404
from rest_framework.views import APIView
from articles.models import Article
from articles.serializers import ArticleSerializer
from drf_yasg.utils import swagger_auto_schema


# Create your views here.


class ArticleList(APIView):
    def get(self, request, format=None):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True) 
        return Response(serializer.data) 

    @swagger_auto_schema(request_body=ArticleSerializer) # swagger에 정확한 api 명세 정보를 위한 데코레이터
    def post(self, request, format=None):
        serializer = ArticleSerializer(data = request.data) # 꼭 data = request.data 지정해줘야 함.
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)    # 저장한 데이터들 보여주기
        else:
            print(serializer.errors)        # 개발 단계에선 error의 정보를 알면 좋지만, 실제에선 쓰면 X
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleDetail(APIView):
    def get(self, request, article_id, format=None):
        article = get_object_or_404(Article, id=article_id)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    def put(self, request, article_id, format=None):
        article = get_object_or_404(Article, id=article_id)
        serializer = ArticleSerializer(article, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, article_id, format=None):
        article = get_object_or_404(Article, id=article_id)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)