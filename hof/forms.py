from .models import *


class AddMultipleScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = ['task', 'acquired_blood_cells']

    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
