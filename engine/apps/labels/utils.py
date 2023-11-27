import logging
import typing

from django.apps import apps  # noqa: I251
from django.conf import settings

if typing.TYPE_CHECKING:
    from apps.alerts.models import AlertGroup
    from apps.labels.models import AssociatedLabel
    from apps.user_management.models import Organization

logger = logging.getLogger(__name__)


LABEL_OUTDATED_TIMEOUT_MINUTES = 30
ASSOCIATED_MODEL_NAME = "AssociatedLabel"


class LabelUpdateParam(typing.TypedDict):
    name: str


class LabelParams(typing.TypedDict):
    id: str
    name: str


class LabelData(typing.TypedDict):
    key: LabelParams
    value: LabelParams


class ValueData(typing.TypedDict):
    value_name: str
    key_name: str


class LabelKeyData(typing.TypedDict):
    key: LabelParams
    values: typing.List[LabelParams]


LabelsData = typing.List[LabelData]
LabelsKeysData = typing.List[LabelParams]


def get_associating_label_model(obj_model_name: str) -> typing.Type["AssociatedLabel"]:
    associating_label_model_name = obj_model_name + ASSOCIATED_MODEL_NAME
    label_model = apps.get_model("labels", associating_label_model_name)
    return label_model


def is_labels_feature_enabled(organization: "Organization") -> bool:
    return (
        settings.FEATURE_LABELS_ENABLED_FOR_ALL
        or organization.org_id in settings.FEATURE_LABELS_ENABLED_FOR_GRAFANA_ORGS  # Grafana org ID, not OnCall org ID
    )


def get_label_verbal(obj: typing.Any) -> dict[str, str]:
    return {label.key.name: label.value.name for label in obj.labels.all().select_related("key", "value")}


def get_alert_group_label_verbal(alert_group: "AlertGroup") -> dict[str, str]:
    """This is different from get_label_verbal because alert group labels store key/value names, not IDs"""
    return {label.key_name: label.value_name for label in alert_group.labels.all()}
