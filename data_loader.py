########################################
##          1. Data Loading           ##
########################################

import pandas as pd

# 1.1 Data Proper Loading
def get_data_from_file(files):
    l = []
    for f in files:
        df = pd.read_csv(f, index_col=None, header=0)
        l.append(df)
    df = pd.concat(l)
    return df

def get_cleaned_data(df, flag):
    if flag == 'atp':
        # remove unnecessary info
        df = df[df['score'].str.contains(r'RET') == False]
        df = df[df['score'].str.contains(r'W/O') == False]
        df = df[df['score'].str.contains(r'DEF') == False]
        df = df[df['score'].str.contains(r'Def') == False]
        df = df[df['tourney_level'].str.contains(r'D') == False]
        df = df[df['tourney_name'].str.contains(r'Olympics') == False]
        df = df[df['tourney_name'].str.contains(r'Laver') == False]
        df = df[df['tourney_name'].str.contains(r'Dvis') == False]
        df = df[df['tourney_id'].str.contains(r'-615') == False]
        df = df[df['tourney_id'].str.contains(r'-0615') == False]
        df = df[df['tourney_id'].str.contains(r'-7696') == False]
        df = df[df['tourney_id'].str.contains(r'-8888') == False]

        # fix match date so as to concat atp and bet datasets
        df['year'] = df['tourney_date'].astype(str).str[0:4].astype(int)
        df['month'] = df['tourney_date'].astype(str).str[4:6].astype(int)
        df['day'] = df['tourney_date'].astype(str).str[6:8].astype(int)

        # fix player names so as to concat atp and bet datasets
        df[['winner_fname', 'winner_lname']] = df['winner_name'].str.split(' ', 1, expand=True)
        df[['loser_fname', 'loser_lname']] = df['loser_name'].str.split(' ', 1, expand=True)

        name_before = ['Ignacio Chela', 'Marcel Stebe', 'Hugues Herbert', 'Marinko Matosevic', 'Patric Smith',
                       'Lennard Struff', 'Vassallo Arguello', 'Hsun Lu', 'Hua Yang', 'Garcia Lopez', 'Rubin Statham',
                       'King Turner', 'Cervantes Huegun', 'Carlos Ferrero', 'Martin del Potro', 'Podlipnik Castillo',
                       'Martin Aranguren', 'Tae Im', 'Bogomolov Jr', 'Henri Mathieu', 'Ludovic Duclos', 'Ming Si',
                       'Xin Gong', 'Pablo Brzezicki', 'Rene Lisnard', 'Sebastian Cabal', 'Elyaas Deen Heshaam',
                       'Shanan Zayed', 'Angel Reyes Varela', 'Ignacio Londero', 'Young Jeong', 'Mecir Jr',
                       'Vijay Sundar Prashanth', 'Silva', 'Elahi Galan', 'Gomez Gb42', 'Shannan Zayid',
                       'Son Kwiatkowski', 'Woo Kwon', 'Andrea Huesler', 'Tseng', 'Mingjie Lin', 'Marco Moroni',
                       'Kumar Mukund', 'Pablo Ficovich', 'Pablo Varillas', 'J Wolf', 'Sung Nam', 'Martin Etcheverry',
                       'Agustin Tirante', 'Manuel Cerundolo', 'Lin Wu', 'Deheart', 'Bautista Agut']
        name_after = ['Chela', 'Stebe', 'Herbert', 'Matosevic', 'Smith', 'Struff', 'Arguello', 'Lu', 'Yang', 'Lopez',
                      'Statham', 'Turner', 'Cervantes', 'Ferrero', 'Potro', 'Podlipnik', 'Aranguren', 'Im', 'Bogomolov',
                      'Mathieu', 'Duclos', 'Si', 'Gong', 'Brzezicki', 'Lisnard', 'Cabal', 'Deen Heshaam', 'Zayed',
                      'Reyes Varela', 'Londero', 'Jeong', 'Mecir', 'Prashanth', 'Silva', 'Galan', 'Gomez', 'Zayid',
                      'Kwiatkowski', 'Kwon', 'Huesler', 'Tseng', 'Lin', 'Moroni', 'Mukund', 'Ficovich', 'Varillas',
                      'Wolf', 'Nam', 'Etcheverry', 'Tirante', 'Cerundolo', 'Wu', 'De Heart', 'Bautista']
        df['winner_lname'] = df['winner_lname'].replace(name_before, name_after)
        df['loser_lname'] = df['loser_lname'].replace(name_before, name_after)

    if flag == 'bet':
        # remove unnecessary info
        df = df[df['Comment'].str.contains(r'Retired') == False]
        df = df[df['Comment'].str.contains(r'Rrtired') == False]
        df = df[df['Comment'].str.contains(r'Disqualified') == False]
        df = df[df['Comment'].str.contains(r'Walkover') == False]
        # fix match date so as to concat atp and bet datasets
        df[['Month', 'Day', 'Year']] = df['Date'].str.split("/", expand=True)
        df['Month'] = df['Month'].astype(int)
        df['Day'] = df['Day'].astype(int)
        df['Year'] = df['Year'].astype(int)

        # fix player names so as to concat atp and bet datasets
        df[['Winner Last Name', 'w']] = df['Winner'].str.split(' ', 1, expand=True)
        df[['Loser Last Name', 'l']] = df['Loser'].str.split(' ', 1, expand=True)

        df.loc[df["Winner"] == "De Bakker T.", "Winner Last Name"] = "De Bakker"
        df.loc[df["Loser"] == "De Bakker T.", "Loser Last Name"] = "De Bakker"
        df.loc[df["Winner"] == "De Minaur A.", "Winner Last Name"] = "De Minaur"
        df.loc[df["Loser"] == "De Minaur A.", "Loser Last Name"] = "De Minaur"
        df.loc[df["Winner"] == "El Aynaoui Y.", "Winner Last Name"] = "El Aynaoui"
        df.loc[df["Loser"] == "El Aynaoui Y.", "Loser Last Name"] = "El Aynaoui"
        df.loc[df["Winner"] == "De Voest R.", "Winner Last Name"] = "De Voest"
        df.loc[df["Loser"] == "De Voest R.", "Loser Last Name"] = "De Voest"
        df.loc[df["Winner"] == "Van Der Merwe I.", "Winner Last Name"] = "Van Der Merwe"
        df.loc[df["Loser"] == "Van Der Merwe I.", "Loser Last Name"] = "Van Der Merwe"
        df.loc[df["Winner"] == "Saavedra Corvalan C.", "Winner Last Name"] = "Saavedra Corvalan"
        df.loc[df["Loser"] == "Saavedra Corvalan C.", "Loser Last Name"] = "Saavedra Corvalan"
        df.loc[df["Winner"] == "Ramirez-Hidalgo R.", "Winner Last Name"] = "Ramirez Hidalgo"
        df.loc[df["Loser"] == "Ramirez-Hidalgo R.", "Loser Last Name"] = "Ramirez Hidalgo"
        df.loc[df["Winner"] == "Dutra Silva R.", "Winner Last Name"] = "Dutra Silva"
        df.loc[df["Loser"] == "Dutra Silva R.", "Loser Last Name"] = "Dutra Silva"
        df.loc[df["Winner"] == "Dutra Da Silva R.", "Winner Last Name"] = "Dutra Silva"
        df.loc[df["Loser"] == "Dutra Da Silva R.", "Loser Last Name"] = "Dutra Silva"
        df.loc[df["Winner"] == "Roger-Vasselin E.", "Winner Last Name"] = "Roger Vasselin"
        df.loc[df["Loser"] == "Roger-Vasselin E.", "Loser Last Name"] = "Roger Vasselin"
        df.loc[df["Winner"] == "El Amrani R.", "Winner Last Name"] = "El Amrani"
        df.loc[df["Loser"] == "El Amrani R.", "Loser Last Name"] = "El Amrani"
        df.loc[df["Winner"] == "Di Mauro A.", "Winner Last Name"] = "Di Mauro"
        df.loc[df["Loser"] == "Di Mauro A.", "Loser Last Name"] = "Di Mauro"
        df.loc[df["Winner"] == "Munoz-De La Nava D.", "Winner Last Name"] = "Munoz de la Nava"
        df.loc[df["Loser"] == "Munoz-De La Nava D.", "Loser Last Name"] = "Munoz de la Nava"
        df.loc[df["Winner"] == "Huta Galung J.", "Winner Last Name"] = "Huta Galung"
        df.loc[df["Loser"] == "Huta Galung J.", "Loser Last Name"] = "Huta Galung"
        df.loc[df["Winner"] == "Dasnieres de Veigy J.", "Winner Last Name"] = "Dasnieres de Veigy"
        df.loc[df["Loser"] == "Dasnieres de Veigy J.", "Loser Last Name"] = "Dasnieres de Veigy"
        df.loc[df["Winner"] == "Dasnieres de Veigy J.", "Winner Last Name"] = "Dasnieres De Veigy"
        df.loc[df["Loser"] == "Dasnieres de Veigy J.", "Loser Last Name"] = "Dasnieres De Veigy"
        df.loc[df["Winner"] == "Van Der Merwe I.", "Winner Last Name"] = "Van Der Merwe"
        df.loc[df["Loser"] == "Van Der Merwe I.", "Loser Last Name"] = "Van Der Merwe"
        df.loc[df["Winner"] == "Haider-Maurer A.", "Winner Last Name"] = "Haider Maurer"
        df.loc[df["Loser"] == "Haider-Maurer A.", "Loser Last Name"] = "Haider Maurer"
        df.loc[df["Winner"] == "Bautista Agut R.", "Winner Last Name"] = "Bautista Agut"
        df.loc[df["Loser"] == "Bautista Agut R.", "Loser Last Name"] = "Bautista Agut"
        df.loc[df["Winner"] == "Carreno-Busta P.", "Winner Last Name"] = "Carreno Busta"
        df.loc[df["Loser"] == "Carreno-Busta P.", "Loser Last Name"] = "Carreno Busta"
        df.loc[df["Winner"] == "De Schepper K.", "Winner Last Name"] = "De Schepper"
        df.loc[df["Loser"] == "De Schepper K.", "Loser Last Name"] = "De Schepper"
        df.loc[df["Winner"] == "Al Mutawa J.", "Winner Last Name"] = "Al Mutawa"
        df.loc[df["Loser"] == "Al Mutawa J.", "Loser Last Name"] = "Al Mutawa"
        df.loc[df["Winner"] == "Brugues-Davi A.", "Winner Last Name"] = "Brugues Davi"
        df.loc[df["Loser"] == "Brugues-Davi A.", "Loser Last Name"] = "Brugues Davi"
        df.loc[df["Winner"] == "Gomez-Herrera C.", "Winner Last Name"] = "Gomez Herrera"
        df.loc[df["Loser"] == "Gomez-Herrera C.", "Loser Last Name"] = "Gomez Herrera"
        df.loc[df["Winner"] == "Menendez-Maceiras A.", "Winner Last Name"] = "Menendez Maceiras"
        df.loc[df["Loser"] == "Menendez-Maceiras A.", "Loser Last Name"] = "Menendez Maceiras"
        df.loc[df["Winner"] == "Deen Heshaam A.", "Winner Last Name"] = "Deen Heshaam"
        df.loc[df["Loser"] == "Deen Heshaam A.", "Loser Last Name"] = "Deen Heshaam"
        df.loc[df["Winner"] == "Reyes-Varela M.A.", "Winner Last Name"] = "Reyes Varela"
        df.loc[df["Loser"] == "Reyes-Varela M.A.", "Loser Last Name"] = "Reyes Varela"
        df.loc[df["Winner"] == "Carballes Baena R.", "Winner Last Name"] = "Carballes Baena"
        df.loc[df["Loser"] == "Carballes Baena R.", "Loser Last Name"] = "Carballes Baena"
        df.loc[df["Winner"] == "Artunedo Martinavarro A.", "Winner Last Name"] = "Artunedo Martinavarro"
        df.loc[df["Loser"] == "Artunedo Martinavarro A.", "Loser Last Name"] = "Artunedo Martinavarro"
        df.loc[df["Winner"] == "Vega Hernandez D.", "Winner Last Name"] = "Vega Hernandez"
        df.loc[df["Loser"] == "Vega Hernandez D.", "Loser Last Name"] = "Vega Hernandez"
        df.loc[df["Winner"] == "Ortega-Olmedo R.", "Winner Last Name"] = "Ortega Olmedo"
        df.loc[df["Loser"] == "Ortega-Olmedo R.", "Loser Last Name"] = "Ortega Olmedo"
        df.loc[df["Winner"] == "Samper-Montana J.", "Winner Last Name"] = "Samper Montana"
        df.loc[df["Loser"] == "Samper-Montana J.", "Loser Last Name"] = "Samper Montana"
        df.loc[df["Winner"] == "Lopez-Perez E.", "Winner Last Name"] = "Lopez Perez"
        df.loc[df["Loser"] == "Lopez-Perez E.", "Loser Last Name"] = "Lopez Perez"
        df.loc[df["Winner"] == "Van Rijthoven T.", "Winner Last Name"] = "Van Rijthoven"
        df.loc[df["Loser"] == "Van Rijthoven T.", "Loser Last Name"] = "Van Rijthoven"
        df.loc[df["Winner"] == "Ojeda Lara R.", "Winner Last Name"] = "Ojeda Lara"
        df.loc[df["Loser"] == "Ojeda Lara R.", "Loser Last Name"] = "Ojeda Lara"
        df.loc[df["Winner"] == "Auger-Aliassime F.", "Winner Last Name"] = "Augera Aliassime"
        df.loc[df["Loser"] == "Auger-Aliassime F.", "Loser Last Name"] = "Auger Aliassime"
        df.loc[df["Winner"] == "Seyboth Wild T.", "Winner Last Name"] = "Seyboth Wild"
        df.loc[df["Loser"] == "Seyboth Wild T.", "Loser Last Name"] = "Seyboth Wild"
        df.loc[df["Winner"] == "Zapata Miralles B.", "Winner Last Name"] = "Zapata Miralles"
        df.loc[df["Loser"] == "Zapata Miralles B.", "Loser Last Name"] = "Zapata Miralles"
        df.loc[df["Winner"] == "Roca Batalla O.", "Winner Last Name"] = "Roca Batalla"
        df.loc[df["Loser"] == "Roca Batalla O.", "Loser Last Name"] = "Roca Batalla"
        df.loc[df["Winner"] == "Lopez Villasenor G.", "Winner Last Name"] = "Lopez Villasenor"
        df.loc[df["Loser"] == "Lopez Villasenor G.", "Loser Last Name"] = "Lopez Villasenor"
        df.loc[df["Winner"] == "Davidovich Fokina A.", "Winner Last Name"] = "Davidovich Fokina"
        df.loc[df["Loser"] == "Davidovich Fokina", "Loser Last Name"] = "Davidovich Fokina"
        df.loc[df["Winner"] == "Vilella Martinez M.", "Winner Last Name"] = "Vilella Martinez"
        df.loc[df["Loser"] == "Vilella Martinez M.", "Loser Last Name"] = "Vilella Martinez"
        df.loc[df["Winner"] == "Diaz Acosta F.", "Winner Last Name"] = "Diaz Acosta"
        df.loc[df["Loser"] == "Diaz Acosta F.", "Loser Last Name"] = "Diaz Acosta"
        df.loc[df["Winner"] == "Barrios Vera M.T.", "Winner Last Name"] = "Barrios Vera"
        df.loc[df["Loser"] == "Barrios Vera M.T.", "Loser Last Name"] = "Barrios Vera"
        df.loc[df["Winner"] == "Van De Zandschulp B.", "Winner Last Name"] = "Van De Zandschulp"
        df.loc[df["Loser"] == "Van De Zandschulp B.", "Loser Last Name"] = "Van De Zandschulp"
        df.loc[df["Winner"] == "Diaz Acosta F.", "Winner Last Name"] = "Diaz Acosta"
        df.loc[df["Loser"] == "Diaz Acosta F.", "Loser Last Name"] = "Diaz Acosta"
        df.loc[df["Winner"] == "Gimeno-Traver D.", "Winner Last Name"] = "Gimeno Traver"
        df.loc[df["Loser"] == "Gimeno-Traver D.", "Loser Last Name"] = "Gimeno Traver"
        df.loc[df["Winner"] == "Del Potro J.M.", "Winner Last Name"] = "Potro"
        df.loc[df["Loser"] == "Del Potro J.M.", "Loser Last Name"] = "Potro"
        df.loc[df["Winner"] == "Del Potro J. M.", "Winner Last Name"] = "Potro"
        df.loc[df["Loser"] == "Del Potro J. M.", "Loser Last Name"] = "Potro"
        df.loc[df["Winner"] == "Garcia-Lopez G.", "Winner Last Name"] = "Lopez"
        df.loc[df["Loser"] == "Garcia-Lopez G.", "Loser Last Name"] = "Lopez"
        df.loc[df["Winner"] == "Vassallo-Arguello M.", "Winner Last Name"] = "Arguello"
        df.loc[df["Loser"] == "Vassallo-Arguello M.", "Loser Last Name"] = "Arguello"
        df.loc[df["Winner"] == "De Heart R.", "Winner Last Name"] = "De Heart"
        df.loc[df["Loser"] == "De Heart R.", "Loser Last Name"] = "De Heart"
        df.loc[df["Winner"] == "King-Turner D.", "Winner Last Name"] = "Turner"
        df.loc[df["Loser"] == "King-Turner D.", "Loser Last Name"] = "Turner"
        df.loc[df["Winner"] == "Navarro-Pastor I.", "Winner Last Name"] = "Navarro"
        df.loc[df["Loser"] == "Navarro-Pastor I.", "Loser Last Name"] = "Navarro"
        df.loc[df["Winner"] == "Deheart R.", "Winner Last Name"] = "De Heart"
        df.loc[df["Loser"] == "Deheart R.", "Loser Last Name"] = "De Heart"
        df.loc[df["Winner"] == "Del Bonis F.", "Winner Last Name"] = "Delbonis"
        df.loc[df["Loser"] == "Del Bonis F.", "Loser Last Name"] = "Delbonis"
        df.loc[df["Winner"] == "Riba-Madrid P.", "Winner Last Name"] = "Riba"
        df.loc[df["Loser"] == "Riba-Madrid P.", "Loser Last Name"] = "Riba"
        df.loc[df["Winner"] == "Ramos-Vinolas A.", "Winner Last Name"] = "Ramos"
        df.loc[df["Loser"] == "Ramos-Vinolas A.", "Loser Last Name"] = "Ramos"
        df.loc[df["Winner"] == "Gutierrez-Ferrol S.", "Winner Last Name"] = "Gutierrez Ferrol"
        df.loc[df["Loser"] == "Gutierrez-Ferrol S.", "Loser Last Name"] = "Gutierrez Ferrol"
        df.loc[df["Winner"] == "Auger-Aliassime F.", "Winner Last Name"] = "Auger Aliassime"
        df.loc[df["Loser"] == "Auger-Aliassime F.", "Loser Last Name"] = "Auger Aliassime"
        df.loc[df["Winner"] == "Davidovich Fokina A.", "Winner Last Name"] = "Davidovich Fokina"
        df.loc[df["Loser"] == "Davidovich Fokina A.", "Loser Last Name"] = "Davidovich Fokina"
        df.loc[df["Winner"] == "Carreno Busta P.", "Winner Last Name"] = "Carreno Busta"
        df.loc[df["Loser"] == "Carreno Busta P.", "Loser Last Name"] = "Carreno Busta"
        df.loc[df["Winner"] == "Bautista Agut R.", "Winner Last Name"] = "Bautista"
        df.loc[df["Loser"] == "Bautista Agut R.", "Loser Last Name"] = "Bautista"
        df.loc[df["Winner"] == "Granollers-Pujol G.", "Winner Last Name"] = "Granollers"
        df.loc[df["Loser"] == "Granollers-Pujol G.", "Loser Last Name"] = "Granollers"
        df.loc[df["Winner"] == "Van D. Merwe I.", "Winner Last Name"] = "Van Der Merwe"
        df.loc[df["Loser"] == "Van D. Merwe I.", "Loser Last Name"] = "Van Der Merwe"
        df.loc[df["Winner"] == "Ali Mutawa J.M.", "Winner Last Name"] = "Al Mutawa"
        df.loc[df["Loser"] == "Ali Mutawa J.M.", "Loser Last Name"] = "Al Mutawa"
        df.loc[df["Winner"] == "Smith J.P.", "Winner Last Name"] = "Patrick Smith"
        df.loc[df["Loser"] == "Smith J.P.", "Loser Last Name"] = "Patrick Smith"
        df.loc[df["Winner"] == "De Greef A.", "Winner Last Name"] = "De Greef"
        df.loc[df["Loser"] == "De Greef A.", "Loser Last Name"] = "De Greef"
        df.loc[df["Winner"] == "Silva F.F.", "Winner Last Name"] = "Ferreira Silva"
        df.loc[df["Loser"] == "Silva F.F.", "Loser Last Name"] = "Ferreira Silva"
        df.loc[df["Winner"] == "Munoz De La Nava D.", "Winner Last Name"] = "Munoz de la Nava"
        df.loc[df["Loser"] == "Munoz De La Nava D.", "Loser Last Name"] = "Munoz de la Nava"
        df.loc[df["Winner"] == "De Loore J.", "Winner Last Name"] = "De Loore"
        df.loc[df["Loser"] == "De Loore J.", "Loser Last Name"] = "De Loore"
        df.loc[df["Winner"] == "Gimeno-Traver D.", "Winner Last Name"] = "Gimeno Traver"
        df.loc[df["Loser"] == "Gimeno-Traver D.", "Loser Last Name"] = "Gimeno Traver"
        df.loc[df["Winner"] == "Silva F.", "Winner Last Name"] = "Ferreira Silva"
        df.loc[df["Loser"] == "Silva F.", "Loser Last Name"] = "Ferreira Silva"
        df.loc[df["Winner"] == "O'Connell C.", "Winner Last Name"] = "Oconnell"
        df.loc[df["Loser"] == "O'Connell C.", "Loser Last Name"] = "Oconnell"
        df.loc[df["Winner"] == "Alawadhi O.", "Winner Last Name"] = "Awadhy"
        df.loc[df["Loser"] == "Alawadhi O.", "Loser Last Name"] = "Awadhy"
        df.loc[df["Winner"] == "Hernandez-Fernandez J.", "Winner Last Name"] = "Hernandez"
        df.loc[df["Loser"] == "Hernandez-Fernandez J.", "Loser Last Name"] = "Hernandez"
        df.loc[df["Winner"] == "De Paula F.", "Winner Last Name"] = "De Paula"
        df.loc[df["Loser"] == "De Paula F.", "Loser Last Name"] = "De Paula"
        df.loc[df["Winner"] == "Tyurnev E.", "Winner Last Name"] = "Tiurnev"
        df.loc[df["Loser"] == "Tyurnev E.", "Loser Last Name"] = "Tiurnev"
        df.loc[df["Winner"] == "Tyurnev E.", "Winner Last Name"] = "Tiurnev"
        df.loc[df["Loser"] == "Tyurnev E.", "Loser Last Name"] = "Tiurnev"
        df.loc[df["Winner"] == "Hernandez-Fernandez J", "Winner Last Name"] = "Hernandez"
        df.loc[df["Loser"] == "Hernandez-Fernandez J", "Loser Last Name"] = "Hernandez"
        df.loc[df["Winner"] == "Tseng C.H.", "Winner Last Name"] = "Hsin Tseng"
        df.loc[df["Loser"] == "Tseng C.H.", "Loser Last Name"] = "Hsin Tseng"
        df.loc[df["Winner"] == "Lee D.H.", "Winner Last Name"] = "Hee Lee"
        df.loc[df["Loser"] == "Lee D.H.", "Loser Last Name"] = "Hee Lee"
        df.loc[df["Winner"] == "Meligeni Rodrigues F", "Winner Last Name"] = "Meligeni Alves"
        df.loc[df["Loser"] == "Meligeni Rodrigues F", "Loser Last Name"] = "Meligeni Alves"
        df.loc[df["Winner"] == "O Connell C.", "Winner Last Name"] = "Oconnell"
        df.loc[df["Loser"] == "O Connell C.", "Loser Last Name"] = "Oconnell"
        df.loc[df["Winner"] == "Ferreira Silva F.", "Winner Last Name"] = "Ferreira Silva"
        df.loc[df["Loser"] == "Ferreira Silva F.", "Loser Last Name"] = "Ferreira Silva"
        df.loc[df["Winner"] == "Barrios M.", "Winner Last Name"] = "Barrios Vera"
        df.loc[df["Loser"] == "Barrios M.", "Loser Last Name"] = "Barrios Vera"

    return df


