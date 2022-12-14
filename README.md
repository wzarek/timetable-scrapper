# Narzędzie do upraszczania planu zajęć - Uniwersytet Opolski
## Timetable scrapper for University Of Opole <p clear='both'>[<a href="#en">EN</a>]</p>
![last commit](https://img.shields.io/github/last-commit/wzarek/timetable-scrapper)
[![link](https://img.shields.io/badge/link_to-web-red)](https://timetable.wzarek.me/)

## Jak to działa?
Jak wiadomo, plan na Uniwersytecie Opolskim podawany jest w dość nieprzejrzystej formie, a dokładniej w arkuszu Excela. Postawiliśmy więc sobie zadanie, aby maksymalnie uprościć podany plan i pokazać go w przejrzystej, graficznej formie. Dodatkowym aspektem tego projektu jest plik iCal, który generowany jest do każdego planu. Dzięki niemu mamy możliwość umieszczenia naszego rozkładu zajęć w kalendarzu np. w telefonie. Całość jest jak najbardziej prosta i przejrzysta, a dodatkowo został stworzony poradnik do obsługi aplikacji, aby każdy użytkownik, bez wyjątków, mógł z łatwością odszyfrować jego plan zajęć. 

## Dolnośląska Szkoła Wyższa
Dzięki [raczu](https://github.com/raczu) i jego [projektowi](https://github.com/raczu/DSW-schedule-scrapper) będziemy w stanie do listy obsługiwanych uczelni dodać również DSW, co pozwala na dalszy rozwój projektu.

<div id='en'></div>

## How it works?
We're downloading excel files for specific fields of study (will be automated soon) and then parsing its rows to the dictionary.
Then it's filtered by chosen groups, parsed to ical file and shown on the screen with a link to the generated ical included.

## University of Lower Silesia
Thanks to [raczu](https://github.com/raczu) and his [project](https://github.com/raczu/DSW-schedule-scrapper) now we can implement timetable views for University of Lower Silesia.

## Screenshots
![home](https://firebasestorage.googleapis.com/v0/b/portfolio-web-dev-bed65.appspot.com/o/images%2Ftimetable-scrapper%2FtimetableScrapper-1.jpg?alt=media&token=5141dd2a-1e92-4b13-9ccc-56b7a60cc993)
![group choosing](https://firebasestorage.googleapis.com/v0/b/portfolio-web-dev-bed65.appspot.com/o/images%2Ftimetable-scrapper%2FtimetableScrapper-2.jpg?alt=media&token=85acaedd-fa0e-4ead-b63e-bff48a8fe953)
![timetable](https://firebasestorage.googleapis.com/v0/b/portfolio-web-dev-bed65.appspot.com/o/images%2Ftimetable-scrapper%2FtimetableScrapper-3.jpg?alt=media&token=77a6c6c2-139e-43e7-99d8-165968b1bc48)
![tutorial](https://firebasestorage.googleapis.com/v0/b/portfolio-web-dev-bed65.appspot.com/o/images%2Ftimetable-scrapper%2FtimetableScrapper-4.jpg?alt=media&token=b37b3546-3173-4663-b05d-487291c98e18)
