from dataclasses import dataclass
@dataclass(frozen=True)
class KodVeri:
    label: str

PUANTAJ_KODLARI = {
    "G": KodVeri(label="Geldi"),
    "Y": KodVeri(label="Yarım Gün"),
    "İ": KodVeri(label="Ücretli İzin"),
    "U": KodVeri(label="Ücretsiz İzin"),
    "X": KodVeri(label="Devamsız"),
}
