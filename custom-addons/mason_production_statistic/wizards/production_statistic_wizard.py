# Copyright 2020 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import models, fields, api, _


class ProductionStatisticWizard(models.TransientModel):
    _name = "production.statistic.wizard"
    _description = "Production Statistic Wizard"

    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Product",
        domain=lambda self: self._get_domain_product_id(),
        index=True,
    )
    workcenter_id = fields.Many2one(
        comodel_name="mrp.workcenter",
        string="Work Center",
        index=True,
    )

    @api.model
    def _get_domain_product_id(self):
        products = self.env["mrp.workorder"].search([]).mapped("product_id")
        return "[('id', 'in', %s)]" % (products.ids, )

    def open_production_statistic(self):
        self.ensure_one()
        domain = []
        if self.product_id:
            domain += [('product_id', '=', self.product_id.id)]
        if self.workcenter_id:
            domain += [('workcenter_id', '=', self.workcenter_id.id)]
        return {
            "name": _("Production Statistic"),
            "view_mode": "tree",
            "res_model": "production.statistic",
            "type": "ir.actions.act_window",
            "context": {
                "product_id": self.product_id.id,
                "workcenter_id": self.workcenter_id.id,
            },
            "domain": domain,
        }
