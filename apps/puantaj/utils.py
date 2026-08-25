from datetime import date

def gun_editable_mi(personel, yil: int, ay: int, gun: int) -> bool:
    return personel.calisiyor_mu(date(yil, ay, gun))
