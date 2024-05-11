from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import Group, User
from djoser.serializers import UserSerializer
from django.shortcuts import get_object_or_404

# Create your views here.
@api_view()
@permission_classes([IsAuthenticated])
def secure_view(request):
    return Response({"message": "success"}, status=status.HTTP_200_OK)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def managers(request):
    if not request.user.groups.filter(name="Managers").exists():
        return Response({"detail": "Forbidden: not enough priviliges"}, status=status.HTTP_403_FORBIDDEN)
    
    managers_user_set = Group.objects.get(name="Managers").user_set
    
    if request.method == "GET":
        serialized_users = UserSerializer(managers_user_set.all(), many=True)

        return Response(serialized_users.data, status=status.HTTP_200_OK)
    elif request.method == "POST":
        if "pk" not in request.data:
            return Response({"detail": "Bad Request: pk not presented"}, status=status.HTTP_400_BAD_REQUEST)
        pk = request.data.get("pk")
        user = get_object_or_404(User, pk=pk)
        managers_user_set.add(user)
        return Response({"detail": "User assigned to managers"}, status=status.HTTP_201_CREATED)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_manager(request, pk):
    if not request.user.groups.filter(name="Managers").exists():
        return Response({"detail": "Forbidden: not enough priviliges"}, status=status.HTTP_403_FORBIDDEN)

    manager_to_delete = get_object_or_404(User, pk=pk)
    Group.objects.get(name="Managers").user_set.remove(manager_to_delete)
    return Response({"detail": "Success"}, status=status.HTTP_200_OK)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def delivery_crew(request):
    if not request.user.groups.filter(name="Managers").exists():
        return Response({"detail": "Forbidden: not enough priviliges"}, status=status.HTTP_403_FORBIDDEN)
    
    delcrew_user_set = Group.objects.get(name="Delivery crew").user_set
    
    if request.method == "GET":
        serialized_users = UserSerializer(delcrew_user_set.all(), many=True)

        return Response(serialized_users.data, status=status.HTTP_200_OK)
    elif request.method == "POST":
        if "pk" not in request.data:
            return Response({"detail": "Bad Request: pk not presented"}, status=status.HTTP_400_BAD_REQUEST)
        pk = request.data.get("pk")
        user = get_object_or_404(User, pk=pk)
        delcrew_user_set.add(user)
        return Response({"detail": "User assigned to delivery crew"}, status=status.HTTP_201_CREATED)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_delivery_crew(request, pk):
    if not request.user.groups.filter(name="Managers").exists():
        return Response({"detail": "Forbidden: not enough priviliges"}, status=status.HTTP_403_FORBIDDEN)

    decrew_to_delete = get_object_or_404(User, pk=pk)
    Group.objects.get(name="Delivery crew").user_set.remove(decrew_to_delete)
    return Response({"detail": "Success"}, status=status.HTTP_200_OK)