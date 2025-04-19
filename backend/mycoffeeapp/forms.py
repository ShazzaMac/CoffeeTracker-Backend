from django import forms
from .models import PriceEntry
from .utils import allowed_file  

# form not tied to a model - for manual entry
# This form is used for manual entry of price data
class PriceForm(forms.Form):
    establishment = forms.CharField(max_length=100)
    date = forms.DateField()
    beverage = forms.ChoiceField(choices=[...])  # Replace with real choices
    price = forms.DecimalField(max_digits=6, decimal_places=2)
    submitter_name = forms.CharField(max_length=100)

# form for OCR uploads
class PriceEntryForm(forms.ModelForm):
    document = forms.FileField(label="Upload Document", required=False)
    ocr_text = forms.CharField(widget=forms.Textarea, required=False, label="OCR Extracted Text (Editable)")

    class Meta:
        model = PriceEntry
        fields = ["manual_text", "document", "ocr_text"]

    def clean_document(self):
        document = self.cleaned_data.get("document")
        if document and not allowed_file(document.name):
            raise forms.ValidationError("Invalid file type")
        return document

    def clean_ocr_text(self):
        ocr_text = self.cleaned_data.get("ocr_text")
        if ocr_text and len(ocr_text) < 10:
            raise forms.ValidationError("OCR text is too short")
        return ocr_text
