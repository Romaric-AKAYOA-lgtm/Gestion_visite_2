from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.conf import settings
from django.db.models import Q

from datetime import datetime
import zipfile
import io
import os

from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

from connection.views import get_connected_user
from .models import ClVisiteur
from .forms import ClVisiteurForm

# Affiche la liste des visiteurs
def visiteur_list(request):
    username = get_connected_user(request)

    # Assurez-vous que le nom d'utilisateur est disponible dans la session
    if not username:
        return redirect('login')  # Redirige vers la page de connexion si pas de nom d'utilisateur dans la session

    visiteurs = ClVisiteur.objects.all()
    return render(request, 'visiteur/visiteur_list.html', {  'username':username,'visiteurs': visiteurs})

# Affiche les détails d'un visiteur
def visiteur_detail(request, id):
    username = get_connected_user(request)

    # Assurez-vous que le nom d'utilisateur est disponible dans la session
    if not username:
        return redirect('login')  # Redirige vers la page de connexion si pas de nom d'utilisateur dans la session

    visiteur = get_object_or_404(ClVisiteur, id=id)
    return render(request, 'visiteur/visiteur_detail.html', {  'username':username,'visiteur': visiteur})

# Permet de créer un nouveau visiteur
def visiteur_create(request):
    username = get_connected_user(request)

    # Assurez-vous que le nom d'utilisateur est disponible dans la session
    if not username:
        return redirect('login')  # Redirige vers la page de connexion si pas de nom d'utilisateur dans la session

    if request.method == 'POST':
        form = ClVisiteurForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('visiteur:visiteur_list')
    else:
        form = ClVisiteurForm()
    return render(request, 'visiteur/visiteur_form.html', {  'username':username,'form': form})

# Permet de modifier les informations d'un visiteur
def visiteur_update(request, id):
    username = get_connected_user(request)

    # Assurez-vous que le nom d'utilisateur est disponible dans la session
    if not username:
        return redirect('login')  # Redirige vers la page de connexion si pas de nom d'utilisateur dans la session

    visiteur = get_object_or_404(ClVisiteur, id=id)
    if request.method == 'POST':
        form = ClVisiteurForm(request.POST, instance=visiteur)
        if form.is_valid():
            form.save()
            return redirect('visiteur:visiteur_list')
    else:
        form = ClVisiteurForm(instance=visiteur)
    return render(request, 'visiteur/visiteur_edit.html', {  'username':username,'form': form, 'visiteur':visiteur})

# Permet de rechercher des visiteurs
def visiteur_search(request):
    username = get_connected_user(request)

    # Assurez-vous que le nom d'utilisateur est disponible dans la session
    if not username:
        return redirect('login')  # Redirige vers la page de connexion si pas de nom d'utilisateur dans la session

    query = request.GET.get('q', '')
    visiteurs = ClVisiteur.objects.filter(tnm__icontains=query)  # Exemple de filtre par nom
    return render(request, 'visiteur/visiteur_list.html', {  'username':username,'visiteurs': visiteurs, 'query': query})
def visiter_search(request):
    username = get_connected_user(request)

    if not username:
        return redirect('login')

    query = request.GET.get('q', '').strip()

    # Debugging: afficher la requête
    print(f"Recherche pour : {query}")

    visiteurs = ClVisiteur.objects.all()

    if query:
        visiteurs = visiteurs.filter(
            Q(tnm__icontains=query) |
            Q(tpm__icontains=query) |
            Q(tsx__icontains=query) |
            Q(ttvst__icontains=query)
        )
        # Debugging: afficher le nombre de résultats
        print(f"Nombre de visiteurs trouvés : {visiteurs.count()}")

    return render(request, 'visiteur/visiteur_list.html', { 
        'username': username, 
        'visiteurs': visiteurs, 
        'query': query
    })

def visiteur_impression(request):
    username = get_connected_user(request)
    if not username:
        return redirect('login')

    visiteurs = ClVisiteur.objects.all()
    doc = Document()
    titre = doc.add_heading('Liste des Visiteurs', 0)
    titre.alignment = WD_ALIGN_PARAGRAPH.CENTER

    for visiteur in visiteurs:
        # Ajout de l'image en haut et centrée
        try:
            if visiteur.img and os.path.exists(visiteur.img.path):
                img_path = visiteur.img.path
            else:
                img_path = os.path.join(settings.MEDIA_ROOT, 'user_images/person-1824147_1280.png')

            if os.path.exists(img_path):
                para_img = doc.add_paragraph()
                para_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run_img = para_img.add_run()
                run_img.add_picture(img_path, width=Inches(1.0), height=Inches(1.25))
        except Exception as e:
            print(f"Erreur image pour {visiteur.tnm} {visiteur.tpm} : {e}")

        table = doc.add_table(rows=10, cols=2)
        table.style = 'Table Grid'
        table.alignment = WD_TABLE_ALIGNMENT.CENTER

        champs = [
            ("Nom", f"{visiteur.tnm or ''} {visiteur.tpm or ''}"),
            ("Sexe", visiteur.tsx or ''),
            ("Date de naissance", str(visiteur.dns or '')),
            ("Lieu de naissance", visiteur.tlns or ''),
            ("Adresse", visiteur.tads or ''),
            ("Email", visiteur.teml or ''),
            ("Téléphone", visiteur.tphne or ''),
            ("Date début", str(visiteur.dsb or '')),
            ("Date fin", str(visiteur.ddf or '')),
            ("Statut", visiteur.tstt or ''),
        ]

        for i, (label, valeur) in enumerate(champs):
            table.cell(i, 0).text = f"{label} :"
            table.cell(i, 1).text = str(valeur)

        doc.add_paragraph()
        date_para = doc.add_paragraph()
        date_para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        run_date = date_para.add_run(f"Fait à Brazzaville, le {datetime.today().strftime('%d/%m/%Y')}")
        run_date.bold = True
        run_date.font.size = Pt(10)

        for _ in range(3):
            doc.add_paragraph()

        ref_para = doc.add_paragraph()
        ref_para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        ref_run = ref_para.add_run(f"{username.user.tnm.upper()} {username.user.tpm}   {' ' * 10}")
        ref_run.bold = True
        ref_run.font.size = Pt(10)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename="visiteurs.docx"'
    doc.save(response)
    return response

