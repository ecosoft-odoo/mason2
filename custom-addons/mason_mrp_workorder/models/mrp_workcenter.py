# Copyright 2020 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import models, fields, api, _
from odoo.exceptions import UserError


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

    @api.constrains("multiplier_piece")
    def _check_multiplier(self):
        for rec in self:
            if not rec.multiplier_piece:
                raise UserError(
                    _("Multiplier / Piece must be greater than zero."))

    @api.constrains("position_ids")
    def _check_position_ids(self):
        for rec in self:
            if not rec.position_ids:
                raise UserError(_("You must add at least one position in "
                                  "this work center."))

    @api.model
    def create(self, values):
        if "position_ids" not in values:
            values["position_ids"] = False
        return super().create(values)


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
