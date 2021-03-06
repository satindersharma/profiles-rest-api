from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from rest_framework import filters
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated

from . import serializers
from . import models
from . import permissions


''' token authentication is the most effective or most popular way
to authwnticate an api
it works by giving the temp token that insert in the headers of the http request
then django rest framework use this token to check that user has an authentictaion with the system
'''
'''here status contain the differnt status code list'''

'''
IsAuthenticated is quit similar to IsAuthenticatedOrReadOnly
except it don't let you  read only, you must be authenticated to use the api at all
'''


# Create your views here.
class HelloAPI(APIView):
    '''test api views'''

    serializer_class = serializers.HelloSerializer
    '''this tels djanfo rest framework serializer_class for this HelloAPI APIView is HelloSerializer in serializers'''

    def get(self, request, format=None):
        '''this is usedwhenever you wanna list of object from a spesfic api'''
        '''return a list of APIView features'''

        an_apiview = [
            'uses HTTP methods as function (get, post, patch, put, delete)',
            'It is similar to a traditional Django view',
            'GIves you the most control over your logic',
            'Is mapped manually to URLs',
        ]
        '''Response is to be dictionary which is converted to json which the output to the screen'''
        return Response({'message': 'Hello!', 'an_apiview': an_apiview})

    '''after discribing a calss serializer_class lest crate a post function
    
    '''
    def post(self, request):
        '''create a hello message with our name
        we  gona return a message that include he name that was posted to the api'''
        serializer = serializers.HelloSerializer(data=request.data)
        '''vaiddate the data'''
        if serializer.is_valid():
            '''this will get the name data'''
            name = serializer.data.get('name')
            message = 'Hello {0}'.format(name)
            return Response({'message':message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, pk=None):
        '''hanles updating an objects'''
        return Response({'method':'put'})

    def patch(self, request, pk=None):
        '''patch request, only updates fields provies in the request'''
        return Response({'method':'patch'})

    def delete(self, request, pk=None):
        '''delete an objects'''
        return Response({'method':'delete'})


class HelloViewset(viewsets.ViewSet):
    '''test api viewset'''
    serializer_class = serializers.HelloSerializer

    def list(self, request):
        '''return a hello message'''
        a_viewset = [
            'uses actions (list, create, retrieve, updae, partial_update',
            'Automatically maps to URLs using Routers',
            'Provides more functionality with less code.'
        ]

        return Response({'message': 'Hello', 'a_viewset': a_viewset})

    def create(self, request):
        """cerate a new hello message"""
        serializer = serializers.HelloSerializer(data=request.data)

        if serializer.is_valid():
            name = serializer.data.get('name')
            message = 'Hello {0}'.format(name)
            return Response({'message':message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        '''handles getting an objects by its id'''
        return Response({'http_method': 'GET'})

    def update(self, request, pk=None):
        '''handles updating an objects'''
        return Response({'http_method': 'PUT'})

    def partial_update(self, request, pk=None):
        '''handle update part of an object'''
        return Response({'http_method': 'PATCH'})

    def destroy(self, request, pk=None):
        '''handles removing an object.'''
        return Response({'http_method': 'DELETE'})


class UserProfileViewset(viewsets.ModelViewSet):
    '''handales creating reading and updating profiles'''
    serializer_class = serializers.UserProfileSerializer
    '''because UserProfileSerializer has a metadeta thats why this class now for which model it has to look for'''

    queryset = models.UserProfile.objects.all()
    '''(TokenAuthentication,) it cointains the all authentication types that is to used in our api
    and it is a tuple so it is imputable'''
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)


class LoginViewset(viewsets.ViewSet):
    ''' check email and password and return an auth token'''
    serializer_class = AuthTokenSerializer

    def create(self, request):
        '''use the obtaintoken APIview to valiadte and create'''
        return ObtainAuthToken().post(request)


class UserProfileFeedViewset(viewsets.ModelViewSet):
    '''handles creating reading and updating  profile feed items'''

    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    '''IsAuthenticatedOrReadOnly gives the user permission  to oto do anythig they want when they authenticated
    but it restrict them to only read only access if they are not authenticated
    
    if user try to update another status then it will run permissions.PostOwnStatus
    IsAuthenticatedOrReadOnly this helps to give only read only acces when they are not authenticated
    '''
    '''we are going to change it from
    permission_classes = (permissions.PostOwnStatus, IsAuthenticatedOrReadOnly)
    to
    permission_classes = (permissions.PostOwnStatus, IsAuthenticated)
    '''
    permission_classes = (permissions.PostOwnStatus, IsAuthenticated)


    def perform_create(self, serializer):
        '''sets the user profile to the looged in user'''

        serializer.save(user_profile=self.request.user)
