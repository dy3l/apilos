from typing import Any, List
from abc import ABC

from django.forms import Form
from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.db.models.functions import Substr
from django.http.request import HttpRequest

from conventions.forms import ConventionResiliationForm, UploadForm
from conventions.models import Convention, ConventionStatut
from conventions.services import utils
from conventions.services.file import ConventionFileService


class ConventionService(ABC):
    convention: Convention
    request: HttpRequest
    return_status: utils.ReturnStatus = utils.ReturnStatus.ERROR
    import_warnings: None | List = None
    redirect_recap: bool = False
    editable_after_upload: bool = False
    form: Form = None
    formset = None
    upform = None

    def __init__(
        self,
        convention: Convention,
        request: HttpRequest,
    ):
        self.convention = convention
        self.request = request

    def get(self):
        pass

    def save(self):
        pass


class ConventionListService:
    # pylint: disable=R0902,R0903,R0913
    search_input: str
    order_by: str
    page: str
    statut_filter: str
    financement_filter: str
    departement_input: str
    my_convention_list: Any  # list[Convention]
    paginated_conventions: Any  # list[Convention]
    total_conventions: int

    def __init__(
        self,
        my_convention_list: Any,
        search_input: str = "",
        statut_filter: str = "",
        financement_filter: str = "",
        departement_input: str = "",
        order_by: str = "",
        page: str = 1,
    ):
        self.search_input = search_input
        self.statut_filter = statut_filter
        self.financement_filter = financement_filter
        self.departement_input = departement_input
        self.order_by = order_by
        self.page = page
        self.my_convention_list = my_convention_list

    def paginate(self) -> None:
        total_user = self.my_convention_list.count()
        if self.search_input:
            self.my_convention_list = self.my_convention_list.filter(
                Q(programme__ville__icontains=self.search_input)
                | Q(programme__nom__icontains=self.search_input)
                | Q(programme__numero_galion__icontains=self.search_input)
            )
        if self.statut_filter:
            self.my_convention_list = self.my_convention_list.filter(
                statut=self.statut_filter
            )
        if self.financement_filter:
            self.my_convention_list = self.my_convention_list.filter(
                financement=self.financement_filter
            )
        if self.departement_input:
            self.my_convention_list = self.my_convention_list.annotate(
                departement=Substr("programme__code_postal", 1, 2)
            ).filter(departement=self.departement_input)

        if self.order_by:
            self.my_convention_list = self.my_convention_list.order_by(self.order_by)

        paginator = Paginator(
            self.my_convention_list, settings.APILOS_PAGINATION_PER_PAGE
        )
        try:
            conventions = paginator.page(self.page)
        except PageNotAnInteger:
            conventions = paginator.page(1)
        except EmptyPage:
            conventions = paginator.page(paginator.num_pages)

        self.paginated_conventions = conventions
        self.total_conventions = total_user


def convention_sent(request, convention_uuid):
    convention = Convention.objects.get(uuid=convention_uuid)
    result_status = None
    if request.method == "POST":
        upform = UploadForm(request.POST, request.FILES)
        if upform.is_valid():
            ConventionFileService.upload_convention_file(
                convention, request.FILES["file"]
            )
            result_status = utils.ReturnStatus.SUCCESS
    else:
        upform = UploadForm()

    return {
        "success": result_status,
        "convention": convention,
        "upform": upform,
    }


def convention_post_action(request, convention_uuid):
    convention = Convention.objects.get(uuid=convention_uuid)
    result_status = None
    if request.method == "POST":
        resiliation_form = ConventionResiliationForm(request.POST)
        if resiliation_form.is_valid():
            convention.statut = ConventionStatut.RESILIEE
            convention.date_resiliation = resiliation_form.cleaned_data[
                "date_resiliation"
            ]
            convention.save()
            # SUCCESS
            result_status = utils.ReturnStatus.SUCCESS

    else:
        resiliation_form = ConventionResiliationForm()

    upform = UploadForm()
    avenant_list_service = ConventionListService(
        my_convention_list=convention.avenants.all()
        .prefetch_related("programme")
        .prefetch_related("lot"),
        order_by="cree_le",
    )
    total_avenants = convention.avenants.all().count()
    avenant_list_service.paginate()

    return {
        "success": result_status,
        "upform": upform,
        "convention": convention,
        "avenants": avenant_list_service,
        "total_avenants": total_avenants,
        "resiliation_form": resiliation_form,
    }