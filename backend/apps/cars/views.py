import random
from django.db.models import Q
from rest_framework.views import APIView
from .models import Car
from .serializers import CarSerializer
from rest_framework.response import Response
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class CarsListView(APIView):
    serializer_class = CarSerializer

    @swagger_auto_schema(
        operation_id="list_cars",
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
                description="List of Cars",
                schema=CarSerializer(many=True),
            ),
            status.HTTP_400_BAD_REQUEST: "Invalid offset or limit value. Offset and limit should be non-negative integers.",
        },
        tags=["Cars"],
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
            queryset = Car.objects.all()[offset : offset + limit]
        else:
            queryset = Car.objects.all()

        serializer = CarSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CarsAddView(APIView):
    serializer_class = CarSerializer

    @swagger_auto_schema(
        operation_id="add_car",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "manufacturer": openapi.Schema(type=openapi.TYPE_STRING),
                "model": openapi.Schema(type=openapi.TYPE_STRING),
                "launch_year": openapi.Schema(type=openapi.TYPE_INTEGER),
                "engine_config": openapi.Schema(type=openapi.TYPE_OBJECT),
                "features": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_STRING),
                ),
                "colors": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_STRING),
                ),
                "categories": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_STRING),
                ),
                "starting_price": openapi.Schema(type=openapi.TYPE_NUMBER),
            },
            required=[
                "manufacturer",
                "model",
                "launch_year",
                "engine_config",
                "features",
                "categories",
                "starting_price",
            ],
        ),
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description="Car Created",
                schema=CarSerializer(),
            ),
            status.HTTP_400_BAD_REQUEST: "Invalid input",
        },
        tags=["Cars"],
    )
    def post(self, request, *args, **kwargs):
        serializer = CarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CarSearchView(APIView):
    serializer_class = CarSerializer

    @swagger_auto_schema(
        operation_id="search_car",
        manual_parameters=[
            openapi.Parameter(
                name="search",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="ID or Keyword to search",
                required=False,
            ),
        ],
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Car Found",
                schema=CarSerializer(),
            ),
            status.HTTP_404_NOT_FOUND: "Car not found",
        },
        tags=["Cars"],
    )
    def get(self, request, *args, **kwargs):
        search_param = request.query_params.get("search", None)

        if search_param is not None:
            try:
                car_instance = Car.objects.get(id=search_param)
                serializer = CarSerializer(car_instance)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except:
                categories = Car.objects.filter(
                    Q(manufacturer__icontains=search_param)
                    | Q(model__icontains=search_param)
                    | Q(engine_config__contains={"motor_type": search_param})
                    | Q(engine_config__contains={"drive_system": search_param})
                    | Q(engine_config__contains={"transmission": search_param})
                    | Q(features__icontains=search_param)
                    | Q(colors__icontains=search_param)
                    | Q(categories__icontains=search_param)
                )
                if len(categories) > 0:
                    serializer = CarSerializer(categories, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)

        all_cars = Car.objects.all()
        if len(all_cars) > 0 and search_param == None:
            random_car = random.choice(all_cars)
            serializer = CarSerializer(random_car)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # No categories in the database
        return Response(
            {"detail": "No Car found in the database."},
            status=status.HTTP_404_NOT_FOUND,
        )


class CarUpdateView(APIView):
    serializer_class = CarSerializer

    @swagger_auto_schema(
        operation_id="update_car",
        request_body=CarSerializer,
        manual_parameters=[
            openapi.Parameter(
                name="car_id",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Car UUID to search",
                required=True,
            ),
        ],
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Car Updated",
                schema=CarSerializer(),
            ),
            status.HTTP_404_NOT_FOUND: "Car not found",
            status.HTTP_400_BAD_REQUEST: "Invalid input",
        },
        tags=["Cars"],
    )
    def put(self, request, *args, **kwargs):
        car_id = request.query_params.get("car_id", None)

        try:
            car_instance = Car.objects.get(id=car_id)
        except Car.DoesNotExist:
            return Response(
                {"detail": "Car not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = CarSerializer(car_instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CarDeleteView(APIView):
    serializer_class = CarSerializer

    @swagger_auto_schema(
        operation_id="delete_car",
        manual_parameters=[
            openapi.Parameter(
                name="car_id",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Car UUID to search",
                required=True,
            ),
        ],
        responses={
            status.HTTP_204_NO_CONTENT: "Car Deleted",
            status.HTTP_404_NOT_FOUND: "Car not found",
        },
        tags=["Cars"],
    )
    def delete(self, request, *args, **kwargs):
        car_id = request.query_params.get("car_id", None)

        try:
            car_instance = Car.objects.get(id=car_id)
        except Car.DoesNotExist:
            return Response(
                {"detail": "Car Category not found"}, status=status.HTTP_404_NOT_FOUND
            )

        car_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
