# Copyright 2020 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

{
    "name": "Mason :: Cost Analysis Report",
    "version": "13.0.1.0.0",
    "category": "Manufacturing/Manufacturing",
    "description": """
        Cost Analysis Report.
    """,
    "depends": [
        "report_xlsx_helper",
        "mason_mrp_workorder",
    ],
    "data": [
        "data/paperformat_data.xml",
        "data/report_data.xml",
        "security/ir.model.access.csv",
        "wizards/cost_analysis_report_wizards.xml",
        "report/cost_analysis_report.xml",
    ],
    "application": False,
    "license": "AGPL-3",
}
