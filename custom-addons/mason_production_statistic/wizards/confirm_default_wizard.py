# Copyright 2020 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import models, _
from odoo.exceptions import UserError


class ConfirmDefaultWizard(models.TransientModel):
    _name = "confirm.default.wizard"
    _description = "Confirm Default Wizard"

    def confirm(self):
        self.ensure_one()
        active_id = self._context.get("active_id")
        active_model = self._context.get("active_model")
        if active_model != "production.statistic":
            raise UserError(_("Can not open this wizard with object %s") % (
                active_model, ))
        active_record = self.env[active_model].browse(active_id)
        prod_stat = self.env[active_model].search([
            ("product_id", "=", active_record.product_id.id),
            ("workcenter_id", "=", active_record.workcenter_id.id),
            ("default", "=", True)])
        prod_stat.write({"default": False})
        active_record.write({"default": True, "confirm": True})
