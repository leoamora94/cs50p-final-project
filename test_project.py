from project import create_start_list, read_csv, generate_pdf_start_lists
import pytest


def test_read_csv():
    with pytest.raises(FileNotFoundError):
        read_csv("inexist_file.csv")

    assert read_csv("./test/test_data.csv") == [
        ['FILHO ', 'Eduilton ', '08/05/1991', 'Masculino', 'SR', 'M109+', 110, 145, 255],
        ['SALES RODRIGUES', 'Fernando Henrique', '19/05/1986', 'Masculino', 'M35', 'M109+', 55, 65, 120],
        ['MENEZES', 'Guthemberg ', '21/02/1989', 'Masculino', 'SR', 'M109+', 117, 150, 267],
        ['LUCAS BATISTA DA SILVA', 'José', '14/06/1993', 'Masculino', 'SR', 'M109+', 118, 142, 260]
    ]


def test_create_start_list():
    athletes = [
        ['FILHO ', 'Eduilton ', '08/05/1991', 'Masculino', 'SR', 'M109+', 110, 145, 255],
        ['SALES RODRIGUES', 'Fernando Henrique', '19/05/1986', 'Masculino', 'M35', 'M109+', 55, 65, 120],
        ['MENEZES', 'Guthemberg ', '21/02/1989', 'Masculino', 'SR', 'M109+', 117, 150, 267],
        ['LUCAS BATISTA DA SILVA', 'José', '14/06/1993', 'Masculino', 'SR', 'M109+', 118, 142, 260]
    ]

    expected_result = [[
        ['SALES RODRIGUES', 'Fernando Henrique', '19/05/1986', 'Masculino', 'M35', 'M109+', 55, 65, 120],
        ['FILHO ', 'Eduilton ', '08/05/1991', 'Masculino', 'SR', 'M109+', 110, 145, 255],
        ['LUCAS BATISTA DA SILVA', 'José', '14/06/1993', 'Masculino', 'SR', 'M109+', 118, 142, 260],
        ['MENEZES', 'Guthemberg ', '21/02/1989', 'Masculino', 'SR', 'M109+', 117, 150, 267]
    ]]

    result_kid, result_male, result_female = create_start_list(athletes, 10)
    assert result_kid == []
    assert result_male == expected_result
    assert result_female == []


def test_generate_pdf_start_lists():
    male_start_list = [[
        ['SALES RODRIGUES', 'Fernando Henrique', '19/05/1986', 'Masculino', 'M35', 'M109+', 55, 65, 120],
        ['FILHO ', 'Eduilton ', '08/05/1991', 'Masculino', 'SR', 'M109+', 110, 145, 255],
        ['LUCAS BATISTA DA SILVA', 'José', '14/06/1993', 'Masculino', 'SR', 'M109+', 118, 142, 260],
        ['MENEZES', 'Guthemberg ', '21/02/1989', 'Masculino', 'SR', 'M109+', 117, 150, 267]
    ]]

    assert generate_pdf_start_lists(male_start_list, ",/test/test_males.pdf", 'M') == None
