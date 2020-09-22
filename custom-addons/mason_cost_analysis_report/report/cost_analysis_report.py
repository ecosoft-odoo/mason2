# Copyright 2020 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import models, fields, api, tools
from datetime import timedelta


class CostAnalysisReportView(models.Model):
    _name = "cost.analysis.report.view"
    _description = "Cost Analysis Report View"
    _auto = False

    mo_name = fields.Char()
    wo_name = fields.Char()
    product_qty = fields.Float()
    budget_unit = fields.Float()
    qty_produced = fields.Float()
    labor_cost_day = fields.Float()
    multiplier = fields.Float()
    origin = fields.Char()
    duration = fields.Float()
    labor_type = fields.Selection(
        selection=[("labor_cost_piece", "Labor Cost/Piece"),
                   ("labor_cost_day", "Labor Cost/Day"),
                   ("labor_cost_day_ot", "Labor Cost/Day(OT)")],
        string="Labor Type",
    )

    def _query(self):
        query = """
            SELECT mw.id, mp.name AS mo_name, mw.name AS wo_name, mp.origin,
                   mp.product_qty, mw.budget_unit, mw.qty_produced, mc.labor_cost_day,
                   CASE WHEN mw.labor_type = 'labor_cost_piece' THEN mc.multiplier1
                        WHEN mw.labor_type = 'labor_cost_day' THEN mc.multiplier2
                        WHEN mw.labor_type = 'labor_cost_day_ot' THEN mc.multiplier3
                        ELSE 0 END AS multiplier,
                   mw.labor_type, mw.duration
            FROM mrp_production mp
            LEFT JOIN mrp_workorder mw ON mp.id = mw.production_id
            LEFT JOIN mrp_workcenter mc ON mw.workcenter_id = mc.id
            WHERE mw.state = 'done'
            ORDER BY mp.name, mw.name
        """
        return query

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("""CREATE OR REPLACE VIEW %s AS (%s)""" % (
            self._table, self._query()))

    def get_hour_spent(self, duration):
        return timedelta(minutes=duration).total_seconds() / 3600


class CostAnalysisReport(models.TransientModel):
    _name = "cost.analysis.report"
    _description = "Cost Analysis Report"

    labor_type = fields.Selection(
        selection=[("labor_cost_piece", "Labor Cost/Piece"),
                   ("labor_cost_day", "Labor Cost/Day"),
                   ("labor_cost_day_ot", "Labor Cost/Day(OT)")],
        string="Labor Type",
    )
    results = fields.Many2many(
        comodel_name="cost.analysis.report.view",
        compute="_compute_results",
        help="Use compute fields, so there is nothing store in database",
    )

    def _compute_results(self):
        self.ensure_one()
        dom = []
        if self.labor_type:
            dom += [("labor_type", "=", self.labor_type)]
        self.results = self.env["cost.analysis.report.view"].search(dom)

    def print_report(self, report_type="qweb"):
        self.ensure_one()
        xml_id = "mason_cost_analysis_report.action_cost_analysis_report"
        action = (
            report_type == "xlsx"
            and self.env.ref("{}_xlsx".format(xml_id))
            or self.env.ref("{}_pdf".format(xml_id))
        )
        return action.report_action(self, config=False)

    def _get_html(self):
        result = {}
        rcontext = {}
        context = dict(self.env.context)
        report = self.browse(context.get("active_id"))
        if report:
            rcontext["o"] = report
            result["html"] = self.env.ref(
                "mason_cost_analysis_report.cost_analysis_report_html"
            ).render(rcontext)
        return result

    @api.model
    def get_html(self, given_context=None):
        return self.with_context(given_context)._get_html()
