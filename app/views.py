from django.shortcuts import render, redirect
from .package_vin.data import *
import json


def index(request):
    if request.method == 'POST':
        vin_number = request.POST['vin']
        if len(vin_number) != 17:
            return render(request, 'app/index.html', {'message': 'Invalid VIN number!'})
        return redirect(f'/{vin_number}')
    return render(request, 'app/index.html')


def decodeVin(request, vin):
    if len(vin) != 17:
        return redirect('/')
    result = vin_decoder(vin)
    context = {"data": result}
    return render(request, 'app/vin.html', context)


def vin_decoder(vin_number):
    result = {}
    check = False

    # Length validation
    if len(vin_number) != 17:
        return "Invalid Vin Number"
    
    # check for Ford Vin number
    if vin_number[1] != 'F':
        return "Invalid Ford Vin Number!"

    # check build region
    for i in REGIONS.keys():
        if vin_number[0] in i:
            check = True
            result['region'] = REGIONS[i]
    
    if (not check):
        result['region'] = 'N/A'
    check = False

    # check World Manufacturer Identifier (WMI)
    if vin_number[:3] in WMI:
        check = True
        result['wmi'] = WMI[vin_number[:3]]
    
    if not check:
        result['wmi'] = 'N/A'
    check = False

    # check vehicle security systems
    if vin_number[3] in SECURITY_SYSTEMS:
        check = True
        result['security_system'] = SECURITY_SYSTEMS[vin_number[3]]

    if not check:
        result['security_system'] = 'N/A'
    check = False

    # check vehicle model
    if vin_number[4:7] in MODEL_3:
        check = True
        result['model'] = MODEL_3[vin_number[4:7]]
    elif vin_number[4:6] in MODEL_2:
        check = True
        result['model'] = MODEL_2[vin_number[4:6]]
    elif vin_number[4] in MODEL_1:
        check = True
        result['model'] = MODEL_1[vin_number[4]]

    if not check:
        result['model'] = 'N/A'
    check = False

    #check model year
    if vin_number[6].isnumeric():
        if vin_number[9] in MODEL_YEAR_OLD:
            check = True
            result['model_year'] = MODEL_YEAR_OLD[vin_number[9]]
    else:
        check = True
        result['model_year'] = MODEL_YEAR_NEW[vin_number[9]]
    
    if not check:
        result['model_year'] = 'N/A'
    check = False

    # check vehicle assembly plant
    if vin_number[10] in ASSEMBLY_PLANT:
        check = True
        result['assembly_plant'] = ASSEMBLY_PLANT[vin_number[10]]

    if not check:
        result['assembly_plant'] = 'N/A'
    check = False

    # vehicle serial number
    result['serial_number'] = vin_number[11:]
    
    return result
