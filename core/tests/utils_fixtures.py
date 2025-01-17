import datetime
import json
import random

from django.contrib.auth.models import Group, Permission

from bailleurs.models import Bailleur
from conventions.models import Convention
from instructeurs.models import Administration
from programmes.models import (
    Annexe,
    Financement,
    Logement,
    Lot,
    Programme,
    TypeHabitat,
    TypologieAnnexe,
    TypologieLogement,
)
from upload.models import UploadedFile
from users.models import User

FILES = [
    {
        "thumbnail": "data:image/png;base64,BLAHBLAH==",
        "size": "31185",
        "filename": "acquereur1.png",
        "content_type": "image/png",
    },
    {
        "thumbnail": "data:image/png;base64,BLIHBLIH==",
        "size": "69076",
        "filename": "acquereur2.png",
        "content_type": "image/png",
    },
]


def _create_upload_files():

    files_and_text = {"text": "this is a test", "files": {}}
    for file in FILES:
        uploaded_file = UploadedFile.objects.create(
            filename=file["filename"],
            size=file["size"],
            content_type=file["content_type"],
        )
        files_and_text["files"][str(uploaded_file.uuid)] = {
            "uuid": str(uploaded_file.uuid),
            **file,
        }
    return json.dumps(files_and_text)


def create_administrations():
    return (
        Administration.objects.create(
            nom="CA d'Arles-Crau-Camargue-Montagnette",
            code="12345",
        ),
        Administration.objects.create(
            nom="Métropole de Marseille",
            code="67890",
        ),
        Administration.objects.create(nom="Paris", code="75000", code_postal="75001"),
        Administration.objects.create(
            nom="DDT Paris",
            code="DD075",
            code_postal="75015",
            adresse="5 rue Leblanc Le Ponant",
        ),
    )


def create_bailleurs():
    return (
        create_bailleur(),
        Bailleur.objects.create(
            nom="HLM",
            siret="987654321",
            capital_social="123456",
            ville="Marseille",
            signataire_nom="Pall Antoine",
            signataire_fonction="DG",
            signataire_date_deliberation=datetime.date(2001, 12, 1),
            signataire_bloc_signature="Mon DG",
        ),
        Bailleur.objects.create(
            nom="SEM",
            siret="2345678901",
            capital_social="123456",
            ville="Marseille",
            signataire_nom="Polo Alto",
            signataire_fonction="PDG",
            signataire_date_deliberation=datetime.date(2011, 12, 1),
            signataire_bloc_signature="Mon PDG",
        ),
    )


def create_group(name, rwd=None, rw=None, ru=None, ro=None):
    group = Group.objects.create(
        name=name,
    )
    permission_set = []
    if rwd is not None:
        for obj in rwd:
            permission_set = permission_set + [
                Permission.objects.get(content_type__model=obj, codename=f"add_{obj}"),
                Permission.objects.get(
                    content_type__model=obj, codename=f"change_{obj}"
                ),
                Permission.objects.get(
                    content_type__model=obj, codename=f"delete_{obj}"
                ),
                Permission.objects.get(content_type__model=obj, codename=f"view_{obj}"),
            ]
    if rw is not None:
        for obj in rw:
            permission_set = permission_set + [
                Permission.objects.get(content_type__model=obj, codename=f"add_{obj}"),
                Permission.objects.get(
                    content_type__model=obj, codename=f"change_{obj}"
                ),
                Permission.objects.get(content_type__model=obj, codename=f"view_{obj}"),
            ]
    if ru is not None:
        for obj in ru:
            permission_set = permission_set + [
                Permission.objects.get(
                    content_type__model=obj, codename=f"change_{obj}"
                ),
                Permission.objects.get(content_type__model=obj, codename=f"view_{obj}"),
            ]
    if ro is not None:
        for obj in ro:
            permission_set.append(
                Permission.objects.get(content_type__model=obj, codename=f"view_{obj}")
            )
    group.permissions.set(permission_set)
    return group


def create_bailleur():
    return Bailleur.objects.create(
        nom="3F",
        siret="12345678901234",
        capital_social="123000.50",
        ville="Marseille",
        signataire_nom="Patrick Patoulachi",
        signataire_fonction="PDG",
        signataire_date_deliberation=datetime.date(2014, 10, 9),
        signataire_bloc_signature="Mon PDG",
    )


