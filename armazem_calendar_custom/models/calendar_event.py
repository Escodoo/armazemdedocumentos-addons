# Copyright 2026 - TODAY, Wesley Oliveira <wesley.oliveira@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models

CALENDAR_LAYOUT = "armazem_calendar_custom.mail_notification_calendar"


class CalendarEvent(models.Model):
    _inherit = "calendar.event"

    def message_notify(self, **kwargs):
        # Invitation, date change and reminder e-mails are sent with the light layout
        if kwargs.get("email_layout_xmlid") == "mail.mail_notification_light":
            kwargs["email_layout_xmlid"] = CALENDAR_LAYOUT
        return super().message_notify(**kwargs)

    def action_open_composer(self):
        action = super().action_open_composer()
        action["context"]["default_email_layout_xmlid"] = CALENDAR_LAYOUT
        return action
