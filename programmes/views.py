from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import resolve
import logging

from conventions.services.search import ProgrammeConventionSearchService
from programmes.services import get_or_create_conventions_from_operation_number

from siap.exceptions import SIAPException, DuplicationSIAPException

logger = logging.getLogger(__name__)


@login_required
def operation_conventions(request, numero_operation):
    # Décorator ?
    # if not request.user.is_cerbere_user():
    #     raise PermissionError("this function is available only for CERBERE user")

    try:
        (programme, _, _) = get_or_create_conventions_from_operation_number(
            request, numero_operation
        )
    except DuplicationSIAPException as exc:
        logger.error(exc)
        # return HttpResponseRedirect(
        #     reverse(
        #         "conventions:recapitulatif",
        #         args=[service.avenant.uuid],
        #     )
        # )
    except SIAPException as exc:
        raise exc
    else:
        service = ProgrammeConventionSearchService(programme)
        paginator = service.paginate()

        return render(
            request,
            "operations/conventions.html",
            {
                "url_name": resolve(request.path_info).url_name,
                "order_by": request.GET.get("order_by", ""),
                "numero_operation": numero_operation,
                "programme": programme,
                "conventions": paginator.get_page(request.GET.get("page", 1)),
                "filtered_conventions_count": paginator.count,
                "all_conventions_count": paginator.count,
                "search_input": "",
            },
        )
