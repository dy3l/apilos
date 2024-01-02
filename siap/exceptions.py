class SIAPException(Exception):
    pass


class HabilitationSIAPException(SIAPException):
    pass


class TimeoutSIAPException(SIAPException):
    pass


class AssociationHLMSIAPException(SIAPException):
    pass


class UnauthorizedSIAPException(SIAPException):
    pass


class UnavailableServiceSIAPException(SIAPException):
    pass


class NoConventionForOperationSIAPException(SIAPException):
    pass


class InconsistentDataSIAPException(SIAPException):
    pass


class NotHandledBailleurPriveSIAPException(SIAPException):
    pass


class FusionAPISIAPException(SIAPException):
    pass


class DuplicatedOperationSIAPException(SIAPException):
    numero_operation = None

    def __init__(self, numero_operation):
        self.numero_operation = numero_operation
        super().__init__(f"Operation {numero_operation} already exists in SIAP")


class OperationToRepairSIAPException(DuplicatedOperationSIAPException):
    pass
