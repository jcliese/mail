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

categories = [(books, "books"), (dvd, "dvd"), (electronics, "electronics"), (fashion, "fashion"), (home, "home"), (office, "office"), (pet, "pet"), (shoes, "shoes"), (software, "software"), (toys, "toys"), (unassigned, "unassigned")]


class ImageForm(forms.Form):
    listing_title = forms.CharField(max_length=256)
    imgfile = forms.ImageField(label='Select an image', required=False)
    min_price = forms.FloatField(min_value=1.0)
    description = forms.CharField()
    category = forms.ChoiceField(choices=categories, initial="unassigned")