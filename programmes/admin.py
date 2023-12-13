from django.contrib import admin

from bailleurs.models import Bailleur
from instructeurs.models import Administration
from programmes.models.models import IndiceEvolutionLoyer

from .models import (
    Annexe,
    Logement,
    Lot,
    Programme,
    ReferenceCadastrale,
    TypeStationnement,
)


@admin.register(Programme)
class ProgrammeAdmin(admin.ModelAdmin):
    list_display = ("nom", "uuid")
    fields = (
        "uuid",
        "nom",
        "code_postal",
        "ville",
        "numero_galion",
        "administration",
        "bailleur",
        "zone_123",
        "zone_abc",
    )
    readonly_fields = (
        "uuid",
        "administration",
        "bailleur",
    )
    search_fields = ("uuid",)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "administration":
            kwargs["queryset"] = Administration.objects.order_by("nom")
        if db_field.name == "bailleur":
            kwargs["queryset"] = Bailleur.objects.order_by("nom")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    search_fields = ["nom"]


@admin.display(description="Programme")
def view_programme(lot):
    return f"{lot.programme.ville} -  {lot.programme.nom}"


@admin.register(Lot)
class LotAdmin(admin.ModelAdmin):
    list_display = (view_programme, "financement", "uuid")

    fields = (
        "uuid",
        "financement",
        "nb_logements",
        "type_habitat",
        "programme",
    )

    readonly_fields = (
        "uuid",
        "programme",
    )

    list_select_related = ("programme",)

    search_fields = ("uuid",)


@admin.register(Annexe)
class AnnexeAdmin(admin.ModelAdmin):
    list_select_related = ("logement",)


@admin.register(Logement)
class LogementAdmin(admin.ModelAdmin):
    readonly_fields = ("lot",)
    list_display = (
        "id",
        "uuid",
        "lot",
        "typologie",
        "designation",
    )
    search_fields = ("uuid",)


@admin.register(ReferenceCadastrale)
class ReferenceCadastraleAdmin(admin.ModelAdmin):
    readonly_fields = ("programme",)


@admin.register(TypeStationnement)
class TypeStationnementAdmin(admin.ModelAdmin):
    list_select_related = ("lot__programme",)
    readonly_fields = ("lot",)


admin.site.register(IndiceEvolutionLoyer)
