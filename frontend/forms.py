from django import forms

operators = (
        ("AO", "Αττική Οδός"),
        ("EG", "Εγνατία"),
        ("GF", "Γέφυρα"),
        ("KO", "Κεντρική Οδός"),
        ("MR", "Μορέας"),
        ("NE", "Νέα Οδός"),
        ("OO", "Ολυμπία Οδός"),
)
no_stations = (20, 13, 1, 10, 9, 17, 14)


def construct_stations():
    form = []
    for i in range(7):
        stations = []
        for j in range(no_stations[i]):
            stations.append( (operators[i][0] + str(j).zfill(2),
                "Station " + str(j)) )
        form.append( (operators[i][1], tuple(stations)) )
    return tuple(form)



class Operators(forms.Form):
    op1 = forms.ChoiceField(choices=operators,
        required=True, label="Operator 1")
    op2 = forms.ChoiceField(choices=operators,
        required=True, label="Operator 2")

class Operator(forms.Form):
    op = forms.ChoiceField(choices=operators,
        required=True, label="Pick an operator")

class Station(forms.Form):
    station = forms.ChoiceField(choices=construct_stations(),
        required=True, label="Pick a station")
    

    