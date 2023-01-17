import datetime
from dateutil.relativedelta import relativedelta

from django import forms
from django.forms import BaseFormSet, formset_factory
from django.core.exceptions import ValidationError

from programmes.models import (
    Financement,
    TypeOperation,
)
from conventions.models import Preteur


class ConventionFinancementForm(forms.Form):

    prets = []
    convention = None

    uuid = forms.UUIDField(
        required=False,
        label="Prêts et financements",
    )
    annee_fin_conventionnement = forms.TypedChoiceField(
        required=True,
        label="",
        coerce=int,
        choices=[(str(year), str(year)) for year in range(2021, 2121)],
        error_messages={
            "required": "La date de fin de conventionnement est obligatoire",
        },
    )
    fond_propre = forms.FloatField(
        required=False,
        label="Fonds propres",
    )
    historique_financement_public = forms.CharField(
        required=False,
        label="Historique de financement public",
        max_length=5000,
        error_messages={
            "max_length": "L'historique de financement public ne doit pas excéder 5000 caractères",
        },
    )

    def clean(self):
        cleaned_data = super().clean()
        annee_fin_conventionnement = cleaned_data.get("annee_fin_conventionnement")

        if (
            self.prets
            and self.convention is not None
            and annee_fin_conventionnement is not None
        ):
            if self.convention.financement == Financement.PLS:
                self._pls_end_date_validation(annee_fin_conventionnement)
            elif self.convention.programme.type_operation == TypeOperation.SANSTRAVAUX:
                self._sans_travaux_end_date_validation(annee_fin_conventionnement)
            else:
                self._other_end_date_validation(annee_fin_conventionnement)

    def _pls_end_date_validation(self, annee_fin_conventionnement):
        today = datetime.date.today()

        min_years = today.year + 15
        max_years = today.year + 40
        if today.month > 6:
            min_years = min_years + 1
            max_years = max_years + 1
        if annee_fin_conventionnement < min_years:
            self.add_error(
                "annee_fin_conventionnement",
                (
                    "L'année de fin de conventionnement ne peut être inférieur à "
                    + f"{min_years}"
                ),
            )
        if annee_fin_conventionnement > max_years:
            self.add_error(
                "annee_fin_conventionnement",
                (
                    "L'année de fin de conventionnement ne peut être supérieur à "
                    + f"{max_years}"
                ),
            )

    def _sans_travaux_end_date_validation(self, annee_fin_conventionnement):
        today = datetime.date.today()

        min_years = today.year + 9
        if today.month > 6:
            min_years = min_years + 1
        if annee_fin_conventionnement < min_years:
            self.add_error(
                "annee_fin_conventionnement",
                (
                    "L'année de fin de conventionnement ne peut être inférieur à "
                    + f"{min_years}"
                ),
            )

    def _other_end_date_validation(self, annee_fin_conventionnement):
        end_conv = None
        cdc_pret = None
        for pret in self.prets:
            if pret.cleaned_data["preteur"] in ["CDCF", "CDCL"]:
                if pret.cleaned_data["date_octroi"] and pret.cleaned_data["duree"]:
                    end_datetime = pret.cleaned_data["date_octroi"] + relativedelta(
                        years=int(pret.cleaned_data["duree"])
                    )
                    if not end_conv or end_datetime > end_conv:
                        end_conv = end_datetime
                        cdc_pret = pret
        if end_conv and cdc_pret:
            cdc_end_year = end_conv.year
            if end_conv.year - cdc_pret.cleaned_data["date_octroi"].year < 9:
                cdc_end_year = cdc_pret.cleaned_data["date_octroi"].year + 9
            # don't add a year for FOYER because end of convention is the 31/12
            if (
                not self.convention.programme.is_foyer()
                and end_conv
                and end_conv.month > 6
            ):
                cdc_end_year = cdc_end_year + 1
            if annee_fin_conventionnement < cdc_end_year:
                self.add_error(
                    "annee_fin_conventionnement",
                    (
                        "L'année de fin de conventionnement ne peut être inférieur à "
                        + f"{cdc_end_year}"
                    ),
                )


class PretForm(forms.Form):

    uuid = forms.UUIDField(
        required=False,
        label="Prêt ou financement",
    )
    numero = forms.CharField(
        required=False,
        label="",
        max_length=255,
        error_messages={
            "max_length": "Le numero ne doit pas excéder 255 caractères",
        },
    )
    preteur = forms.TypedChoiceField(required=False, label="", choices=Preteur.choices)
    autre = forms.CharField(
        required=False,
        label="",
        max_length=255,
        error_messages={
            "max_length": "Le prêteur ne doit pas excéder 255 caractères",
        },
    )
    date_octroi = forms.DateField(
        required=False,
        label="",
    )
    duree = forms.IntegerField(
        required=False,
        label="",
    )
    montant = forms.DecimalField(
        label="",
        max_digits=12,
        decimal_places=2,
        error_messages={
            "required": "Le montant du prêt est obligatoire",
            "max_digits": "Le montant du prêt doit-être inférieur à 10 000 000 000 €",
        },
    )

    def clean(self):
        cleaned_data = super().clean()
        preteur = cleaned_data.get("preteur")

        if preteur in ["CDCF", "CDCL"]:
            if not cleaned_data.get("date_octroi"):
                self.add_error(
                    "date_octroi",
                    "La date d'octroi est obligatoire pour un prêt de la "
                    + "Caisse de dépôts et consignations",
                )
            if not cleaned_data.get("duree"):
                self.add_error(
                    "duree",
                    "La durée est obligatoire pour un prêt de la Caisse de dépôts et consignations",
                )
            if not cleaned_data.get("numero"):
                self.add_error(
                    "numero",
                    (
                        "Le numéro est obligatoire pour un prêt"
                        + " de la Caisse de dépôts et consignations"
                    ),
                )
        if preteur in ["AUTRE"]:
            if not cleaned_data.get("autre"):
                self.add_error("autre", "Merci de préciser le prêteur")


class BasePretFormSet(BaseFormSet):

    convention = None

    def clean(self):
        self.manage_cdc_validation()

    def manage_cdc_validation(self):
        if (
            self.convention is not None
            and self.convention.financement != Financement.PLS
            and self.convention.programme.type_operation != TypeOperation.SANSTRAVAUX
        ):
            for form in self.forms:
                if form.cleaned_data.get("preteur") in ["CDCF", "CDCL"]:
                    return
            error = ValidationError(
                "Au moins un prêt à la Caisee des dépôts et consignations doit-être déclaré "
                + "(CDC foncière, CDC locative)"
            )
            self._non_form_errors.append(error)


PretFormSet = formset_factory(PretForm, formset=BasePretFormSet, extra=0)