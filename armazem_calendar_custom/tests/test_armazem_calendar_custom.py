# Copyright 2026 - TODAY, Wesley Oliveira <wesley.oliveira@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import datetime, timedelta

from odoo.tests.common import TransactionCase

from ..models.mail_template import CALENDAR_TEMPLATES

ODOO_PURPLE = "#875A7B"
GREEN = "#009140"
DARK_GREEN = "#006B30"


class TestArmazemCalendarCustom(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.env["res.lang"]._activate_lang("pt_BR")
        cls.env["mail.template"]._armazem_sync_calendar_translations()
        cls.partner = cls.env["res.partner"].create(
            {"name": "Cliente Agenda", "email": "cliente.agenda@example.com"}
        )
        start = datetime.now() + timedelta(days=2)
        cls.event_vals = {
            "name": "Reunião de alinhamento",
            "start": start,
            "stop": start + timedelta(hours=1),
            "location": "Joinville",
        }

    def test_templates_use_company_green_in_portuguese(self):
        for xmlid in CALENDAR_TEMPLATES:
            for lang in ("en_US", "pt_BR"):
                template = self.env.ref(xmlid).with_context(lang=lang)
                self.assertNotIn(ODOO_PURPLE, template.body_html, xmlid)
                self.assertIn(GREEN, template.body_html, xmlid)
                self.assertIn("Detalhes do evento", template.body_html, xmlid)

    def test_invitation_mail_uses_armazem_layout(self):
        event = self.env["calendar.event"].create(
            dict(self.event_vals, partner_ids=[(4, self.partner.id)])
        )
        mail = self.env["mail.mail"].search(
            [("model", "=", "calendar.event"), ("res_id", "=", event.id)]
        )
        self.assertEqual(len(mail), 1)
        self.assertIn("Convite para reunião", mail.body_html)
        self.assertIn(DARK_GREEN, mail.body_html)
        self.assertNotIn(ODOO_PURPLE, mail.body_html)
        self.assertNotIn("Powered by", mail.body_html)

    def test_other_layouts_are_kept(self):
        event = self.env["calendar.event"].create(self.event_vals)
        event.with_context(mail_notify_force_send=False).message_notify(
            partner_ids=self.partner.ids,
            body="Aviso",
            email_layout_xmlid="mail.mail_notification_layout",
        )
        mail = self.env["mail.mail"].search(
            [("model", "=", "calendar.event"), ("res_id", "=", event.id)]
        )
        self.assertEqual(len(mail), 1)
        self.assertNotIn(DARK_GREEN, mail.body_html)

    def test_composer_uses_armazem_layout(self):
        event = self.env["calendar.event"].create(
            dict(self.event_vals, partner_ids=[(4, self.partner.id)])
        )
        action = event.action_open_composer()
        self.assertEqual(
            action["context"]["default_email_layout_xmlid"],
            "armazem_calendar_custom.mail_notification_calendar",
        )