# 1.2 Data Merging ( ATP & Bets )
def transform_feature_tourney_id(df):
    df[['y', 'tourney_id_']] = df['tourney_id'].str.split("-", 1, expand=True)
    df.drop(columns='y', inplace=True)
    df['tourney_id_'] = df['tourney_id_'].replace(
        ['M007', 'M006', '0410', '0421', '0352', '0425', 'M024', 'M009', '0495', 'M021', '0407', '0414', '0499', '0451',
         '0403', '0404', '0496', '0506', '0375', '0319', 'M035', '0337', '0500', '0311', '0568', '0439', '0322', '0308',
         '0321', '0314', '0315', '0316', '0891', 'M004', '0360', '0717', '0429', '0301', '0341', '0328', 'M015', '0329',
         '0422', '0416', 'M020', 'M010', '0533', '0424', 'M014', 'M001', '0741', '0418', '0605', 'M016', '0096', 'O16',
         '0807', '0402', '0438', '0773', 'M056', '0440', '8996', 'M052'],
        ['403', '404', '410', '421', '352', '425', '422', '416', '495', '1536', '407', '414', '499', '451', '403',
         '404', '496', '506', '375', '319', '418', '337', '500', '311', '568', '439', '322', '308', '321', '314', '315',
         '316', '891', '807', '360', '717', '429', '301', '341', '328', '747', '329', '422', '416', '339', '440', '533',
         '424', '438', '338', '741', '418', '605', '741', '96', '96', '807', '402', '438', '773', '8998', '440', '505',
         '6932'])
    return df

def add_features(df, tourney_id, money_prize, tourney_lvl, court, location, tourney_name):
    df['Label'] = 1
    df.loc[df['tourney_id'] == tourney_id, 'money_prize'] = money_prize
    df.loc[df['tourney_id'] == tourney_id, 'location'] = location
    df.loc[df['tourney_id'] == tourney_id, 'long_tourney_name'] = tourney_name
    df.loc[df['tourney_id'] == tourney_id, 'court'] = court
    df.loc[df['tourney_id'] == tourney_id, 'tourney_lvl'] = tourney_lvl

