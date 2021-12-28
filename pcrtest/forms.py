from django import forms

class LoginForm(forms.Form):
    """ Form to login to existing block as existing user """

    blockchain_id = forms.CharField(max_length=8, label="Blokkæde-ID",
                                    help_text="Indtast blokkædens ID")

    miner_id = forms.CharField(max_length=8, label="Minearbejder-ID",
                               help_text="Indtast dit minearbejder-ID")


    # def clean_blockchain_id(self):
    #     """ Additional validation of the form's blockchain_id field """
    #     blockchain_id = self.cleaned_data['blockchain_id'].lower()
    #     if not Blockchain.objects.filter(id=blockchain_id).exists():
    #         raise forms.ValidationError(
    #             'Der findes ingen blokkæde med dette ID.')
    #     return blockchain_id
