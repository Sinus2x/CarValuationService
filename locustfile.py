import random
from locust import HttpUser, task, between


brand = [
    'Volkswagen', 'Renault', 'Mercedes-Benz', 'Hyundai', 'Jaguar',
    'ГАЗ', 'Skoda', 'Toyota', 'ZOTYE', 'BMW', 'Dodge', 'Chevrolet',
    'Mazda', 'Audi', 'Lexus', 'Volvo', 'Subaru', 'Kia', 'Daewoo',
    'Great Wall', 'Ford', 'ВАЗ (LADA)', 'Iran Khodro', 'Honda',
    'Geely', 'Mitsubishi', 'Peugeot', 'Citroen', 'Москвич',
    'SsangYong', 'Infiniti', 'Opel', 'Nissan', 'Porsche', 'Smart',
    'Suzuki', 'Chery', 'SEAT', 'Daihatsu', 'LIFAN', 'Genesis',
    'Vortex', 'Haval', 'Jeep', 'Богдан', 'MINI', 'FIAT', 'Ravon',
    'УАЗ', 'Land Rover', 'Scion', 'ТагАЗ', 'Chrysler', 'ВИС', 'BYD',
    'Cadillac', 'ИЖ', 'JAC', 'Hafei', 'Iveco', 'ЗАЗ', 'Saab', 'FAW',
    'ЛуАЗ', 'ZX', 'Pontiac', 'Datsun', 'Exeed', 'GAC', 'Changan',
    'Brilliance', 'Bentley', 'Rover', 'BAW', 'Tesla', 'Acura'
]

