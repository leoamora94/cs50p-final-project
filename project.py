import csv, sys, re, datetime
from datetime import date
from reportlab.lib import colors, pagesizes
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, KeepTogether, Spacer


'''
--- LIST OF KEYS FROM .CSV FILE ---
    Nome                    - 2
    Sobrenome               - 3
    Data de nascimento      - 4
    Sexo                    - 5
    Categoria de Peso       - 8
    Categoria de Idade      - 9
    Arranco Inicial         - 10
    Arremesso Inicial       - 11
'''


# CONSTANTS VARIABLES
CHAMP = 'III Campeonato Cearense'
LOGO = './images/felp.png'

FILENAME = "subs.csv"

AGE_CATEGORIES = ['INF', 'YTH', 'JR', 'SR', 'UNI', 'M30', 'M35', 'M40', 'M45', 'M50', 'M55', 'M60']

DAY_ONE = date.today()
DAY_TWO = DAY_ONE + datetime.timedelta(days=1)
DAY_THREE = DAY_TWO + datetime.timedelta(days=1)

START_TIME = 8
WEIGHT_START_TIME = START_TIME - 2

def main():
    ''' TO-DO in next versions:
    Defines when event start and finish
    Defines at what time event start and finish (each day?)
    Defines if start list will be alternated between females and males, or not
    '''
    while True:
        try:
            NUM_PLATFORM = int(sys.argv[1])
            break
        except IndexError:
            sys.exit("You need to specify number of platforms avalible in event!")

    athletes = read_csv(FILENAME)

    kid_start_list, male_start_list, female_start_list = create_start_list(athletes, NUM_PLATFORM)

    generate_pdf_start_lists(kid_start_list, "./files/kids.pdf", 'K')
    generate_pdf_start_lists(male_start_list, "./files/males.pdf", 'M')
    generate_pdf_start_lists(female_start_list, "./files/females.pdf", 'F')

    print("Files were created successfully!")


def read_csv(filename):
    athletes = []
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        # append important data for start lists into a list
        for row in reader:
            # formatting datas
            snatch = int(row['Arranco Inicial'])
            cleanjerk = int(row['Arremesso Inicial'])
            total = int(row['Arranco Inicial']) + int(row['Arremesso Inicial'])

            athletes.append([               # index
                row['Sobrenome'].upper(),   # 0
                row['Nome'].title(),        # 1
                row['Data de nascimento'],  # 2
                row['Sexo'],                # 3
                row['Categoria de Idade'],  # 4
                row['Categoria de Peso'],   # 5
                snatch,                     # 6
                cleanjerk,                  # 7
                total                       # 8
            ])
    return athletes


def sort_key(athlete):
        num_part = int(re.search(r'\d+', athlete[5]).group())
        return (num_part, athlete[5], athlete[8])


def create_start_list(athletes, num_platforms):
    male_athletes = []      # Males YTH, JR, SR or Master
    female_athletes = []    # Females YTH, JR, SR or Master
    kid_athletes = []       # INF athletes (Male or Female)

    # appending each athlete into a different list
    for athlete in athletes:
        athlete_cat = [item.strip() for item in athlete[4].split(',')]

        if 'INF' in athlete_cat:
            kid_athletes.append(athlete)
        else:
            if athlete[3] == 'Masculino':
                male_athletes.append(athlete)
            elif athlete[3] == 'Femenino':
                female_athletes.append(athlete)

    # sorting athletes by ascending order of weight categories and total entry
    kid_athletes = sorted(kid_athletes, key=sort_key)
    male_athletes = sorted(male_athletes, key=sort_key)
    female_athletes = sorted(female_athletes, key=sort_key)

    # create start lists
    kid_start_lists = [kid_athletes[i:i+num_platforms] for i in range(0, len(kid_athletes), num_platforms)]
    male_start_lists = [male_athletes[i:i+num_platforms] for i in range(0, len(male_athletes), num_platforms)]
    female_start_lists = [female_athletes[i:i+num_platforms] for i in range(0, len(female_athletes), num_platforms)]

    return kid_start_lists, male_start_lists, female_start_lists


def generate_pdf_start_lists(start_lists, output_filename, genre):
    doc = SimpleDocTemplate(output_filename, pagesize=pagesizes.A4)
    content = []

    for index, start_list in enumerate(start_lists):
        if genre == 'K':
            data = [[f'GRUPO {genre}{index+1}  -  PESAGEM: {DAY_ONE} às {WEIGHT_START_TIME+index*2}:00  -  INICIO: {DAY_ONE} às {START_TIME+index*2}:00']]
        elif genre == 'F':
            data = [[f'GRUPO {genre}{index+1}  -  PESAGEM: {DAY_TWO} às {WEIGHT_START_TIME+index*2}:00  -  INICIO: {DAY_TWO} às {START_TIME+index*2}:00']]
        elif genre == 'M':
            data = [[f'GRUPO {genre}{index+1}  -  PESAGEM: {DAY_THREE} às {WEIGHT_START_TIME+index*2}:00  -  INICIO: {DAY_THREE} às {START_TIME+index*2}:00']]

        data.append(['SOBRENOME', 'NOME', 'DT NASC', 'CATEGORIA', 'ARRANCO', 'ARREMESSO', 'TOTAL'])

        for athlete in start_list:
            data.append([
                athlete[0],
                athlete[1],
                athlete[2],
                athlete[4] + " " + athlete[5],
                athlete[6],
                athlete[7],
                athlete[8]])

        table = Table(data, colWidths=[165,90,60,95,60,70,40])
        # Style of tables
        table.setStyle(TableStyle([
            ('SPAN', (0, 0), (-1, 0)),
            ('BACKGROUND', (0, 0), (-1, 1), colors.lightgrey),
            ('ALIGN', (2, 0), (2, -1), 'CENTER'),  # Center-align DT NASC column
            ('ALIGN', (3, 0), (3, -1), 'RIGHT'),   # Right-align CATEGORIA column
            ('ALIGN', (4, 0), (-1, -1), 'CENTER'), # Center-align the last three columns (ARRANCO, ARREMESSO, TOTAL)
            ('ALIGN', (0, 0), (-1, 0), 'LEFT'),    # Left-align HOURS (first row)
            ('ALIGN', (0, 1), (-1, 1), 'CENTER'),  # Center-align the HEADER (second row)
            ('FONTNAME', (0, 0), (-1, 1), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)])
        )

        content.append(KeepTogether(table))
        if index < len(start_lists) - 1:
            content.append(Spacer(1, 15))

    doc.build(content)


if __name__ == "__main__":
    main()
