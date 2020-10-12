# Copyright 2020 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ProductionStatistic(models.Model):
    _name = "production.statistic"
    _description = "Production Statistic"
    _order = "create_date"

    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Product",
        default=lambda self: self._context.get("product_id"),
        ondelete="restrict",
        required=True,
        index=True,
    )
    origin = fields.Char(
        string="SO",
    )
    production_id = fields.Many2one(
        comodel_name="mrp.production",
        string="MO",
        ondelete="restrict",
        index=True,
    )
    workcenter_id = fields.Many2one(
        comodel_name="mrp.workcenter",
        string="Work Center",
        default=lambda self: self._context.get("workcenter_id"),
        ondelete="restrict",
        required=True,
        index=True,
    )
    qty_per_day = fields.Float(
        string="Quantity / Day",
        digits=(25, 10),
        default=0.0,
    )
    multiplier = fields.Float(
        string="Multiplier",
        default=lambda self: self._get_default_multiplier(),
    )
    labor_cost_piece = fields.Float(
        string="Labor Cost / Piece",
        digits=(25, 10),
        default=0.0,
    )
    default = fields.Boolean(
        string="Default",
        default=False,
    )
    type = fields.Selection(
        selection=[
            ("system", "System"),
            ("adjustment", "Adjustment"),
        ],
        string="Type",
        default="adjustment",
        required=True,
    )
    approved_id = fields.Many2one(
        comodel_name="res.users",
        string="Approved",
        default=lambda self: self.env.user,
        ondelete="restrict",
        required=True,
        index=True,
    )
    note = fields.Text(
        string="Note",
    )
    confirm = fields.Boolean(
        string="Confirm",
        default=False,
    )

    @api.model
    def _get_default_multiplier(self):
        multiplier = 0.0
        workcenter_id = self._context.get("workcenter_id")
        if workcenter_id:
            workcenter = self.env["mrp.workcenter"].browse(workcenter_id)
            multiplier = workcenter.multiplier_piece
        return multiplier

    @api.model
    def create(self, values):
        res = super().create(values)
        if res.type == "adjustment":
            return res
        prod_stat = self.search([
            ("product_id", "=", res.product_id.id),
            ("workcenter_id", "=", res.workcenter_id.id),
            ("default", "=", True)])
        if not prod_stat:
            res.default = True
        else:
            if res.labor_cost_piece < prod_stat.labor_cost_piece:
                prod_stat.default = False
                res.default = True
        return res

    def unlink(self):
        for rec in self:
            if rec.type == "system":
                raise UserError(_("You cannot delete a system type."))
            if rec.confirm:
                raise UserError(_(
                    "You cannot delete a adjustment type as confirm already."))
        return super().unlink()
