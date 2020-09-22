# Copyright 2020 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import models, fields, _
from odoo.exceptions import ValidationError


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    def post_inventory(self):
        for order in self:
            check_qty_approved = [
                wo.qty_approved == wo.qty_production
                for wo in order.workorder_ids]
            if not all(check_qty_approved):
                raise ValidationError(
                    _("Please check Approved Quantity in Work Orders of %s"
                      % (order.name, )))
        return super().post_inventory()
