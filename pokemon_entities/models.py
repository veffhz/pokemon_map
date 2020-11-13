from django.db import models


class Pokemon(models.Model):
    """Покемон"""
    title = models.CharField('Название', max_length=200)
    image = models.ImageField('Изображение', null=True, blank=True)
    description = models.TextField('Описание', blank=True)
    title_en = models.CharField('Название на английском', max_length=200, blank=True)
    title_jp = models.CharField('Название на японском', max_length=200, blank=True)

    previous_evolution = models.ForeignKey(
        'Pokemon', on_delete=models.PROTECT, related_name='next_evolutions',
        null=True, blank=True, verbose_name='Предыдущая эволюция',
    )

    @property
    def next_evolution(self):
        return self.next_evolutions.first() # noqa

    def __str__(self):
        return f'{self.title}'


class PokemonEntity(models.Model):
    """Характеристики покемона"""
    lat = models.FloatField('Широта')
    lon = models.FloatField('Долгота')
    appeared_at = models.DateTimeField('Появляется в', null=True, blank=True)
    disappeared_at = models.DateTimeField('Исчезает в', null=True, blank=True)
    level = models.IntegerField('Уровень', default=0)
    health = models.IntegerField('Здоровье', default=10, null=True, blank=True)
    strength = models.IntegerField('Сила', default=1, null=True, blank=True)
    defence = models.IntegerField('Защита', default=1, null=True, blank=True)
    stamina = models.IntegerField('Выносливость', default=1, null=True, blank=True)

    pokemon = models.ForeignKey(
        Pokemon, on_delete=models.CASCADE, related_name='entities', verbose_name='Покемон',
    )

    def __str__(self):
        return f'Покемон {self.pokemon}'
