# Gebruikersgegevens
opgeslagen_gebruiker = "admin"
opgeslagen_pincode = "1234"

# Status variabelen
pogingen = 0
max_pogingen = 3
toegang = False

print("--- Beveiligd Inlogsysteem ---")

while pogingen < max_pogingen:
    invul_naam = input("Gebruikersnaam: ")
    invul_pin = input("Pincode: ")

    if invul_naam == opgeslagen_gebruiker and invul_pin == opgeslagen_pincode:
        print("\nInloggen geslaagd! Welkom.")
        toegang = True
        break  # Stop de loop direct bij succes
    else:
        pogingen += 1
        over = max_pogingen - pogingen
        print(f"Onjuist! Je hebt nog {over} poging(en) over.")
        print("-" * 30)

# Controleer of de gebruiker binnen is of geblokkeerd is
if toegang:
    print("Je hebt nu toegang tot je banksaldo en transacties.")
    # Hier zou je de code van je bankprogramma kunnen plakken!
else:
    print("\nSysteem geblokkeerd. Neem contact op met de bank.")