model = [
    'Passat', 'Kaptur', 'M-класс', 'GL-класс AMG', 'Tucson', 'E-Pace',
    '24 Волга', 'Viano', 'Superb', 'GLC-класс Coupe', 'Probox', 'T600',
    'Prius Alpha', 'X6', 'Caravan', 'Malibu', 'Demio', 'ГАЗель 3221',
    'A4', 'Mark II', '7 серия', 'Touareg', 'Kodiaq', 'RAV4', '3', 'LX',
    'S40', 'ГАЗель 2705', 'Forester', 'Land Cruiser', 'Sportage',
    'ГАЗель 3302', 'Sandero', 'Corolla', 'Phaeton', 'A8', 'Matrix',
    'Leganza', 'Hover H3', 'Fusion', '6', '2103', 'Samand',
    'Corolla Spacio', 'Elantra', 'Accord', 'Atlas', 'Outlander', 'TT',
    'Boxer', 'XV', 'Getz', 'C-класс', 'ProCeed', 'C4', '2141',
    'Granta Cross', 'Actyon', 'Octavia', 'Corona', 'Solaris', 'X1',
    'FX35', 'Land Cruiser Prado', 'Astra GTC', 'Skyline', 'Frontera',
    '3 серия GT', 'Соболь 2217', 'Sunny', 'Premio', 'i30', 'Transit',
    'GLA-класс', 'Cayenne GTS', 'Pajero Sport', 'X5', 'Transporter',
    'Fortwo', '308', 'Grand Vitara', 'GS', 'Tiggo (T11)', 'Qashqai',
    'Primera', 'Mondeo', 'Creta', '460', 'Duster', 'A3', 'Zafira',
    'MK', 'Camry', 'E-класс', 'Jetta', 'Serena', 'Note', 'Toledo',
    '2112', 'Soul', 'Cerato', '3 серия', 'A6', 'Macan Turbo', 'Golf',
    'Leaf', 'Colt', 'i40', 'Astra', 'S-класс', 'YRV', '5 серия',
    '2101', 'Corsa', 'X50', 'Lancer', 'Rio', '2121 (4x4) Фора',
    'Kalina', 'Cresta', 'Cayenne', 'V40', 'Liberty', 'Logan',
    'Terrano', '2107', 'XC90', 'Domani', 'Соболь 2752', 'G80', 'Focus',
    'Q5', 'Wish', 'M37', 'Hover', 'Pajero', 'Avensis', 'Ram', 'Q7',
    'CR-V', 'Yeti', 'Funcargo', 'Jimny', 'Highlander', 'B-Series',
    'ГАЗель 33023', 'Caddy', 'Mirage', 'Fabia', 'Tiguan', 'Juke',
    'EcoSport', 'Sonata', 'IS', '3110 Волга', 'ГАЗель Next',
    'Emgrand EC7', 'CX-3', 'Prius', 'Corona Premio', 'X70',
    'Corolla Ceres', 'March', '207', 'Santa Fe',
    'Mark II Wagon Qualis', 'Tingo', 'W124', 'ES', 'H6',
    'Grand Cherokee', '2110', 'Legacy', 'Panamera 4',
    'Cooper S Countryman', 'Volga Siber', 'G-класс AMG', 'Clio',
    'Grand Scenic', 'Fit', 'Chaser', 'Safe', 'Linea', 'Passat CC',
    'Carina', 'Coupa', 'Polo', 'XRAY', '4x4 (Нива)', 'Galant',
    'Largus', 'Lancer Cedia', 'Megane', 'Starlet', 'Bassara',
    'Caldina', '2105', 'Scorpio', 'Rapid', 'R2', 'Vito', 'Compass',
    '100', 'Escort', 'XJ', 'Ceed', 'Carina ED', 'Saber', 'Taurus',
    'Picanto', 'Logo', 'Fiesta', 'Granta', 'Ractis', 'X-Trail',
    'Patriot', 'CLK-класс', '307', 'X5 M', 'Jolion', 'GLE-класс Coupe',
    'Outback', 'Optima', 'Cefiro', 'S80', 'Escudo', 'Venza', 'M35',
    '1 серия', 'Bora', 'Accent', '190 (W201)', 'Hover H5',
    'Freelander', 'Murano', 'Sweet (QQ)', 'Terracan', 'CX-5',
    'Golf GTI', 'Kuga', 'C-Elysee', 'Maxima', 'Staria',
    'Maybach S-класс', 'xB', 'Gaia', 'GL-класс', 'Emgrand X7', '408',
    'Punto', 'Vectra', 'Crown', 'Leon', 'SX4', 'Gentra', 'Avenir',
    'M11 (A3)', '323', 'Q5 Sportback', 'Range Rover', 'A-класс',
    'Cooper', 'Sprinter', 'Q8', 'Omega', 'QX56', 'Профи',
    'Cooper Countryman', 'Celica', 'Master (LC100)', 'AMG GT',
    'Vitara', 'S60', 'Niva Legend', 'Impreza', 'Captiva',
    'Sprinter Marino', 'GV80', '2104', 'Symbol', 'Seltos', 'Voyager',
    'C3', 'Hiace', 'Eclipse Cross', 'ix35', 'Fluence',
    'Discovery Sport', 'A4 Allroad Quattro', '31512',
    'Sprinter Classic', 'GLE-класс', 'A5', 'Teramont', 'Stinger',
    'Cebrium (720)', '2349', 'Move', 'GLC-класс', 'Succeed', 'Cruze',
    'L200', 'X2', 'Cayenne S', '2115 Samara', 'Harrier', 'Mokka',
    'Corolla II', '80', 'Nexia', 'Sorento Prime', 'A7', 'Ist', 'Edix',
    'Mustang', 'F3', 'Dokker', '401', '1111 Ока', 'Cayenne Turbo',
    'X60', 'Transit Connect', 'Kyron', 'Odyssey', 'Venga', 'Arkana',
    'Insignia', 'Istana', 'Святогор', 'Logan Stepway', 'Carnival',
    'C2', 'Yaris', 'Tribute', 'Pickup', 'Antara', 'M5', 'SRX',
    'Town Ace Noah', 'Alto', 'X7', 'Cherokee', '107', 'Micra',
    'Corolla Fielder', 'Estina', '3909', 'MPV', 'CX-9', 'Rio X',
    'Avella', 'TrailBlazer', '406', 'Corona EXiV', 'Roomster',
    'GLK-класс', 'Veloster', 'Tribeca', 'Scenic', 'AD', 'Premacy',
    'RX', 'Solano', 'Pajero iO', 'Musso', 'Hunter',
    'V40 Cross Country', 'Pacifica', 'Auris', 'Koleos', 'G-класс',
    'ix55', 'Ka', 'Laguna', '21261', 'Panamera GTS', 'Carisma', 'S3',
    'Liana', '3 MPS', 'Brio', 'Niva', '2346', 'Discovery',
    'Sandero Stepway', 'Civic', 'Tiggo 4', 'F7x', 'Patrol', 'Kangoo',
    'Teana', 'Escalade', '2131 (4x4) Urban', 'Sharan', 'X3', 'Spectra',
    'Progres', 'Galaxy', '407', 'Aveo', 'Traveller', 'Nubira',
    'C3 Picasso', 'Spark', 'RVR', 'Fortuner', 'Range Rover Evoque',
    'Rio X-Line', 'Chariot', 'Sorento', 'Efini MS-8', 'Belta',
    'Grandeur', 'A1', 'Pathfinder', 'FX37', 'Priora', 'Forfour',
    'Almera', 'Tahoe', 'Capa', 'GLE-класс AMG', 'PT Cruiser',
    'Space Star', 'Kadett', '306', 'Bongo', '626', 'Wingroad', 'Tiida',
    'Kizashi', 'Tiggo 5', 'G70', 'XRAY Cross', 'S90', 'E-класс AMG',
    'Dayz', 'Meriva', 'Hilux', 'Cami', 'Cobalt', 'XC70', 'F-Pace',
    'Explorer', '2347', 'X4', 'Festiva', 'C5', 'GLS-класс', '6 серия',
    'Prairie', 'Torneo', '2140', '31514', 'Ascot Innova', 'Sebring',
    '3102 Волга', 'Pajero Pinin', 'Mobilio Spike', '4007',
    'Sprinter Carib', 'Daily', 'QX70', 'Felicia', 'ASX', 'Safari',
    '2206', 'Mira e:S', 'Golf Plus', 'Crosstour', 'Multivan', 'Trafic',
    'Jazz', 'Tino', 'V-класс', 'CL-класс', 'Corolla Axio', 'NP300',
    '2717', 'HR-V', 'L400', 'Swift', 'Freed', 'Epica', 'Golf R',
    'Stella', '31519', 'Coolray', 'Integra SJ', '2329', '440', 'N-WGN',
    '6 серия Gran Coupe', 'Ducato', 'Porter', '39094', '1103 Славута',
    'Partner', '3962', 'GLC-класс AMG', 'Q3', 'Touran', 'Berlingo',
    '3741', 'Bongo Friendee', 'GX', 'Tiggo 3', 'Combo', 'Windom',
    '2109', 'SLK-класс', 'Actyon Sports', 'Passo', 'Domingo',
    'Fora (A21)', 'FX30', '9000', '2126', 'Stepwgn', '2111', 'Avante',
    'Breez (520)', '968 Запорожец', 'ГАЗель 2747', 'V5', 'i20',
    'Mohave', 'Presage', 'Xsara Picasso', 'Atenza', '969', 'Expert',
    'Axela', 'Cube', '2113 Samara', 'Vesta', 'Atos', 'Caliber',
    'Bluebird', 'WRX STI', '3151', '21 Волга', 'Landmark', 'Orlando',
    'Elysion', 'Prelude', 'Elgrand', 'B-класс', '607', 'CLS-класс',
    'Panamera Turbo', 'CrossEastar (B14)', 'DS 4', 'Inspire', 'Jade',
    'Vibe', 'Altea Freetrack', 'Tigra', '2108', 'Kalina Cross',
    'Camry Gracia', 'CLA-класс', 'XC60', '4 серия', 'Sephia',
    'A6 Allroad Quattro', '9-3', 'Kimo (A1)', 'Escape',
    'Urban Cruiser', 'Airtrek', 'mi-DO', 'NX', 'QQ6 (S21)', 'Tico',
    'Hiace Regius', 'R-класс', 'Tiggo 7 Pro', 'Ceed GT', 'Pointer',
    'Vesta Cross', 'Grand Santa Fe', '29891', 'Fusion (North America)',
    'H-1', 'Vista', '469', 'Master', 'C-HR', 'Tiggo 8 Pro', 'EX35',
    'Niva Travel', 'TXL', 'R Nessa', 'Macan', 'T6', 'Deer',
    '2121 (4x4) Urban', 'Sentra', 'Corolla Levin', 'Range Rover Sport',
    'Hilux Surf', 'Smily (320)', 'GN8', 'Lite Ace', 'Doblo', 'Boon',
    '3303', 'Voltz', 'CS35', 'Ignis', 'Crafter', 'Kona', 'M2 (BS4)',
    'Largo', 'on-DO', 'Movano', 'Verna', 'S-MX', 'Impreza WRX STI',
    'Civic Ferio', 'Vitz', 'IndiS (S18D)', '500', '206',
    'Continental GT', 'CLS-класс AMG', '5008', 'GLB-класс', 'XE',
    '31105 Волга', 'Raum', 'John Cooper Works Clubman', 'Quoris',
    'Sens', 'Rexton', 'Largus Cross', 'Allion', 'Amulet (A15)',
    'Pulsar', '310221 Волга', 'Lanos', 'Dingo', 'Beetle', 'QX50',
    'Legnum', 'Viva', 'CR-Z', 'C-MAX', '75', 'Карго',
    'John Cooper Works', 'Kicks', 'X6 M', 'Rodius', 'Grand Starex',
    'Sierra', 'Vanette', 'RX-8', 'F7', 'Amarok', 'Espero', 'XT5',
    '21099', 'Stream', 'Oley', 'Macan S', 'Aqua', 'Tracker', 'CTS',
    'Emgrand 7', 'Intrepid', 'Xsara', 'Nadia', 'Solio', 'Alphard',
    'Tiida Latio', 'Karoq', 'S-MAX', 'Kluger', 'C3 Aircross', 'Paseo',
    'H9', '69', 'Trans Sport', 'Verso', 'Pajero Mini', 'Jumpy', '9-5',
    'Duet', 'Platz', 'Bonus (A13)', '2 серия', 'Matiz', 'Besturn B50',
    'Starex', 'M2', 'Voxy', 'GLS-класс AMG', '4Runner', 'Courier',
    'Espace', 'Grand C4 Picasso', 'LS', 'Vega', 'Sprinter Trueno',
    'Caravelle', 'Prius V', 'Москвич-412', 'V90 Cross Country',
    'Kadjar', 'CX-7', 'Qashqai+2', 'Fit Shuttle', 'Z4', 'XC40',
    'Соболь 2310', '301', 'Traviq', '31029 Волга', 'Grandis', 'Vento',
    'Navara', 'Very', 'Leone', 'Panamera 4S', 'WiLL', '8 серия',
    '2715', 'C-Crosser', 'Grand Caravan', 'V60', 'JX', '19', 'Lacetti',
    'Fenix', '452 Буханка', '2106', 'Familia', 'Corda', 'Montero',
    'Altezza', 'Town Ace', 'Cabstar', 'Genesis', 'Opa',
    'Bluebird Sylphy', 'C-класс AMG', 'Cooper S', 'Ibiza', 'Taos',
    'Allex', 'Picnic', 'Carens', 'CX-30', 'Almera Tino', 'VX',
    'Wrangler', 'Palisade', '940', 'Terios', 'M-класс AMG',
    'Corolla Rumion', '2102', '3008', 'Rezzo', 'Evanda', 'Libero',
    'H5', 'Ascona', 'UX', 'MX-3', 'Blazer', 'Jumper', 'Model S',
    'QX80', 'Q50', 'MDX', 'Ipsum'
]

