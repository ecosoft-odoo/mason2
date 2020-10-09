# Copyright 2020 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

{
    "name": "Mason :: Production Statistic",
    "version": "13.0.1.0.0",
    "category": "Manufacturing/Manufacturing",
    "description": """
        This is add production statistic menu.
    """,
    "depends": [
        "mason_mrp_workorder",
    ],
    "data": [
        "security/ir.model.access.csv",
        "wizards/production_statistic_wizard_views.xml",
        "wizards/confirm_default_wizard_views.xml",
        "views/production_statistic_views.xml",
    ],
    "application": False,
    "license": "AGPL-3",
}
