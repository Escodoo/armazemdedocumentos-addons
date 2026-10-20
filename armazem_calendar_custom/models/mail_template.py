# Copyright 2026 - TODAY, Wesley Oliveira <wesley.oliveira@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models

CALENDAR_TEMPLATES = (
    "calendar.calendar_template_meeting_invitation",
    "calendar.calendar_template_meeting_changedate",
    "calendar.calendar_template_meeting_reminder",
    "calendar.calendar_template_meeting_update",
)


class MailTemplate(models.Model):
    _inherit = "mail.template"

    @api.model
    def _armazem_sync_calendar_translations(self):
        """Copy the subject and body written by this module to every installed
        language, so the old translations of the calendar templates are not used."""
        templates = self.browse()
        for xmlid in CALENDAR_TEMPLATES:
            templates |= self.env.ref(xmlid, raise_if_not_found=False) or self.browse()
        langs = [
            code
            for code, _name in self.env["res.lang"].get_installed()
            if code != "en_US"
        ]
        for template in templates.with_context(lang="en_US"):
            values = {"subject": template.subject, "body_html": template.body_html}
            for lang in langs:
                template.with_context(lang=lang).write(values)
