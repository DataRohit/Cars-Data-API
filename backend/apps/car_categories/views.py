import random
from django.db.models import Q
from rest_framework.views import APIView
from .models import CarCategory
from .serializers import CarCategorySerializer
from rest_framework.response import Response
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class CarCategoryListView(APIView):
    serializer_class = CarCategorySerializer

    @swagger_auto_schema(
        operation_id="list_car_categories",
        manual_parameters=[
            openapi.Parameter(
                name="offset",
                default=0,
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Offset for pagination",
                required=False,
            ),
            openapi.Parameter(
                name="limit",
                default=None,
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Limit for pagination",
                required=False,
            ),
        ],
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="List of Car Categories",
                schema=CarCategorySerializer(many=True),
            ),
            status.HTTP_400_BAD_REQUEST: "Invalid offset or limit value. Offset and limit should be non-negative integers.",
        },
        tags=["Car Categories"],
    )
    def get(self, request, *args, **kwargs):
        offset = int(request.query_params.get("offset", 0))
        limit_param = request.query_params.get("limit", None)

        if offset < 0 or (limit_param is not None and not limit_param.isdigit()):
            return Response(
                {
                    "detail": "Invalid offset or limit value. Offset and limit should be non-negative integers."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        limit = int(limit_param) if limit_param is not None else None

        if limit is not None and limit >= 0:
            queryset = CarCategory.objects.all()[offset : offset + limit]
        else:
            queryset = CarCategory.objects.all()

        serializer = CarCategorySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CarCategoryAddView(APIView):
    serializer_class = CarCategorySerializer

    @swagger_auto_schema(
        operation_id="add_car_category",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "category_name": openapi.Schema(type=openapi.TYPE_STRING),
                "baseline_parameters": openapi.Schema(type=openapi.TYPE_OBJECT),
                "description": openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=["category_name", "baseline_parameters", "description"],
        ),
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description="Car Category Created",
                schema=CarCategorySerializer(),
            ),
            status.HTTP_400_BAD_REQUEST: "Invalid input",
        },
        tags=["Car Categories"],
    )
    def post(self, request, *args, **kwargs):
        serializer = CarCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CarCategorySearchView(APIView):
    serializer_class = CarCategorySerializer

    @swagger_auto_schema(
        operation_id="search_car_category",
        manual_parameters=[
            openapi.Parameter(
                name="search",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Car Category UUID to search",
                required=False,
            ),
        ],
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Car Category Found",
                schema=CarCategorySerializer(),
            ),
            status.HTTP_404_NOT_FOUND: "Car Category not found",
        },
        tags=["Car Categories"],
    )
    def get(self, request, *args, **kwargs):
        search_param = request.query_params.get("search", None)

        if search_param is not None:
            try:
                category_instance = CarCategory.objects.get(id=search_param)
                serializer = CarCategorySerializer(category_instance)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except:
                categories = CarCategory.objects.filter(
                    Q(category_name__icontains=search_param)
                    | Q(description__icontains=search_param)
                )
                if len(categories) > 0:
                    serializer = CarCategorySerializer(categories, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)

        all_categories = CarCategory.objects.all()
        if len(all_categories) > 0 and search_param == None:
            random_category = random.choice(all_categories)
            serializer = CarCategorySerializer(random_category)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # No categories in the database
        return Response(
            {"detail": "No Car Categories found in the database."},
            status=status.HTTP_404_NOT_FOUND,
        )


class CarCategoryUpdateView(APIView):
    serializer_class = CarCategorySerializer

    @swagger_auto_schema(
        operation_id="update_car_category",
        request_body=CarCategorySerializer,
        manual_parameters=[
            openapi.Parameter(
                name="category_id",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Category UUID to search",
                required=True,
            ),
        ],
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Car Category Updated",
                schema=CarCategorySerializer(),
            ),
            status.HTTP_404_NOT_FOUND: "Car Category not found",
            status.HTTP_400_BAD_REQUEST: "Invalid input",
        },
        tags=["Car Categories"],
    )
    def put(self, request, *args, **kwargs):
        category_id = request.query_params.get("category_id", None)

        try:
            category_instance = CarCategory.objects.get(id=category_id)
        except CarCategory.DoesNotExist:
            return Response(
                {"detail": "Car Category not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = CarCategorySerializer(
            category_instance, data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CarCategoryDeleteView(APIView):
    serializer_class = CarCategorySerializer

    @swagger_auto_schema(
        operation_id="delete_car_category",
        manual_parameters=[
            openapi.Parameter(
                name="category_id",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="ID or Keyword to search",
                required=True,
            ),
        ],
        responses={
            status.HTTP_204_NO_CONTENT: "Car Category Deleted",
            status.HTTP_404_NOT_FOUND: "Car Category not found",
        },
        tags=["Car Categories"],
    )
    def delete(self, request, *args, **kwargs):
        category_id = request.query_params.get("category_id", None)

        try:
            category_instance = CarCategory.objects.get(id=category_id)
        except CarCategory.DoesNotExist:
            return Response(
                {"detail": "Car Category not found"}, status=status.HTTP_404_NOT_FOUND
            )

        category_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
