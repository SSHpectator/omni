input_file = "alive.txt"  # File originale
output_file = "cleaned_alive.txt"  # File di output

# Funzione per rimuovere i numeri iniziali
def clean_urls(input_file, output_file):
    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        for line in infile:
            # Split la riga per rimuovere la parte numerica iniziale
            cleaned_line = line.split(maxsplit=1)[-1].strip()
            outfile.write(cleaned_line + "\n")

clean_urls(input_file, output_file)
print(f"[+] File pulito salvato in {output_file}")
