# Copyright 2020 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import models, fields


class MrpWorkcenter(models.Model):
    _inherit = "mrp.workcenter"

    multiplier_piece = fields.Float(
        string="Multiplier / Piece",
        default=0.0,
    )
    position_ids = fields.One2many(
        comodel_name="mrp.workcenter.position",
        inverse_name="workcenter_id",
        string="Positions",
    )


class MrpWorkcenterPosition(models.Model):
    _name = "mrp.workcenter.position"
    _description = "MRP Workcenter Position"

    name = fields.Char(
        string="Name",
        required=True,
    )
    labor_cost_day = fields.Float(
        string="Labor Cost / Day",
        default=0.0,
    )
    workcenter_id = fields.Many2one(
        comodel_name="mrp.workcenter",
        string="Workcenter",
        index=True,
    )
