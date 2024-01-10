from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class HomeView(APIView):
    @swagger_auto_schema(
        operation_id="home",
        manual_parameters=[
            openapi.Parameter(
                name="message",
                default="Welcome to Los Santos Customs API",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Enter a Message!",
                required=False,
            ),
        ],
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Message Received Successfully!",
            )
        },
        tags=["Home"],
    )
    def get(self, request, *args, **kwargs):
        message = request.query_params.get(
            "message", "Welcome to Los Santos Customs API"
        )

        response_data = {"message": message}

        return Response(response_data, status=status.HTTP_200_OK)
