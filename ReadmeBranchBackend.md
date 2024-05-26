Ta gałąź dotyczy backendu

Work done as for now:
zrobione są wszystkie kontrakty *(na chwilę obecną wszystkie)* do komunikacji z frontendem.
Przetestowane, działa we front endzie tak, jak powinno. Kontrakt na chwilę obecną zostaje oficjalnie uznazny za zamknięty.

Teraz zadanie - niezwykle trudne, I know, to nasza najlepsza **(bo jedyna xD)** "baza danych"
tj. absolutny szczyt technologii jakim jest zapisywanie wszystkiego w olbrzymich dwóch jsonach.

Zajęło to zdecydowanie więcej czasu niż powinno, ale ***działa!!!!!!***
Profesjonalna baza danych jest


Dane są pod adresem /choices/...
do wyboru są prow - prowadzący, przed - przedmioty oraz rygory - czyli rygory XD

Format dodawania taska:

zrobić POST pod adres /tasks/
{
        "task": "Task 1",
        "studentID": 1,
        "start": "2024-05-28T21:00:00",
        "end": "2024-05-28T23:30:00"
    }

dodawanie timeframe:

zrobić POST pod adresem /timeframes/
{
    "start" : "2024-05-28 18:00",
    "end" : "2024-05-28 20:00"
}

planowanie:

zrobić POST pod adresem /plan/ (puste body)

wyświetlenie tasków:
GET pod adresem /tasks/

wyświetlanie zaplanowanych:
GET pod adresem /planne_tasks/