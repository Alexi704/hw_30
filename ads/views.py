from ads.serializers import AdSerializer, CategorySerializer, AdCreateSerializer, AdUpdateSerializer, \
    AdDeleteSerializer, CategoryDetailSerializer, CategoryCreateSerializer, CategoryUpdateSerializer, \
    CategoryDeleteSerializer
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from hw30_project_config import settings
from ads.models import Ad, Category
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from users.models import User


def index(request):
    return JsonResponse({"main page": "status ok"}, status=200)


class CategoryViewSet(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailView(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer


class CategoryCreateView(CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer


class CategoryUpdateView(UpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryUpdateSerializer


class CategoryDeleteView(DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDeleteSerializer


class AdListView(ListAPIView):
    """
    Получение списка всех объявлений.
    """
    queryset = Ad.objects.all()
    serializer_class = AdSerializer

    def get(self, request, *args, **kwargs):

        self.queryset = self.queryset.select_related('author', 'category').order_by('-price')

        search_categories = request.GET.getlist("cat", [])
        if search_categories:
            self.queryset = self.queryset.filter(category_id__in=search_categories)

        search_text = request.GET.get('text', None)
        if search_text:
            self.queryset = self.queryset.filter(name__icontains=search_text)

        search_location = request.GET.get("location", None)
        if search_location:
            self.queryset = self.queryset.filter(author__locations__name__icontains=search_location)

        if request.GET.get("price_from", None):
            self.queryset = self.queryset.filter(price__gte=request.GET.get("price_from"))

        if request.GET.get("price_to", None):
            self.queryset = self.queryset.filter(price__lte=request.GET.get("price_to"))

        self.queryset = self.queryset.select_related('author').order_by("-price")
        paginator = Paginator(self.queryset, settings.REST_FRAMEWORK['PAGE_SIZE'])
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return super().get(request, *args, **kwargs)


class AdDetailView(RetrieveAPIView):
    """
    Получение объявления по id.
    """
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    # permission_classes = [IsAuthenticated]


class AdCreateView(CreateAPIView):
    """
    Создание объявления.
    """
    queryset = Ad.objects.all()
    serializer_class = AdCreateSerializer


class AdUpdateView(UpdateAPIView):
    """
    Обновление объявления.
    """
    queryset = Ad.objects.all()
    serializer_class = AdUpdateSerializer


class AdDeleteView(DestroyAPIView):
    """
    Удаление объявления.
    """
    queryset = Ad.objects.all()
    serializer_class = AdDeleteSerializer


@method_decorator(csrf_exempt, name='dispatch')
class AdUpLoadImageView(UpdateView):
    model = Ad
    fields = ['image']

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.image = request.FILES.get('image', None)
        self.object.save()

        response = {
            'id': self.object.id,
            'name': self.object.name,
            'author_id': self.object.author_id,
            'author': self.object.author.first_name,
            'price': self.object.price,
            'description': self.object.description,
            'is_published': self.object.is_published,
            'category_id': self.object.category_id,
            'image': self.object.image.url if self.object.image else None,
        }
        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False})
