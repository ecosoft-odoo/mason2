# Copyright 2020 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class UpdateQTYApproved(models.TransientModel):
    _name = "update.qty.approved"
    _description = "Update QTY Approved"

    qty_approved = fields.Float(
        string="Approved Quantity",
        digits="Product Unit of Measure",
    )
    workorder_ids = fields.Many2many(
        comodel_name="mrp.workorder",
        relation="update_qty_approved_mrp_workorder_rel",
        column1="approved_id",
        column2="workorder_id",
        string="Workorders",
    )

    @api.model
    def view_init(self, fields):
        active_ids = self._context.get("active_ids")
        workorders = self.env["mrp.workorder"].browse(active_ids)
        if len(workorders) > 1:
            raise ValidationError(_("Please select 1 work order."))
        return super().view_init(fields)

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        active_id = self._context.get("active_id")
        active_workorder = self.env["mrp.workorder"].browse(active_id)
        updated_workorder = self._get_updated_workorder(active_workorder)
        res.update({
            "qty_approved": active_workorder.qty_approved,
            "workorder_ids": [(6, 0, updated_workorder.ids)],
        })
        return res

    def _get_updated_workorder(self, workorder):
        updated_workorder = workorder
        while True:
            previous_workorder = self.env["mrp.workorder"].search(
                [("next_work_order_id", "=", workorder.id)])
            if not previous_workorder:
                break
            updated_workorder |= previous_workorder
            workorder = previous_workorder
        return updated_workorder.sorted("id")

    def update_qty_approved(self):
        self.ensure_one()
        for workorder in self.workorder_ids:
            if workorder.state in ["pending", "cancel"]:
                raise ValidationError(
                    _("Can not update Approved Quantity "
                      "for state 'Waiting for another WO' or 'Cancelled'"))
            if self.qty_approved > workorder.qty_produced:
                raise ValidationError(
                    _("Workorder %s Quantity Produced %s %s "
                      "but Approved Quantity %s %s") %
                    (workorder.name, workorder.qty_produced,
                     workorder.product_uom_id.name,
                     self.qty_approved, workorder.product_uom_id.name)
                )
            self._cr.execute("""
                update mrp_workorder set qty_approved = %s where id = %s
            """, (self.qty_approved, workorder.id))
