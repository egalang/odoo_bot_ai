/** @odoo-module */
import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";

registry.category("discuss.channel_commands").add("ask_ai", {
    help: _t("Ask the AI bot a question (/ai your question)"),
    methodName: "execute_command_ask_ai",
});
