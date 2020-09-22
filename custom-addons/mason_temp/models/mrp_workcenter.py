# Copyright 2020 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import models, fields


class MrpWorkcenter(models.Model):
    _inherit = "mrp.workcenter"

    position_ids = fields.One2many(
        comodel_name="mrp.workcenter.position",
        inverse_name="workcenter_id",
        string="Position",
    )


class MrpWorkcenterPosition(models.Model):
    _name = "mrp.workcenter.position"
    _description = "Mrp Workcenter Position"

    name = fields.Char()
    labor_cost_day = fields.Float(string="Labor Cost/Day")
    workcenter_id = fields.Many2one(
        comodel_name="mrp.workorder",
    )
