# -*- coding: UTF-8 -*-

# Generated by Django 2.2.6 on 2019-11-04 17:15

# datamigrations: fill data on homepage

from django.db import migrations

def fill_pages(apps, schema_editor):
    HtmlContent = apps.get_model('pages', 'HtmlContent')
    data = [
        {'keyword': 'homepage-content', 'content': '<p>Celem gry jest maksymalizacja zwrotu z portfela projektów. Zwrot jest rozumiany jako stosunek zysków do kosztów.</p><p>Gra składa się z rund. W każdej rundzie generowane są losowo dane na temat dziewięciu projektów. Zadaniem gracza jest wybór trzech spośród dziewięciu podanych projektów, które łącznie tworzą portfel.</p><p>Po zatwierdzeniu portfela generowane są losowo rzeczywste zyski projektów. Losowanie odbywa się zgodnie z podanymi na wykresach rozkładami prawdopodobieństwa realizacji przychodów dla poszczególnych projektów.</p><p>Podgląd wykresów jest możliwy po kliknięciu odpowiedniego projektu. Przed zatwierdzeniem portfela można zobaczyć wykres funkcji zysków wszystkich portfeli względem ryzyka (mapa).</p>'},
    ]
    for el in data:
        if 'keyword' not in el:
            continue
        if 'content' not in el:
            continue
        hc = HtmlContent.objects.filter(keyword=el['keyword'])
        if hc.count() != 0:
            hc = hc[0]
        else:
            hc = HtmlContent()
            hc.keyword = el['keyword']
        hc.content = el['content']
        hc.save()
    return

class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(fill_pages),
    ]