import pytest
import ckan.plugins.toolkit as toolkit
from markupsafe import Markup

from ckanext.data_comparision.libs.commons import Commons
from ckanext.data_comparision.libs.table_builder import Builder
from ckanext.data_comparision.libs.template_helper import TemplateHelper
from ckanext.data_comparision.plugin import DataComparisionPlugin


@pytest.mark.parametrize(
    ("resource", "is_csv", "is_xlsx"),
    [
        ({"format": "csv", "name": "data"}, True, False),
        ({"format": "", "name": "DATA.CSV"}, True, False),
        ({"format": "XLSX", "name": "workbook"}, False, True),
        ({"format": None, "name": "book.XLSX"}, False, True),
        ({"format": "PDF", "name": "report.pdf"}, False, False),
    ],
)
def test_resource_type_helpers_are_case_insensitive(resource, is_csv, is_xlsx):
    assert TemplateHelper.is_csv(resource) is is_csv
    assert TemplateHelper.is_xlsx(resource) is is_xlsx


def test_process_resource_id_preserves_sheet_delimiters():
    assert Commons.process_resource_id("resource-id---sheet---one") == [
        "resource-id",
        "sheet---one",
    ]


def test_process_resource_id_rejects_invalid_value():
    with pytest.raises(toolkit.ValidationError):
        Commons.process_resource_id("resource-id")


def test_cast_string_to_num_handles_decimal_commas_and_invalid_values():
    assert Commons.cast_string_to_num(["1,5", 2, None, "bad"]) == [1.5, 2.0, 0, 0]


def test_generated_cells_escape_untrusted_resource_values():
    cell = Builder.build_body_cell(1, Markup('<script>alert(1)</script>'), 'id', 'None')
    assert "<script>" not in cell
    assert "&lt;script&gt;" in cell


def test_plugin_exposes_all_blueprint_routes():
    blueprint = DataComparisionPlugin().get_blueprint()
    assert len(blueprint.deferred_functions) == 6
