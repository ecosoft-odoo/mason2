# Copyright 2020 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import models, fields


class MrpWorkorder(models.Model):
    _inherit = "mrp.workorder"

    man_ids = fields.One2many(
        comodel_name="mrp.workorder.man",
        inverse_name="workorder_id",
        string="Man Quantity",
    )


class MrpWorkorderMan(models.Model):
    _name = "mrp.workorder.man"
    _description = "MRP Workorder Man"

    position_id = fields.Many2one(
        comodel_name="mrp.workcenter.position",
        required=True,
        index=True,
    )
    qty_man = fields.Integer(
        string="Man Quantity",
        default=0,
    )
    workorder_id = fields.Many2one(
        comodel_name="mrp.workorder",
        string="Workorder",
    )