def generate_word(request):
    username = get_connected_user(request)  # Supposons que cette fonction existe et retourne l'utilisateur connecté
    if not username:
        return redirect('login')  # Redirige si l'utilisateur n'est pas connecté

    # Récupérer les IDs des visiteurs sélectionnés depuis le formulaire POST
    visiteur_ids = request.POST.getlist('visiteur_select')  # Utilisez `getlist` pour récupérer une liste de valeurs
    if not visiteur_ids:
        return HttpResponse("Aucun visiteur sélectionné", status=400)  # Message d'erreur si aucun visiteur n'est sélectionné

    # Créer un fichier ZIP en mémoire
    zip_buffer = io.BytesIO()

    # Créer un fichier ZIP pour y ajouter les fichiers Word
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for visiteur_id in visiteur_ids:
            try:
                visiteur = ClVisiteur.objects.get(id=visiteur_id)
            except ClVisiteur.DoesNotExist:
                continue  # Si le visiteur n'existe pas, on passe au suivant

            # Création du document Word pour chaque visiteur
            doc = Document()
            titre = doc.add_heading("Fiche du Visiteur", 0)
            titre.alignment = WD_ALIGN_PARAGRAPH.CENTER

            # Ajout image
            try:
                if visiteur.img and os.path.exists(visiteur.img.path):
                    img_path = visiteur.img.path
                else:
                    img_path = os.path.join(settings.MEDIA_ROOT, 'user_images/person-1824147_1280.png')

                if os.path.exists(img_path):
                    para_img = doc.add_paragraph()
                    para_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    run_img = para_img.add_run()
                    run_img.add_picture(img_path, width=Inches(1.0), height=Inches(1.25))
            except Exception as e:
                print(f"Erreur chargement image : {e}")

            # Création du tableau avec les informations du visiteur
            table = doc.add_table(rows=10, cols=2)
            table.style = 'Table Grid'
            table.alignment = WD_TABLE_ALIGNMENT.CENTER

            champs = [
                ("Nom", f"{visiteur.tnm or ''} {visiteur.tpm or ''}"),
                ("Sexe", visiteur.tsx or ''),
                ("Date de naissance", str(visiteur.dns or '')),
                ("Lieu de naissance", visiteur.tlns or ''),
                ("Adresse", visiteur.tads or ''),
                ("Email", visiteur.teml or ''),
                ("Téléphone", visiteur.tphne or ''),
                ("Date début", str(visiteur.dsb or '')),
                ("Date fin", str(visiteur.ddf or '')),
                ("Statut", visiteur.tstt or ''),
            ]

            for i, (label, valeur) in enumerate(champs):
                table.cell(i, 0).text = f"{label} :"
                table.cell(i, 1).text = str(valeur)

            # Date et utilisateur qui a généré le document
            doc.add_paragraph()
            date_para = doc.add_paragraph()
            date_para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            run_date = date_para.add_run(f"Fait à Brazzaville, le {datetime.today().strftime('%d/%m/%Y')}")
            run_date.bold = True
            run_date.font.size = Pt(10)

            for _ in range(3):
                doc.add_paragraph()

            ref_para = doc.add_paragraph()
            ref_para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            ref_run = ref_para.add_run(f"{username.user.tnm.upper()} {username.user.tpm}   {' ' * 10}")
            ref_run.bold = True
            ref_run.font.size = Pt(10)

            # Sauvegarde du document Word dans un buffer mémoire
            word_buffer = io.BytesIO()
            doc.save(word_buffer)
            word_buffer.seek(0)

            # Nom du fichier Word
            filename = f"Visiteur_{visiteur.tnm}_{visiteur.tpm}.docx"
            zip_file.writestr(filename, word_buffer.read())  # Ajoute le fichier Word au ZIP

    # Réinitialisation du buffer du ZIP pour l'envoyer
    zip_buffer.seek(0)

    # Réponse HTTP avec le fichier ZIP contenant les documents Word
    response = HttpResponse(zip_buffer, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="visiteurs.zip"'

    return response
