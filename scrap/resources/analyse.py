import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist

stop_words = set(stopwords.words('spanish'))

text = "Gobierno pide suspender venta presencial de electrodomésticos en días sin IVA " \
       "753 comparendos y 320 fiestas intervenidas el fin de semana en Barranquilla El " \
       "Atlántico supera las mil muertes por COVID-19 En el Calancala se han duplicado " \
       "las inhumaciones por la COVID-19 “Bogotá tiene que adquirir ventiladores”: Minsalud " \
       "Ejército investiga otra presunta violación a niña indígena en el Guaviare Funeraria " \
       "no prestó servicios a adulto mayor  Realizan concurso del ‘más comelón’ en La Paz, " \
       "Cesar, violando la cuarentena Sucre registra 160 casos de coronavirus en un día No hay " \
       "un solo caso de COVID en la cárcel de Riohacha Maicao cumple 94 años con 198 casos de " \
       "COVID-19 Dos hombres mueren en La Luz tras balacera con la Policía Asesinan a hombre " \
       "durante un sepelio en el Calancala Las huellas que va dejando Muriel en el ‘Calcio’ " \
       "italiano Fallece a los 72 años el excampeón de boxeo panameño Ernesto ‘Ñato’ Marcel " \
       "El Barcelona ficha a Pjanic por 60 millones de euros “Los barcos no se hunden por el " \
       "agua que los rodea”, Djokovic a sus críticos   “El sistema del torneo me parece muy bueno”: " \
       "Comesaña  “Hubo algún contacto con Junior”: Jorge Luis Pinto  Junior jugaría en el Romelio " \
       "y la Liga tendría cuadrangulares semifinales ‘Mucho mucho amor’, el documental de Netflix " \
       "sobre Walter Mercado Broadway anuncia que no abrirá sus teatros hasta 2021 Convertir la " \
       "moda en conciencia: un reto para el Fitness Ecosistemas liberarán más metano por calentamiento " \
       "global, según expertos Reik y Morat, juntos por ‘La bella y la bestia’ La alimentación: " \
       "el escudo protector del sistema inmune Giselle Barceló: “Ser Chica M! fue especial y siempre " \
       "estaré agradecida con EL HERALDO” ¡Sigue el horror en Colombia! Virus deja 157 nuevos muertos " \
       "Mensajeros y mujeres, las víctimas de hurto durante la cuarentena Duque posesionó a Campo como " \
       "director de la UNP Comercio de Valledupar se movilizará por domicilios Gobernador propone la " \
       "fórmula ‘matrícula cero’ Comercio de Valledupar se movilizará por domicilios Gobernador propone " \
       "la fórmula ‘matrícula cero’ Plantón en el Hospital para pedir reintegro de trabajadores despedidos " \
       "Hoy se posesiona Alfonso Campo en la dirección de UNP De manera gradual se restableció el servicio " \
       "de energía Alcaldes no podrán cambiar el slogan ni escudo del municipio ¡Sigue el horror en " \
       "Colombia! Virus deja 157 nuevos muertos Duque posesionó a Campo como director de la UNP Fenalco " \
       "consideró de “positiva”  la jornada Virus mató a otras 54 personas en Colombia Carta de Mindeporte " \
       "pone en aprietos al presidente de la Dimayor El “garrafal error” que reconoció árbitro de final de " \
       "la Champions 2016 Fútbol colombiano da un paso adelante para reapertura: será por fases Fuerte pulla " \
       "de Aquivaldo a Pékerman: “Si veo irrespeto, prefiero retirarme” Condenado a 60 años de prisión el " \
       "segundo de las Águilas Negras en Cesar Mensajeros y mujeres, las víctimas de hurto durante la " \
       "cuarentena Bebé se cayó de la cama y murió Bebé murió calcinado durmiendo en su casa Estudiante " \
       "fue asesinado tras oponerse a robo en Fundación Ataque de sicarios dejó un muerto y un herido Uribe " \
       "dice que pagó $ 208 millones en impuestos ´La reforma a la justicia se radicaría en julio y no en marzo´: " \
       "Cabello Arturo Char, el elegido para presidir el Senado Se ´derrumbó´ la Bolsa de Valores Coophumana " \
       "propone fortalecer el sector financiero y el consumo Inflación llegaría a 3,36 % Esposa de expolicía " \
       "detenido por muerte de George Floyd le pide el divorcio Joven de 18 años con coronavirus se salvó gracias " \
       "a trasplante de pulmones Corea del Sur vuelve al confinamiento tras nuevo brote del virus Palestinos " \
       "lanzaron globos incendiarios desde Gaza hacia Israel Multitudinaria protesta Directora de laboratorio " \
       "de Wuhan rechaza las acusaciones del mundo Peter Manjarrés deberá pagar millonario pleito a su antiguo " \
       "corista Gran parranda virtual con 4 Reyes de Reyes Rafael Díaz anuncia su canción ‘Te esperaré’ Conciertos " \
       "vallenatos virtuales Hoy se cumplen 28 años de su asesinato Daniela Álvarez, aislada por sospecha de " \
       "Covid-19 Días sin IVA: se suspende venta de electrodomésticos de forma presencial Muere Ernesto Marcel, ex " \
       "campeón mundial panameño de boxeo  Corte de EE.UU. anula ley para clínicas de aborto de Luisiana  Mientras " \
       "estés en casa, cuida tu cuerpo  ¿Más casos de violaciones en las Fuerzas Armadas?  Secretaría de " \
       "Participación reubica a 34 adultos mayores en estado de abandono  Este lunes arranca nueva rotación de " \
       "pico y placa para taxis en Cartagena  OMS: “El coronavirus tiene todavía mucho espacio para moverse”  " \
       "Cartagena tiene más recuperados que casos activos de COVID-19  Irán registra un récord diario de 162 muertes " \
       "por COVID-19  A 49 aumentó cifra de personas fallecidas por COVID-19 en Sucre  Rebrote de COVID-19 causa " \
       "confinamiento de 500.000 personas en China Universidad del Sinú adquiere robot para pruebas COVID  " \
       "Personas en 6 continentes prueban vacunas contra el COVID-19  Crece el número de muertes por COVID-19 en " \
       "Córdoba  Policía decomisa 1.224 kilos de cocaína en puerto de Cartagena  $ 745.000 millones para Familias " \
       "y Jóvenes en Acción  Reflexión de Natalia Reyes por el polémico caso de Ciro Guerra  Estas son las " \
       "futbolistas más destacadas a nivel mundial  Sonia Osorio: Colombia en un ballet ‘Monos’ ganó dos premios " \
       "Plantino Xcaret del cine iberoamericano  Netflix lanza el tráiler de su documental sobre Walter Mercado " \
       "Corte de EE.UU. anula ley para clínicas de aborto de Luisiana  Muere Ernesto Marcel, ex campeón mundial " \
       "panameño de boxeo  Barranquilla, donde se practican más pruebas PCR para COVID-19  Mientras estés en casa, " \
       "cuida tu cuerpo  Secretaría de Participación reubica a 34 adultos mayores en estado de abandono " \
       "Sandra Narváez, una estratega a prueba de dificultades  ¿Más casos de violaciones en las Fuerzas Armadas?  " \
       "Lluvia y sol: cuidado con los cambios de clima  320 fiestas se intervinieron en Barranquilla en el fin de " \
       "semana  Explosiones en mercado de Afganistán dejan 23 víctimas fatales Saludo con la gorra en el 100mo " \
       "aniversario de Ligas Negras  La mujer que casi muere por el COVID-19 y por las mentiras de las redes  " \
       "Los deseos de Gabo en los hombros de Jaime Abello  “Ha sido muy difícil todo esto”: dueños " \
       "del ‘mandarizano’  " \
       "‘Pachito’ Aldana, un guerrero de mil batallas Jose Ricardo transforma a Cartagena desde la comunicación " \
       "Cada idea es un sueño de éxito en medio de la crisis  Vuelo humanitario: las travesías de un repatriado " \
       "Federico García Lorca, secretos guardados Bombones con sabor al sur de Bolívar  Día sin IVA: Gobierno " \
       "recomienda suspender ventas presenciales de electrodomésticos Udes anuncia pregrado de Comunicación Social " \
       "y Periodismo en Valledupar Fiesta y concurso de ‘El más comelón’ en La Paz durante el toque de queda Irán " \
       "emite orden de arresto contra Donald Trump por muerte de Soleimaní Envían a la cárcel a encargados de " \
       "laboratorio de coca en Chimichagua ¡Mea culpa! Mortal champeta en Codazzi “Alea jacta est” Semblanza del " \
       "Colegio Nacional Loperena Pero no vuelven En la pandemia gratuidad en la educación " \
       "superior Investigan cerco " \
       "epidemiológico de primer caso de covid-19 en Manaure Mataron a habitante de calle en medio del " \
       "toque de queda " \
       "en Valledupar Familia sacó cadáver de una IPS en Soledad, Atlántico “No es una opción viable " \
       "encerrarnos hasta " \
       "que aparezca una vacuna”: Duque Casas de apuestas en Colombia, un negocio en constante auge " \
       "Joven creó tapabocas " \
       "transparente para comunidad sorda “Los casos de covid-19 seguirán en aumento”: expertos en salud " \
       "Buscan disminuir " \
       "indicadores de pobreza de municipios mineros Uno más, sigue el abandono de adultos mayores Las " \
       "bodas de plata de " \
       "LuisEnrique con Rosalbina Festival virtual y serenatas a distancia en La Peña y Guaymaral La " \
       "perjudicial división " \
       "del arte en Valledupar: consejeros vs. Oficina de Cultura Murió por coronavirus el cantante " \
       "barranquillero " \
       "‘Joe’ Urquijo Renuncian representantes del Consejo de Cultura de Valledupar Yina Calderón y Manuela " \
       "González volvieron a estallar las redes con un beso “No se logró ni funcionó porque él no quiso”, " \
       "Lina Tejeiro sobre su relación con Andy Rivera Estos son los estrenos que trae Netflix en julio " \
       "“El cemento puede esperar, la prioridades contener la pandemia”: Mello Castro Fiesta y concurso de ‘El más " \
       "comelón’ en La Paz durante el toque de queda Envían a la cárcel a encargados de laboratorio de coca " \
       "en Chimichagua Investigan cerco epidemiológico de primer caso de covid-19 en Manaure Cierran barrios de " \
       "Riohacha donde se presentan mayores brotes de la covid-19 Casas de apuestas en Colombia, un negocio en " \
       "constante auge Conozca Skrill, una de las plataformas más reconocidas para comprar criptomonedas Falla " \
       "mundial en WhatsApp: no muestra última conexión Pasos para descargar WhatsApp Plus gratis"

tokenizer = nltk.RegexpTokenizer(r"\w+")
new_words = tokenizer.tokenize(text)
print(new_words)

tokenized_word = word_tokenize(text)
print(tokenized_word)

fdist = FreqDist(new_words)
print(fdist)

filtered_sent = []
for w in new_words:
    if w not in stop_words:
        filtered_sent.append(w)
print("Tokenized Sentence:", new_words)
print("Filterd Sentence:", filtered_sent)

fdist = FreqDist(filtered_sent)
print(fdist['días'])
print(fdist.hapaxes())
print(fdist.most_common(10))
