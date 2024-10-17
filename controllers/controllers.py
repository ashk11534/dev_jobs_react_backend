from odoo import http
from odoo.http import request as req
import json, base64
from bs4 import BeautifulSoup

class FetchJobs(http.Controller):

    @http.route('/dev-jobs', type='http', methods=['GET', 'OPTIONS'], auth='none', cors='*')
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
            ('Access-Control-Allow-Methods', 'GET, OPTIONS'),
        ])

    @http.route('/job-details/<int:job_id>', type='http', methods=['GET', 'OPTIONS'], auth='none', cors='*')
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
            ('Access-Control-Allow-Methods', 'GET, OPTIONS')
        ])

    @http.route('/job-application', type='http', methods=['POST', 'OPTIONS'], auth='none', csrf=False, cors='*')
    def submit_application(self, **kwargs):
        form_data = req.httprequest.form
        email = form_data.get('email').strip() if form_data.get('email') else ''
        cover_letter = form_data.get('coverLetter').strip() if form_data.get('coverLetter') else ''
        resume = base64.b64encode(req.httprequest.files.get('resume').read()) if req.httprequest.files.get('resume') else None

        req.env['job.application'].sudo().create({
            'email': email,
            'cover_letter': cover_letter,
            'resume': resume
        })

        return req.make_response(json.dumps({'code': 200}), headers=[
            ('Content-Type', 'application/json'),
            ('Access-Control-Allow-Origin', '*'),
            ('Access-Control-Allow-Methods', 'POST, OPTIONS')
        ])

    @http.route('/job-search', type='http', methods=['POST', 'OPTIONS'], auth='none', csrf=False, cors='*')
    def search_job(self, **kwargs):
        form_data = req.httprequest.form

        print(form_data)

        title = form_data.get('title').strip() if form_data.get('title') else None
        location = form_data.get('location').strip() if form_data.get('location') else None
        fullTime = 'full_time' if form_data.get('fullTime') == 'true' else None

        query_list = ['|']

        if title:
            query_list.append(('job_title', 'ilike', title))
            query_list.append(('company_name', 'ilike', title))

        if location:
            query_list.append(('country.name', 'ilike', location))

        if fullTime:
            query_list.append(('job_type', '=', fullTime))

        if len(query_list) == 1 or len(query_list) == 2:
            query_list.remove('|')

        dev_jobs = req.env['dev.job'].sudo().search(query_list)

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

        print(title, location, fullTime)

        return req.make_response(json.dumps({'code': 200, 'dev_jobs': jobs_list}), headers=[
            ('Content-Type', 'application/json'),
            ('Access-Control-Allow-Origin', '*'),
            ('Access-Control-Allow-Methods', 'POST, OPTIONS')
        ])
