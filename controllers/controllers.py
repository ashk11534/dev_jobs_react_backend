from odoo import http
from odoo.http import request as req
import json, base64
from bs4 import BeautifulSoup

class FetchJobs(http.Controller):

    @http.route('/dev-jobs', type='http', methods=['GET', 'POST', 'OPTIONS'], auth='none', cors='*')
    def fetch_jobs(self):
        dev_jobs = req.env['dev.job'].sudo().search([])

        jobs_list = []

        for job in dev_jobs:
            if job.company_logo:
                image_base64 = base64.b64decode(job.company_logo)
                company_logo = base64.b64encode(image_base64).decode('utf-8')
            jobs_list.append({
                'job_id': job.id,
                'created_date': job.format_created_date(),
                'job_title': job.job_title,
                'job_type': job.job_type,
                'company_name': job.company_name,
                'company_logo': company_logo if company_logo else '',
                'country': job.country.name,
            })

        return req.make_response(json.dumps({'code': 200, 'dev_jobs': jobs_list}), headers=[
            ('Content-Type', 'application/json'),
            ('Access-Control-Allow-Origin', '*'),
            ('Access-Control-Allow-Methods', 'GET, POST, OPTIONS'),
        ])

    @http.route('/job-details/<int:job_id>', type='http', methods=['GET', 'POST', 'OPTIONS'], auth='none', cors='*')
    def job_details(self, job_id):
        job_obj = req.env['dev.job'].sudo().search([('id', '=', job_id)])

        if job_obj.company_logo:
            image_base64 = base64.b64decode(job_obj.company_logo)
            company_logo = base64.b64encode(image_base64).decode('utf-8')

        job_data = {
            'job_title': job_obj.job_title,
            'created_date': job_obj.format_created_date(),
            'job_type': job_obj.job_type,
            'job_description': BeautifulSoup(job_obj.job_description, 'html.parser').get_text(),
            'company_name': job_obj.company_name,
            'company_logo': company_logo if company_logo else '',
            'company_website_url': job_obj.company_website_url,
            'country': job_obj.country.name
        }

        return req.make_response(json.dumps({'code': 200, 'job_data': job_data}), headers=[
            ('Content-Type', 'application/json'),
            ('Access-Control-Allow-Origin', '*'),
            ('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        ])
