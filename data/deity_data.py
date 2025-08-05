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
