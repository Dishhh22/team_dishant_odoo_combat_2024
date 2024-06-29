import json
import logging
import pprint

import requests
import werkzeug
from werkzeug import urls

from odoo import http, _
from odoo.exceptions import ValidationError
from odoo.http import request

_logger = logging.getLogger(__name__)


class PaystackController(http.Controller):
    _notify_url = '/payment/paystack/ipn/'
    _return_url = '/payment/paystack/dpn'

    def _validate_data_authenticity(self, **post):
        # this method is used to validate transaction from paystack transaction on base of reference code
        res = False
        if post.get('reference') and request.session.get('paystack_reference'):
            post['transactionReference'] = request.session['paystack_reference']
            del request.session['paystack_reference']
            tx_sudo = request.env['payment.transaction'].sudo()._get_tx_from_notification_data(
                'paystack', post
            )
            if tx_sudo:
                headers = {
                    'Authorization': 'Bearer ' + tx_sudo.sudo().provider_id.paystack_secret_key,
                }
                # verify transaction status from paystack
                # from the doc https://paystack.com/docs/api/#transaction-verify
                resp = requests.get('https://api.paystack.co/transaction/verify/' + post.get('reference'), headers=headers)
                resp.raise_for_status()
                resp = json.loads(resp.content)
                # if no error and status is success than proceed further
                post['status'] = resp['data'].get('status')
                post['error'] = resp['data'].get('log') and resp['data']['log'].get('errors')
                if resp['data'].get('status') == 'success':
                    _logger.info('Paystack: validated data')
                    # Handle the notification data
                    tx_sudo._handle_notification_data('paystack', post)
                    return post
                error_message = "PayStack: " + _("Data were not acknowledged.")
                tx_sudo._set_error(error_message)
                raise ValidationError(error_message)
        raise ValidationError("PayStack:" + _("Can't find transaction reference."))

    @http.route('/paystack/redirect/hack', type='http', auth='public', methods=['POST'], csrf=False, website=True)
    def paystack_redirect_hack(self, **post):
        # this is hook method to redirect header with the paystack create page for the payment redirect
        # https://paystack.com/docs/api/#page-create link to the documentation
        headers = {
            'Authorization': post['Authorization'],
            'Content-Type': post['Content-Type'],
        }
        del post['Authorization']
        del post['Content-Type']
        post['amount'] = float(post['amount'])
        # currently giving static redirect url to return on the odoo payment page and process further
        # _return_url = 'payment/paystack/dpn/'
        post['redirect_url'] = urls.url_join(request.httprequest.host_url, self._return_url)

        # redirecting to the https://api.paystack.co/page URL for paystack payment page with the headers
        resp = requests.post('https://api.paystack.co/page', data=json.dumps(post), headers=headers)
        content = json.loads(resp.content)
        if not content['status']:
            return request.redirect(self._return_url + '?error=' + content['message'])
        resp.raise_for_status()
        # redirecting to the payment url which is created from the paystack api and given in response through the slug
        # and the page is accessible at https://paystack.com/pay/[slug]
        url_query_param = ('first_name=%s&email=%s' % (post.get('name', ''), post.get('email', '')))
        return request.redirect('https://paystack.com/pay/%s?%s' % (content['data']['slug'], url_query_param), local=False)

    @http.route(_notify_url, type='http', auth='public', methods=['POST'], csrf=False)
    def paystack_ipn(self, **post):
        _logger.info('Beginning Paystack IPN form_feedback with post data %s', pprint.pformat(post))  # debug
        try:
            # Check the origin and integrity of the notification
            self._validate_data_authenticity(**post)
        except ValidationError:
            _logger.exception("unable to handle the IPN data; skipping to acknowledge the notif")
        return ''

    @http.route(_return_url, type='http', auth="public", methods=['POST', 'GET'], csrf=False)
    def paystack_dpn(self, error=False, **post):
        _logger.info('Beginning Paystack DPN form_feedback with post data %s', pprint.pformat(post))
        try:
            post = self._validate_data_authenticity(**post)
        except ValidationError:
            _logger.exception('Unable to validate the Paystack payment')
            # The transaction has been moved to state 'error'. Redirect to /payment/status.
            if error:
                return request.render("payment_paystack.cancelled_payment",
                    {'message': error})
        return request.redirect('/payment/status')
