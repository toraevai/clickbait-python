from main import parse_file, process_clickbait, main
import sys

# --- Unit Tests for Logic ---

def test_process_clickbait_filtering(capsys):
    """Проверка, что ctr > 15 и retention_rate < 40 работает корректно."""
    data = [
        {"title": "Видео А", "ctr": "20.5", "retention_rate": "30", "views": "5000", "likes": "100", "avg_watch_time": "3.5"},
        {"title": "Видео Б", "ctr": "10", "retention_rate": "30", "views": "10000", "likes": "1000", "avg_watch_time": "5"},
        {"title": "Видео В", "ctr": "25", "retention_rate": "50", "views": "15000", "likes": "900", "avg_watch_time": "8"},
        {"title": "Видео Г", "ctr": "15.5", "retention_rate": "40", "views": "52000", "likes": "1500", "avg_watch_time": "2.5"}
    ]
    process_clickbait(data)
    out = capsys.readouterr().out
    
    assert "Видео А" in out
    assert "Видео Б" not in out
    assert "Видео В" not in out
    assert "Видео Г" not in out

def test_process_clickbait_sorting(capsys):
    """Проверка, что сортировка по ctr работает корректно."""
    data = [
        {"title": "Видео А", "ctr": "16", "retention_rate": "10", "views": "15000", "likes": "900", "avg_watch_time": "8"},
        {"title": "Видео Б", "ctr": "25", "retention_rate": "10", "views": "5000", "likes": "100", "avg_watch_time": "3.5"},
    ]
    process_clickbait(data)
    out = capsys.readouterr().out
    
    assert out.find("Видео Б") < out.find("Видео А")

# --- Integration Tests for File Handling ---

def test_parse_file_success():
    """Проверка считывания файла stats1.csv."""
    videos = []
    parse_file("stats1.csv", videos)
    
    assert len(videos) == 10
    assert videos[0]["title"] == "Я бросил IT и стал фермером"

def test_parse_file_missing(capsys):
    """Проверка на обработку отсутствующего файла."""
    videos = []
    parse_file("non_existent_file.csv", videos)
    out = capsys.readouterr().out
    assert "отсутствует" in out

# --- CLI & Functional Tests ---

def test_main_no_args(capsys, monkeypatch):
    """Проверка скрипта при отсутствующих аргументах."""
    monkeypatch.setattr(sys, 'argv', ['main.py'])
    main()
    out = capsys.readouterr().out
    assert "Вы не указали файлы" in out

def test_main_no_report(capsys, monkeypatch):
    """Проверка скрипта при отсутсвующем отчете."""
    monkeypatch.setattr(sys, 'argv', ['main.py', '--files', 'stats1.csv'])
    main()
    out = capsys.readouterr().out
    assert "Вы не указали отчет" in out

def test_no_duplicate_records_when_same_file_passed_twice(capsys, monkeypatch):
    args = ['main.py', '--files', 'stats1.csv', 'stats1.csv', '--report', 'clickbait']
    monkeypatch.setattr(sys, 'argv', args)
    main()
    out = capsys.readouterr().out
    assert out.count("Секрет который скрывают тимлиды") == 1, "Найдено дублирующееся видео."

def test_main_clickbait_full_flow(capsys, monkeypatch):
    """Проверка работы скрипта на файлах stats1.csv stats2.csv."""
    monkeypatch.setattr(sys, 'argv', ['main.py', '--files', 'stats1.csv', 'stats2.csv', '--report', 'clickbait'])

    main()
    
    out = capsys.readouterr().out
    assert "Секрет который скрывают тимлиды" in out
    assert "Почему продакшн упал в пятницу вечером" in out
    assert "Рефакторинг выходного дня" not in out
    assert "Дедлайн подкрался незаметно" not in out