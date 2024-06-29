from odoo import http
from odoo.http import request
from odoo.addons.http_routing.models.ir_http import slug

class FurnitureRental(http.Controller):
    @http.route(['/appliances-and-furniture-for-rent'], type='http', auth="public", website=True)
    def appliances_and_furniture_for_rent(self, **kwargs):
        """
            Handles the route for displaying furniture and appliance rental categories.

            This method retrieves references to predefined furniture categories and
            constructs a list of dictionaries, each containing the name, URL, and image
            URL of a category. The constructed list is then passed to the template for
            rendering the categories on the webpage.

            :param kwargs: Additional keyword arguments (currently unused).
            :return: Rendered webpage displaying the furniture and appliance rental categories.
        """
        categories_url = '/shop/category/'
        categories = [
            {
                'name': 'Bed Room Furniture for Rent',
                'url': '%s%s' % (categories_url, slug(request.env.ref('furniture_renting_system.category_bed_room_furniture_rent'))),
                'image_url': '/furniture_renting_system/static/src/img/bed_room_furniture.jpg',
            },
            {
                'name': 'Dining Room Furniture for Rent',
                'url': '%s%s' % (categories_url, slug(request.env.ref('furniture_renting_system.category_dining_room_furniture_rent'))),
                'image_url': '/furniture_renting_system/static/src/img/dining_room_furniture.jpg',
            },
            {
                'name': 'Living Room Furniture for Rent',
                'url': '%s%s' % (categories_url, slug(request.env.ref('furniture_renting_system.category_living_room_furniture_rent'))),
                'image_url': '/furniture_renting_system/static/src/img/living_room_furniture.jpg',
            },
            {
                'name': 'Study Room Furniture for Rent',
                'url': '%s%s' % (categories_url, slug(request.env.ref('furniture_renting_system.category_study_room_furniture_rent'))),
                'image_url': '/furniture_renting_system/static/src/img/study_room_furniture.jpg',
            },
        ]
        return request.render("furniture_renting_system.appliances_and_furniture_for_rent_template", {
            'categories': categories
        })