sale_end_date = [
    '2023-01-30T00:00:00.000000000',
    '2023-01-19T00:00:00.000000000', '2023-02-02T00:00:00.000000000',
    '2023-01-08T00:00:00.000000000', '2023-01-17T00:00:00.000000000',
    '2023-01-04T00:00:00.000000000', '2022-12-10T00:00:00.000000000',
    '2023-01-07T00:00:00.000000000', '2022-12-05T00:00:00.000000000',
    '2022-12-29T00:00:00.000000000', '2023-01-15T00:00:00.000000000',
    '2022-11-24T00:00:00.000000000', '2023-02-04T00:00:00.000000000',
    '2022-11-26T00:00:00.000000000', '2022-10-29T00:00:00.000000000',
    '2022-10-28T00:00:00.000000000', '2022-08-16T00:00:00.000000000',
    '2022-10-06T00:00:00.000000000', '2022-10-16T00:00:00.000000000',
    '2022-08-30T00:00:00.000000000', '2022-09-26T00:00:00.000000000',
    '2022-11-21T00:00:00.000000000', '2022-09-08T00:00:00.000000000',
    '2022-10-05T00:00:00.000000000', '2022-06-30T00:00:00.000000000',
    '2023-01-29T00:00:00.000000000', '2023-01-12T00:00:00.000000000',
    '2023-01-18T00:00:00.000000000', '2023-01-24T00:00:00.000000000',
    '2023-01-27T00:00:00.000000000', '2022-12-21T00:00:00.000000000',
    '2022-12-25T00:00:00.000000000', '2022-12-11T00:00:00.000000000',
    '2022-08-07T00:00:00.000000000', '2022-12-04T00:00:00.000000000',
    '2023-01-11T00:00:00.000000000', '2022-12-03T00:00:00.000000000',
    '2022-12-19T00:00:00.000000000', '2022-11-19T00:00:00.000000000',
    '2022-12-07T00:00:00.000000000', '2022-11-22T00:00:00.000000000',
    '2022-11-23T00:00:00.000000000', '2022-10-26T00:00:00.000000000',
    '2022-11-11T00:00:00.000000000', '2022-11-07T00:00:00.000000000',
    '2022-09-25T00:00:00.000000000', '2022-09-27T00:00:00.000000000',
    '2022-10-03T00:00:00.000000000', '2022-12-15T00:00:00.000000000',
    '2022-09-07T00:00:00.000000000', '2022-11-30T00:00:00.000000000',
    '2022-11-20T00:00:00.000000000', '2022-12-24T00:00:00.000000000',
    '2022-11-10T00:00:00.000000000', '2022-08-26T00:00:00.000000000',
    '2022-12-23T00:00:00.000000000', '2022-09-30T00:00:00.000000000',
    '2022-10-11T00:00:00.000000000', '2022-09-22T00:00:00.000000000',
    '2022-07-21T00:00:00.000000000', '2022-09-24T00:00:00.000000000',
    '2022-07-29T00:00:00.000000000', '2022-07-22T00:00:00.000000000',
    '2022-10-04T00:00:00.000000000', '2022-08-23T00:00:00.000000000',
]


