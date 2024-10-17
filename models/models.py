from odoo import fields, models, api
from datetime import datetime

class DevJob(models.Model):
    _name = 'dev.job'
    _description = 'dev.job'
    _rec_name = 'job_title'
    _order = 'id desc'

    job_title = fields.Char(string='Job title')
    job_type = fields.Selection([
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time')
    ], string='Job type')
    job_description = fields.Html(string='Job description')
    company_name = fields.Char(string='Company name')
    company_logo = fields.Image(string='Company logo')
    company_website_url = fields.Char(string='Company website url')
    country = fields.Many2one('res.country', string='Country')

    def format_created_date(self):
        date_obj = datetime.strptime(str(self.create_date.date()), "%Y-%m-%d")
        formatted_date = date_obj.strftime("%B %d, %Y")

        return formatted_date


class JobApplication(models.Model):
    _name = 'job.application'
    _description = 'job.application'
    _order = 'id desc'

    email = fields.Char(string='Email')
    cover_letter = fields.Html(string='Cover letter')
    resume = fields.Binary(string='Resume')
