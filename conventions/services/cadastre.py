from django.http import HttpRequest

from conventions.services.conventions import ConventionService
from conventions.services import utils, upload_objects
from conventions.models import Convention
from conventions.forms import UploadForm
from programmes.models import ReferenceCadastrale
from programmes.forms import ProgrammeCadastralForm, ReferenceCadastraleFormSet


def _get_choices_from_object(object_list):
    return [(instance.uuid, str(instance)) for instance in object_list]


class ConventionCadastreService(ConventionService):
    convention: Convention
    request: HttpRequest
    form: ProgrammeCadastralForm
    formset: ReferenceCadastraleFormSet
    upform: UploadForm = UploadForm()
    return_status: utils.ReturnStatus = utils.ReturnStatus.ERROR
    redirect_recap: bool = False
    editable_after_upload: bool = False

    def get(self):
        initial = []
        referencecadastrales = (
            self.convention.programme.referencecadastrales.all().order_by("section")
        )
        for referencecadastrale in referencecadastrales:
            initial.append(
                {
                    "uuid": referencecadastrale.uuid,
                    "section": referencecadastrale.section,
                    "numero": referencecadastrale.numero,
                    "lieudit": referencecadastrale.lieudit,
                    "surface": referencecadastrale.surface,
                }
            )
        self.formset = ReferenceCadastraleFormSet(initial=initial)
        self.form = ProgrammeCadastralForm(
            initial={
                "uuid": self.convention.programme.uuid,
                "permis_construire": self.convention.programme.permis_construire,
                "date_acte_notarie": utils.format_date_for_form(
                    self.convention.programme.date_acte_notarie
                ),
                "date_achevement_previsible": utils.format_date_for_form(
                    self.convention.programme.date_achevement_previsible
                ),
                "date_achat": utils.format_date_for_form(
                    self.convention.programme.date_achat
                ),
                "date_autorisation_hors_habitat_inclusif": utils.format_date_for_form(
                    self.convention.programme.date_autorisation_hors_habitat_inclusif
                ),
                "date_convention_location": utils.format_date_for_form(
                    self.convention.programme.date_convention_location
                ),
                "date_achevement": utils.format_date_for_form(
                    self.convention.programme.date_achevement
                ),
                **utils.get_text_and_files_from_field(
                    "vendeur", self.convention.programme.vendeur
                ),
                **utils.get_text_and_files_from_field(
                    "acquereur", self.convention.programme.acquereur
                ),
                **utils.get_text_and_files_from_field(
                    "reference_notaire", self.convention.programme.reference_notaire
                ),
                **utils.get_text_and_files_from_field(
                    "reference_publication_acte",
                    self.convention.programme.reference_publication_acte,
                ),
                **utils.get_text_and_files_from_field(
                    "effet_relatif", self.convention.programme.effet_relatif
                ),
                **utils.get_text_and_files_from_field(
                    "acte_de_propriete", self.convention.programme.acte_de_propriete
                ),
                **utils.get_text_and_files_from_field(
                    "certificat_adressage",
                    self.convention.programme.certificat_adressage,
                ),
                **utils.get_text_and_files_from_field(
                    "reference_cadastrale",
                    self.convention.programme.reference_cadastrale,
                ),
            }
        )

    def save(self):
        self.editable_after_upload = self.request.POST.get(
            "editable_after_upload", False
        )
        # When the user cliked on "Téléverser" button
        if self.request.POST.get("Upload", False):
            self.form = ProgrammeCadastralForm(self.request.POST)
            self._upload_cadastre()
        # When the user cliked on "Enregistrer et Suivant"
        else:
            self._programme_cadastrale_atomic_update()

    def _upload_cadastre(self):
        self.formset = ReferenceCadastraleFormSet(self.request.POST)
        self.upform = UploadForm(self.request.POST, self.request.FILES)
        if self.upform.is_valid():
            result = upload_objects.handle_uploaded_xlsx(
                self.upform,
                self.request.FILES["file"],
                ReferenceCadastrale,
                self.convention,
                "cadastre.xlsx",
            )
            if result["success"] != utils.ReturnStatus.ERROR:
                refcads_by_section = {}
                for refcad in ReferenceCadastrale.objects.filter(
                    programme_id=self.convention.programme_id
                ):
                    refcads_by_section[
                        f"{refcad.section}__{refcad.numero}"
                    ] = refcad.uuid

                for obj in result["objects"]:
                    if (
                        "section" in obj
                        and "numero" in obj
                        and f"{obj['section']}__{obj['numero']}" in refcads_by_section
                    ):
                        obj["uuid"] = refcads_by_section[
                            f"{obj['section']}__{obj['numero']}"
                        ]

                self.formset = ReferenceCadastraleFormSet(initial=result["objects"])
                self.import_warnings = result["import_warnings"]
                self.editable_after_upload = True

    def _programme_cadastrale_atomic_update(self):
        self.form = ProgrammeCadastralForm(
            {
                "uuid": self.convention.programme.uuid,
                **utils.build_partial_form(
                    self.request,
                    self.convention.programme,
                    [
                        "permis_construire",
                        "date_acte_notarie",
                        "date_achevement_previsible",
                        "date_autorisation_hors_habitat_inclusif",
                        "date_convention_location",
                        "date_achat",
                        "date_achevement",
                    ],
                ),
                **utils.build_partial_text_and_files_form(
                    self.request,
                    self.convention.programme,
                    [
                        "vendeur",
                        "acquereur",
                        "reference_notaire",
                        "reference_publication_acte",
                        "acte_de_propriete",
                        "effet_relatif",
                        "certificat_adressage",
                        "reference_cadastrale",
                    ],
                ),
            }
        )
        form_is_valid = self.form.is_valid()

        self.formset = ReferenceCadastraleFormSet(self.request.POST)
        initformset = {
            "form-TOTAL_FORMS": self.request.POST.get(
                "form-TOTAL_FORMS", len(self.formset)
            ),
            "form-INITIAL_FORMS": self.request.POST.get(
                "form-INITIAL_FORMS", len(self.formset)
            ),
        }
        for idx, form_reference_cadastrale in enumerate(self.formset):
            if form_reference_cadastrale["uuid"].value():
                reference_cadastrale = ReferenceCadastrale.objects.get(
                    uuid=form_reference_cadastrale["uuid"].value()
                )
                initformset = {
                    **initformset,
                    f"form-{idx}-uuid": reference_cadastrale.uuid,
                    f"form-{idx}-section": utils.get_form_value(
                        form_reference_cadastrale, reference_cadastrale, "section"
                    ),
                    f"form-{idx}-numero": utils.get_form_value(
                        form_reference_cadastrale, reference_cadastrale, "numero"
                    ),
                    f"form-{idx}-lieudit": utils.get_form_value(
                        form_reference_cadastrale, reference_cadastrale, "lieudit"
                    ),
                    f"form-{idx}-surface": utils.get_form_value(
                        form_reference_cadastrale, reference_cadastrale, "surface"
                    ),
                }
            else:
                initformset = {
                    **initformset,
                    f"form-{idx}-section": form_reference_cadastrale["section"].value(),
                    f"form-{idx}-numero": form_reference_cadastrale["numero"].value(),
                    f"form-{idx}-lieudit": form_reference_cadastrale["lieudit"].value(),
                    f"form-{idx}-surface": form_reference_cadastrale["surface"].value(),
                }
        self.formset = ReferenceCadastraleFormSet(initformset)
        formset_is_valid = self.formset.is_valid()

        if form_is_valid and formset_is_valid:
            self._save_programme_cadastrale()
            self._save_programme_reference_cadastrale()
            self.return_status = utils.ReturnStatus.SUCCESS

    def _save_programme_cadastrale(self):
        self.convention.programme.permis_construire = self.form.cleaned_data[
            "permis_construire"
        ]
        self.convention.programme.date_acte_notarie = self.form.cleaned_data[
            "date_acte_notarie"
        ]
        self.convention.programme.date_achevement_previsible = self.form.cleaned_data[
            "date_achevement_previsible"
        ]
        self.convention.programme.date_autorisation_hors_habitat_inclusif = (
            self.form.cleaned_data["date_autorisation_hors_habitat_inclusif"]
        )
        self.convention.programme.date_convention_location = self.form.cleaned_data[
            "date_convention_location"
        ]
        self.convention.programme.date_achat = self.form.cleaned_data["date_achat"]
        self.convention.programme.date_achevement = self.form.cleaned_data[
            "date_achevement"
        ]
        self.convention.programme.vendeur = utils.set_files_and_text_field(
            self.form.cleaned_data["vendeur_files"],
            self.form.cleaned_data["vendeur"],
        )
        self.convention.programme.acquereur = utils.set_files_and_text_field(
            self.form.cleaned_data["acquereur_files"],
            self.form.cleaned_data["acquereur"],
        )
        self.convention.programme.reference_notaire = utils.set_files_and_text_field(
            self.form.cleaned_data["reference_notaire_files"],
            self.form.cleaned_data["reference_notaire"],
        )
        self.convention.programme.reference_publication_acte = (
            utils.set_files_and_text_field(
                self.form.cleaned_data["reference_publication_acte_files"],
                self.form.cleaned_data["reference_publication_acte"],
            )
        )
        self.convention.programme.effet_relatif = utils.set_files_and_text_field(
            self.form.cleaned_data["effet_relatif_files"],
        )
        self.convention.programme.acte_de_propriete = utils.set_files_and_text_field(
            self.form.cleaned_data["acte_de_propriete_files"],
        )
        self.convention.programme.certificat_adressage = utils.set_files_and_text_field(
            self.form.cleaned_data["certificat_adressage_files"],
        )
        self.convention.programme.reference_cadastrale = utils.set_files_and_text_field(
            self.form.cleaned_data["reference_cadastrale_files"],
        )
        self.convention.programme.save()

    def _save_programme_reference_cadastrale(self):
        obj_uuids1 = list(map(lambda x: x.cleaned_data["uuid"], self.formset))
        obj_uuids = list(filter(None, obj_uuids1))
        self.convention.programme.referencecadastrales.exclude(
            uuid__in=obj_uuids
        ).delete()
        for form in self.formset:
            if form.cleaned_data["uuid"]:
                reference_cadastrale = ReferenceCadastrale.objects.get(
                    uuid=form.cleaned_data["uuid"]
                )
                reference_cadastrale.section = form.cleaned_data["section"]
                reference_cadastrale.numero = form.cleaned_data["numero"]
                reference_cadastrale.lieudit = form.cleaned_data["lieudit"]
                reference_cadastrale.surface = form.cleaned_data["surface"]
            else:
                reference_cadastrale = ReferenceCadastrale.objects.create(
                    programme=self.convention.programme,
                    section=form.cleaned_data["section"],
                    numero=form.cleaned_data["numero"],
                    lieudit=form.cleaned_data["lieudit"],
                    surface=form.cleaned_data["surface"],
                )
            reference_cadastrale.save()