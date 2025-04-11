
from django.shortcuts import redirect, render

from django.shortcuts import render
from django.utils import timezone

from connection.views import get_connected_user
from directeur.models import ClDirecteur
from programme_visite.models import ClProgrammeVisite
from secretaire.models import ClSecretaire
from visite.models import ClVisite
from visiteur.models import ClVisiteur

def home_view(request):
    username = get_connected_user(request)

    # Assurez-vous que le nom d'utilisateur est disponible dans la session
    if not username:
        return redirect('login')  # Redirige vers la page de connexion si pas de nom d'utilisateur dans la session

    # Récupérer tous les directeurs, secrétaires, et visiteurs
    directeurs = ClDirecteur.objects.all()
    secretaires = ClSecretaire.objects.all()
    visiteurs = ClVisiteur.objects.all()

    # Récupérer les visites en cours, reportées, et du jour
    visites_en_cours = ClVisite.objects.filter(tsttvst='confirmé', ddvst__gte=timezone.now()).order_by('ddvst')
    programmes_reportes = ClProgrammeVisite.objects.filter(tsttpvst='annulé').order_by('ddpvst')
    visites_du_jour = ClVisite.objects.filter(ddvst=timezone.now().date()).order_by('hvst')
    programmes =ClProgrammeVisite.objects.all().order_by()
    # Récupérer les visites de la semaine et du mois
    today = timezone.now().date()
    start_of_week = today - timezone.timedelta(days=today.weekday())
    end_of_week = start_of_week + timezone.timedelta(days=6)
    start_of_month = today.replace(day=1)
    
    visites_de_la_semaine = ClVisite.objects.filter(ddvst__range=[start_of_week, end_of_week]).order_by('ddvst')
    visites_du_mois = ClVisite.objects.filter(ddvst__month=today.month, ddvst__year=today.year).order_by('ddvst')

    # Contexte avec les données à passer au template
    context = {
           'username':username, 
        'directeurs': directeurs,
        'secretaires': secretaires,
        'visiteurs': visiteurs,
        'programmes':programmes,
        'visites_en_cours': visites_en_cours,
        'programmes_reportes': programmes_reportes,
        'visites_du_jour': visites_du_jour,
        'visites_de_la_semaine': visites_de_la_semaine,
        'visites_du_mois': visites_du_mois,
        'start_of_month':start_of_month
    }

    # Rendre la vue avec le template 'home.html' et passer les données au contexte
    return render(request, "home.html", context)
