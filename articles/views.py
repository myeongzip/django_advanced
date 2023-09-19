from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from articles.models import Article
from articles.serializers import ArticleSerializer


# Create your views here.
@api_view(['GET', 'POST'])
def articleAPI(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True) # article이 두 개 이상이 온다면, many=True 옵션을 붙여줘야 함. 리스트 형식으로 만들어줌
        return Response(serializer.data) # 그냥 serializer -> 오류 남. repretation(?)이 필요하기에, .data를 붙여줘야 함
    elif request.method == 'POST':
        serializer = ArticleSerializer(data = request.data) # 꼭 data = request.data !!!!
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)    # 저장한 데이터들 보여주기
        else:
            print(serializer.errors)        # 개발 단계에선 error의 정보를 알면 좋지만, 실제에선 쓰면 X
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # return Response()                       # 저장하고 나서 http status code, allow options, content-type, Vary 가 뜸
        
@api_view(['GET', 'PUT', 'DELETE'])
def articleDetailAPI(request, article_id):
    if request.method == 'GET':
        # article = Article.objects.get(id=article_id)   # Article table에서 id를 가져와랏
        article = get_object_or_404(Article, id=article_id)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
    elif request.method == "PUT":
        article = get_object_or_404(Article, id=article_id)
        serializer = ArticleSerializer(article, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        article = get_object_or_404(Article, id=article_id)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

        