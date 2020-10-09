# Copyright 2020 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

{
    "name": "Mason :: MRP II",
    "version": "13.0.1.0.0",
    "category": "Manufacturing/Manufacturing",
    "description": """
        Mason extension for MRP which inherited from mrp module.
    """,
    "depends": [
        "mrp",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/mrp_workcenter_views.xml",
        "views/mrp_workorder_views.xml",
    ],
    "application": False,
    "license": "AGPL-3",
}
