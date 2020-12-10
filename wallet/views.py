from django.shortcuts import render, redirect, reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
import json
import jwt
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import IsAuthenticated
from .authentication import ClientTokenAuthentication
from rest_framework.decorators import api_view, authentication_classes
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_403_FORBIDDEN,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_401_UNAUTHORIZED,
    HTTP_201_CREATED
)
from rest_framework import generics
from wallet.models import *
from wallet.serializers import *
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import datetime

today = datetime.date.today()


@api_view(["POST"])
def ClientLogin(request):
    if not request.data:
        return Response({'Error': "Please provide username/password"}, status="400")

    username = request.data['email']
    password = request.data['password']
    try:
        user = User.objects.get(email=username)


        if user.is_active == False:
            return Response({'Error': "User is not verified"}, status="400")

        password = check_password(password=password, encoded=user.password)
        if password == False:
            return Response({'Error': "Password is not verified"}, status="400")


    except User.DoesNotExist:
        return Response({'Error': "Invalid username/password"}, status="400")

    if user and password:
        payload = {
            'id': user.id,
            'email': user.email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=8),
            'first_name': user.first_name,

        }
        jwt_token = {'token': jwt.encode(payload, "SECRET").decode("utf-8")}

        return HttpResponse(
            json.dumps(jwt_token),
            status=200,
            content_type="application/json"
        )
    else:
        return Response(
            json.dumps({'Error': "Missing data for required field."}),
            status=403,
            content_type="application/json"
        )


class MyWallet(APIView):
    authentication_classes = [ClientTokenAuthentication]
    def post(self, request):
        try:
            if Wallet.objects.filter(owned = request.user).count() > 0:
                wal_obj = Wallet.objects.get(owned = request.user,status="disabled")
                wal_obj.status = "enabled"
                wal_obj.save()
            else:
                wallet = Wallet()
                wallet.owned = request.user
                wallet.save()
            wallet = Wallet.objects.filter(owned = request.user,status="enabled")
            listserializer = ListWalletSerializer(wallet,many =True)
            return Response({'status':"success","data":{"wallet":listserializer.data} })    
        except:
            return Response({'status':"fail",'data':{"error": "Disabled"}})
       
    # @authentication_classes((ClientTokenAuthentication,))
    def get(self, request):
        try:
            wallet = Wallet.objects.filter(owned = request.user,status="enabled")
            serializer = ListWalletSerializer(wallet,many =True)
            if serializer.data:
                return Response({'status':"success","data":{"wallet":serializer.data} })
            else:
                return Response({'status':"fail","data":{"error": "Disabled"}})
        except:
            return Response({'status':"fail","data":{"error": "Disabled"}})

    def patch(self, request):
        try:
            if Wallet.objects.filter(owned = request.user,status="enabled").count() > 0:
                wal_obj = Wallet.objects.get(owned = request.user,status="enabled")
                wal_obj.status = "disabled"
                wal_obj.save()
                wallet = Wallet.objects.filter(owned = request.user,status="disabled")
                listserializer = ListWalletSerializer(wallet,many =True)
                return Response({'status':"success","data":{"wallet":listserializer.data} })
            else:
                wallet = Wallet()
                wallet.owned = request.user
                wallet.save()
        except:
            return Response({'status':"fail",'data':{"error": "Disabled"}})
        


class Deposits(APIView):
    authentication_classes = [ClientTokenAuthentication]
    def post(self, request):
        if request.data:
            wallet = Wallet.objects.filter(owned = request.user,status="enabled")
            listserializer = DepositSerializer(wallet,many =True)
            
            try:
                if wallet.count() > 0:
                    walletobj = Wallet.objects.get(owned = request.user)
                    balance = Balance()
                    balance.type = "Deposit"
                    balance.amount = request.data['amount'] 
                    balance.deposited_by = request.user
                    balance.reference_id = walletobj.walletid + '-' + 'deposit' 
                    balance.save()
                    walletobj.balance.add(balance)
                    walletobj.save()                    
                    
                    return Response({'status':"success","data":{"wallet":listserializer.data} })
                else:
                    return Response({'status':"fail",'data':{"error": "Disabled"}})

            except:
                return Response({'status':"fail",'data':{"error": "Disabled"}})
        else:
            return Response({'status':"Something went wrong. Please try again later",'data':[]})

class Withdrawal(APIView):
    authentication_classes = [ClientTokenAuthentication]
    def post(self, request):
        wallet = Wallet.objects.filter(owned = request.user,status="enabled")
        listserializer = WidrawalSerializer(wallet,many =True)
        if wallet.count() > 0:
                        
            try:
                walletobj = Wallet.objects.get(owned = request.user)
                if int(request.data['amount']) > walletobj.balance_amount():
                     return Response({'status':"fail",'data':{"error": "No Balance"}})
                else:
                    balance = Balance()
                    balance.type = "Withdrawal"
                    balance.amount = request.data['amount'] 
                    balance.deposited_by = request.user
                    balance.reference_id = walletobj.walletid+ '-' + 'withdrawal'
                    balance.save()
                    walletobj.balance.add(balance)
                    walletobj.save()                    
                    
                    return Response({'status':"success","data":{"wallet":listserializer.data} })
            except:
                return Response({'status':"fail",'data':{"error": "Disabled"}})
        else:
            return Response({'status':"fail",'data':{"error": "Disabled"}})
