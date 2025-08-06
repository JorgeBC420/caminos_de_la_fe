DEITY_BONUSES = {
    'Cruzados': {
        'vida': 20,
        'resistencia': 10,
        'skills': [
            {
                'name': 'Juicio Divino',
                'desc': 'Invoca una cruz de luz que daña y cura en área.',
                'cooldown': 30
            },
            {
                'name': 'Estigma de los Herejes',
                'desc': 'Marca hasta 3 enemigos. Al morir, explotan con daño sagrado que se propaga.',
                'cooldown': 20
            },
            {
                'name': 'Bendición Divina',
                'desc': 'Cura y aumenta la defensa de los aliados cercanos. Invoca estandartes que otorgan beneficios.',
                'cooldown': 25
            }
        ]
    },
    'Sarracenos': {
        'ataque': 15,
        'velocidad': 5,
        'skills': [
            {
                'name': 'Llamarada del Desierto',
                'desc': 'Ola de fuego y arena que avanza, ciega y quema enemigos.',
                'cooldown': 30
            },
            {
                'name': 'Danza del Velo',
                'desc': 'Aumenta la evasión y contraataca automáticamente si esquiva un ataque.',
                'cooldown': 18
            },
            {
                'name': 'Genio Menor',
                'desc': 'Invoca un genio menor para distraer o dañar enemigos. Ráfagas de flechas y ataques de arena.',
                'cooldown': 22
            }
        ]
    },
    'Antiguos': {
        'defensa': 25,
        'skills': [
            {
                'name': 'Corazón del Bosque',
                'desc': 'Árbol gigante emerge, cura aliados y lanza semillas explosivas a enemigos cercanos.',
                'cooldown': 30
            },
            {
                'name': 'Piel de Bestia',
                'desc': 'Transforma al jugador en un híbrido con garras y mayor velocidad de ataque, causando sangrado.',
                'cooldown': 20
            },
            {
                'name': 'Furia Berserker',
                'desc': 'Aumenta el daño y la resistencia temporalmente. Invoca espíritus animales y ataques elementales.',
                'cooldown': 25
            }
        ]
    }
}

DEITIES = {
    'cruzado': [
        {
            'name': 'San Jorge, el Guerrero Santo',
            'passive': '+20% resistencia a daño demoníaco',
            'ultimate': 'Llama del Mártir',
            'ultimate_desc': 'Gran cruz luminosa que quema enemigos y cura aliados.'
        },
        {
            'name': 'Santa Lucía, la Guardiana de la Luz',
            'passive': '+regeneración de maná',
            'ultimate': 'Milagro de Luz',
            'ultimate_desc': 'Cura masiva e invulnerabilidad temporal.'
        }
    ],
    'sarraceno': [
        {
            'name': 'Djin del Viento Cortante',
            'passive': '+velocidad de ataque',
            'ultimate': 'Tornado de Arena',
            'ultimate_desc': 'Daño en área, empuja enemigos.'
        },
        {
            'name': 'Ifrit de las Sombras Ardientes',
            'passive': '+probabilidad de crítico',
            'ultimate': 'Fuego Interior',
            'ultimate_desc': 'Explosión con efecto DoT (daño prolongado).'
        }
    ],
    'antiguo': [
        {
            'name': 'Espíritu del Oso de Piedra',
            'passive': '+vida máxima',
            'ultimate': 'Pisotón del Guardián',
            'ultimate_desc': 'Aturde en área y daña.'
        },
        {
            'name': 'Árbol-Madre de los Bosques',
            'passive': '+regeneración pasiva',
            'ultimate': 'Llamado del Bosque',
            'ultimate_desc': 'Invoca raíces para atrapar enemigos y curar aliados.'
        }
    ]
}
