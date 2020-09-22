# Copyright 2020 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import models, fields


class MrpWorkcenterProductivity(models.Model):
    _inherit = "mrp.workcenter.productivity"

    qty_done = fields.Float(
        string="Done Quantity",
        digits="Product Unit of Measure",
        compute="_compute_qty_done",
    )
    line_ids = fields.One2many(
        comodel_name="mrp.workcenter.productivity.line",
        inverse_name="productivity_id",
        string="Production Tracking",
        copy=False,
    )

    def _compute_qty_done(self):
        for rec in self:
            rec.qty_done = sum(rec.line_ids.mapped("qty_done"))


class MrpWorkcenterProductivityLine(models.Model):
    _name = "mrp.workcenter.productivity.line"
    _description = "MRP Workcenter Productivity Line"
    _order = "date_start"

    productivity_id = fields.Many2one(
        comodel_name="mrp.workcenter.productivity",
    )
    date_start = fields.Datetime(
        string="Start Date",
    )
    date_end = fields.Datetime(
        string="End Date",
    )
    qty_done = fields.Float(
        string="Done Quantity",
        digits="Product Unit of Measure",
    )
    qty_men = fields.Integer(
        string="Men Quantity",
    )


class MrpWorkcenter(models.Model):
    _inherit = "mrp.workcenter"

    labor_cost_day = fields.Float(
        string="Labor Cost/Day",
        default=0.0,
    )
    multiplier1 = fields.Float(
        string="Multiplier (Piece)",
        default=0.0,
    )
    multiplier2 = fields.Float(
        string="Multiplier (Day)",
        default=0.0,
    )
    multiplier3 = fields.Float(
        string="Multiplier (OT)",
    )
