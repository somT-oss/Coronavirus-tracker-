from django.shortcuts import render
from .models import CountryName
from .form import EnterCountry
from django.contrib import messages
import covid19_data
import requests



def home_view(request):
    # Handling Nigeria covid data 
    url = "https://nigeria-covid-19.p.rapidapi.com/api/states"

    nigeria_covid_info = []

    headers = {
        'x-rapidapi-host': "nigeria-covid-19.p.rapidapi.com",
        'x-rapidapi-key': "c1a059f87emsh26a81e2d8d51a85p11018ajsnbbe48df9b6bb"
        }

    response = requests.request("GET", url, headers=headers).json()
    for dict in response:
        dict_info =  {
            "id": dict['id'],
            "State": dict["States"],
            "cases": dict["No_of_cases"],
            "Admitted": dict["No_on_admission"],
            "Discharged": dict["No_discharged"],
            "Death": dict["No_of_deaths"]
        }
        nigeria_covid_info.append(dict_info)

    # Handling user entry data         
    if request.method == "POST":
        form = EnterCountry(request.POST)
        if form.is_valid():
            form.save()
            form = EnterCountry()
    else:
        form = EnterCountry()

    countries = CountryName.objects.all()
    list_data = [] 
    for country in countries: 
        try:
            data = covid19_data.dataByName(country.country_name)
            dict_data = {
                "confirmed_cases": data.confirmed,
                "deaths": data.deaths,
                "active_cases": data.cases,
                "recovered_cases": data.recovered,
                "caller": data.caller,
            }
            list_data.append(dict_data)

        except Exception:
            wrong_entry = CountryName.objects.all().last()
            error_message = messages.error(request, f"Sorry could'nt pull up covid status on {wrong_entry }")
            get_error = CountryName.objects.all().last().delete()

    context = {
            "items": list_data,
            "search_form": form,
            "covid_info": nigeria_covid_info
        }

    return render(request, 'home.html', context)



# Create your views here.


