# Copyright 2020 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class MrpWorkorder(models.Model):
    _inherit = "mrp.workorder"

    man_ids = fields.One2many(
        comodel_name="mrp.workorder.man",
        inverse_name="workorder_id",
        string="Man Quantity",
        readonly=False,
        states={"done": [("readonly", True)]},
    )
    time_ids = fields.One2many(
        readonly=False,
        states={"done": [("readonly", True)]},
    )

    @api.constrains("man_ids", "man_ids.position_id", "man_ids.qty_man")
    def _check_man_position_id(self):
        for rec in self:
            if rec.man_ids:
                self._cr.execute("""
                    select position_id, count(*)
                    from mrp_workorder_man where workorder_id = %s
                    group by position_id having count(*) > 1
                """, (rec.id, ))
                if self._cr.dictfetchall():
                    raise UserError(_("There is same position more than "
                                      "one line in man tab."))
                if rec.man_ids.filtered(lambda l: not l.qty_man):
                    raise UserError(
                        _("Man quantity must be greater than zero."))

    def _check_man_ids(self):
        for rec in self:
            if not rec.man_ids:
                raise UserError(_("You must add at least one man in "
                                  "this work order."))

    def do_finish(self):
        action = super().do_finish()
        self._check_man_ids()
        return action


class MrpWorkorderMan(models.Model):
    _name = "mrp.workorder.man"
    _description = "MRP Workorder Man"

    position_id = fields.Many2one(
        comodel_name="mrp.workcenter.position",
        required=True,
        index=True,
    )
    qty_man = fields.Integer(
        string="Man Quantity",
        default=0,
    )
    workorder_id = fields.Many2one(
        comodel_name="mrp.workorder",
        string="Workorder",
    )