description = [
    'Все вопросы по телефону',
    '.',
    'В хорошем состоянии',
    'Продам',
    'В отличном состоянии',
    'На ходу',
    '₽ – Данная цена автомобиля указана с учетом акции, подробности у менеджеров по телефону\n\n.',
    'Авто в отличном состоянии\nГБО нет и не было\nЛето на оригинальных дисках\nЕсть крашеные детали Касметика \nМотор и АКП обслужены\nВсе что нужно все сделано. \n\nБез влажений торг минимальный\n\nНа переучёт',
    'Отличное состояние! Косяки по кузову там,сям. Резина зима лето на дисках. Пробег родной. Оформлена на меня,без запретов и залогов! Без торга!',
    'Автомобил в хорошем состоянии всё работает все вопросы по телефону срочно обмен на хундай портер или фургон с ваше доплата срочно срочно',
    ''
]


year = [
    2008, 2012, 2007, 2011, 2013, 2014, 2010, 2006, 2018, 2017, 2019,
    2016, 2015, 2021, 2005, 2020, 2009, 2004, 2003, 2001, 2002, 2000,
    1999, 1998, 1997, 1996, 1993, 1992, 1994, 1995, 1991, 2022, 1990,
    1989, 1988, 1987, 1986, 1985, 1984, 1983, 1981, 1982, 1980, 1979,
    1976, 1978, 1975, 1974, 1977, 1973, 1972, 1971, 1970, 1969, 1967,
    1966, 1965, 1968, 1963, 1962, 1961, 1964, 1960, 1954, 1959, 1958,
    1956, 1953, 1955, 1957, 2023, 1934
]

