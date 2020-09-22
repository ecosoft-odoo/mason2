# Copyright 2020 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import models, fields, api


class MrpWorkorder(models.Model):
    _inherit = "mrp.workorder"

    cost_ids = fields.One2many(
        comodel_name="mrp.workorder.cost",
        inverse_name="workorder_id",
        string="Labor Cost/Day",
    )
    forcast_qty = fields.Float(
        string="Forcast QTY/Day",
    )


class MrpWorkorderCost(models.Model):
    _name = "mrp.workorder.cost"
    _description = "Mrp Workorder Cost"

    position_id = fields.Many2one(
        comodel_name="mrp.workcenter.position",
        string="name",
    )
    man_number = fields.Integer(string="Man Number")
    labor_cost_day = fields.Float(string="Labor Cost/Day")
    total_labor_cost_day = fields.Float(
        string="Total Labor Cost/Day",
        compute="_compute_total_labor_cost_day",
    )
    workorder_id = fields.Many2one(
        comodel_name="mrp.workorder",
    )
    workcenter_id = fields.Many2one(
        comodel_name="mrp.workcenter",
        related="workorder_id.workcenter_id"
    )

    @api.onchange("position_id")
    def _onchange_position_id(self):
        for rec in self:
            rec.labor_cost_day = rec.position_id.labor_cost_day

    @api.depends("man_number", "labor_cost_day")
    def _compute_total_labor_cost_day(self):
        for rec in self:
            rec.total_labor_cost_day = rec.man_number * rec.labor_cost_day
