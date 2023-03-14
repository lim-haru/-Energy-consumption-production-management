from django.shortcuts import render
from .models import Energy
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serailizer import EnergySerializer
from django.core.paginator import Paginator
from django.core.cache import cache

class EnergyDetail(APIView):
    def get(self, request):
        if cache.get('energy'):
            obj = cache.get('energy')
        else:
            obj = Energy.objects.all().order_by('-datetime')
            cache.set('energy', obj)

        serialzier = EnergySerializer(obj, many=True)
        return Response(serialzier.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = EnergySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete('energy')
            cache.delete('totProduced')
            cache.delete('totConsumed')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class EnergyInfo(APIView):
    def get(self, request, id):
        try:
            obj = Energy.objects.get(id=id)
        except Energy.DoesNotExist:
            msg = {"msg": "Not found"}
            return Response(msg, status=status.HTTP_404_NOT_FOUND)

        serializer = EnergySerializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

def home(request):
    if cache.get('energy'):
        energy = cache.get('energy')
        totProduced = cache.get('totProduced')
        totConsumed = cache.get('totConsumed')
    else:
        energy = Energy.objects.all().order_by('-datetime')
        cache.set('energy', energy, 60*15)

        totProduced = 0
        totConsumed = 0
        for p in energy:
            totProduced += p.produced_energy_in_watt
        for c in energy:
            totConsumed += c.consumed_energy_in_watt
        cache.set('totProduced', totProduced, 60*15)
        cache.set('totConsumed', totConsumed, 60*15)

    if request.method == "GET":
        search = request.GET.get('search')
        if search:
            energy = energy.filter(txId=search).values()

    paginator = Paginator(energy, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'totProduced': round(totProduced, 2),
        'totConsumed': round(totConsumed, 2),
    }
    return render(request, 'home.html', context)