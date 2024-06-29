/** @odoo-module */
//alert("hello")
import checkoutForm from 'payment.checkout_form';
import manageForm from 'payment.manage_form';
var ajax = require('web.ajax');

const paystackMixin = {

    /**
     * Redirect the customer to Paystack hosted payment page.
     *
     * @override method from payment.payment_form_mixin
     * @private
     * @param {string} code - The code of the payment option
     * @param {number} paymentOptionId - The id of the payment option handling the transaction
     * @param {object} processingValues - The processing values of the transaction
     * @return {undefined}
     */
    _processRedirectPayment: function (code, paymentOptionId, processingValues) {
        if (code !== 'paystack') {
            return this._super(...arguments);
        }
        var $form = $(processingValues.redirect_form_html);
        var paystack_wizard = $form.find('[name="paystack_wizard"]').val();
        if (paystack_wizard) {
            var self = this;
            const paystack = new PaystackPop();
            paystack.newTransaction({
                key: $form.find('[name="paystack_public_key"]').val(),
                email: $form.find('[name="email"]').val(),
                amount: $form.find('[name="amount"]').val(),
                onSuccess: (transaction) => {
                    var return_url = $form.find('[name="return_url"]').val();
                    window.location.href = return_url + "?reference=" + transaction.reference;
                },
                onCancel: () => {
                    window.location.reload();
                }
            });
        } else {
            return this._super(...arguments);
        }
    },
};

checkoutForm.include(paystackMixin);
manageForm.include(paystackMixin);