def get_data_with_new_features(df):
    df['money_prize'] = ""
    df['location'] = ""
    df['long_tourney_name'] = ""
    df['court'] = ""
    df['tourney_lvl'] = ""
    # 2010
    add_features(df, '2010-339', 372500, 'A250', 'Hard', 'AUS', 'Brisbane International')
    add_features(df, '2010-891', 398250, 'A250', 'Hard', 'IND', 'Chennai Open')
    add_features(df, '2010-451', 1024000, 'A250', 'Hard', 'QAT', 'Qatar ExxonMobil Open')
    add_features(df, '2010-301', 355500, 'A250', 'Hard', 'NZL', 'Auckland Open')
    add_features(df, '2010-338', 372500, 'A250', 'Hard', 'AUS', 'Sydney International')
    add_features(df, '2010-580', 11048640, 'G', 'Hard', 'AUS', 'Australia Open')
    add_features(df, '2010-5012', 442500, 'A250', 'Hard', 'RSA', 'SA Tennis Open')
    add_features(df, '2010-505', 398250, 'A250', 'Clay', 'CHI', 'Chile Open')
    add_features(df, '2010-2276', 398250, 'A250', 'Hard Indoors', 'CRO', 'PBZ Zagreb Indoors')
    add_features(df, '2010-533', 442500, 'A250', 'Clay', 'BRA', 'Brasil Open')
    add_features(df, '2010-407', 1150000, 'A500', 'Hard Indoors', 'NED', 'ABN AMRO World Tennis Tournament')
    add_features(df, '2010-424', 531000, 'A250', 'Hard Indoors', 'USA', 'SAP Open')
    add_features(df, '2010-506', 475300, 'A250', 'Clay', 'ARG', 'Argentina Open')
    add_features(df, '2010-496', 512750, 'A250', 'Hard Indoors', 'FRA', 'Open 13')
    add_features(df, '2010-402', 1100000, 'A500', 'Hard', 'USA', 'Regions Morgan Keegan Championships')
    add_features(df, '2010-807', 955000, 'A500', 'Clay', 'MEX', 'Abierto Mexicano Telcel')
    add_features(df, '2010-499', 442500, 'A250', 'Hard', 'USA', 'Delray Beach Open')
    add_features(df, '2010-495', 1619500, 'A500', 'Hard', 'UAE', 'Dubai Duty Free Tennis Championship')
    add_features(df, '2010-404', 3645000, 'A1000', 'Hard', 'USA', 'BNP Paribas Open')
    add_features(df, '2010-403', 3645000, 'A1000', 'Hard', 'USA', 'Miami Open')
    add_features(df, '2010-360', 398250, 'A250', 'Clay', 'MAR', 'Grand Prix Hassan II')
    add_features(df, '2010-717', 442500, 'A250', 'Clay', 'USA', 'U.S. Mens Clay Court Championship')
    add_features(df, '2010-410', 2227500, 'A1000', 'Clay', 'MON', 'Monte-Carlo Rolex Masters')
    add_features(df, '2010-425', 1550000, 'A500', 'Clay', 'ESP', 'Barcelona Open')
    add_features(df, '2010-416', 2227500, 'A1000', 'Clay', 'ITA', "Internazionali BNL d'Italia")
    add_features(df, '2010-308', 398250, 'A250', 'Clay', 'GER', 'BMW Open')
    add_features(df, '2010-5053', 373200, 'A250', 'Clay', 'SER', 'Serbia Open')
    add_features(df, '2010-468', 398250, 'A250', 'Clay', 'POR', 'Estoril Open')
    add_features(df, '2010-1536', 2835000, 'A1000', 'Clay', 'ESP', 'Mutua Madrid Open')
    add_features(df, '2010-615', 1764700, 'A250', 'Clay', 'GER', "ARAG World Team Cup")
    add_features(df, '2010-6120', 398250, 'A250', 'Clay', 'FRA', "Open De Nice Cote d'Azur")
    add_features(df, '2010-520', 7580800, 'G', 'Clay', 'FRA', 'Roland Garros')
    add_features(df, '2010-500', 475300, 'A250', 'Grass', 'GER', 'Gerry Weber Open')
    add_features(df, '2010-311', 627700, 'A250', 'Grass', 'UK', 'Aegon Championships')
    add_features(df, '2010-741', 405000, 'A250', 'Grass', 'UK', 'Aegon Open')
    add_features(df, '2010-440', 398250, 'A250', 'Grass', 'NED', 'UNICEF Open')
    add_features(df, '2010-540', 6196000, 'G', 'Grass', 'UK', 'Wimbledon')
    add_features(df, '2010-315', 442500, 'A250', 'Grass', 'UK', "Hall of Fame Tennis Championship")
    add_features(df, '2010-316', 398250, 'A250', 'Clay', 'SWE', 'SkiStar Swedish Open')
    add_features(df, '2010-321', 398250, 'A250', 'Clay', 'GER', 'Mercedes Cup')
    add_features(df, '2010-6116', 531000, 'A250', 'Hard', 'USA', 'Atlanta Tennis Championship')
    add_features(df, '2010-414', 1000000, 'A500', 'Clay', 'GER', 'International German Open')
    add_features(df, '2010-314', 398250, 'A250', 'Clay', 'SWI', 'Swiss Open Gstaad')
    add_features(df, '2010-423', 619500, 'A250', 'Hard', 'USA', 'Farmers Classic')
    add_features(df, '2010-439', 398250, 'A250', 'Clay', 'CRO', 'Croatia Open')
    add_features(df, '2010-418', 1165500, 'A500', 'Hard', 'USA', 'Citi Open')
    add_features(df, '2010-421', 2430000, 'A1000', 'Hard', 'CAN', 'Rogers Cup')
    add_features(df, '2010-422', 2430000, 'A1000', 'Hard', 'USA', 'Western & Southern Financial Group Masters')
    add_features(df, '2010-3348', 663750, 'A250', 'Hard', 'USA', 'Pilot Pen Tennis')
    add_features(df, '2010-560', 10508000, 'G', 'Hard', 'USA', 'US Open')
    add_features(df, '2010-773', 368450, 'A250', 'Clay', 'ROM', 'BRD Nastase Tiriac Trophy')
    add_features(df, '2010-341', 398250, 'A250', 'Hard', 'FRA', 'Moselle Open')
    add_features(df, '2010-1720', 551000, 'A250', 'Hard', 'THA', 'Thailand Open')
    add_features(df, '2010-6003', 850000, 'A250', 'Hard', 'MAS', 'Malaysian Open')
    add_features(df, '2010-747', 2100000, 'A500', 'Hard', 'CHN', 'China Open')
    add_features(df, '2010-329', 1100000, 'A500', 'Hard', 'JAP', 'Rakuten Japan Open Tennis Championship')
    add_features(df, '2010-5014', 3240000, 'A1000', 'Hard', 'CHN', 'Shanghai Rolex Masters')
    add_features(df, '2010-438', 1000000, 'A250', 'Hard', 'RUS', 'Kremlin Cup')
    add_features(df, '2010-429', 531000, 'A250', 'Hard', 'SWE', 'Stockholm Open')
    add_features(df, '2010-375', 575250, 'A250', 'Hard', 'FRA', 'Open Sud de France')
    add_features(df, '2010-568', 663750, 'A250', 'Hard Indoor', 'RUS', 'St. Petersburg Open')
    add_features(df, '2010-337', 575250, 'A250', 'Hard', 'AUT', 'Erste Bank Open')
    add_features(df, '2010-573', 1357000, 'A500', 'Hard', 'ESP', 'Valencia Open 500')
    add_features(df, '2010-328', 1225000, 'A500', 'Hard Indoors', 'SWI', 'Swiss Indoors Basel')
    add_features(df, '2010-352', 2227500, 'A1000', 'Hard', 'FRA', 'BNP Paribas Masters')
    add_features(df, '2010-605', 5070000, 'AF', 'Hard', 'UK', 'ATP World Tour Finals')

    # 2011
    add_features(df, '2011-339', 422300, 'A250', 'Hard', 'AUS', 'Brisbane International')
    add_features(df, '2011-891', 398250, 'A250', 'Hard', 'IND', 'Chennai Open')
    add_features(df, '2011-451', 1024000, 'A250', 'Hard', 'QAT', 'Qatar ExxonMobil Open')
    add_features(df, '2011-301', 398250, 'A250', 'Hard', 'NZL', 'Auckland Open')
    add_features(df, '2011-338', 422300, 'A250', 'Hard', 'AUS', 'Sydney International')
    add_features(df, '2011-580', 11414950, 'G', 'Hard', 'AUS', 'Australia Open')
    add_features(df, '2011-5012', 442500, 'A250', 'Hard', 'RSA', 'SA Tennis Open')
    add_features(df, '2011-505', 398250, 'A250', 'Clay', 'CHI', 'Chile Open')
    add_features(df, '2011-2276', 398250, 'A250', 'Hard Indoors', 'CRO', 'PBZ Zagreb Indoors')
    add_features(df, '2011-533', 470200, 'A250', 'Clay', 'BRA', 'Brasil Open')
    add_features(df, '2011-407', 1150000, 'A500', 'Hard Indoors', 'NED', 'ABN AMRO World Tennis Tournament')
    add_features(df, '2011-424', 531000, 'A250', 'Hard Indoors', 'USA', 'SAP Open')
    add_features(df, '2011-506', 478900, 'A250', 'Clay', 'ARG', 'Argentina Open')
    add_features(df, '2011-496', 512750, 'A250', 'Hard Indoors', 'FRA', 'Open 13')
    add_features(df, '2011-402', 1100000, 'A500', 'Hard', 'USA', 'Regions Morgan Keegan Championships')
    add_features(df, '2011-807', 1100000, 'A500', 'Clay', 'MEX', 'Abierto Mexicano Telcel')
    add_features(df, '2011-499', 442500, 'A250', 'Hard', 'USA', 'Delray Beach Open')
    add_features(df, '2011-495', 1619500, 'A500', 'Hard', 'UAE', 'Dubai Duty Free Tennis Championship')
    add_features(df, '2011-404', 3645000, 'A1000', 'Hard', 'USA', 'BNP Paribas Open')
    add_features(df, '2011-403', 3645000, 'A1000', 'Hard', 'USA', 'Miami Open')
    add_features(df, '2011-360', 398250, 'A250', 'Clay', 'MAR', 'Grand Prix Hassan II')
    add_features(df, '2011-717', 442500, 'A250', 'Clay', 'USA', 'U.S. Mens Clay Court Championship')
    add_features(df, '2011-410', 2227500, 'A1000', 'Clay', 'MON', 'Monte-Carlo Rolex Masters')
    add_features(df, '2011-425', 1550000, 'A500', 'Clay', 'ESP', 'Barcelona Open')
    add_features(df, '2011-308', 398250, 'A250', 'Clay', 'GER', 'BMW Open')
    add_features(df, '2011-5053', 364900, 'A250', 'Clay', 'SER', 'Serbia Open')
    add_features(df, '2011-468', 398250, 'A250', 'Clay', 'POR', 'Estoril Open')
    add_features(df, '2011-1536', 2835000, 'A1000', 'Clay', 'ESP', 'Mutua Madrid Open')
    add_features(df, '2011-416', 2227500, 'A1000', 'Clay', 'ITA', "Internazionali BNL d'Italia")
    add_features(df, '2011-6120', 398250, 'A250', 'Clay', 'FRA', "Open De Nice Cote d'Azur")
    add_features(df, '2011-520', 7884000, 'G', 'Clay', 'FRA', 'Roland Garros')
    add_features(df, '2011-500', 663750, 'A250', 'Grass', 'GER', 'Gerry Weber Open')
    add_features(df, '2011-311', 608000, 'A250', 'Grass', 'UK', 'Aegon Championships')
    add_features(df, '2011-741', 410925, 'A250', 'Grass', 'UK', 'Aegon Open')
    add_features(df, '2011-440', 398250, 'A250', 'Grass', 'NED', 'UNICEF Open')
    add_features(df, '2011-540', 6631000, 'G', 'Grass', 'UK', 'Wimbledon')
    add_features(df, '2011-315', 442500, 'A250', 'Grass', 'UK', "Hall of Fame Tennis Championship")
    add_features(df, '2011-316', 398250, 'A250', 'Clay', 'SWE', 'SkiStar Swedish Open')
    add_features(df, '2011-321', 398250, 'A250', 'Clay', 'GER', 'Mercedes Cup')
    add_features(df, '2011-6116', 531000, 'A250', 'Hard', 'USA', 'Atlanta Tennis Championship')
    add_features(df, '2011-414', 1000000, 'A500', 'Clay', 'GER', 'International German Open')
    add_features(df, '2011-314', 398250, 'A250', 'Clay', 'SWI', 'Swiss Open Gstaad')
    add_features(df, '2011-423', 619500, 'A250', 'Hard', 'USA', 'Farmers Classic')
    add_features(df, '2011-439', 398250, 'A250', 'Clay', 'CRO', 'Croatia Open')
    add_features(df, '2011-319', 398250, 'A250', 'Clay', 'AUS', 'Bet-At-Home Cup Kitzbuhel')
    add_features(df, '2011-418', 1166400, 'A500', 'Hard', 'USA', 'Citi Open')
    add_features(df, '2011-421', 2430000, 'A1000', 'Hard', 'CAN', 'Rogers Cup')
    add_features(df, '2011-422', 2592000, 'A1000', 'Hard', 'USA', 'Western & Southern Financial Group Masters')
    add_features(df, '2011-6242', 553125, 'A250', 'Hard', 'USA', "Winston-Salem Open")
    add_features(df, '2011-560', 10768000, 'G', 'Hard', 'USA', 'US Open')
    add_features(df, '2011-773', 371200, 'A250', 'Clay', 'ROM', 'BRD Nastase Tiriac Trophy')
    add_features(df, '2011-341', 398250, 'A250', 'Hard', 'FRA', 'Moselle Open')
    add_features(df, '2011-1720', 587000, 'A250', 'Hard', 'THA', 'Thailand Open')
    add_features(df, '2011-6003', 850000, 'A250', 'Hard', 'MAS', 'Malaysian Open')
    add_features(df, '2011-747', 2100000, 'A500', 'Hard', 'CHN', 'China Open')
    add_features(df, '2011-329', 1214500, 'A500', 'Hard', 'JAP', 'Rakuten Japan Open Tennis Championship')
    add_features(df, '2011-5014', 3240000, 'A1000', 'Hard', 'CHN', 'Shanghai Rolex Masters')
    add_features(df, '2011-438', 725000, 'A250', 'Hard', 'RUS', 'Kremlin Cup')
    add_features(df, '2011-429', 531000, 'A250', 'Hard', 'SWE', 'Stockholm Open')
    add_features(df, '2011-568', 663750, 'A250', 'Hard Indoor', 'RUS', 'St. Petersburg Open')
    add_features(df, '2011-337', 575250, 'A250', 'Hard', 'AUT', 'Erste Bank Open')
    add_features(df, '2011-328', 1308100, 'A500', 'Hard Indoors', 'SWI', 'Swiss Indoors Basel')
    add_features(df, '2011-573', 1357000, 'A500', 'Hard', 'ESP', 'Valencia Open 500')
    add_features(df, '2011-352', 2227500, 'A1000', 'Hard', 'FRA', 'BNP Paribas Masters')
    add_features(df, '2011-605', 5070000, 'AF', 'Hard', 'UK', 'ATP World Tour Finals')

    # 2012
    add_features(df, '2012-339', 434250, 'A250', 'Hard', 'AUS', 'Brisbane International')
    add_features(df, '2012-891', 398250, 'A250', 'Hard', 'IND', 'Chennai Open')
    add_features(df, '2012-451', 1024000, 'A250', 'Hard', 'QAT', 'Qatar ExxonMobil Open')
    add_features(df, '2012-301', 398250, 'A250', 'Hard', 'NZL', 'Auckland Open')
    add_features(df, '2012-338', 434250, 'A250', 'Hard', 'AUS', 'Sydney International')
    add_features(df, '2012-580', 11806550, 'G', 'Hard', 'AUS', 'Australia Open')
    add_features(df, '2012-375', 398250, 'A250', 'Hard', 'FRA', 'Open Sud de France')
    add_features(df, '2012-2276', 398250, 'A250', 'Hard Indoors', 'CRO', 'PBZ Zagreb Indoors')
    add_features(df, '2012-505', 398250, 'A250', 'Clay', 'CHI', 'Chile Open')
    add_features(df, '2012-533', 475300, 'A250', 'Clay', 'BRA', 'Brasil Open')
    add_features(df, '2012-407', 1207500, 'A500', 'Hard Indoors', 'NED', 'ABN AMRO World Tennis Tournament')
    add_features(df, '2012-424', 531000, 'A250', 'Hard Indoors', 'USA', 'SAP Open')
    add_features(df, '2012-506', 484100, 'A250', 'Clay', 'ARG', 'Argentina Open')
    add_features(df, '2012-496', 512750, 'A250', 'Hard Indoors', 'FRA', 'Open 13')
    add_features(df, '2012-402', 1155000, 'A500', 'Hard', 'USA', 'Regions Morgan Keegan Championships')
    add_features(df, '2012-807', 1155000, 'A500', 'Clay', 'MEX', 'Abierto Mexicano Telcel')
    add_features(df, '2012-499', 442500, 'A250', 'Hard', 'USA', 'Delray Beach Open')
    add_features(df, '2012-495', 1700475, 'A500', 'Hard', 'UAE', 'Dubai Duty Free Tennis Championship')
    add_features(df, '2012-404', 4694969, 'A1000', 'Hard', 'USA', 'BNP Paribas Open')
    add_features(df, '2012-403', 3973050, 'A1000', 'Hard', 'USA', 'Miami Open')
    add_features(df, '2012-360', 398250, 'A250', 'Clay', 'MAR', 'Grand Prix Hassan II')
    add_features(df, '2012-717', 442500, 'A250', 'Clay', 'USA', 'U.S. Mens Clay Court Championship')
    add_features(df, '2012-410', 2427975, 'A1000', 'Clay', 'MON', 'Monte-Carlo Rolex Masters')
    add_features(df, '2012-773', 398250, 'A250', 'Clay', 'ROM', 'BRD Nastase Tiriac Trophy')
    add_features(df, '2012-425', 1627500, 'A500', 'Clay', 'ESP', 'Barcelona Open')
    add_features(df, '2012-308', 398250, 'A250', 'Clay', 'GER', 'BMW Open')
    add_features(df, '2012-5053', 366950, 'A250', 'Clay', 'SER', 'Serbia Open')
    add_features(df, '2012-468', 398250, 'A250', 'Clay', 'POR', 'Estoril Open')
    add_features(df, '2012-1536', 3090150, 'A1000', 'Clay', 'ESP', 'Mutua Madrid Open')
    add_features(df, '2012-416', 2427975, 'A1000', 'Clay', 'ITA', "Internazionali BNL d'Italia")
    add_features(df, '2012-6120', 398250, 'A250', 'Clay', 'FRA', "Open De Nice Cote d'Azur")
    add_features(df, '2012-520', 8487000, 'G', 'Clay', 'FRA', 'Roland Garros')
    add_features(df, '2012-500', 663750, 'A250', 'Grass', 'GER', 'Gerry Weber Open')
    add_features(df, '2012-311', 625300, 'A250', 'Grass', 'UK', 'Aegon Championships')
    add_features(df, '2012-741', 403950, 'A250', 'Grass', 'UK', 'Aegon Open')
    add_features(df, '2012-440', 398250, 'A250', 'Grass', 'NED', 'UNICEF Open')
    add_features(df, '2012-540', 7285200, 'G', 'Grass', 'UK', 'Wimbledon')
    add_features(df, '2012-315', 398250, 'A250', 'Grass', 'UK', "Hall of Fame Tennis Championship")
    add_features(df, '2012-316', 358425, 'A250', 'Clay', 'SWE', 'SkiStar Swedish Open')
    add_features(df, '2012-321', 358425, 'A250', 'Clay', 'GER', 'Mercedes Cup')
    add_features(df, '2012-6116', 477900, 'A250', 'Hard', 'USA', 'BB & T Atlanta Open')
    add_features(df, '2012-414', 900000, 'A500', 'Clay', 'GER', 'International German Open')
    add_features(df, '2012-314', 358425, 'A250', 'Clay', 'SWI', 'Swiss Open Gstaad')
    add_features(df, '2012-423', 557550, 'A250', 'Hard', 'USA', 'Farmers Classic')
    add_features(df, '2012-439', 358425, 'A250', 'Clay', 'CRO', 'Croatia Open')
    add_features(df, '2012-319', 358425, 'A250', 'Clay', 'AUS', 'Bet-At-Home Cup Kitzbuhel')
    add_features(df, '2012-418', 1049760, 'A500', 'Hard', 'USA', 'Citi Open')
    add_features(df, '2012-421', 2648700, 'A1000', 'Hard', 'CAN', 'Rogers Cup')
    add_features(df, '2012-422', 2825280, 'A1000', 'Hard', 'USA', 'Western & Southern Financial Group Masters')
    add_features(df, '2012-6242', 553125, 'A250', 'Hard', 'USA', "Winston-Salem Open")
    add_features(df, '2012-560', 11777000, 'G', 'Hard', 'USA', 'US Open')
    add_features(df, '2012-568', 410850, 'A250', 'Hard Indoor', 'RUS', 'St. Petersburg Open')
    add_features(df, '2012-341', 398250, 'A250', 'Hard', 'FRA', 'Moselle Open')
    add_features(df, '2012-1720', 551000, 'A250', 'Hard', 'THA', 'Thailand Open')
    add_features(df, '2012-6003', 850000, 'A250', 'Hard', 'MAS', 'Malaysian Open')
    add_features(df, '2012-747', 2205000, 'A500', 'Hard', 'CHN', 'China Open')
    add_features(df, '2012-329', 1280565, 'A500', 'Hard', 'JAP', 'Rakuten Japan Open Tennis Championship')
    add_features(df, '2012-5014', 3531600, 'A1000', 'Hard', 'CHN', 'Shanghai Rolex Masters')
    add_features(df, '2012-438', 673150, 'A250', 'Hard', 'RUS', 'Kremlin Cup')
    add_features(df, '2012-429', 486750, 'A250', 'Hard', 'SWE', 'Stockholm Open')
    add_features(df, '2012-337', 486750, 'A250', 'Hard', 'AUT', 'Erste Bank Open')
    add_features(df, '2012-328', 1404300, 'A500', 'Hard Indoors', 'SWI', 'Swiss Indoors Basel')
    add_features(df, '2012-573', 1424850, 'A500', 'Hard', 'ESP', 'Valencia Open 500')
    add_features(df, '2012-352', 2427975, 'A1000', 'Hard', 'FRA', 'BNP Paribas Masters')
    add_features(df, '2012-605', 5500000, 'AF', 'Hard', 'UK', 'ATP World Tour Finals')

    ## 2013
    add_features(df, '2013-339', 436630, 'A250', 'Hard', 'AUS', 'Brisbane International')
    add_features(df, '2013-891', 385150, 'A250', 'Hard', 'IND', 'Chennai Open')
    add_features(df, '2013-451', 1054720, 'A250', 'Hard', 'QAT', 'Qatar ExxonMobil Open')
    add_features(df, '2013-301', 433400, 'A250', 'Hard', 'NZL', 'Auckland Open')
    add_features(df, '2013-338', 436630, 'A250', 'Hard', 'AUS', 'Sydney International')
    add_features(df, '2013-580', 13803160, 'G', 'Hard', 'AUS', 'Australia Open')
    add_features(df, '2013-375', 410200, 'A250', 'Hard', 'FRA', 'Open Sud de France')
    add_features(df, '2013-2276', 410200, 'A250', 'Hard Indoors', 'CRO', 'PBZ Zagreb Indoors')
    add_features(df, '2013-505', 410200, 'A250', 'Clay', 'CHI', 'Chile Open')
    add_features(df, '2013-533', 455775, 'A250', 'Clay', 'BRA', 'Brasil Open')
    add_features(df, '2013-407', 1267875, 'A500', 'Hard Indoors', 'NED', 'ABN AMRO World Tennis Tournament')
    add_features(df, '2013-424', 546930, 'A250', 'Hard Indoors', 'USA', 'SAP Open')
    add_features(df, '2013-402', 1212750, 'A500', 'Hard Indoors', 'USA', 'U.S. National Indoor Tennis Championships')
    add_features(df, '2013-496', 528135, 'A250', 'Hard Indoors', 'FRA', 'Open 13')
    add_features(df, '2013-506', 493670, 'A250', 'Clay', 'ARG', 'Argentina Open')
    add_features(df, '2013-807', 1212750, 'A500', 'Clay', 'MEX', 'Abierto Mexicano Telcel')
    add_features(df, '2013-495', 1785500, 'A500', 'Hard', 'UAE', 'Dubai Duty Free Tennis Championship')
    add_features(df, '2013-499', 455775, 'A250', 'Hard', 'USA', 'Delray Beach Open')
    add_features(df, '2013-404', 5191943, 'A1000', 'Hard', 'USA', 'BNP Paribas Open')
    add_features(df, '2013-403', 4330625, 'A1000', 'Hard', 'USA', 'Miami Open')
    add_features(df, '2013-360', 410200, 'A250', 'Clay', 'MAR', 'Grand Prix Hassan II')
    add_features(df, '2013-717', 455775, 'A250', 'Clay', 'USA', 'U.S. Mens Clay Court Championship')
    add_features(df, '2013-410', 2646495, 'A1000', 'Clay', 'MON', 'Monte-Carlo Rolex Masters')
    add_features(df, '2013-773', 410200, 'A250', 'Clay', 'ROM', 'BRD Nastase Tiriac Trophy')
    add_features(df, '2013-425', 1708875, 'A500', 'Clay', 'ESP', 'Barcelona Open')
    add_features(df, '2013-308', 410200, 'A250', 'Clay', 'GER', 'BMW Open')
    add_features(df, '2013-468', 410200, 'A250', 'Clay', 'POR', 'Estoril Open')
    add_features(df, '2013-1536', 3368265, 'A1000', 'Clay', 'ESP', 'Mutua Madrid Open')
    add_features(df, '2013-416', 2646495, 'A1000', 'Clay', 'ITA', "Internazionali BNL d'Italia")
    add_features(df, '2013-6710', 410200, 'A250', 'Clay', 'GER', "Power Horse Open")
    add_features(df, '2013-6120', 410200, 'A250', 'Clay', 'FRA', "Open De Nice Cote d'Azur")
    add_features(df, '2013-520', 10104000, 'G', 'Clay', 'FRA', 'Roland Garros')
    add_features(df, '2013-311', 683665, 'A250', 'Grass', 'UK', 'Aegon Championships')
    add_features(df, '2013-500', 683665, 'A250', 'Grass', 'GER', 'Gerry Weber Open')
    add_features(df, '2013-440', 410200, 'A250', 'Grass', 'NED', 'Topshelf Open')
    add_features(df, '2013-741', 468460, 'A250', 'Grass', 'UK', 'Aegon Open')
    add_features(df, '2013-540', 10514000, 'G', 'Grass', 'UK', 'Wimbledon')
    add_features(df, '2013-315', 455775, 'A250', 'Grass', 'UK', "Hall of Fame Tennis Championship")
    add_features(df, '2013-316', 433770, 'A250', 'Clay', 'SWE', 'SkiStar Swedish Open')
    add_features(df, '2013-321', 410200, 'A250', 'Clay', 'GER', 'Mercedes Cup')
    add_features(df, '2013-6718', 638085, 'A250', 'Hard', 'COL', 'Claro Open Colombia')
    add_features(df, '2013-414', 1102500, 'A500', 'Clay', 'GER', 'International German Open')
    add_features(df, '2013-314', 410200, 'A250', 'Clay', 'SWI', 'Swiss Open Gstaad')
    add_features(df, '2013-439', 410200, 'A250', 'Clay', 'CRO', 'Croatia Open')
    add_features(df, '2013-6116', 546930, 'A250', 'Hard', 'USA', 'BB & T Atlanta Open')
    add_features(df, '2013-319', 410200, 'A250', 'Clay', 'AUS', 'Bet-At-Home Cup Kitzbuhel')
    add_features(df, '2013-418', 1295790, 'A500', 'Hard', 'USA', 'Citi Open')
    add_features(df, '2013-421', 2887085, 'A1000', 'Hard', 'CAN', 'Rogers Cup')
    add_features(df, '2013-422', 3079555, 'A1000', 'Hard', 'USA', 'Western & Southern Financial Group Masters')
    add_features(df, '2013-6242', 575250, 'A250', 'Hard', 'USA', "Winston-Salem Open")
    add_features(df, '2013-560', 16102000, 'G', 'Hard', 'USA', 'US Open')
    add_features(df, '2013-568', 455775, 'A250', 'Hard Indoor', 'RUS', 'St. Petersburg Open')
    add_features(df, '2013-341', 410200, 'A250', 'Hard', 'FRA', 'Moselle Open')
    add_features(df, '2013-6003', 875500, 'A250', 'Hard', 'MAS', 'Malaysian Open')
    add_features(df, '2013-1720', 567530, 'A250', 'Hard', 'THA', 'Thailand Open')
    add_features(df, '2013-329', 1297000, 'A500', 'Hard', 'JAP', 'Rakuten Japan Open Tennis Championship')
    add_features(df, '2013-747', 2315250, 'A500', 'Hard', 'CHN', 'China Open')
    add_features(df, '2013-5014', 3849445, 'A1000', 'Hard', 'CHN', 'Shanghai Rolex Masters')
    add_features(df, '2013-337', 501355, 'A250', 'Hard', 'AUT', 'Erste Bank Open')
    add_features(df, '2013-429', 530165, 'A250', 'Hard', 'SWE', 'Stockholm Open')
    add_features(df, '2013-438', 746750, 'A250', 'Hard', 'RUS', 'Kremlin Cup')
    add_features(df, '2013-573', 1496095, 'A500', 'Hard', 'ESP', 'Valencia Open 500')
    add_features(df, '2013-328', 1445835, 'A500', 'Hard Indoors', 'SWI', 'Swiss Indoors Basel')
    add_features(df, '2013-352', 2646495, 'A1000', 'Hard', 'FRA', 'BNP Paribas Masters')
    add_features(df, '2013-605', 6000000, 'AF', 'Hard', 'UK', 'ATP World Tour Finals')

    ## 2014
    add_features(df, '2014-451', 1096910, 'A250', 'Hard', 'QAT', 'Qatar ExxonMobil Open')
    add_features(df, '2014-339', 452670, 'A250', 'Hard', 'AUS', 'Brisbane International')
    add_features(df, '2014-891', 399985, 'A250', 'Hard', 'IND', 'Chennai Open')
    add_features(df, '2014-301', 455190, 'A250', 'Hard', 'NZL', 'Auckland Open')
    add_features(df, '2014-338', 452670, 'A250', 'Hard', 'AUS', 'Sydney International')
    add_features(df, '2014-580', 14982200, 'G', 'Hard', 'AUS', 'Australia Open')
    add_features(df, '2014-375', 426605, 'A250', 'Hard', 'FRA', 'Open Sud de France')
    add_features(df, '2014-2276', 426605, 'A250', 'Hard Indoors', 'CRO', 'PBZ Zagreb Indoors')
    add_features(df, '2014-505', 426605, 'A250', 'Clay', 'CHI', 'Chile Open')
    add_features(df, '2014-407', 1396305, 'A500', 'Hard Indoors', 'NED', 'ABN AMRO World Tennis Tournament')
    add_features(df, '2014-402', 568805, 'A500', 'Hard Indoors', 'USA', 'U.S. National Indoor Tennis Championships')
    add_features(df, '2014-506', 488890, 'A250', 'Clay', 'ARG', 'Argentina Open')
    add_features(df, '2014-6932', 1309770, 'A500', 'Clay', 'BRA', 'Rio Open')
    add_features(df, '2014-496', 549260, 'A250', 'Hard Indoors', 'FRA', 'Open 13')
    add_features(df, '2014-499', 474005, 'A250', 'Hard', 'USA', 'Delray Beach Open')
    add_features(df, '2014-807', 1309770, 'A500', 'Clay', 'MEX', 'Abierto Mexicano Telcel')
    add_features(df, '2014-495', 1928340, 'A500', 'Hard', 'UAE', 'Dubai Duty Free Tennis Championship')
    add_features(df, '2014-533', 474005, 'A250', 'Clay', 'BRA', 'Brasil Open')
    add_features(df, '2014-404', 5240015, 'A1000', 'Hard', 'USA', 'BNP Paribas Open')
    add_features(df, '2014-403', 4720380, 'A1000', 'Hard', 'USA', 'Miami Open')
    add_features(df, '2014-360', 426605, 'A250', 'Clay', 'MAR', 'Grand Prix Hassan II')
    add_features(df, '2014-717', 474005, 'A250', 'Clay', 'USA', 'U.S. Mens Clay Court Championship')
    add_features(df, '2014-410', 2884675, 'A1000', 'Clay', 'MON', 'Monte-Carlo Rolex Masters')
    add_features(df, '2014-773', 426605, 'A250', 'Clay', 'ROM', 'BRD Nastase Tiriac Trophy')
    add_features(df, '2014-425', 1845585, 'A500', 'Clay', 'ESP', 'Barcelona Open')
    add_features(df, '2014-308', 426605, 'A250', 'Clay', 'GER', 'BMW Open')
    add_features(df, '2014-468', 426605, 'A250', 'Clay', 'POR', 'Estoril Open')
    add_features(df, '2014-1536', 3671405, 'A1000', 'Clay', 'ESP', 'Mutua Madrid Open')
    add_features(df, '2014-416', 2884675, 'A1000', 'Clay', 'ITA', "Internazionali BNL d'Italia")
    add_features(df, '2014-6710', 426605, 'A250', 'Clay', 'GER', "Power Horse Open")
    add_features(df, '2014-6120', 426605, 'A250', 'Clay', 'FRA', "Open De Nice Cote d'Azur")
    add_features(df, '2014-520', 11552000, 'G', 'Clay', 'FRA', 'Roland Garros')
    add_features(df, '2014-311', 711010, 'A250', 'Grass', 'UK', 'Aegon Championships')
    add_features(df, '2014-500', 711010, 'A250', 'Grass', 'GER', 'Gerry Weber Open')
    add_features(df, '2014-440', 426605, 'A250', 'Grass', 'NED', 'Topshelf Open')
    add_features(df, '2014-741', 503185, 'A250', 'Grass', 'UK', 'Aegon Open')
    add_features(df, '2014-540', 11715000, 'G', 'Grass', 'UK', 'Wimbledon')
    add_features(df, '2014-315', 474005, 'A250', 'Grass', 'UK', "Hall of Fame Tennis Championship")
    add_features(df, '2014-316', 426605, 'A250', 'Clay', 'SWE', 'SkiStar Swedish Open')
    add_features(df, '2014-321', 426605, 'A250', 'Clay', 'GER', 'Mercedes Cup')
    add_features(df, '2014-6718', 663610, 'A250', 'Hard', 'COL', 'Claro Open Colombia')
    add_features(df, '2014-414', 1190700, 'A500', 'Clay', 'GER', 'International German Open')
    add_features(df, '2014-314', 426605, 'A250', 'Clay', 'SWI', 'Swiss Open Gstaad')
    add_features(df, '2014-439', 426605, 'A250', 'Clay', 'CRO', 'Croatia Open')
    add_features(df, '2014-6116', 568805, 'A250', 'Hard', 'USA', 'BB & T Atlanta Open')
    add_features(df, '2014-319', 426605, 'A250', 'Clay', 'AUS', 'Bet-At-Home Cup Kitzbuhel')
    add_features(df, '2014-418', 1399700, 'A500', 'Hard', 'USA', 'Citi Open')
    add_features(df, '2014-421', 3146920, 'A1000', 'Hard', 'CAN', 'Rogers Cup')
    add_features(df, '2014-422', 3356715, 'A1000', 'Hard', 'USA', 'Western & Southern Financial Group Masters')
    add_features(df, '2014-6242', 598260, 'A250', 'Hard', 'USA', "Winston-Salem Open")
    add_features(df, '2014-560', 17852868, 'G', 'Hard', 'USA', 'US Open')
    add_features(df, '2014-568', 455775, 'A250', 'Hard Indoor', 'RUS', 'St. Petersburg Open')
    add_features(df, '2014-341', 426605, 'A250', 'Hard', 'FRA', 'Moselle Open')
    add_features(df, '2014-6967', 590230, 'A250', 'Hard', 'FRA', 'Shenzhen Open')
    add_features(df, '2014-6003', 910520, 'A250', 'Hard', 'MAS', 'Malaysian Open')
    add_features(df, '2014-329', 1228825, 'A500', 'Hard', 'JAP', 'Rakuten Japan Open Tennis Championship')
    add_features(df, '2014-747', 2500470, 'A500', 'Hard', 'CHN', 'China Open')
    add_features(df, '2014-5014', 4195895, 'A1000', 'Hard', 'CHN', 'Shanghai Rolex Masters')
    add_features(df, '2014-337', 521405, 'A250', 'Hard', 'AUT', 'Erste Bank Open')
    add_features(df, '2014-429', 521405, 'A250', 'Hard', 'SWE', 'Stockholm Open')
    add_features(df, '2014-438', 776620, 'A250', 'Hard', 'RUS', 'Kremlin Cup')
    add_features(df, '2014-573', 1615780, 'A500', 'Hard', 'ESP', 'Valencia Open 500')
    add_features(df, '2014-328', 1458610, 'A500', 'Hard Indoors', 'SWI', 'Swiss Indoors Basel')
    add_features(df, '2014-352', 2884675, 'A1000', 'Hard', 'FRA', 'BNP Paribas Masters')
    add_features(df, '2014-605', 6500000, 'AF', 'Hard', 'UK', 'ATP World Tour Finals')

    ## 2015
    add_features(df, '2015-451', 1129815, 'A250', 'Hard', 'QAT', 'Qatar ExxonMobil Open')
    add_features(df, '2015-339', 439405, 'A250', 'Hard', 'AUS', 'Brisbane International')
    add_features(df, '2015-891', 403495, 'A250', 'Hard', 'IND', 'Chennai Open')
    add_features(df, '2015-301', 464490, 'A250', 'Hard', 'NZL', 'Auckland Open')
    add_features(df, '2015-338', 439405, 'A250', 'Hard', 'AUS', 'Sydney International')
    add_features(df, '2015-580', 17748600, 'G', 'Hard', 'AUS', 'Australia Open')
    add_features(df, '2015-375', 439405, 'A250', 'Hard', 'FRA', 'Open Sud de France')
    add_features(df, '2015-2276', 439405, 'A250', 'Hard Indoors', 'CRO', 'PBZ Zagreb Indoors')
    add_features(df, '2015-7161', 439405, 'A250', 'Clay', 'ECU', 'Ecuador Open Quito')
    add_features(df, '2015-533', 444650, 'A250', 'Clay', 'BRA', 'Brasil Open')
    add_features(df, '2015-407', 1478850, 'A500', 'Hard Indoors', 'NED', 'ABN AMRO World Tennis Tournament')
    add_features(df, '2015-402', 585870, 'A500', 'Hard Indoors', 'USA', 'Memphis Open')
    add_features(df, '2015-6932', 1414550, 'A500', 'Clay', 'BRA', 'Rio Open')
    add_features(df, '2015-496', 565735, 'A250', 'Hard Indoors', 'FRA', 'Open 13')
    add_features(df, '2015-499', 488225, 'A250', 'Hard', 'USA', 'Delray Beach Open')
    add_features(df, '2015-807', 1414550, 'A500', 'Clay', 'MEX', 'Abierto Mexicano Telcel')
    add_features(df, '2015-495', 2082605, 'A500', 'Hard', 'UAE', 'Dubai Duty Free Tennis Championship')
    add_features(df, '2015-506', 500550, 'A250', 'Clay', 'ARG', 'Argentina Open')
    add_features(df, '2015-404', 5381235, 'A1000', 'Hard', 'USA', 'BNP Paribas Open')
    add_features(df, '2015-403', 5381235, 'A1000', 'Hard', 'USA', 'Miami Open')
    add_features(df, '2015-360', 439405, 'A250', 'Clay', 'MAR', 'Grand Prix Hassan II')
    add_features(df, '2015-717', 488225, 'A250', 'Clay', 'USA', 'U.S. Mens Clay Court Championship')
    add_features(df, '2015-410', 3288530, 'A1000', 'Clay', 'MON', 'Monte-Carlo Rolex Masters')
    add_features(df, '2015-773', 439405, 'A250', 'Clay', 'ROM', 'BRD Nastase Tiriac Trophy')
    add_features(df, '2015-425', 1993230, 'A500', 'Clay', 'ESP', 'Barcelona Open')
    add_features(df, '2015-308', 439405, 'A250', 'Clay', 'GER', 'BMW Open')
    add_features(df, '2015-7290', 439405, 'A250', 'Clay', 'POR', 'Estoril Open')
    add_features(df, '2015-7163', 439405, 'A250', 'Clay', 'TUR', 'Istanbul Open')
    add_features(df, '2015-1536', 4185405, 'A1000', 'Clay', 'ESP', 'Mutua Madrid Open')
    add_features(df, '2015-416', 3288530, 'A1000', 'Clay', 'ITA', "Internazionali BNL d'Italia")
    add_features(df, '2015-322', 439405, 'A250', 'Clay', 'SWI', 'Geneva Open')
    add_features(df, '2015-6120', 439405, 'A250', 'Clay', 'FRA', "Open De Nice Cote d'Azur")
    add_features(df, '2015-520', 13008000, 'G', 'Clay', 'FRA', 'Roland Garros')
    add_features(df, '2015-321', 574965, 'A250', 'Clay', 'GER', 'Mercedes Cup')
    add_features(df, '2015-440', 537050, 'A250', 'Grass', 'NED', 'Topshelf Open')
    add_features(df, '2015-311', 1574640, 'A500', 'Grass', 'UK', 'Aegon Championships')
    add_features(df, '2015-500', 1574640, 'A500', 'Grass', 'GER', 'Gerry Weber Open')
    add_features(df, '2015-741', 589160, 'A250', 'Grass', 'UK', 'Aegon Open')
    add_features(df, '2015-540', 12568000, 'G', 'Grass', 'UK', 'Wimbledon')
    add_features(df, '2015-315', 488225, 'A250', 'Grass', 'UK', "Hall of Fame Tennis Championship")
    add_features(df, '2015-316', 439405, 'A250', 'Clay', 'SWE', 'SkiStar Swedish Open')
    add_features(df, '2015-6718', 683515, 'A250', 'Hard', 'COL', 'Claro Open Colombia')
    add_features(df, '2015-439', 439405, 'A250', 'Clay', 'CRO', 'Croatia Open')
    add_features(df, '2015-314', 439405, 'A250', 'Clay', 'SWI', 'Swiss Open Gstaad')
    add_features(df, '2015-414', 1285955, 'A500', 'Clay', 'GER', 'International German Open')
    add_features(df, '2015-6116', 585870, 'A250', 'Hard', 'USA', 'BB & T Atlanta Open')
    add_features(df, '2015-319', 439405, 'A250', 'Clay', 'AUS', 'Generali Open')
    add_features(df, '2015-418', 1508815, 'A500', 'Hard', 'USA', 'Citi Open')
    add_features(df, '2015-421', 3587490, 'A1000', 'Hard', 'CAN', 'Rogers Cup')
    add_features(df, '2015-422', 3826655, 'A1000', 'Hard', 'USA', 'Western & Southern Financial Group Masters')
    add_features(df, '2015-6242', 616210, 'A250', 'Hard', 'USA', "Winston-Salem Open")
    add_features(df, '2015-560', 19852700, 'G', 'Hard', 'USA', 'US Open')
    add_features(df, '2015-568', 1030000, 'A250', 'Hard Indoor', 'RUS', 'St. Petersburg Open')
    add_features(df, '2015-341', 439405, 'A250', 'Hard', 'FRA', 'Moselle Open')
    add_features(df, '2015-6967', 607940, 'A250', 'Hard', 'FRA', 'Shenzhen Open')
    add_features(df, '2015-6003', 937835, 'A250', 'Hard', 'MAS', 'Malaysian Open')
    add_features(df, '2015-329', 1263045, 'A500', 'Hard', 'JAP', 'Rakuten Japan Open Tennis Championship')
    add_features(df, '2015-747', 2700510, 'A500', 'Hard', 'CHN', 'China Open')
    add_features(df, '2015-5014', 4783320, 'A1000', 'Hard', 'CHN', 'Shanghai Rolex Masters')
    add_features(df, '2015-337', 1745040, 'A500', 'Hard', 'AUT', 'Erste Bank Open')
    add_features(df, '2015-429', 537050, 'A250', 'Hard', 'SWE', 'Stockholm Open')
    add_features(df, '2015-438', 698325, 'A250', 'Hard', 'RUS', 'Kremlin Cup')
    add_features(df, '2015-573', 537050, 'A500', 'Hard', 'ESP', 'Valencia Open 500')
    add_features(df, '2015-328', 1575295, 'A500', 'Hard Indoors', 'SWI', 'Swiss Indoors Basel')
    add_features(df, '2015-352', 3288530, 'A1000', 'Hard', 'FRA', 'BNP Paribas Masters')
    add_features(df, '2015-605', 7000000, 'AF', 'Hard', 'UK', 'ATP World Tour Finals')

    ## 2016
    add_features(df, '2016-0451', 1189605, 'A250', 'Hard', 'QAT', 'Qatar ExxonMobil Open')
    add_features(df, '2016-M020', 404780, 'A250', 'Hard', 'AUS', 'Brisbane International')
    add_features(df, '2016-0891', 425535, 'A250', 'Hard', 'IND', 'Chennai Open')
    add_features(df, '2016-0301', 463520, 'A250', 'Hard', 'NZL', 'Auckland Open')
    add_features(df, '2016-M001', 404780, 'A250', 'Hard', 'AUS', 'Sydney International')
    add_features(df, '2016-580', 19703000, 'G', 'Hard', 'AUS', 'Australia Open')
    add_features(df, '2016-7434', 463520, 'A250', 'Hard', 'BUL', 'Sofia Open')
    add_features(df, '2016-7161', 463520, 'A250', 'Clay', 'ECU', 'Ecuador Open Quito')
    add_features(df, '2016-0375', 463520, 'A250', 'Hard', 'FRA', 'Open Sud de France')
    add_features(df, '2016-0407', 1597155, 'A500', 'Hard Indoors', 'NED', 'ABN AMRO World Tennis Tournament')
    add_features(df, '2016-0402', 618030, 'A250', 'Hard Indoors', 'USA', 'Memphis Open')
    add_features(df, '2016-0506', 523470, 'A250', 'Clay', 'ARG', 'Argentina Open')
    add_features(df, '2016-M052', 1333085, 'A500', 'Clay', 'BRA', 'Rio Open')
    add_features(df, '2016-0499', 514065, 'A250', 'Hard', 'USA', 'Delray Beach Open')
    add_features(df, '2016-0496', 596790, 'A250', 'Hard Indoors', 'FRA', 'Open 13')
    add_features(df, '2016-M004', 1413600, 'A500', 'Clay', 'MEX', 'Abierto Mexicano Telcel')
    add_features(df, '2016-0495', 2249215, 'A500', 'Hard', 'UAE', 'Dubai Duty Free Tennis Championship')
    add_features(df, '2016-0533', 436220, 'A250', 'Clay', 'BRA', 'Brasil Open')
    add_features(df, '2016-M006', 6134605, 'A1000', 'Hard', 'USA', 'BNP Paribas Open')
    add_features(df, '2016-M007', 6134605, 'A1000', 'Hard', 'USA', 'Miami Open')
    add_features(df, '2016-0360', 463520, 'A250', 'Clay', 'MAR', 'Grand Prix Hassan II')
    add_features(df, '2016-0717', 515025, 'A250', 'Clay', 'USA', 'U.S. Mens Clay Court Championship')
    add_features(df, '2016-0410', 3748925, 'A1000', 'Clay', 'MON', 'Monte-Carlo Rolex Masters')
    add_features(df, '2016-0773', 463520, 'A250', 'Clay', 'ROM', 'BRD Nastase Tiriac Trophy')
    add_features(df, '2016-0425', 2152690, 'A500', 'Clay', 'ESP', 'Barcelona Open')
    add_features(df, '2016-0308', 463520, 'A250', 'Clay', 'GER', 'BMW Open')
    add_features(df, '2016-7290', 463520, 'A250', 'Clay', 'POR', 'Estoril Open')
    add_features(df, '2016-7163', 426530, 'A250', 'Clay', 'TUR', 'Istanbul Open')
    add_features(df, '2016-M021', 4771360, 'A1000', 'Clay', 'ESP', 'Mutua Madrid Open')
    add_features(df, '2016-M009', 3748925, 'A1000', 'Clay', 'ITA', "Internazionali BNL d'Italia")
    add_features(df, '2016-0322', 499645, 'A250', 'Clay', 'SWI', 'Geneva Open')
    add_features(df, '2016-6120', 463520, 'A250', 'Clay', 'FRA', "Open De Nice Cote d'Azur")
    add_features(df, '2016-520', 16008750, 'G', 'Clay', 'FRA', 'Roland Garros')
    add_features(df, '2016-0321', 606525, 'A250', 'Grass', 'GER', 'Mercedes Cup')
    add_features(df, '2016-M010', 566525, 'A250', 'Grass', 'NED', 'Topshelf Open')
    add_features(df, '2016-0311', 1802945, 'A500', 'Grass', 'UK', 'Aegon Championships')
    add_features(df, '2016-0500', 1700610, 'A500', 'Grass', 'GER', 'Gerry Weber Open')
    add_features(df, '2016-0741', 648255, 'A250', 'Grass', 'UK', 'Aegon Open')
    add_features(df, '2016-540', 13163000, 'G', 'Grass', 'UK', 'Wimbledon')
    add_features(df, '2016-0316', 463520, 'A250', 'Clay', 'SWE', 'SkiStar Swedish Open')
    add_features(df, '2016-0414', 1388830, 'A500', 'Clay', 'GER', 'International German Open')
    add_features(df, '2016-0315', 515025, 'A250', 'Grass', 'UK', "Hall of Fame Tennis Championship")
    add_features(df, '2016-0319', 463520, 'A250', 'Clay', 'AUS', 'Generali Open')
    add_features(df, '2016-0314', 463520, 'A250', 'Clay', 'SWI', 'Swiss Open Gstaad')
    add_features(df, '2016-M035', 1629475, 'A500', 'Hard', 'USA', 'Citi Open')
    add_features(df, '2016-0439', 463520, 'A250', 'Clay', 'CRO', 'Croatia Open')
    add_features(df, '2016-0421', 4089740, 'A1000', 'Hard', 'CAN', 'Rogers Cup')
    add_features(df, '2016-6116', 618030, 'A250', 'Hard', 'USA', 'BB & T Atlanta Open')
    add_features(df, '2016-7480', 721030, 'A250', 'Hard', 'MEX', 'Mifel Open')
    add_features(df, '2016-M024', 4362385, 'A1000', 'Hard', 'USA', 'Western & Southern Financial Group Masters')
    add_features(df, '2016-6242', 639255, 'A250', 'Hard', 'USA', "Winston-Salem Open")
    add_features(df, '2016-560', 21862744, 'G', 'Hard', 'USA', 'US Open')
    add_features(df, '2016-0568', 923550, 'A250', 'Hard Indoor', 'RUS', 'St. Petersburg Open')
    add_features(df, '2016-0341', 463520, 'A250', 'Hard', 'FRA', 'Moselle Open')
    add_features(df, '2016-6967', 641305, 'A250', 'Hard', 'FRA', 'Shenzhen Open')
    add_features(df, '2016-7581', 840915, 'A250', 'Hard', 'CHN', 'Chengdu Open')
    add_features(df, '2016-0329', 1368605, 'A500', 'Hard', 'JAP', 'Rakuten Japan Open Tennis Championship')
    add_features(df, '2016-M015', 2916550, 'A500', 'Hard', 'CHN', 'China Open')
    add_features(df, '2016-5014', 5452985, 'A1000', 'Hard', 'CHN', 'Shanghai Rolex Masters')
    add_features(df, '2016-7485', 566525, 'A250', 'Hard', 'BEL', 'European Open')
    add_features(df, '2016-0429', 566525, 'A250', 'Hard', 'SWE', 'Stockholm Open')
    add_features(df, '2016-M014', 717250, 'A250', 'Hard', 'RUS', 'Kremlin Cup')
    add_features(df, '2016-0328', 1701320, 'A500', 'Hard Indoors', 'SWI', 'Swiss Indoors Basel')
    add_features(df, '2016-0337', 1884645, 'A500', 'Hard', 'AUT', 'Erste Bank Open')
    add_features(df, '2016-0352', 3748925, 'A1000', 'Hard', 'FRA', 'BNP Paribas Masters')
    add_features(df, '2016-0605', 7500000, 'AF', 'Hard', 'UK', 'ATP World Tour Finals')

    ## 2017
    add_features(df, '2017-0451', 1237190, 'A250', 'Hard', 'QAT', 'Qatar ExxonMobil Open')
    add_features(df, '2017-M020', 437380, 'A250', 'Hard', 'AUS', 'Brisbane International')
    add_features(df, '2017-0891', 447480, 'A250', 'Hard', 'IND', 'Chennai Open')
    add_features(df, '2017-0301', 450110, 'A250', 'Hard', 'NZL', 'Auckland Open')
    add_features(df, '2017-M001', 437380, 'A250', 'Hard', 'AUS', 'Sydney International')
    add_features(df, '2017-580', 22624000, 'G', 'Hard', 'AUS', 'Australia Open')
    add_features(df, '2017-7434', 482060, 'A250', 'Hard', 'BUL', 'Sofia Open')
    add_features(df, '2017-7161', 482060, 'A250', 'Clay', 'ECU', 'Ecuador Open Quito')
    add_features(df, '2017-0375', 482060, 'A250', 'Hard', 'FRA', 'Open Sud de France')
    add_features(df, '2017-0407', 1724930, 'A500', 'Hard Indoors', 'NED', 'ABN AMRO World Tennis Tournament')
    add_features(df, '2017-0402', 642750, 'A250', 'Hard Indoors', 'USA', 'Memphis Open')
    add_features(df, '2017-0506', 546680, 'A250', 'Clay', 'ARG', 'Argentina Open')
    add_features(df, '2017-6932', 1461560, 'A500', 'Clay', 'BRA', 'Rio Open')
    add_features(df, '2017-0499', 534625, 'A250', 'Hard', 'USA', 'Delray Beach Open')
    add_features(df, '2017-0496', 620660, 'A250', 'Hard Indoors', 'FRA', 'Open 13')
    add_features(df, '2017-M004', 1491310, 'A500', 'Clay', 'MEX', 'Abierto Mexicano Telcel')
    add_features(df, '2017-0495', 2429150, 'A500', 'Hard', 'UAE', 'Dubai Duty Free Tennis Championship')
    add_features(df, '2017-0533', 455565, 'A250', 'Clay', 'BRA', 'Brasil Open')
    add_features(df, '2017-M006', 6993450, 'A1000', 'Hard', 'USA', 'BNP Paribas Open')
    add_features(df, '2017-M007', 6993450, 'A1000', 'Hard', 'USA', 'Miami Open')
    add_features(df, '2017-0360', 482060, 'A250', 'Clay', 'MAR', 'Grand Prix Hassan II')
    add_features(df, '2017-0717', 535625, 'A250', 'Clay', 'USA', 'U.S. Mens Clay Court Championship')
    add_features(df, '2017-0410', 4273775, 'A1000', 'Clay', 'MON', 'Monte-Carlo Rolex Masters')
    add_features(df, '2017-0425', 2324905, 'A500', 'Clay', 'ESP', 'Barcelona Open')
    add_features(df, '2017-7648', 482060, 'A250', 'Clay', 'HUN', 'Gazprom Hungarian Open')
    add_features(df, '2017-0308', 482060, 'A250', 'Clay', 'GER', 'BMW Open')
    add_features(df, '2017-7290', 482060, 'A250', 'Clay', 'POR', 'Estoril Open')
    add_features(df, '2017-7163', 439005, 'A250', 'Clay', 'TUR', 'Istanbul Open')
    add_features(df, '2017-M021', 5439350, 'A1000', 'Clay', 'ESP', 'Mutua Madrid Open')
    add_features(df, '2017-M009', 4273775, 'A1000', 'Clay', 'ITA', "Internazionali BNL d'Italia")
    add_features(df, '2017-7694', 482060, 'A250', 'Clay', 'FRA', 'Lyon Open')
    add_features(df, '2017-0322', 482060, 'A250', 'Clay', 'SWI', 'Geneva Open')
    add_features(df, '2017-520', 16790000, 'G', 'Clay', 'FRA', 'Roland Garros')
    add_features(df, '2017-0321', 630785, 'A250', 'Grass', 'GER', 'Mercedes Cup')
    add_features(df, '2017-M010', 589185, 'A250', 'Grass', 'NED', 'Libema Open')
    add_features(df, '2017-0311', 1836660, 'A500', 'Grass', 'UK', 'Aegon Championships')
    add_features(df, '2017-0500', 1836660, 'A500', 'Grass', 'GER', 'Gerry Weber Open')
    add_features(df, '2017-7650', 439005, 'A250', 'Grass', 'TUR', 'Antalya Open')
    add_features(df, '2017-M016', 635660, 'A250', 'Grass', 'UK', 'Aegon Open')
    add_features(df, '2017-540', 14840000, 'G', 'Grass', 'UK', 'Wimbledon')
    add_features(df, '2017-0315', 535625, 'A250', 'Grass', 'UK', "Hall of Fame Tennis Championship")
    add_features(df, '2017-0316', 482060, 'A250', 'Clay', 'SWE', 'SkiStar Swedish Open')
    add_features(df, '2017-0439', 482060, 'A250', 'Clay', 'CRO', 'Croatia Open')
    add_features(df, '2017-0314', 482060, 'A250', 'Clay', 'SWI', 'Swiss Open Gstaad')
    add_features(df, '2017-0414', 1499940, 'A500', 'Clay', 'GER', 'International German Open')
    add_features(df, '2017-6116', 642750, 'A250', 'Hard', 'USA', 'BB & T Atlanta Open')
    add_features(df, '2017-7480', 637395, 'A250', 'Hard', 'MEX', 'Mifel Open')
    add_features(df, '2017-0319', 482060, 'A250', 'Clay', 'AUS', 'Generali Open')
    add_features(df, '2017-M035', 1750080, 'A500', 'Hard', 'USA', 'Citi Open')
    add_features(df, '2017-0421', 4662300, 'A1000', 'Hard', 'CAN', 'Rogers Cup')
    add_features(df, '2017-M024', 4973120, 'A1000', 'Hard', 'USA', 'Western & Southern Financial Group Masters')
    add_features(df, '2017-6242', 664825, 'A250', 'Hard', 'USA', "Winston-Salem Open")
    add_features(df, '2017-560', 24193400, 'G', 'Hard', 'USA', 'US Open')
    add_features(df, '2017-0568', 1000000, 'A250', 'Hard Indoor', 'RUS', 'St. Petersburg Open')
    add_features(df, '2017-0341', 482060, 'A250', 'Hard', 'FRA', 'Moselle Open')
    add_features(df, '2017-6967', 666960, 'A250', 'Hard', 'FRA', 'Shenzhen Open')
    add_features(df, '2017-7581', 1028885, 'A250', 'Hard', 'CHN', 'Chengdu Open')
    add_features(df, '2017-0329', 1563795, 'A500', 'Hard', 'JAP', 'Rakuten Japan Open Tennis Championship')
    add_features(df, '2017-M015', 3028080, 'A500', 'Hard', 'CHN', 'China Open')
    add_features(df, '2017-5014', 5924890, 'A1000', 'Hard', 'CHN', 'Shanghai Rolex Masters')
    add_features(df, '2017-M014', 745940, 'A250', 'Hard', 'RUS', 'Kremlin Cup')
    add_features(df, '2017-7485', 589185, 'A250', 'Hard', 'BEL', 'European Open')
    add_features(df, '2017-0429', 589185, 'A250', 'Hard', 'SWE', 'Stockholm Open')
    add_features(df, '2017-0328', 1837425, 'A500', 'Hard Indoors', 'SWI', 'Swiss Indoors Basel')
    add_features(df, '2017-0337', 2035415, 'A500', 'Hard', 'AUT', 'Erste Bank Open')
    add_features(df, '2017-0352', 4273775, 'A1000', 'Hard', 'FRA', 'BNP Paribas Masters')
    add_features(df, '2017-7696', 1275000, 'AF', 'Hard', 'ITA', 'Next Gen ATP Finals')
    add_features(df, '2017-0605', 8000000, 'AF', 'Hard', 'UK', 'ATP World Tour Finals')

    ## 2018
    add_features(df, '2018-0451', 1286675, 'A250', 'Hard', 'QAT', 'Qatar ExxonMobil Open')
    add_features(df, '2018-M020', 468910, 'A250', 'Hard', 'AUS', 'Brisbane International')
    add_features(df, '2018-0891', 501345, 'A250', 'Hard', 'IND', 'Chennai Open')
    add_features(df, '2018-0301', 501345, 'A250', 'Hard', 'NZL', 'Auckland Open')
    add_features(df, '2018-M001', 468910, 'A250', 'Hard', 'AUS', 'Sydney International')
    add_features(df, '2018-580', 25096000, 'G', 'Hard', 'AUS', 'Australia Open')
    add_features(df, '2018-7434', 501345, 'A250', 'Hard', 'BUL', 'Sofia Open')
    add_features(df, '2018-7161', 501345, 'A250', 'Clay', 'ECU', 'Ecuador Open Quito')
    add_features(df, '2018-0375', 501345, 'A250', 'Hard', 'FRA', 'Open Sud de France')
    add_features(df, '2018-0407', 1862925, 'A500', 'Hard Indoors', 'NED', 'ABN AMRO World Tennis Tournament')
    add_features(df, '2018-0506', 568190, 'A250', 'Clay', 'ARG', 'Argentina Open')
    add_features(df, '2018-0424', 668460, 'A250', 'Hard', 'USA', 'New York Open')
    add_features(df, '2018-6932', 1695825, 'A500', 'Clay', 'BRA', 'Rio Open')
    add_features(df, '2018-0499', 556010, 'A250', 'Hard', 'USA', 'Delray Beach Open')
    add_features(df, '2018-0496', 645485, 'A250', 'Hard Indoors', 'FRA', 'Open 13')
    add_features(df, '2018-M004', 1642795, 'A500', 'Clay', 'MEX', 'Abierto Mexicano Telcel')
    add_features(df, '2018-0495', 2623485, 'A500', 'Hard', 'UAE', 'Dubai Duty Free Tennis Championship')
    add_features(df, '2018-0533', 516205, 'A250', 'Clay', 'BRA', 'Brasil Open')
    add_features(df, '2018-M006', 7972535, 'A1000', 'Hard', 'USA', 'BNP Paribas Open')
    add_features(df, '2018-M007', 7972535, 'A1000', 'Hard', 'USA', 'Miami Open')
    add_features(df, '2018-0360', 501345, 'A250', 'Clay', 'MAR', 'Grand Prix Hassan II')
    add_features(df, '2018-0717', 557050, 'A250', 'Clay', 'USA', 'U.S. Mens Clay Court Championship')
    add_features(df, '2018-0410', 4872105, 'A1000', 'Clay', 'MON', 'Monte-Carlo Rolex Masters')
    add_features(df, '2018-0425', 2510900, 'A500', 'Clay', 'ESP', 'Barcelona Open')
    add_features(df, '2018-7648', 501345, 'A250', 'Clay', 'HUN', 'Gazprom Hungarian Open')
    add_features(df, '2018-0308', 501345, 'A250', 'Clay', 'GER', 'BMW Open')
    add_features(df, '2018-7290', 501345, 'A250', 'Clay', 'POR', 'Estoril Open')
    add_features(df, '2018-7163', 426145, 'A250', 'Clay', 'TUR', 'Istanbul Open')
    add_features(df, '2018-M021', 6200860, 'A1000', 'Clay', 'ESP', 'Mutua Madrid Open')
    add_features(df, '2018-M009', 4872105, 'A1000', 'Clay', 'ITA', "Internazionali BNL d'Italia")
    add_features(df, '2018-7694', 501345, 'A250', 'Clay', 'FRA', 'Lyon Open')
    add_features(df, '2018-0322', 501345, 'A250', 'Clay', 'SWI', 'Geneva Open')
    add_features(df, '2018-520', 18232000, 'G', 'Clay', 'FRA', 'Roland Garros')
    add_features(df, '2018-0321', 656015, 'A250', 'Grass', 'GER', 'Mercedes Cup')
    add_features(df, '2018-M010', 612755, 'A250', 'Grass', 'NED', 'Libema Open')
    add_features(df, '2018-0311', 1983595, 'A500', 'Grass', 'UK', 'Aegon Championships')
    add_features(df, '2018-0500', 1983595, 'A500', 'Grass', 'GER', 'Gerry Weber Open')
    add_features(df, '2018-7650', 426145, 'A250', 'Grass', 'TUR', 'Antalya Open')
    add_features(df, '2018-M016', 661085, 'A250', 'Grass', 'UK', 'Nature Valley International')
    add_features(df, '2018-540', 15982000, 'G', 'Grass', 'UK', 'Wimbledon')
    add_features(df, '2018-0315', 557050, 'A250', 'Grass', 'UK', "Hall of Fame Tennis Championship")
    add_features(df, '2018-0316', 501345, 'A250', 'Clay', 'SWE', 'SkiStar Swedish Open')
    add_features(df, '2018-0414', 1619935, 'A500', 'Clay', 'GER', 'International German Open')
    add_features(df, '2018-0439', 501345, 'A250', 'Clay', 'CRO', 'Croatia Open')
    add_features(df, '2018-0314', 501345, 'A250', 'Clay', 'SWI', 'Swiss Open Gstaad')
    add_features(df, '2018-6116', 668460, 'A250', 'Hard', 'USA', 'BB & T Atlanta Open')
    add_features(df, '2018-7480', 715455, 'A250', 'Hard', 'MEX', 'Mifel Open')
    add_features(df, '2018-0319', 501345, 'A250', 'Clay', 'AUS', 'Generali Open')
    add_features(df, '2018-M035', 1890165, 'A500', 'Hard', 'USA', 'Citi Open')
    add_features(df, '2018-0421', 5315025, 'A1000', 'Hard', 'CAN', 'Rogers Cup')
    add_features(df, '2018-M024', 5669360, 'A1000', 'Hard', 'USA', 'Western & Southern Financial Group Masters')
    add_features(df, '2018-6242', 691415, 'A250', 'Hard', 'USA', "Winston-Salem Open")
    add_features(df, '2018-560', 25282400, 'G', 'Hard', 'USA', 'US Open')
    add_features(df, '2018-0568', 1175900, 'A250', 'Hard Indoor', 'RUS', 'St. Petersburg Open')
    add_features(df, '2018-0341', 501345, 'A250', 'Hard', 'FRA', 'Moselle Open')
    add_features(df, '2018-6967', 733655, 'A250', 'Hard', 'FRA', 'Shenzhen Open')
    add_features(df, '2018-7581', 1070040, 'A250', 'Hard', 'CHN', 'Chengdu Open')
    add_features(df, '2018-0329', 1781930, 'A500', 'Hard', 'JAP', 'Rakuten Japan Open Tennis Championship')
    add_features(df, '2018-M015', 3401860, 'A500', 'Hard', 'CHN', 'China Open')
    add_features(df, '2018-5014', 7086700, 'A1000', 'Hard', 'CHN', 'Shanghai Rolex Masters')
    add_features(df, '2018-M014', 856445, 'A250', 'Hard', 'RUS', 'Kremlin Cup')
    add_features(df, '2018-7485', 612755, 'A250', 'Hard', 'BEL', 'European Open')
    add_features(df, '2018-0429', 612755, 'A250', 'Hard', 'SWE', 'Stockholm Open')
    add_features(df, '2018-0328', 1984420, 'A500', 'Hard Indoors', 'SWI', 'Swiss Indoors Basel')
    add_features(df, '2018-0337', 2198250, 'A500', 'Hard', 'AUT', 'Erste Bank Open')
    add_features(df, '2018-0352', 4872105, 'A1000', 'Hard', 'FRA', 'BNP Paribas Masters')
    add_features(df, '2018-7696', 1335000, 'AF', 'Hard', 'ITA', 'Next Gen ATP Finals')
    add_features(df, '2018-0605', 8500000, 'AF', 'Hard', 'UK', 'ATP World Tour Finals')

    ## 2019
    add_features(df, '2019-0451', 1313215, 'A250', 'Hard', 'QAT', 'Qatar ExxonMobil Open')
    add_features(df, '2019-M020', 527880, 'A250', 'Hard', 'AUS', 'Brisbane International')
    add_features(df, '2019-0891', 527880, 'A250', 'Hard', 'IND', 'Chennai Open')
    add_features(df, '2019-0301', 527880, 'A250', 'Hard', 'NZL', 'Auckland Open')
    add_features(df, '2019-M001', 527880, 'A250', 'Hard', 'AUS', 'Sydney International')
    add_features(df, '2019-580', 29687000, 'G', 'Hard', 'AUS', 'Australia Open')
    add_features(df, '2019-9158', 527880, 'A250', 'Clay', 'ESP', 'Cordoba Open')
    add_features(df, '2019-7434', 524340, 'A250', 'Hard', 'BUL', 'Sofia Open')
    add_features(df, '2019-0375', 524340, 'A250', 'Hard', 'FRA', 'Open Sud de France')
    add_features(df, '2019-0407', 1961160, 'A500', 'Hard Indoors', 'NED', 'ABN AMRO World Tennis Tournament')
    add_features(df, '2019-0506', 590745, 'A250', 'Clay', 'ARG', 'Argentina Open')
    add_features(df, '2019-0424', 694995, 'A250', 'Hard', 'USA', 'New York Open')
    add_features(df, '2019-6932', 1786690, 'A500', 'Clay', 'BRA', 'Rio Open')
    add_features(df, '2019-0499', 582550, 'A250', 'Hard', 'USA', 'Delray Beach Open')
    add_features(df, '2019-0496', 668485, 'A250', 'Hard Indoors', 'FRA', 'Open 13')
    add_features(df, '2019-M004', 1780060, 'A500', 'Clay', 'MEX', 'Abierto Mexicano Telcel')
    add_features(df, '2019-0495', 2736845, 'A500', 'Hard', 'UAE', 'Dubai Duty Free Tennis Championship')
    add_features(df, '2019-0533', 550145, 'A250', 'Clay', 'BRA', 'Brasil Open')
    add_features(df, '2019-M006', 8359455, 'A1000', 'Hard', 'USA', 'BNP Paribas Open')
    add_features(df, '2019-M007', 8359455, 'A1000', 'Hard', 'USA', 'Miami Open')
    add_features(df, '2019-0360', 501345, 'A250', 'Clay', 'MAR', 'Grand Prix Hassan II')
    add_features(df, '2019-0717', 583585, 'A250', 'Clay', 'USA', 'U.S. Mens Clay Court Championship')
    add_features(df, '2019-0410', 5207405, 'A1000', 'Clay', 'MON', 'Monte-Carlo Rolex Masters')
    add_features(df, '2019-0425', 2609135, 'A500', 'Clay', 'ESP', 'Barcelona Open')
    add_features(df, '2019-7648', 524340, 'A250', 'Clay', 'HUN', 'Gazprom Hungarian Open')
    add_features(df, '2019-0308', 524340, 'A250', 'Clay', 'GER', 'BMW Open')
    add_features(df, '2019-7290', 524340, 'A250', 'Clay', 'POR', 'Estoril Open')
    add_features(df, '2019-M021', 6536160, 'A1000', 'Clay', 'ESP', 'Mutua Madrid Open')
    add_features(df, '2019-M009', 5207405, 'A1000', 'Clay', 'ITA', "Internazionali BNL d'Italia")
    add_features(df, '2019-7694', 524340, 'A250', 'Clay', 'FRA', 'Lyon Open')
    add_features(df, '2019-0322', 524340, 'A250', 'Clay', 'SWI', 'Geneva Open')
    add_features(df, '2019-520', 20060000, 'G', 'Clay', 'FRA', 'Roland Garros')
    add_features(df, '2019-0321', 679015, 'A250', 'Grass', 'GER', 'Mercedes Cup')
    add_features(df, '2019-M010', 635750, 'A250', 'Grass', 'NED', 'Libema Open')
    add_features(df, '2019-0311', 2081830, 'A500', 'Grass', 'UK', 'Aegon Championships')
    add_features(df, '2019-0500', 2081830, 'A500', 'Grass', 'GER', 'Gerry Weber Open')
    add_features(df, '2019-7650', 445690, 'A250', 'Grass', 'TUR', 'Antalya Open')
    add_features(df, '2019-M016', 684080, 'A250', 'Grass', 'UK', 'Nature Valley International')
    add_features(df, '2019-540', 17769000, 'G', 'Grass', 'UK', 'Wimbledon')
    add_features(df, '2019-0315', 583585, 'A250', 'Grass', 'UK', "Hall of Fame Tennis Championship")
    add_features(df, '2019-0316', 524340, 'A250', 'Clay', 'SWE', 'SkiStar Swedish Open')
    add_features(df, '2019-0414', 1718170, 'A500', 'Clay', 'GER', 'International German Open')
    add_features(df, '2019-0439', 524340, 'A250', 'Clay', 'CRO', 'Croatia Open')
    add_features(df, '2019-0314', 524340, 'A250', 'Clay', 'SWI', 'Swiss Open Gstaad')
    add_features(df, '2019-6116', 694995, 'A250', 'Hard', 'USA', 'BB & T Atlanta Open')
    add_features(df, '2019-7480', 762455, 'A250', 'Hard', 'MEX', 'Mifel Open')
    add_features(df, '2019-0319', 524340, 'A250', 'Clay', 'AUS', 'Generali Open')
    add_features(df, '2019-M035', 1895290, 'A500', 'Hard', 'USA', 'Citi Open')
    add_features(df, '2019-0421', 5701945, 'A1000', 'Hard', 'CAN', 'Rogers Cup')
    add_features(df, '2019-M024', 6056280, 'A1000', 'Hard', 'USA', 'Western & Southern Financial Group Masters')
    add_features(df, '2019-6242', 717955, 'A250', 'Hard', 'USA', "Winston-Salem Open")
    add_features(df, '2019-560', 28619350, 'G', 'Hard', 'USA', 'US Open')
    add_features(df, '2019-0568', 1180000, 'A250', 'Hard Indoor', 'RUS', 'St. Petersburg Open')
    add_features(df, '2019-0341', 524340, 'A250', 'Hard', 'FRA', 'Moselle Open')
    add_features(df, '2019-7581', 1096575, 'A250', 'Hard', 'CHN', 'Chengdu Open')
    add_features(df, '2019-9164', 931335, 'A250', 'Hard', 'CHN', 'Zhuhai Open')
    add_features(df, '2019-0329', 1895290, 'A500', 'Hard', 'JAP', 'Rakuten Japan Open Tennis Championship')
    add_features(df, '2019-M015', 3515225, 'A500', 'Hard', 'CHN', 'China Open')
    add_features(df, '2019-5014', 7473620, 'A1000', 'Hard', 'CHN', 'Shanghai Rolex Masters')
    add_features(df, '2019-M014', 840130, 'A250', 'Hard', 'RUS', 'Kremlin Cup')
    add_features(df, '2019-7485', 635750, 'A250', 'Hard', 'BEL', 'European Open')
    add_features(df, '2019-0429', 635750, 'A250', 'Hard', 'SWE', 'Stockholm Open')
    add_features(df, '2019-0328', 2082655, 'A500', 'Hard Indoors', 'SWI', 'Swiss Indoors Basel')
    add_features(df, '2019-0337', 2296490, 'A500', 'Hard', 'AUT', 'Erste Bank Open')
    add_features(df, '2019-0352', 5207405, 'A1000', 'Hard', 'FRA', 'BNP Paribas Masters')
    add_features(df, '2019-7696', 1400000, 'AF', 'Hard', 'ITA', 'Next Gen ATP Finals')
    add_features(df, '2019-0605', 9000000, 'AF', 'Hard', 'UK', 'ATP World Tour Finals')

    ## 2020
    add_features(df, '2020-8888', 15000000, 'AF', 'Hard', 'AUS', 'ATP Cup')
    add_features(df, '2020-0451', 1359180, 'A250', 'Hard', 'QAT', 'Qatar ExxonMobil Open')
    add_features(df, '2020-M056', 546355, 'A250', 'Hard', 'AUS', 'Adelaide International')
    add_features(df, '2020-0891', 546355, 'A250', 'Hard', 'IND', 'Chennai Open')
    add_features(df, '2020-0301', 546355, 'A250', 'Hard', 'NZL', 'Auckland Open')
    add_features(df, '2020-580', 32505000, 'G', 'Hard', 'AUS', 'Australia Open')
    add_features(df, '2020-9158', 546355, 'A250', 'Clay', 'ESP', 'Cordoba Open')
    add_features(df, '2020-0375', 542695, 'A250', 'Hard', 'FRA', 'Open Sud de France')
    add_features(df, '2020-0407', 2013855, 'A500', 'Hard Indoors', 'NED', 'ABN AMRO World Tennis Tournament')
    add_features(df, '2020-0424', 719320, 'A250', 'Hard', 'USA', 'New York Open')
    add_features(df, '2020-0506', 611420, 'A250', 'Clay', 'ARG', 'Argentina Open')
    add_features(df, '2020-6932', 1759905, 'A500', 'Clay', 'BRA', 'Rio Open')
    add_features(df, '2020-0499', 602935, 'A250', 'Hard', 'USA', 'Delray Beach Open')
    add_features(df, '2020-0496', 691880, 'A250', 'Hard Indoors', 'FRA', 'Open 13')
    add_features(df, '2020-M004', 1845265, 'A500', 'Clay', 'MEX', 'Abierto Mexicano Telcel')
    add_features(df, '2020-0495', 2794840, 'A500', 'Hard', 'UAE', 'Dubai Duty Free Tennis Championship')
    add_features(df, '2020-8996', 604010, 'A250', 'Clay', 'CHI', 'Chile Open')
    add_features(df, '2020-M024', 4222190, 'A1000', 'Hard', 'USA', 'Western & Southern Financial Group Masters')
    add_features(df, '2020-560', 21656000, 'G', 'Hard', 'USA', 'US Open')
    add_features(df, '2020-0319', 336680, 'A250', 'Clay', 'AUS', 'Generali Open')
    add_features(df, '2020-M009', 3465045, 'A1000', 'Clay', 'ITA', "Internazionali BNL d'Italia")
    add_features(df, '2020-0414', 1062520, 'A500', 'Clay', 'GER', 'International German Open')
    add_features(df, '2020-520', 18209040, 'G', 'Clay', 'FRA', 'Roland Garros')
    add_features(df, '2020-0568', 1243790, 'A500', 'Hard Indoor', 'RUS', 'St. Petersburg Open')
    add_features(df, '2020-9404', 271345, 'A250', 'Hard Indoor', 'GER', 'bett1HULKS Indoors')
    add_features(df, '2020-9408', 271345, 'A250', 'Clay', 'ITA', 'Sardegna Open')
    add_features(df, '2020-9406', 271345, 'A250', 'Hard', 'GER', 'bett1HULKS Championship')
    add_features(df, '2020-7485', 394800, 'A250', 'Hard', 'BEL', 'European Open')
    add_features(df, '2020-0337', 1409510, 'A500', 'Hard', 'AUT', 'Erste Bank Open')
    add_features(df, '2020-9410', 273345, 'A250', 'Hard', 'KAZ', 'Astana Open')
    add_features(df, '2020-0352', 3343725, 'A1000', 'Hard', 'FRA', 'BNP Paribas Masters')
    add_features(df, '2020-7434', 325615, 'A250', 'Hard', 'BUL', 'Sofia Open')
    add_features(df, '2020-0605', 5700000, 'AF', 'Hard', 'UK', 'ATP World Tour Finals')

    ## 2021
    add_features(df, '2021-9426', 300000, 'A250', 'Hard', 'TUR', 'Antalya Open')
    add_features(df, '2021-0499', 349530, 'A250', 'Hard', 'USA', 'Delray Beach Open')
    add_features(df, '2021-8998', 320775, 'A250', 'Hard', 'AUS', 'Great Ocean Road Open')
    add_features(df, '2021-9428', 320775, 'A250', 'Hard', 'AUS', 'Murray River Open')
    add_features(df, '2021-8888', 4555556, 'AF', 'Hard', 'AUS', 'ATP Cup')
    add_features(df, '2021-580', 32790000, 'G', 'Hard', 'AUS', 'Australia Open')
    add_features(df, '2021-0375', 419470, 'A250', 'Hard', 'FRA', 'Open Sud de France')
    add_features(df, '2021-9158', 452600, 'A250', 'Clay', 'ESP', 'Cordoba Open')
    add_features(df, '2021-9460', 480000, 'A250', 'Hard', 'SGP', 'Singapore Open')
    add_features(df, '2021-0407', 1176695, 'A500', 'Hard Indoors', 'NED', 'ABN AMRO World Tennis Tournament')
    add_features(df, '2021-0506', 506770, 'A250', 'Clay', 'ARG', 'Argentina Open')
    add_features(df, '2021-0451', 1050570, 'A250', 'Hard', 'QAT', 'Qatar ExxonMobil Open')
    add_features(df, '2021-8996', 500345, 'A250', 'Clay', 'CHI', 'Chile Open')
    add_features(df, '2021-0496', 534790, 'A250', 'Hard Indoors', 'FRA', 'Open 13')
    add_features(df, '2021-0495', 1897805, 'A500', 'Hard', 'UAE', 'Dubai Duty Free Tennis Championship')
    add_features(df, '2021-0807', 1053910, 'A500', 'Clay', 'MEX', 'Abierto Mexicano Telcel')
    add_features(df, '2021-0403', 3343785, 'A1000', 'Hard', 'USA', 'Miami Open')
    add_features(df, '2021-9481', 408800, 'A250', 'Clay', 'ITA', 'Sardegna Open')
    add_features(df, '2021-9462', 408800, 'A250', 'Clay', 'ESP', 'AnyTech365 Andalucia Open')
    add_features(df, '2021-0410', 2082960, 'A1000', 'Clay', 'MON', 'Monte-Carlo Rolex Masters')
    add_features(df, '2021-0425', 1565480, 'A500', 'Clay', 'ESP', 'Barcelona Open')
    add_features(df, '2021-5053', 650000, 'A250', 'Clay', 'SER', 'Serbia Open')
    add_features(df, '2021-0308', 419470, 'A250', 'Clay', 'GER', 'BMW Open')
    add_features(df, '2021-7290', 419470, 'A250', 'Clay', 'POR', 'Estoril Open')
    add_features(df, '2021-1536', 2614465, 'A1000', 'Clay', 'ESP', 'Mutua Madrid Open')
    add_features(df, '2021-0416', 2082960, 'A1000', 'Clay', 'ITA', "Internazionali BNL d'Italia")
    add_features(df, '2021-7694', 419470, 'A250', 'Clay', 'FRA', 'Lyon Open')
    add_features(df, '2021-0322', 419470, 'A250', 'Clay', 'SWI', 'Geneva Open')
    add_features(df, '2021-9510', 480000, 'A250', 'Clay', 'ITA', 'Emilia-Romagna Open')
    add_features(df, '2021-9512', 511000, 'A250', 'Clay', 'ITA', 'Belgrade Open')
    add_features(df, '2021-520', 17171108, 'G', 'Clay', 'FRA', 'Roland Garros')
    add_features(df, '2021-0321', 543210, 'A250', 'Grass', 'GER', 'Mercedes Cup')
    add_features(df, '2021-0311', 1290135, 'A500', 'Grass', 'UK', 'Aegon Championships')
    add_features(df, '2021-0500', 1318605, 'A500', 'Grass', 'GER', 'Gerry Weber Open')
    add_features(df, '2021-8994', 720000, 'A250', 'Grass', 'ESP', 'Mallorca Championships')
    add_features(df, '2021-0741', 547265, 'A250', 'Grass', 'GER', 'Aegon Open')
    add_features(df, '2021-540', 17066000, 'G', 'Grass', 'UK', 'Wimbledon')
    add_features(df, '2021-0315', 466870, 'A250', 'Grass', 'UK', "Hall of Fame Tennis Championship")
    add_features(df, '2021-0316', 419470, 'A250', 'Clay', 'SWE', 'SkiStar Swedish Open')
    add_features(df, '2021-0414', 1005125, 'A500', 'Clay', 'GER', 'International German Open')
    add_features(df, '2021-7480', 598545, 'A250', 'Hard', 'MEX', 'Mifel Open')
    add_features(df, '2021-0314', 419470, 'A250', 'Clay', 'SWI', 'Swiss Open Gstaad')
    add_features(df, '2021-0439', 524340, 'A250', 'Clay', 'CRO', 'Croatia Open')
    add_features(df, '2021-0319', 419470, 'A250', 'Clay', 'AUS', 'Generali Open')
    add_features(df, '2021-6116', 555995, 'A250', 'Hard', 'USA', 'BB & T Atlanta Open')
    add_features(df, '2021-0418', 1895290, 'A500', 'Hard', 'USA', 'Citi Open')
    add_features(df, '2021-0421', 2850975, 'A1000', 'Hard', 'CAN', 'Rogers Cup')
    add_features(df, '2021-0422', 6056280, 'A1000', 'Hard', 'USA', 'Western & Southern Financial Group Masters')
    add_features(df, '2021-6242', 717955, 'A250', 'Hard', 'USA', "Winston-Salem Open")
    add_features(df, '2021-560', 27200000, 'G', 'Hard', 'USA', 'US Open')
    add_features(df, '2021-0341', 419470, 'A250', 'Hard', 'FRA', 'Moselle Open')
    add_features(df, '2021-9410', 480000, 'A250', 'Hard', 'KAZ', 'Astana Open')
    add_features(df, '2021-7434', 419470, 'A250', 'Hard', 'BUL', 'Sofia Open')
    add_features(df, '2021-9569', 600000, 'A250', 'Hard', 'USA', 'San Diego Open')
    add_features(df, '2021-0404', 8359455, 'A1000', 'Hard', 'USA', 'BNP Paribas Open')
    add_features(df, '2021-7485', 508600, 'A250', 'Hard', 'BEL', 'European Open')
    add_features(df, '2021-0438', 697125, 'A250', 'Hard', 'RUS', 'Kremlin Cup')
    add_features(df, '2021-0568', 863705, 'A250', 'Hard Indoors', 'RUS', 'St. Petersburg Open')
    add_features(df, '2021-0337', 1952015, 'A500', 'Hard', 'AUT', 'Erste Bank Open')
    add_features(df, '2021-0352', 5207405, 'A1000', 'Hard', 'FRA', 'BNP Paribas Masters')
    add_features(df, '2021-0429', 635750, 'A250', 'Hard', 'SWE', 'Stockholm Open')
    add_features(df, '2021-7696', 1300000, 'AF', 'Hard', 'BRA', 'Next Gen ATP Finals')
    add_features(df, '2021-0605', 7250000, 'AF', 'Hard', 'ITA', 'ATP World Tour Finals')

    # 2022
    add_features(df, '2022-8888', 10000000, 'AF', 'Hard', 'AUS', 'ATP Cup')
    add_features(df, '2022-8998', 416800, 'A250', 'Hard', 'AUS', 'Adelaide International 1')
    add_features(df, '2022-9665', 521000, 'A250', 'Hard', 'AUS', 'Melbourne Summer Set')
    add_features(df, '2022-9663', 521000, 'A250', 'Hard', 'AUS', 'Sydney International')
    add_features(df, '2022-9667', 430530, 'A250', 'Hard', 'AUS', 'Adelaide International 2')
    add_features(df, '2022-580', 33784200, 'G', 'Hard', 'AUS', 'Australia Open')
    add_features(df, '2022-0375', 427645, 'A250', 'Hard Indoors', 'FRA', 'Open Sud de France')
    add_features(df, '2022-0891', 546355, 'A250', 'Hard', 'IND', 'Chennai Open')
    add_features(df, '2022-9158', 430530, 'A250', 'Clay', 'ESP', 'Cordoba Open')
    add_features(df, '2022-0407', 1208315, 'A500', 'Hard Indoors', 'NED', 'ABN AMRO World Tennis Tournament')
    add_features(df, '2022-0424', 708530, 'A250', 'Hard', 'USA', 'Dallas Open')
    add_features(df, '2022-0506', 602250, 'A250', 'Clay', 'ARG', 'Argentina Open')
    add_features(df, '2022-0451', 1071030, 'A250', 'Hard', 'QAT', 'Qatar ExxonMobil Open')
    add_features(df, '2022-6932', 1660290, 'A500', 'Clay', 'BRA', 'Rio Open')
    add_features(df, '2022-0496', 545200, 'A250', 'Hard Indoors', 'FRA', 'Open 13')
    add_features(df, '2022-0499', 593895, 'A250', 'Hard', 'USA', 'Delray Beach Open')
    add_features(df, '2022-M004', 1678065, 'A500', 'Clay', 'MEX', 'Abierto Mexicano Telcel')
    add_features(df, '2022-0495', 2794840, 'A500', 'Hard', 'UAE', 'Dubai Duty Free Tennis Championship')
    add_features(df, '2022-8996', 475960, 'A250', 'Clay', 'CHI', 'Chile Open')
    add_features(df, '2022-404', 8584055, 'A1000', 'Hard', 'USA', 'BNP Paribas Open')
    add_features(df, '2022-M007', 8584055, 'A1000', 'Hard', 'USA', 'Miami Open')
    add_features(df, '2022-0360', 534555, 'A250', 'Clay', 'MAR', 'Grand Prix Hassan II')
    add_features(df, '2022-0717', 594950, 'A250', 'Clay', 'USA', 'U.S. Mens Clay Court Championship')
    add_features(df, '2022-0410', 5415410, 'A1000', 'Clay', 'MON', 'Monte-Carlo Rolex Masters')
    add_features(df, '2022-0425', 2661825, 'A500', 'Clay', 'ESP', 'Barcelona Open')
    add_features(df, '2022-5053', 534555, 'A250', 'Clay', 'SER', 'Serbia Open')
    add_features(df, '2022-7290', 534555, 'A250', 'Clay', 'POR', 'Estoril Open')
    add_features(df, '2022-M021', 6744165, 'A1000', 'Clay', 'ESP', 'Mutua Madrid Open')
    add_features(df, '2022-M009', 5415410, 'A1000', 'Clay', 'ITA', "Internazionali BNL d'Italia")
    add_features(df, '2022-7694', 534555, 'A250', 'Clay', 'FRA', 'Lyon Open')
    add_features(df, '2022-0322', 534555, 'A250', 'Clay', 'SWI', 'Geneva Open')
    add_features(df, '2022-520', 21256800, 'G', 'Clay', 'FRA', 'Roland Garros')
    add_features(df, '2022-0321', 543210, 'A250', 'Grass', 'GER', 'Mercedes Cup')
    add_features(df, '2022-M010', 648130, 'A250', 'Grass', 'NED', 'Libema Open')
    add_features(df, '2022-0311', 2134520, 'A500', 'Grass', 'UK', 'Aegon Championships')
    add_features(df, '2022-0500', 2134520, 'A500', 'Grass', 'GER', 'Gerry Weber Open')
    add_features(df, '2022-8994', 886500, 'A250', 'Grass', 'ESP', 'Mallorca Championships')
    add_features(df, '2022-0741', 697405, 'A250', 'Grass', 'GER', 'Aegon Open')
    add_features(df, '2022-540', 18652000, 'G', 'Grass', 'UK', 'Wimbledon')
    add_features(df, '2022-0315', 594950, 'A250', 'Grass', 'UK', "Hall of Fame Tennis Championship")
    add_features(df, '2022-0316', 534555, 'A250', 'Clay', 'SWE', 'SkiStar Swedish Open')
    add_features(df, '2022-0314', 534555, 'A250', 'Clay', 'SWI', 'Swiss Open Gstaad')
    add_features(df, '2022-0414', 1770865, 'A500', 'Clay', 'GER', 'International German Open')
    add_features(df, '2022-0319', 534555, 'A250', 'Clay', 'AUS', 'Generali Open')
    add_features(df, '2022-0439', 534555, 'A250', 'Clay', 'CRO', 'Croatia Open')
    add_features(df, '2022-6116', 708530, 'A250', 'Hard', 'USA', 'BB & T Atlanta Open')
    add_features(df, '2022-7480', 822110, 'A250', 'Hard', 'MEX', 'Mifel Open')
    add_features(df, '2022-M035', 1953285, 'A500', 'Hard', 'USA', 'Citi Open')
    add_features(df, '2022-0421', 5926545, 'A1000', 'Hard', 'CAN', 'Rogers Cup')
    add_features(df, '2022-M024', 6280880, 'A1000', 'Hard', 'USA', 'Western & Southern Financial Group Masters ')
    add_features(df, '2022-6242', 731935, 'A250', 'Hard', 'USA', "Winston-Salem Open")
    add_features(df, '2022-560', 27915200, 'G', 'Hard', 'USA', 'US Open')

    return df

