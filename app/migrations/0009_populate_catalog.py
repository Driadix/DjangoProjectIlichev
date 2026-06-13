from django.db import migrations
from decimal import Decimal


def populate_catalog(apps, schema_editor):
    Category = apps.get_model('app', 'Category')
    Product = apps.get_model('app', 'Product')

    hw = Category.objects.create(name='Ретро-железо', slug='retro-hardware', description='Винтажные компьютеры, периферия и компоненты')
    sw = Category.objects.create(name='Софт и носители', slug='software', description='Программное обеспечение на физических носителях')
    acc = Category.objects.create(name='Аксессуары', slug='accessories', description='Мерч, литература и аксессуары для ретро-энтузиастов')

    products = [
        Product(category=hw, name='Commodore 64', description='Легендарный 8-битный домашний компьютер 1982 года. MOS 6510, 64 КБ RAM.', price=Decimal('12500.00')),
        Product(category=hw, name='ZX Spectrum 48K', description='Британская классика от Sinclair. Z80A, 48 КБ RAM, резиновая клавиатура.', price=Decimal('8900.00')),
        Product(category=hw, name='IBM Model M', description='Механическая клавиатура с buckling spring. Made in USA, 1989.', price=Decimal('6500.00')),
        Product(category=hw, name='Apple Macintosh 128K', description='Первый Macintosh 1984 года. Motorola 68000, 128 КБ RAM, 9\" монохромный дисплей.', price=Decimal('45000.00')),
        Product(category=hw, name='Amiga 500', description='Мультимедийный компьютер Commodore. Motorola 68000, OCS чипсет, 512 КБ RAM.', price=Decimal('18000.00')),

        Product(category=sw, name='MS-DOS 6.22 (дискеты)', description='Комплект из 3 дискет 3.5\". Последняя standalone-версия MS-DOS.', price=Decimal('1200.00')),
        Product(category=sw, name='Windows 3.11 for Workgroups', description='Оригинальная коробка с дискетами. Сетевая версия Windows 3.x.', price=Decimal('2500.00')),
        Product(category=sw, name='Turbo Pascal 7.0', description='Borland Turbo Pascal. Коробочное издание с документацией.', price=Decimal('3000.00')),
        Product(category=sw, name='Norton Commander 5.0', description='Файловый менеджер для DOS. Двухпанельный интерфейс.', price=Decimal('800.00')),
        Product(category=sw, name='Doom (shareware, дискета)', description='Оригинальная shareware-версия id Software, 1993. 1 дискета 3.5\".', price=Decimal('1500.00')),

        Product(category=acc, name='Книга "Искусство программирования" (Кнут)', description='Том 1: Основные алгоритмы. Классика computer science.', price=Decimal('4200.00')),
        Product(category=acc, name='Футболка "> Hello World"', description='Чёрная футболка с зелёным принтом. 100% хлопок. Размеры S-XXL.', price=Decimal('1800.00')),
        Product(category=acc, name='Кружка "There is no place like 127.0.0.1"', description='Керамическая кружка 350 мл с гик-принтом.', price=Decimal('650.00')),
        Product(category=acc, name='Набор стикеров "Retro OS"', description='12 виниловых стикеров с логотипами DOS, Amiga, Atari, Apple II.', price=Decimal('350.00')),
        Product(category=acc, name='Постер "UNIX Timeline"', description='Генеалогическое древо UNIX-систем. Формат A2, матовая бумага.', price=Decimal('900.00')),
    ]
    Product.objects.bulk_create(products)


def reverse_func(apps, schema_editor):
    Product = apps.get_model('app', 'Product')
    Category = apps.get_model('app', 'Category')
    Product.objects.all().delete()
    Category.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_category_alter_comment_post_product'),
    ]

    operations = [
        migrations.RunPython(populate_catalog, reverse_func),
    ]
