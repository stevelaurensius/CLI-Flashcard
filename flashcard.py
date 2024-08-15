import os
import random
from io import StringIO
import argparse

hardest_list = {}
memory_file = StringIO()
card_lists = {}


def instruction():
    print('Pilih Menu (tambah, buang, import, export, ujian, keluar, log, kartu tersulit, reset stats):')
    memory_file.write('Pilih Menu (tambah, buang, import, export, ujian, keluar, log, kartu tersulit, reset stats):\n')
    user_input = input()
    memory_file.write(f'{user_input}\n')
    return user_input


def tambah():
    print('Kartu:')
    memory_file.write('Kartu:\n')
    while True:
        term_input = input()
        memory_file.write(f'{term_input}\n')
        if term_input in card_lists:
            print(f'Kartu "{term_input}" sudah pernah ditambahkan. Coba lagi:')
            memory_file.write(f'Kartu "{term_input}" sudah pernah ditambahkan. Coba lagi:\n')
        else:
            break
    print('Definisi kartu:')
    memory_file.write('Definisi kartu:\n')
    while True:
        definition_input = input()
        memory_file.write(f'{definition_input}\n')
        if definition_input in card_lists.values():
            print(f'Definisi "{definition_input}" sudah pernah ditambahkan. Coba lagi:')
            memory_file.write(f'Definisi "{definition_input}" sudah pernah ditambahkan. Coba lagi:\n')
        else:
            break
    card_lists[term_input] = definition_input
    print(f'Pasangan kartu dan definisi ("{term_input}":"{definition_input}") telah ditambahkan.')
    memory_file.write(f'Pasangan kartu dan definisi ("{term_input}":"{definition_input}") telah ditambahkan.\n')


def buang():
    print('Kartu mana?')
    memory_file.write('Kartu mana?\n')
    remove_card = input()
    memory_file.write(f'{remove_card}\n')
    if remove_card in card_lists:
        card_lists.pop(remove_card)
        print('Kartu telah dibuang.')
        memory_file.write('Kartu telah dibuang.\n')
    else:
        print(f'Tidak dapat membuang kartu "{remove_card}": kartu tidak ditemukan.')
        memory_file.write(f'Tidak dapat membuang kartu "{remove_card}": kartu tidak ditemukan.\n')


def ujian():
    print('Uji berapa kartu?')
    memory_file.write('Uji berapa kartu?\n')
    no_of_cards = int(input())
    memory_file.write(f'{no_of_cards}\n')
    card_items = list(card_lists.items())

    for _ in range(no_of_cards):
        data = random.choice(card_items)
        card_name = data[0]
        correct_answer = data[1]
        user_answer = input(f'Definisi dari "{card_name}":\n')
        memory_file.write(f'{user_answer}\n')

        if user_answer == correct_answer:
            print('Benar!')
            memory_file.write('Benar!\n')
        elif user_answer in card_lists.values() and user_answer != correct_answer:
            if card_name not in hardest_list:
                hardest_list[card_name] = 1
            else:
                hardest_list[card_name] += 1
            for key, value in card_lists.items():
                if value == user_answer:
                    print(f'Masih salah. Jawaban yang benar adalah "{correct_answer}", jawaban kamu adalah definisi dari "{key}".')
                    memory_file.write(f'Masih salah. Jawaban yang benar adalah "{correct_answer}", jawaban kamu adalah definisi '
                                      f'dari "{key}".\n')
        else:
            if card_name not in hardest_list:
                hardest_list[card_name] = 1
            else:
                hardest_list[card_name] += 1
            print(f'Masih salah. Jawaban yang benar adalah "{correct_answer}".')
            memory_file.write(f'Masih salah. Jawaban yang benar adalah "{correct_answer}".\n')


def import_file():
    print('Nama file:')
    memory_file.write('Nama file:\n')
    file_name = input()
    memory_file.write(f'{file_name}\n')
    import_from_file(file_name)


def import_from_file(file_name):
    if os.path.isfile(file_name):
        with open(file_name, 'r') as file:
            counter = 0
            for line in file:
                line = line.strip()
                term, definition = line.split(',')
                card_lists[term] = definition
                counter += 1
            print(f'{counter} kartu telah diimport.')
            memory_file.write(f'{counter} kartu telah diimport.\n')
    else:
        print('File tidak ditemukan.')
        memory_file.write('File ditemukan.\n')


def export_file():
    print('Nama File:')
    memory_file.write('Nama File:\n')
    output_file = input()
    memory_file.write(f'{output_file}\n')
    export_to_file(output_file)


def export_to_file(file_name):
    with open(file_name, 'w') as output:
        for key, value in card_lists.items():
            output.write(f'{key},{value}\n')
    print(f'{len(card_lists)} kartu telah disimpan.')
    memory_file.write(f'{len(card_lists)} kartu telah disimpan.\n')


def open_log():
    print('Nama File:')
    memory_file.write('Nama File:\n')
    log_name = input()
    memory_file.write(f'{log_name}\n')
    print('Log telah disimpan.')
    memory_file.write('Log telah disimpan.\n')
    memory_file.seek(0)
    with open(log_name, 'w') as log:
        for line in memory_file:
            log.write(line)


def hardest_card():
    if not hardest_list:
        print('Kamu belum pernah gagal di kartu apapun.')
        memory_file.write('Kamu belum pernah gagal di kartu apapun.\n')
    else:
        max_value = max(hardest_list.values())
        hardest_cards = [term for term, errors in hardest_list.items() if errors == max_value]
        if len(hardest_cards) > 1:
            cards_str = ', '.join(f'"{term}"' for term in hardest_cards)
            print(f'Kartu-kartu yang sering gagal adalah {cards_str}. Kamu pernah {max_value} gagal menjawab.')
            memory_file.write(f'Kartu-kartu yang sering gagal adalah {cards_str}. Kamu pernah {max_value} gagal menjawab.\n')
        else:
            print(f'The hardest card is "{hardest_cards[0]}". You have {max_value} errors answering it.')
            memory_file.write(f'The hardest card is "{hardest_cards[0]}". You have {max_value} errors answering it.\n')


def reset_stats():
    global hardest_list
    hardest_list = {}
    print('Statistik telah direset.')
    memory_file.write('Statistik telah direset.\n')


parser = argparse.ArgumentParser()
parser.add_argument('--import_from', help='File to import cards from')
parser.add_argument('--export_to', help='File to export cards to')
args = parser.parse_args()

if args.import_from:
    import_from_file(args.import_from)

while True:
    action = instruction().lower()
    if action == 'tambah':
        tambah()
    elif action == 'buang':
        buang()
    elif action == 'import':
        import_file()
    elif action == 'export':
        export_file()
    elif action == 'ujian':
        ujian()
    elif action == 'keluar':
        exit_message = 'Sampai jumpa!'
        print(exit_message)
        memory_file.write(f'{exit_message}\n')
        if args.export_to:
            export_to_file(args.export_to)
        break
    elif action == 'log':
        open_log()
    elif action == 'kartu tersulit':
        hardest_card()
    elif action == 'reset stats':
        reset_stats()
