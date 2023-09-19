from rest_framework.response import Response
from rest_framework.decorators import api_view

from articles.models import Article
from articles.serializers import ArticleSerializer


# Create your views here.
@api_view(['GET', 'POST'])
def index(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True) # article이 두 개 이상이 온다면, many=True 옵션을 붙여줘야 함. 리스트 형식으로 만들어줌
        return Response(serializer.data) # 그냥 serializer -> 오류 남. repretation(?)이 필요하기에, .data를 붙여줘야 함
    elif request.method == 'POST':
        serializer = ArticleSerializer(data = request.data) # 꼭 data = request.data !!!!
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)    # 저장한 데이터들 보여주기
        else:
            print(serializer.errors)
            return Response(serializer.errors)
        return Response()                       # 저장하고 나서 http status code, allow options, content-type, Vary 가 뜸
        