def create_programme(
    bailleur,
    administration=None,
    nom="Programme",
    numero_galion="12345",
    code_postal="75007",
):
    return Programme.objects.create(
        nom=nom,
        administration=administration,
        bailleur=bailleur,
        code_postal=code_postal,
        code_insee_departement=code_postal[0:2],
        ville="Paris",
        adresse="22 rue segur",
        numero_galion=numero_galion,
        annee_gestion_programmation=2018,
        zone_123="3",
        zone_abc="B1",
        surface_utile_totale=5243.21,
        nb_locaux_commerciaux=5,
        nb_bureaux=25,
        autres_locaux_hors_convention="quelques uns",
        vendeur=random.choice([_create_upload_files(), "", "n'importe quoi", None]),
        acquereur=random.choice([_create_upload_files(), "", "n'importe quoi", None]),
        reference_notaire=random.choice(
            [_create_upload_files(), "", "n'importe quoi", None]
        ),
        reference_publication_acte=random.choice(
            [_create_upload_files(), "", "n'importe quoi", None]
        ),
        acte_de_propriete=random.choice(
            [_create_upload_files(), "", "n'importe quoi", None]
        ),
        certificat_adressage=random.choice(
            [_create_upload_files(), "", "n'importe quoi", None]
        ),
        effet_relatif=random.choice(
            [_create_upload_files(), "", "n'importe quoi", None]
        ),
        reference_cadastrale=random.choice(
            [_create_upload_files(), "", "n'importe quoi", None]
        ),
        permis_construire="123 456 789 ABC",
        date_achevement_previsible=datetime.date(2024, 1, 2),
        date_achat=datetime.date(2022, 1, 2),
        date_achevement=datetime.date(2024, 4, 11),
        edd_stationnements='{"text": "EDD stationnements", "files": {"fbb9890f-171b-402d-a35e-71e1bd791b70": '
        '{"uuid": "fbb9890f-171b-402d-a35e-71e1bd791b70", "thumbnail": "data:image/png;base64'
        ',BLAHBLAH==", "size": "31185", "filename": "acquereur1.png", "content_type": "image/png"},'
        '"dccd310d-2e50-45d8-a477-db7b08ae1d71": {"uuid": "dccd310d-2e50-45d8-a477-db7b08ae1d71", '
        '"thumbnail": "data:image/png;base64,BLIHBLIH==", "size": "69076", "filename": '
        '"acquereur2.png", "content_type": "image/png"}}}',
    )


def create_lot(programme: Programme, financement: Financement, type_habitat=None):
    return Lot.objects.create(
        programme=programme,
        financement=financement,
        type_habitat=type_habitat
        if type_habitat
        else random.choice(
            [
                TypeHabitat.COLLECTIF,
                TypeHabitat.INDIVIDUEL,
                TypeHabitat.MIXTE,
            ]
        ).value,
        edd_volumetrique=random.choice(
            [_create_upload_files(), "", "n'importe quoi", None]
        ),
        edd_classique=random.choice(
            [_create_upload_files(), "", "n'importe quoi", None]
        ),
    )


def create_logement(lot: Lot, designation: str, typologie: TypologieLogement):
    return Logement.objects.create(
        lot=lot,
        designation=designation,
        typologie=typologie,
        surface_habitable=50,
        surface_annexes=20,
        surface_annexes_retenue=10,
        surface_utile=60,
        loyer_par_metre_carre=5.5,
        coeficient=0.9,
        loyer=60 * 5.5 * 0.9,
    )


def create_annexe(logement: Logement, typologie: TypologieAnnexe):
    return Annexe.objects.create(
        logement=logement,
        typologie=typologie,
        surface_hors_surface_retenue=5,
        loyer_par_metre_carre=0.1,
        loyer=0.5,
    )


def create_convention(lot: Lot, numero: str = "0001"):
    return Convention.objects.create(
        numero=numero,
        lot=lot,
        programme=lot.programme,
        financement=lot.financement,
        commentaires=_create_upload_files(),
    )


def create_all_for_siap():
    user1 = User.objects.create_user("sabine", "sabine@apilos.com", "12345")
    user1.first_name = "Sabine"
    user1.last_name = "Marini"
    user1.cerbere_login = "sabine@apilos.com"
    administration = Administration.objects.create(
        nom="CA d'Arles-Crau-Camargue-Montagnette",
        code="12345",
    )
    bailleur = create_bailleur()
    create_group("Instructeur", rwd=["logement", "convention"])
    create_group("Bailleur", rw=["logement", "convention"])
    programme_75 = create_programme(
        bailleur, administration, nom="Programme 1", numero_galion="20220600005"
    )
    lot_plai = create_lot(
        programme_75, Financement.PLAI, type_habitat=TypeHabitat.MIXTE
    )
    lot_plus = create_lot(
        programme_75, Financement.PLUS, type_habitat=TypeHabitat.COLLECTIF
    )
    create_convention(lot_plus, numero="0001")
    create_convention(lot_plai, numero="0002")
    log1 = create_logement(lot_plai, "PLAI 1", TypologieLogement.T1)
    create_annexe(log1, TypologieAnnexe.COUR)
    create_annexe(log1, TypologieAnnexe.JARDIN)
    create_logement(lot_plai, "PLAI 2", TypologieLogement.T2)
    create_logement(lot_plai, "PLAI 3", TypologieLogement.T3)
    create_logement(lot_plus, "PLUS 1", TypologieLogement.T1)