generation = [
    'I рестайлинг (2003—2010)', 'II (2010—2023)', 'I (2016—2020)',
    'I (2012—2017)', 'H рестайлинг (2006—2014)', 'III (2013—2017)',
    'I (2015—2023)', 'I (2019—2023)', 'I рестайлинг (2010—2013)',
    'II (2016—2020)', 'I (1991—2000)', '80 (1989—1994)', 'III (1985—1992)', 'III (1996—2003)',
    'II (1985—1994)', 'K160 (1980—1994)',
    'C190/R190/X290 рестайлинг (2017—2023)', 'I (1990—1996)',
    'P70 (1985—1989)', 'IV (1999—2018)'
]
body_type = [
    'Седан', 'Внедорожник', 'Хетчбэк', 'Универсал', 'Фургон', 'Лифтбек',
    'Минивэн', 'Микроавтобус', 'Пикап', 'Купе', 'Кабриолет'
]
modification = [
    '2.0 AT (150 л.с.)', '2.0 4WD AT (150 л.с.)', '1.6 MT (102 л.с.)',
    '1.6 MT (82 л.с.)', '1.6 MT (105 л.с.)', '1.8 MT (140 л.с.)',
    '1.6 MT (106 л.с.)', '2.0 4WD CVT (146 л.с.)', '2.9 MT (107 л.с.)',
    '1.6 MT (114 л.с.)',
    '3.3 D 4WD MT (95 л.с.)', '2.5 4WD MT (171 л.с.)', '1.2 MT (75 л.с.)',
    '4.2 D AT (135 л.с.)', '0.7 AT (58 л.с.)', '2.0 D AT (190 л.с.)',
    '2.0 D 4WD AT (86 л.с.)', '3.0 4WD AT (130 л.с.)', '2.8 AT (174 л.с.)',
    '1.9 TDCi MT (130 л.с.)'
]
drive_type = ['Передний', 'Полный', 'Задний']
transmission_type = ['Автомат', 'Механика', 'Вариатор', 'Робот']
engine_type = ['Бензин', 'Дизель', 'Гибрид', 'Газ', 'Электро']
doors_number = [5, 4, 3, 2]
color = [
    'Чёрный', 'Белый', 'Серый', 'Серебряный', 'Синий', 'Красный', 'Зелёный',
    'Коричневый', 'Бежевый', 'Голубой', 'Бордовый', 'Золотой', 'Жёлтый',
    'Оранжевый', 'Фиолетовый', 'Пурпурный', 'Розовый'
]
pts = ['Оригинал', 'Дубликат', 'Электронный']
owners_count = ['> 3', '3', '1', '2']
mileage = (1000, 1000000)
latitude = (41.459186, 71.638912)
longitude = (19.892177, 177.689817)


def generate_car():
    return {
        "brand": random.choice(brand),
        "model": random.choice(model),
        "sale_end_date": random.choice(sale_end_date),
        "description": random.choice(description),
        "year": random.choice(year),
        "generation": random.choice(generation),
        "body_type": random.choice(body_type),
        "modification": random.choice(modification),
        "drive_type": random.choice(drive_type),
        "transmission_type": random.choice(transmission_type),
        "engine_type": random.choice(engine_type),
        "doors_number": random.choice(doors_number),
        "color": random.choice(color),
        "pts": random.choice(pts),
        "owners_count": random.choice(owners_count),
        "mileage": random.randint(mileage[0], mileage[1]),
        "latitude": random.uniform(latitude[0], latitude[1]),
        "longitude": random.uniform(longitude[0], longitude[1]),
    }


class QuickstartUser(HttpUser):
    wait_time = between(0.5, 1)

    @task
    def predict(self):
        self.client.post('/predict/', json=generate_car())
