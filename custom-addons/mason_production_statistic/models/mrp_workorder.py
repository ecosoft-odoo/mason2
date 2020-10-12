# Copyright 2020 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import models
from datetime import timedelta


class MrpWorkorder(models.Model):
    _inherit = "mrp.workorder"

    def _prepare_production_statistic(self):
        self.ensure_one()
        actual_hours = timedelta(minutes=self.duration).total_seconds() / 3600
        qty_per_day = self.qty_produced * 8 / actual_hours
        total_labor_cost = sum(
            [l.qty_man * l.position_id.labor_cost_day for l in self.man_ids])
        multiplier = self.workcenter_id.multiplier_piece
        labor_cost_piece = total_labor_cost / qty_per_day * multiplier
        return {
            "product_id": self.product_id.id,
            "origin": self.production_id.origin,
            "production_id": self.production_id.id,
            "workcenter_id": self.workcenter_id.id,
            "qty_per_day": qty_per_day,
            "multiplier": multiplier,
            "labor_cost_piece": labor_cost_piece,
            "type": "system",
            "approved_id": self.env.ref("base.user_root").id,
        }

    def _create_production_statistic(self):
        vals = []
        for rec in self:
            vals.append(rec._prepare_production_statistic())
        prod_stat = self.env["production.statistic"].with_user(
            self.env.ref("base.user_root")).create(vals)
        return prod_stat

    def do_finish(self):
        action = super().do_finish()
        self._create_production_statistic()
        return action
