from odoo import models, fields, api, _
from odoo.exceptions import UserError
from ast import literal_eval
import requests
import base64
import base64
import mimetypes
import logging
_logger = logging.getLogger(__name__)
class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    enable_pdf_upload = fields.Boolean(
        string='Enable PDF Upload',
        config_parameter='odoo_bot_ai.enable_pdf_upload',
        default=False,
        help='Enable or disable the PDF upload feature.'
    )

    def action_odoobotai_pdf_upload(self):
        """Opens the view for managing Odoo Bot AI PDF uploads."""
        action = self.env["ir.actions.actions"]._for_xml_id("odoo_bot_ai.action_pdf_upload")  # Replace 'your_module' with the actual name of your module
        return action


class OdooBotAIConfig(models.Model):
    _name = 'odoobotai.config'
    _description = 'Odoo Bot AI Configuration'

    name = fields.Char(
        string="Configuration Name", 
        default="Odoo Bot AI Config", 
        required=True
    )
    api_url = fields.Char(
        string="API URL", 
        required=True,
        default='http://host.docker.internal:8000/'
    )
    in_used = fields.Boolean(
        string="In Use", 
        default=False,
        help="Only one configuration can be active at a time."
    )
    pdf_upload_ids = fields.One2many(
        'pdf.uploads', 
        'config_id', 
        string="PDF Uploads"
    )
    enable_pdf_upload = fields.Boolean(
        string='Enable PDF Upload',
        default=False,
        help='Enable or disable the PDF upload feature.'
    )

    @api.constrains('in_used')
    def _check_single_in_used(self):
        for rec in self:
            if rec.in_used:
                others = self.search([('in_used', '=', True), ('id', '!=', rec.id)])
                if others:
                    raise UserError(_("Only one configuration can be set as 'In Use'."))
                
class PdfUpload(models.Model):
    _name = 'pdf.uploads'
    _description = 'PDF Uploads'

    name = fields.Char(string="File Name", required=True)
    file_data = fields.Binary(string="PDF File", required=True)
    extension = fields.Char(string="Extension", compute="_compute_extension", store=True)
    mimetype = fields.Char(string="MIME Type", compute="_compute_mimetype", store=True)
    status = fields.Selection([
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed')
    ], string="Status", default='pending')
    config_id = fields.Many2one(
        'odoobotai.config', 
        string="Configuration", 
        ondelete='cascade'
    )

    @api.depends('name')
    def _compute_extension(self):
        for record in self:
            if record.name and '.' in record.name:
                record.extension = record.name.split('.')[-1].lower()
            else:
                record.extension = ''

    @api.depends('file_data', 'name')
    def _compute_mimetype(self):
        for record in self:
            mt, _ = mimetypes.guess_type(record.name) if record.name else (None, None)
            record.mimetype = mt or 'application/pdf'

    def upload_pdf_to_api(self):
        """Uploads the PDF file to an external API and updates the status."""
        self.ensure_one()
        config_rec = self.env['odoobotai.config'].search([('in_used', '=', True)], limit=1).sudo()
        if config_rec:
            base_url = config_rec.api_url
        else:
            base_url = 'http://host.docker.internal:8000/'
        api_url = base_url.rstrip('/') + '/upload_pdf/'
                
        try:
            file_content = base64.b64decode(self.file_data) if self.file_data else b''
            files = {'file': (self.name, file_content, self.mimetype)}
            response = requests.post(api_url, files=files, timeout=1000)
            _logger.info(response)
            if response.status_code == 200:
                self.status = 'success'
            else:
                self.status = 'failed'
            return response.json()
        
        except Exception as e:
            self.status = 'failed'
            return {'error': str(e)}

    @api.model
    def create(self, vals):
        # Create the record first
        record = super(PdfUpload, self).create(vals)
        # If file_data is provided, automatically trigger the API upload
        if vals.get('file_data'):
            record.upload_pdf_to_api()
        return record

    def write(self, vals):
        res = super(PdfUpload, self).write(vals)
        # If the file_data field is updated, trigger the API upload on all affected records
        if vals.get('file_data'):
            for rec in self:
                rec.upload_pdf_to_api()
        return res
    def unlink(self):
        # """Deletes the record and calls the API to remove the corresponding vectors."""
        for record in self:
            config_rec = self.env['odoobotai.config'].search([('in_used', '=', True)], limit=1).sudo()
            if config_rec:
                base_url = config_rec.api_url
            else:
                base_url = 'http://host.docker.internal:8000/'
            delete_api_url = base_url.rstrip('/') + '/vectors'
            params = {'filename': record.name}
            try:
                response = requests.delete(delete_api_url, params=params, timeout=10)
                _logger.info(f"API delete response for {record.name}: {response.status_code}, {response.text}")
                if response.status_code != 200:
                    _logger.warning(f"Failed to delete vectors for {record.name} from API. Status code: {response.status_code}, Response: {response.text}")
            except requests.exceptions.RequestException as e:
                _logger.error(f"Error calling API to delete vectors for {record.name}: {e}")
            return super(PdfUpload, self).unlink()
