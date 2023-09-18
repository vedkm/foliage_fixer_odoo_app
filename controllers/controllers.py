# -*- coding: utf-8 -*-
# from odoo import http


# class FoliageFixerApp(http.Controller):
#     @http.route('/foliage_fixer_app/foliage_fixer_app', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/foliage_fixer_app/foliage_fixer_app/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('foliage_fixer_app.listing', {
#             'root': '/foliage_fixer_app/foliage_fixer_app',
#             'objects': http.request.env['foliage_fixer_app.foliage_fixer_app'].search([]),
#         })

#     @http.route('/foliage_fixer_app/foliage_fixer_app/objects/<model("foliage_fixer_app.foliage_fixer_app"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('foliage_fixer_app.object', {
#             'object': obj
#         })
