
"""
Los Continentes del Velo Roto: La elección de facción transforma la experiencia y el inicio de la historia. Cada facción tiene su propia mentalidad, mentor, misión inicial y visión del Velo Roto.
"""
FACTION_INTROS = {
    'cruzado': {
        'mentalidad': "Eres un Guardián. Crees en el orden, la disciplina y la fuerza de la fe. La Disonancia es una herejía que debe ser purgada.",
        'inicio': "Ciudadela Amurallada de Aethelgard, continente de Valoria. Tras tu Rito de Iniciación, tu mentor Sir Kaelan te encomienda tu primera misión.",
        'mentor_dialogue': "Novato. Has jurado proteger el Equilibrio. Tu primera prueba te espera. En la frontera, el pozo sagrado se ha corrompido. Ve, purifica el agua y aplasta a cualquier criatura que porte el estigma de la Sombra.",
        'mision': "Viaja a la aldea, elimina las abominaciones y realiza el ritual de purificación. Descubres un fragmento de artefacto y tienes una visión de los otros portadores.",
        'descubrimiento': "Al purificar el agua, emerge un fragmento. Al tocarlo, ves a un Sarraceno y a un Antiguo encontrando fragmentos idénticos. La figura encapuchada te hace dudar.",
        'llamado': "Regresas con Sir Kaelan. Él te encomienda cruzar el océano y encontrar a los otros portadores para descubrir la verdad."
    },
    'sarraceno': {
        'mentalidad': "Eres un Erudito. Crees en el conocimiento y el equilibrio cósmico. La Disonancia es una anomalía peligrosa que debe ser estudiada y neutralizada.",
        'inicio': "Ciudad-Biblioteca de Qashir, continente de Al-Andar. Tras tu Rito de Iniciación, tu mentora Zahra te presenta tu primer desafío académico y práctico.",
        'mentor_dialogue': "Iniciado. Has jurado estudiar el Velo. En el Oasis de los Espejismos, el flujo de energía es errático. Lleva tus reactivos y escáner arcano. Cataloga las anomalías y recoge muestras.",
        'mision': "Analiza la flora y el agua, estudia los escorpiones alterados y usa tu habilidad de Danza de Cimitarras. Descubres un fragmento y una visión global.",
        'descubrimiento': "Al analizar la fuente, desentierras un fragmento. Ves a un Cruzado y a un Antiguo encontrando artefactos idénticos. La figura encapuchada es la variable desconocida.",
        'llamado': "Presentas tus hallazgos a Zahra. Ella te encomienda buscar a los otros portadores y compartir datos para formular una hipótesis sobre el verdadero enemigo."
    },
    'antiguo': {
        'mentalidad': "Eres un Vigilante. Crees en el ciclo de la vida y la Disonancia es una enfermedad que debe ser comprendida y sanada.",
        'inicio': "Aldea costera en el Archipiélago Central. Tras tu Rito de Iniciación, tu mentora Elowen te pide sanar la Isla de la Fuente.",
        'mentor_dialogue': "Joven espíritu. Has jurado escuchar a la tierra. El manantial ha empezado a susurrar pena. Ve, calma a las bestias y escucha lo que el agua tiene que decirte.",
        'mision': "Usa tus habilidades para calmar a los animales y sigue las líneas de energía hasta el epicentro. Encuentras un fragmento y tienes una visión compartida.",
        'descubrimiento': "En el manantial, encuentras un fragmento clavado en la tierra. Al tocarlo, ves a un Cruzado y a un Sarraceno intentando sanar heridas similares. La figura encapuchada es un vacío ajeno al ciclo natural.",
        'llamado': "Regresas con Elowen. Ella te encomienda viajar a las tierras de los otros portadores y unirlos para sanar la herida global."
    }
}
# Estructura narrativa y diálogos para los Actos II-VII, con capítulos desbloqueables por semana y progresión de Ciudadela
MISSION_STORY = {
    'act2': { # Semana 1
        'objective': "Cruzar el Gran Océano y encontrar a los otros portadores. La Disonancia infecta las relaciones entre continentes.",
        'chapters': [
            # ...igual que antes...
        ],
        'turning_point': "Los tres héroes comprenden su misión: llegar a la Grieta del Olvido antes que la Orden, unir los fragmentos y restaurar la prisión."
    },
    'act3': { # Semana 1-2
        'objective': "Regreso triunfal y ascenso a Guardián de la Grieta. Ceremonia pública y mejora de la Ciudadela al Tier 2.",
        'chapters': [
            {
                'title': 'La Carrera hacia la Grieta del Olvido',
                'events': [
                    'Regreso como héroe, ceremonia pública ante el líder de tu facción.',
                    'Discurso del líder: "Has enfrentado la oscuridad y contenido la herida del mundo. Mereces un bastión a la altura de tu leyenda."',
                    'Mejora de la Ciudadela a Casa de Piedra y Madera (Tier 2).',
                    'Desbloqueo de nuevas funciones: Puesto de Emisario, Armería de Guardián.'
                ]
            }
        ],
        'reward': "Acceso a funciones avanzadas y fondo de perfil heroico."
    },
    'act4': { # Semana 2-3
        'objective': "Reconstruir el mundo tras contener la Grieta del Olvido. Gestionar la política, la ciudadela y enfrentar nuevas amenazas.",
        'chapters': [
            # ...igual que antes...
        ],
        'endgame': "El jugador pasa de héroe a líder, gestionando el mundo y sentando las bases para futuras expansiones y dilemas morales."
    },
    'act5': { # Semana 3-4
        'objective': "El Legado de la Disonancia: la paz es frágil, la ambición humana es la nueva arma.",
        'chapters': [
            {
                'title': 'La Cruzada del Lobo Solitario',
                'events': [
                    'Rebelión de Lord Valerius, discurso apasionado a sus soldados.',
                    'Misiones de sabotaje, rescate y decisiones morales.',
                    '¿Capturas o convences a los soldados de Valerius?'
                ]
            },
            {
                'title': 'El Susurro en la Sombra',
                'events': [
                    'Descubres al Maestro de la Orden del Silencio como consejero de Valerius.',
                    'Infiltración en el Sanctum Interno, mazmorra de trampas y enemigos élite.',
                    'Encuentras el Aquila de la Legión Aeterna.'
                ]
            },
            {
                'title': 'El Juicio del Guardián',
                'events': [
                    'Regreso a la capital bajo control marcial.',
                    'Asalto urbano y duelo contra Lord Valerius.',
                    'Presentas pruebas, Valerius se rinde, guerra civil evitada.'
                ]
            }
        ],
        'reward': "Ciudadela Tier 3 (Casa Señorial), poder político y Aquila misteriosa."
    },
    'act6': { # Semana 4-5
        'objective': "El Despertar de la Legión: el orden contra la libertad, la amenaza lógica de Nova Roma.",
        'chapters': [
            {
                'title': 'El Continente Perdido',
                'events': [
                    'Expedición a Nova Roma, flota atraviesa niebla mágica.',
                    'Primer contacto con el Cónsul Aurelian, cultura avanzada pero sin magia espiritual.',
                    'Exploración y misiones secundarias para aprender sobre la sociedad romana.'
                ]
            },
            {
                'title': 'El Puño de Hierro de la Razón',
                'events': [
                    'Declaración formal de guerra del Senado de Nova Roma.',
                    'Invasión táctica, misiones de defensa global y gestión de recursos en la Ciudadela.',
                    'Batalla campal contra el Cónsul Aurelian en la torre de asedio.'
                ]
            }
        ],
        'reward': "Tregua con Nova Roma, respeto mutuo y apertura a la diplomacia."
    },
    'act7': { # Semana 8
        'objective': "El Secreto de las Arenas: el despertar de un poder antiguo y la guerra de los tres frentes.",
        'chapters': [
            {
                'title': 'La Tormenta Silenciosa',
                'events': [
                    'El Sumo Sacerdote Neferkare desata una tormenta de arena y un ejército de no-muertos.',
                    'Misiones de survival horror en tumbas y pirámides.',
                    'Trampas, puzzles y enemigos implacables.'
                ]
            },
            {
                'title': 'La Guerra de los Tres Frentes',
                'events': [
                    'Gestión de crisis en la War Table: Orden del Silencio, Legión Aeterna, invasión no-muerta.',
                    'Misiones de crisis con tiempo límite para salvar ciudades y recursos.',
                    'Decisiones estratégicas de alto impacto.'
                ]
            },
            {
                'title': 'La Gran Pirámide Negra',
                'events': [
                    'Mazmorra final con avatares de dioses egipcios.',
                    'Batalla final contra el Sumo Sacerdote Neferkare y el Avatar de Anubis.',
                    'Destrucción del avatar, liberación del mundo.'
                ]
            }
        ],
        'reward': "Ciudadela Tier 4 (Gran Mansión), escena final y post-créditos con presagio de la expansión nórdica."
    }
}