def transform_bet_data(df):
    df['Tournament'] = df['Tournament'].replace(
        ['French Open', 'Monte Carlo Masters', 'Shanghai Masters', 'Rogers Masters',
         'Winston-Salem Open at Wake Forest University', 'AEGON Championships', 'Dubai Tennis Championships',
         'Abierto Mexicano', 'Qatar Exxon Mobil Open', 'Open Banco Sabadell', 'Hall of Fame Championships',
         'Swiss Indoors', 'Rakuten Japan Open Tennis Championships', 'Open de Moselle',
         "U.S. Men's Clay Court Championships", 'BB&T Atlanta Open', 'Forte Village Sardegna Open',
         'BA-CA Tennis Trophy', 'Viking International', 'Power Horse Cup', 'Tata Open', 'Proton Malaysian Open',
         'Hungarian Open', 'Portugal Open', 'Millenium Estoril Open', 'Millennium Estoril Open',
         "Open de Nice Côte d’Azur", 'Masters Cup', 'ATP Vegeta Croatia Open', 'Studena Croatia Open',
         'Konzum Croatia Open', 'German Open Tennis Championships', 'Mutua Madrilena Madrid Open',
         'Barcelona Open BancSabadell', 'Heineken Open', 'ASB Classic', 'Unicef Open', 'Mutua Madrileña Madrid Open',
         'Medibank International', 'Australian Open', 'Movistar Open', 'Copa Telmex', 'International Championships',
         'Barcelona Open BancSabadell', "Open de Nice Cote d'Azur", 'AEGON International',
         'Atlanta Tennis Championships', 'Allianz Suisse Open', 'Legg Mason Classic', 'Open Romania', 'Copa Claro',
         'Apia International', 'VTR Open', 'Bet-At-Home Cup', 'Vienna Open'],
        ['Roland Garros', 'Monte-Carlo Rolex Masters', 'Shanghai Rolex Masters', 'Rogers Cup', 'Winston-Salem Open',
         'Aegon Championships', 'Dubai Duty Free Tennis Championship', 'Abierto Mexicano Telcel',
         'Qatar ExxonMobil Open', 'Barcelona Open BancSabadell', 'Hall of Fame Tennis Championship',
         'Swiss Indoors Basel', 'Rakuten Japan Open Tennis Championship', 'Moselle Open',
         "U.S. Mens Clay Court Championship", 'BB & T Atlanta Open', 'Sardegna Open', 'Erste Bank Open', 'Aegon Open',
         'Power Horse Open', 'Tata Open Maharashtra', 'Malaysian Open', 'Gazprom Hungarian Open', 'Estoril Open',
         'Estoril Open', 'Estoril Open', "Open de Nice Cote d'Azur", 'ATP World Tour Finals', 'Croatia Open',
         'Croatia Open', 'Croatia Open', 'International German Open', 'Mutua Madrid Open', 'Barcelona Open',
         'Auckland Open', 'Auckland Open', 'UNICEF Open', 'Mutua Madrid Open', 'Sydney International', 'Australia Open',
         'Chile Open', 'Argentina Open', 'Delray Beach Open', 'Barcelona Open', "Open De Nice Cote d'Azur",
         'Aegon Open', 'Atlanta Tennis Championship', 'Swiss Open Gstaad', 'Citi Open', 'BCR Open Romania',
         'Argentina Open', 'Sydney International', 'Chile Open', 'Bet-At-Home Cup Kitzbuhel', 'Erste Bank Open'])

    df['Tournament'] = df['Tournament'].replace(
        ["Barcelona Open BancSabadell", "Open de Nice Cote d'Azur", "BCR Open Romania",
         "Crédit Agricole Suisse Open Gstaad", "Royal Guard Open Chile", "bet-at-home Open", "Ecuador Open",
         "Sony Ericsson Open", "AEGON Open", "Suisse Open Gstaad", "Abierto Mexicano Mifel", "Canadian Open",
         "Rakuten Japan Open Tennis Championships", "Dusseldorf Open", "German Tennis Championships", "Tata Open",
         "Garanti Koza Sofia Open", "Ricoh Open", "Eastbourne International", "Maharashtra Open",
         "Queen's Club Championships", "Halle Open", "Open Banco Sabadell", "Rosmalen Grass Court Championships"],
        ["Barcelona Open", "Open De Nice Cote d'Azur", "BRD Nastase Tiriac Trophy", "Swiss Open Gstaad", "Chile Open",
         "International German Open", "Ecuador Open Quito", "Miami Open", "Aegon Open", "Swiss Open Gstaad",
         "Mifel Open", "Rogers Cup", "Rakuten Japan Open Tennis Championship", "Power Horse Open",
         "International German Open", "Chennai Open", "Sofia Open", "Libema Open", "Nature Valley International",
         "Chennai Open", "Aegon Championships", "Gerry Weber Open", "Barcelona Open", "Libema Open"])
    return df

