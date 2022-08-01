from ads.permissions import AdEditPermission, SelectionEditPermission
from ads.serializers import AdSerializer, CategorySerializer, AdCreateSerializer, AdUpdateSerializer, \
    AdDeleteSerializer, CategoryDetailSerializer, CategoryCreateSerializer, CategoryUpdateSerializer, \
    CategoryDeleteSerializer, SelectionListSerializer, SelectionDetailSerializer, SelectionSerializer
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView

from hw30_project_config import settings
from ads.models import Ad, Category, Selection
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated


def index(request):
    return JsonResponse({"main page": "status ok"}, status=200)


class CategoryViewSet(ListAPIView):
    """Просмотр всех категорий"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailView(RetrieveAPIView):
    """Просмотр категории объявления по id категории"""
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer


class CategoryCreateView(CreateAPIView):
    """Создание новой категории"""
    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer


class CategoryUpdateView(UpdateAPIView):
    """Обновление существующей категории"""
    queryset = Category.objects.all()
    serializer_class = CategoryUpdateSerializer


class CategoryDeleteView(DestroyAPIView):
    """Удаление категории"""
    queryset = Category.objects.all()
    serializer_class = CategoryDeleteSerializer


class AdListView(ListAPIView):
    """Получение списка всех объявлений."""
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
    """Получение объявления по id."""
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticated]


class AdCreateView(CreateAPIView):
    """Создание объявления."""
    queryset = Ad.objects.all()
    serializer_class = AdCreateSerializer


class AdUpdateView(UpdateAPIView):
    """Обновление объявления."""
    queryset = Ad.objects.all()
    serializer_class = AdUpdateSerializer
    permission_classes = [IsAuthenticated, AdEditPermission]


class AdDeleteView(DestroyAPIView):
    """Удаление объявления."""
    queryset = Ad.objects.all()
    serializer_class = AdDeleteSerializer
    permission_classes = [IsAuthenticated, AdEditPermission]


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


class SelectionListView(ListAPIView):
    """Просмотр всех подборок по объявлениям."""
    queryset = Selection.objects.all()
    serializer_class = SelectionListSerializer


class SelectionDetailView(RetrieveAPIView):
    """Просмотр подбороки по ее id."""
    queryset = Selection.objects.all()
    serializer_class = SelectionDetailSerializer


class SelectionCreateView(CreateAPIView):
    """Создание подборки (только для зарегистрированных пользователей)."""
    queryset = Selection.objects.all()
    serializer_class = SelectionSerializer
    permission_classes = [IsAuthenticated]


class SelectionUpdateView(UpdateAPIView):
    """Обновление подборки по ее id. Только для владельцев подборки."""
    queryset = Selection.objects.all()
    serializer_class = SelectionSerializer
    permission_classes = [IsAuthenticated, SelectionEditPermission]


class SelectionDeleteView(DestroyAPIView):
    """Удаление подборки по ее id. Только для создателя подборки."""
    queryset = Selection.objects.all()
    serializer_class = SelectionSerializer
    permission_classes = [IsAuthenticated, SelectionEditPermission]
