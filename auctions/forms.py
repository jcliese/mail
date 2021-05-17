from django import forms


books = "books"
dvd = "dvd"
electronics = "electronics"
fashion = "fashion"
home = "home"
office = "office"
pet = "pet"
shoes ="shoes"
software = "software"
toys = "toys"
unassigned = "unassigned"

categories = [(books, "Books"), (dvd, "DVD"), (electronics, "Electronics"), (fashion, "Fashion"), (home, "Home"), (office, "Office"), (pet, "Pet"), (shoes, "Shoes"), (software, "Software"), (toys, "Toys"), (unassigned, "Unassigned")]


class ImageForm(forms.Form):
    listing_title = forms.CharField(max_length=256, widget=forms.TextInput(attrs={'class': 'form-control'}))
    imgfile = forms.ImageField(label='Select an image', required=False)
    min_price = forms.FloatField(min_value=1.0, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    category = forms.ChoiceField(choices=categories, initial="unassigned", widget=forms.Select(attrs={'class': 'form-control'}))

class BidForm(forms.Form):
    def __init__(self,min_price):
        # call standard __init__
        super().__init__()
        #extend __init__
        min_val=min_price+1
        self.fields["bid_price"] = forms.FloatField(min_value=min_val, widget=forms.NumberInput(attrs={'class': 'form-control', 'name': 'bid_price'}))

    bid_price = forms.FloatField()