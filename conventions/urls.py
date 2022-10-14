from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("selection", views.select_programme_create, name="selection"),
    #    path("bailleur/<convention_uuid>", views.bailleur, name="bailleur"),
    path(
        "bailleur/<convention_uuid>",
        views.ConventionBailleurView.as_view(),
        name="bailleur",
    ),
    path(
        "programme/<convention_uuid>",
        views.ConventionProgrammeView.as_view(),
        name="programme",
    ),
    path("cadastre/<convention_uuid>", views.cadastre, name="cadastre"),
    path("edd/<convention_uuid>", views.edd, name="edd"),
    path("financement/<convention_uuid>", views.financement, name="financement"),
    path("logements/<convention_uuid>", views.logements, name="logements"),
    path(
        "avenant_logements/<convention_uuid>",
        views.avenant_logements,
        name="avenant_logements",
    ),
    path("annexes/<convention_uuid>", views.annexes, name="annexes"),
    path(
        "avenant_annexes/<convention_uuid>",
        views.avenant_annexes,
        name="avenant_annexes",
    ),
    path(
        "stationnements/<convention_uuid>",
        views.ConventionTypeStationnementView.as_view(),
        name="stationnements",
    ),
    path(
        "comments/<convention_uuid>",
        views.ConventionCommentsView.as_view(),
        name="comments",
    ),
    path(
        "avenant_comments/<convention_uuid>",
        views.AvenantCommentsView.as_view(),
        name="avenant_comments",
    ),
    path("recapitulatif/<convention_uuid>", views.recapitulatif, name="recapitulatif"),
    path(
        "save/<convention_uuid>",
        views.save_convention,
        name="save",
    ),
    path(
        "delete/<convention_uuid>",
        views.delete_convention,
        name="delete",
    ),
    path(
        "feedback/<convention_uuid>",
        views.feedback_convention,
        name="feedback",
    ),
    path(
        "validate/<convention_uuid>",
        views.validate_convention,
        name="validate",
    ),
    path(
        "generate/<convention_uuid>",
        views.generate_convention,
        name="generate",
    ),
    path(
        "load_xlsx_model/<file_type>",
        views.load_xlsx_model,
        name="load_xlsx_model",
    ),
    path(
        "operation/<programme_uuid>/<programme_financement>",
        views.display_operation,
        name="display_operation",
    ),
    path(
        "preview/<convention_uuid>",
        views.preview,
        name="preview",
    ),
    path(
        "sent/<convention_uuid>",
        views.sent,
        name="sent",
    ),
    path(
        "post_action/<convention_uuid>",
        views.post_action,
        name="post_action",
    ),
    path(
        "display_pdf/<convention_uuid>",
        views.display_pdf,
        name="display_pdf",
    ),
    path(
        "fiche_caf/<convention_uuid>",
        views.fiche_caf,
        name="fiche_caf",
    ),
    path("new_avenant/<convention_uuid>", views.new_avenant, name="new_avenant"),
]