def drop_some_extra_rows(df):
    to_drop = df[
        (df['tourney_name'] == 'Australian Open') & (df['tourney_id'] == '2016-580') & (df['match_num'] == 102)].index
    df.drop(to_drop, inplace=True)
    to_drop = df[
        (df['tourney_name'] == 'Australian Open') & (df['tourney_id'] == '2016-580') & (df['match_num'] == 104)].index
    df.drop(to_drop, inplace=True)
    to_drop = df[
        (df['tourney_name'] == 'Australian Open') & (df['tourney_id'] == '2016-580') & (df['match_num'] == 126)].index
    df.drop(to_drop, inplace=True)
    to_drop = df[
        (df['tourney_name'] == 'Australian Open') & (df['tourney_id'] == '2016-580') & (df['match_num'] == 139)].index
    df.drop(to_drop, inplace=True)
    to_drop = df[
        (df['tourney_name'] == 'Australian Open') & (df['tourney_id'] == '2016-580') & (df['match_num'] == 147)].index
    df.drop(to_drop, inplace=True)
    to_drop = df[
        (df['tourney_name'] == 'Australian Open') & (df['tourney_id'] == '2016-580') & (df['match_num'] == 158)].index
    df.drop(to_drop, inplace=True)
    to_drop = df[
        (df['tourney_name'] == 'Roland Garros') & (df['tourney_id'] == '2020-520') & (df['match_num'] == 1307)].index
    df.drop(to_drop, inplace=True)
    to_drop = df[
        (df['tourney_name'] == 'Roland Garros') & (df['tourney_id'] == '2020-520') & (df['match_num'] == 1308)].index
    df.drop(to_drop, inplace=True)
    return df

