from django.shortcuts import render
from .models import Guest,Movie,Reservation 
from rest_framework.decorators import api_view
from rest_framework.response import Response 
from .serializers import *
from rest_framework import status,filters
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import generics, mixins, viewsets





# Create your views here.
#1.1 GET POST
@api_view(['GET','POST'])
def FBV_List(request):

    #GET
    if request.method == 'GET':
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests,many=True)
        print(f'Serializer :{serializer.data}')
        return Response(serializer.data)
    #POST
    elif request.method == 'POST':
        serializer = GuestSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status= status.HTTP_201_CREATED)
        return Response(serializer.data,status= status.HTTP_400_BAD_REQUEST)

#1.2 GET PUT DELETE
@api_view(['GET','PUT','DELETE'])
def FBV_pk(request,pk):
    try:
        guest = Guest.objects.get(pk=pk)
    except Guest.DoesNotExist:
         return Response(status=status.HTTP_404_NOT_FOUND)

    #GET
    if request.method == "GET":
        serializer = GuestSerializer(guest,many=False)
        return Response(serializer.data)
    #PUT
    elif request.method == "PUT":
        serializer = GuestSerializer(guest,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == "DELETE":
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)     
    

#2.1 GET POST with Class based View

class CBV_List(APIView):
    def get(self , request):
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests,many=True)
        return Response(serializer.data)
    def post(self , request ):
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.data,
            status=status.HTTP_400_BAD_REQUEST
        )
            


#2.2 GET PUT DELETE with Class based View

class CBV_pk(APIView):
    def get_object(self , pk):
        try:
            return Guest.objects.get(pk=pk)
        except Guest.DoesNotExist:
            raise Http404
    def get(self,request,pk):
        guest = self.get_object(pk)
        serializer = GuestSerializer(guest,many=False)
        return Response(serializer.data)
    def put(self,request,pk):
        guest = self.get_object(pk)
        serializer = GuestSerializer(guest,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.error,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk):
        guest = self.get_object(pk)
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#3.1 GET POST with Mixins

class mixins_List(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    def get(self,request):
        return self.list(request)
    
    def post(self,request):
        return self.create(request)


#3.2 GET PUT DELETE with Mixins

class mixins_pk(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    def get(self,request , pk ):
        return self.retrieve(request)
    
    def put(self,request , pk):
        return self.update(request)

    def delete(self,request , pk):
        return self.destroy(request)
    

#4.1 GET POST with Generics

class generics_list(generics.ListCreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer


#4.2 GET PUT DELETE with Generics

class generics_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer