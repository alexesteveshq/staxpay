/** @odoo-module **/

import { _t } from '@web/core/l10n/translation';
import paymentForm from '@payment/js/payment_form';
import { RPCError } from '@web/core/network/rpc_service';

paymentForm.include({

    async _prepareInlineForm(providerId, providerCode, paymentOptionId, paymentMethodCode, flow) {
        if (providerCode !== 'staxpay') {
            this._super(...arguments);
            return;
        }
        const radio = document.querySelector('input[name="o_payment_radio"]:checked');
        const inlineForm = this._getInlineForm(radio);
        const public_key = $(inlineForm).find('#staxpay_public_key').val()

        this.staxCheckout = new StaxJs(public_key, {
            number: {
                id: 'card-number',
                placeholder: '0000 0000 0000 0000',
                style: 'background: #ebebeb; padding: 10px; border-radius: 10px;',
                type: 'tel',
                format: 'prettyFormat',
            },
            cvv: {
                id: 'card-cvv',
                placeholder: 'CVV',
                style: 'background: #ebebeb; padding: 10px; border-radius: 10px;',
                type: 'text',
                format: 'prettyFormat',
            }
        });

        this.staxCheckout.showCardForm().then((handler) => {
            console.log("form was loaded");
        }).catch((err) => {
           console.log("there was an error loading the form: ", err);
        });
    },

    _initiatePaymentFlow(providerCode, paymentOptionId, paymentMethodCode, flow) {
        if (providerCode !== 'staxpay') {
            this._super(...arguments);
            return;
        }
        const _super = this._super.bind(this);
        var price = $(document).find('#o_payment_form').attr('data-amount')
        const year = $(this.target).find('#year').val()
        const month = $(this.target).find('#month').val()

        const data = this.rpc("/payment/staxpay/get_data", {partner_id: this.paymentContext.partnerId}).then((data) => {
            if (data.error !== undefined){
                this._displayErrorDialog(_t("Payment processing failed"), data.error);
                this._enableButton();
                return;
            }
            const extraDetails = {
              total: parseFloat(price),
              firstname: data.firstname,
              lastname: data.lastname,
              method: 'card',
              year: year,
              month: month,
              phone: data.phone,
              address_1: data.address,
              address_city: data.city,
              address_state: data.state,
              address_zip: data.zip,
              address_country: data.country,
              send_receipt: false,
              match_customer: false,
              validate: false,
              meta: {
                invoice_merchant_custom_fields: [
                  {
                    id: data.merchant_code,
                  },
                ],
              },
            };

            this.staxCheckout.pay(extraDetails).then((response) => {
              console.log("invoice object:", response);
              _super(...arguments)
            }).catch((err) => {
              if (err.message !== undefined){
                this._displayErrorDialog(_t("Payment processing failed"), err.message);
              }else if(err.payment_attempt_message !== undefined){
                this._displayErrorDialog(_t("Payment processing failed"), err.payment_attempt_message);
              }else{
                 this._displayErrorDialog(_t("Payment processing failed"), JSON.stringify(err));
              }
              this._enableButton();
            });
        })
    },
});