def change_winner_loser_to_A_B(df):
    df = df[['tourney_id_', 'Tournament', 'Location', 'location', 'Surface', 'Court', 'draw_size', 'Series',
             'money_prize', 'tourney_date', 'year', 'month', 'day', 'match_num', 'best_of', 'Round', 'score',
             'W1', 'L1', 'W2', 'L2', 'W3', 'L3', 'W4', 'L4', 'W5', 'L5', 'Wsets', 'Lsets', 'minutes', 'winner_id',
             'winner_name', 'loser_id', 'loser_name', 'winner_rank', 'loser_rank', 'winner_seed', 'winner_entry',
             'winner_hand', 'winner_ht', 'winner_ioc', 'winner_age', 'loser_seed', 'loser_entry', 'loser_hand',
             'loser_ht', 'loser_ioc', 'loser_age', 'w_ace', 'w_df', 'w_svpt', 'w_1stIn', 'w_1stWon', 'w_2ndWon',
             'w_SvGms', 'w_bpSaved', 'w_bpFaced', 'l_ace', 'l_df', 'l_svpt', 'l_1stIn', 'l_1stWon', 'l_2ndWon',
             'l_SvGms', 'l_bpSaved', 'l_bpFaced', 'winner_rank_points', 'loser_rank_points', 'B365W', 'B365L',
             'PSW', 'PSL', 'MaxW', 'MaxL', 'AvgW', 'AvgL', 'EXW', 'EXL', 'LBW', 'LBL', 'SJW', 'SJL', 'Label']]
    df.rename(columns={'tourney_id_': 'tourney_id', 'Tournament': 'tournament', 'Location': 'country',
                       'Surface': 'surface', 'Court': 'court', 'Series': 'series', 'Round': 'round', 'W1': 'A1',
                       'L1': 'B1', 'W2': 'A2', 'L2': 'B2', 'W3': 'A3', 'L3': 'B3', 'W4': 'A4', 'L4': 'B4', 'W5': 'A5',
                       'L5': 'B5', 'Wsets': 'Asets', 'Lsets': 'Bsets', 'winner_id': 'A_id', 'winner_name': 'A_name',
                       'loser_id': 'B_id', 'loser_name': 'B_name', 'winner_rank': 'A_rank', 'loser_rank': 'B_rank',
                       'winner_seed': 'A_seed', 'winner_entry': 'A_entry', 'winner_hand': 'A_hand', 'winner_ht': 'A_ht',
                       'winner_ioc': 'A_ioc', 'winner_age': 'A_age', 'loser_seed': 'B_seed', 'loser_entry': 'B_entry',
                       'loser_hand': 'B_hand', 'loser_ht': 'B_ht', 'loser_ioc': 'B_ioc', 'loser_age': 'B_age',
                       'w_ace': 'A_ace', 'w_df': 'A_df', 'w_svpt': 'A_svpt', 'w_1stIn': 'A_1stIn',
                       'w_1stWon': 'A_1stWon', 'w_2ndWon': 'A_2ndWon', 'w_SvGms': 'A_SvGms', 'w_bpSaved': 'A_bpSaved',
                       'w_bpFaced': 'A_bpFaced', 'l_ace': 'B_ace', 'l_df': 'B_df', 'l_svpt': 'B_svpt',
                       'l_1stIn': 'B_1stIn', 'l_1stWon': 'B_1stWon', 'l_2ndWon': 'B_2ndWon', 'l_SvGms': 'B_SvGms',
                       'l_bpSaved': 'B_bpSaved', 'l_bpFaced': 'B_bpFaced', 'winner_rank_points': 'A_rank_points',
                       'loser_rank_points': 'B_rank_points', 'B365W': 'A_B365',  'B365L': 'B_B365', 'PSW': 'A_PS',
                       'PSL': 'B_PS', 'MaxW': 'A_Max', 'MaxL': 'B_Max', 'AvgW': 'A_Avg', 'AvgL': 'B_Avg', 'EXW': 'A_EX',
                       'EXL': 'B_EX', 'LBW': 'A_LB', 'LBL': 'B_LB', 'SJW': 'A_SJ', 'SJL': 'B_SJ'
                       },  inplace=True)
    return df

def merger_data(df_atp, df_bet):
    transformed_atp = transform_feature_tourney_id(df_atp)
    df_atp_features = get_data_with_new_features(transformed_atp)
    transformed_bets = transform_bet_data(df_bet)

    merger = pd.merge(df_atp_features, transformed_bets,
                      how='left',
                      left_on=['year', 'long_tourney_name', 'winner_lname', 'loser_lname'],
                      right_on=['Year', 'Tournament', 'Winner Last Name', 'Loser Last Name']
                      )
    merger.sort_values(['tourney_date', 'tourney_id'], inplace=True)
    merger = drop_some_extra_rows(merger)
    merger = change_winner_loser_to_A_B(merger)
    return merger



