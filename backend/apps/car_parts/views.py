import random
from django.db.models import Q
from rest_framework.views import APIView
from .models import CarPart
from .serializers import CarPartSerializer
from rest_framework.response import Response
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class PartsListView(APIView):
    serializer_class = CarPartSerializer

    @swagger_auto_schema(
        operation_id="list_parts",
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
                description="List of Parts",
                schema=CarPartSerializer(many=True),
            ),
            status.HTTP_400_BAD_REQUEST: "Invalid offset or limit value. Offset and limit should be non-negative integers.",
        },
        tags=["Car Parts"],
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
            queryset = CarPart.objects.all()[offset : offset + limit]
        else:
            queryset = CarPart.objects.all()

        serializer = CarPartSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PartAddView(APIView):
    serializer_class = CarPartSerializer

    @swagger_auto_schema(
        operation_id="add_part",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "part_name": openapi.Schema(type=openapi.TYPE_STRING),
                "part_number": openapi.Schema(type=openapi.TYPE_STRING),
                "description": openapi.Schema(type=openapi.TYPE_STRING),
                "manufacturer": openapi.Schema(type=openapi.TYPE_STRING),
                "price": openapi.Schema(type=openapi.TYPE_NUMBER),
            },
            required=["part_name", "part_number", "manufacturer", "price"],
        ),
        responses={
            201: openapi.Response(description="Part Created", schema=CarPartSerializer),
            400: "Invalid input",
        },
        tags=["Car Parts"],
    )
    def post(self, request, *args, **kwargs):
        serializer = CarPartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PartSearchView(APIView):
    serializer_class = CarPartSerializer

    @swagger_auto_schema(
        operation_id="search_part",
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
                schema=CarPartSerializer(),
            ),
            status.HTTP_404_NOT_FOUND: "Part not found",
        },
        tags=["Car Parts"],
    )
    def get(self, request, *args, **kwargs):
        search_param = request.query_params.get("search", None)

        if search_param is not None:
            try:
                car_part_instance = CarPart.objects.get(id=search_param)
                serializer = CarPartSerializer(car_part_instance)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except:
                parts = CarPart.objects.filter(
                    Q(manufacturer__icontains=search_param)
                    | Q(part_name__icontains=search_param)
                    | Q(part_number__icontains=search_param)
                    | Q(description__icontains=search_param)
                )
                if len(parts) > 0:
                    serializer = CarPartSerializer(parts, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)

        all_parts = CarPart.objects.all()
        if len(all_parts) > 0 and search_param == None:
            random_part = random.choice(all_parts)
            serializer = CarPartSerializer(random_part)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # No categories in the database
        return Response(
            {"detail": "No part found in the database."},
            status=status.HTTP_404_NOT_FOUND,
        )


class PartUpdateView(APIView):
    serializer_class = CarPartSerializer

    @swagger_auto_schema(
        operation_id="update_part",
        request_body=CarPartSerializer,
        manual_parameters=[
            openapi.Parameter(
                name="part_id",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Part UUID to search",
                required=True,
            ),
        ],
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Part Updated",
                schema=CarPartSerializer(),
            ),
            status.HTTP_404_NOT_FOUND: "Part not found",
            status.HTTP_400_BAD_REQUEST: "Invalid input",
        },
        tags=["Car Parts"],
    )
    def put(self, request, *args, **kwargs):
        part_id = request.query_params.get("part_id", None)

        try:
            car_part_instance = CarPart.objects.get(id=part_id)
        except CarPart.DoesNotExist:
            return Response(
                {"detail": "Part not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = CarPartSerializer(
            car_part_instance, data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PartDeleteView(APIView):
    serializer_class = CarPartSerializer

    @swagger_auto_schema(
        operation_id="delete_part",
        manual_parameters=[
            openapi.Parameter(
                name="part_id",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Part UUID to search",
                required=True,
            ),
        ],
        responses={
            status.HTTP_204_NO_CONTENT: "Part Deleted",
            status.HTTP_404_NOT_FOUND: "Part not found",
        },
        tags=["Car Parts"],
    )
    def delete(self, request, *args, **kwargs):
        part_id = request.query_params.get("part_id", None)

        try:
            car_part_instance = CarPart.objects.get(id=part_id)
        except CarPart.DoesNotExist:
            return Response(
                {"detail": "Part Category not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        car_part_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
