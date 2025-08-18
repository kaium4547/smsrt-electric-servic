from django.http import JsonResponse
from .models import Division, District, Upazila, Union, Village

def get_divisions(request):
    qs = Division.objects.all().order_by('bn_name', 'name')
    data = [{'id': d.id, 'name': d.bn_name or d.name} for d in qs]
    return JsonResponse({'results': data})

def get_districts(request):
    division_id = request.GET.get('division_id')
    qs = District.objects.filter(division_id=division_id).order_by('bn_name', 'name')
    data = [{'id': d.id, 'name': d.bn_name or d.name} for d in qs]
    return JsonResponse({'results': data})

def get_upazilas(request):
    district_id = request.GET.get('district_id')
    qs = Upazila.objects.filter(district_id=district_id).order_by('bn_name', 'name')
    data = [{'id': u.id, 'name': u.bn_name or u.name} for u in qs]
    return JsonResponse({'results': data})

def get_unions(request):
    upazila_id = request.GET.get('upazila_id')
    qs = Union.objects.filter(upazila_id=upazila_id).order_by('bn_name', 'name')
    data = [{'id': u.id, 'name': u.bn_name or u.name} for u in qs]
    return JsonResponse({'results': data})

def get_villages(request):
    union_id = request.GET.get('union_id')
    qs = Village.objects.filter(union_id=union_id).order_by('bn_name', 'name')
    data = [{'id': v.id, 'name': v.bn_name or v.name} for v in qs]
    return JsonResponse({'results': data})

