"""
This module conatins the BlueSky Web Scrapper CLI
"""

# pylint: disable=C0301

import click

lang_dict = {
    'Afar': 'aa',
    'Abkhazian': 'ab',
    'Afrikaans': 'af',
    'Akan': 'ak',
    'Albanian': 'sq',
    'Amharic': 'am',
    'Arabic': 'ar',
    'Aragonese': 'an',
    'Armenian': 'hy',
    'Assamese': 'as',
    'Avaric': 'av',
    'Avestan': 'ae',
    'Aymara': 'ay',
    'Azerbaijani': 'az',
    'Bashkir': 'ba',
    'Bambara': 'bm',
    'Basque': 'eu',
    'Belarusian': 'be',
    'Bengali': 'bn',
    'Bihari languages': 'bh',
    'Bislama': 'bi',
    'Tibetan': 'bo',
    'Bosnian': 'bs',
    'Breton': 'br',
    'Bulgarian': 'bg',
    'Burmese': 'my',
    'Catalan': 'ca',
    'Czech': 'cs',
    'Chamorro': 'ch',
    'Chechen': 'ce',
    'Chinese': 'zh',
    'Church Slavic': 'cu',
    'Chuvash': 'cv',
    'Cornish': 'kw',
    'Corsican': 'co',
    'Cree': 'cr',
    'Welsh': 'cy',
    'Danish': 'da',
    'German': 'de',
    'Divehi': 'dv',
    'Dzongkha': 'dz',
    'Greek, Modern (1453-)': 'el',
    'English': 'en',
    'Esperanto': 'eo',
    'Estonian': 'et',
    'Ewe': 'ee',
    'Faroese': 'fo',
    'Persian': 'fa',
    'Fijian': 'fj',
    'Finnish': 'fi',
    'French': 'fr',
    'Western Frisian': 'fy',
    'Fulah': 'ff',
    'Georgian': 'ka',
    'Gaelic': 'gd',
    'Irish': 'ga',
    'Galician': 'gl',
    'Manx': 'gv',
    'Guarani': 'gn',
    'Pushto': 'ps',
    'Quechua': 'qu',
    'Romansh': 'rm',
    'Romanian': 'ro',
    'Russian': 'ru',
    'Sango': 'sg',
    'Sanskrit': 'sa',
    'Sinhala': 'si',
    'Slovak': 'sk',
    'Slovenian': 'sl',
    'Northern Sami': 'se',
    'Samoan': 'sm',
    'Shona': 'sn',
    'Sindhi': 'sd',
    'Somali': 'so',
    'Sotho, Southern': 'st',
    'Spanish': 'es',
    'Sardinian': 'sc',
    'Serbian': 'sr',
    'Swati': 'ss',
    'Sundanese': 'su',
    'Swahili': 'sw',
    'Swedish': 'sv',
    'Tahitian': 'ty',
    'Tamil': 'ta',
    'Tatar': 'tt',
    'Telugu': 'te',
    'Tajik': 'tg',
    'Tagalog': 'tl',
    'Thai': 'th',
    'Tigrinya': 'ti',
    'Tonga (Tonga Islands)': 'to',
    'Tswana': 'tn',
    'Tsonga': 'ts',
    'Turkmen': 'tk',
    'Turkish': 'tr',
    'Twi': 'tw',
    'Uighur': 'ug',
    'Ukrainian': 'uk',
    'Urdu': 'ur',
    'Uzbek': 'uz',
    'Venda': 've',
    'Vietnamese': 'vi',
    'Volapük': 'vo',
    'Walloon': 'wa',
    'Wolof': 'wo',
    'Xhosa': 'xh',
    'Yiddish': 'yi',
    'Yoruba': 'yo',
    'Zhuang': 'za',
    'Zulu': 'zu',
}

@click.command()
@click.option(
    '-q',
    '--query',
    type=str,
    required=True,
    help='Search query string. Required'
)

@click.option(
    '-s',
    '--sort',
    type=click.Choice(['top', 'latest'], case_sensitive=False),
    required=False,
    help='Rank results by "top" or "latest',
)

@click.option(
    '--since',
    type=str,
    required=False,
    help=(
        'Filter results for posts after the specified datetime (inclusive). '
        'Use ISO 8601 format: "YYYY-MM-DD" or full datetime. Uses "sortAt" timestamp.'
    )
)

@click.option(
    '--until',
    type=str,
    required=False,
    help=(
        'Filter results for posts before the specified datetime (not inclusive). '
        'Use ISO 8601 format: "YYYY-MM-DD" or full datetime. Uses "sortAt" timestamp.'
    )
)

@click.option(
    '-m',
    '--mentions',
    type=str,
    help='Filter posts mentioning the specified account (omit the @ symbol).'
)

@click.option(
    '-a',
    '--author',
    type=str,
    required=False,
    help='Filter posts by the specified account (omit the @ symbol).'
)

@click.option(
    '-l',
    '--lang',
    type=str,
    required=False,
    help=f"Filter posts by language.\n\nLanguage Options:\n\n {', '.join(list(lang_dict.keys()))}\n\n"
)

@click.option(
    '-d',
    '--domain',
    type=str,
    required=False,
    help='Filter posts containing links to the specified domain.'
)

@click.option(
    '-t',
    '--tags',
    type=str,
    multiple=True,
    required=False,
    help=(
        'Filter posts by hashtag (omit the # symbol). '
        'Multiple tags can be specified: -t tag1 -t tag2. OR -t "tag1, tag2"'
    )
)

@click.option(
    '--limit',
    type=click.IntRange(1,100),
    required=False,
    help='Set the maximum number of posts to retrieve (default: 25).'
)

def params(query="", sort="", since="", until="", mentions="", author="", lang="", domain="", tags=tuple()):
    """
    method that tests if each click param flag is being passed in correctly
    """
    # pylint: disable=R0913
    # pylint: disable=R0917

    click.echo(f"Query: {query}")
    click.echo(f"Sort: {sort}")
    click.echo(f"Since: {since}")
    click.echo(f"Until: {until}")
    click.echo(f"Mentions: {mentions}")
    click.echo(f"Author: {author}")
    click.echo(f"Language: {lang_dict[lang]}")
    click.echo(f"Domain: {domain}")
    click.echo(f"Tags: {list(tags)}")

if __name__ == '__main__':
    params()
