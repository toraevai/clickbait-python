import argparse
from pathlib import Path
import csv
from tabulate import tabulate

def parse_file(path, videos):
    if Path(path).exists():
        with open(path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                videos.append(row)
    else:
        print(f"Файл по пути {path} отсутствует")

def process_clickbait(videos):
    filtered_videos = [video for video in videos if float(video["ctr"]) > 15 and int(video["retention_rate"]) < 40]
    filtered_videos.sort(key=lambda video: video["ctr"], reverse=True)
    columns_to_show = ["title", "ctr", "retention_rate"]
    info_to_show = [{column: video[column] for column in columns_to_show} for video in filtered_videos]
    print(tabulate(info_to_show, headers="keys", tablefmt="grid"))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--files", nargs="*", help="Названия файлов для обработки, например: 'stats1.csv stats2.csv', '*.csv'")
    parser.add_argument("--report", nargs="*", help="Название выводимого отчета, например: 'clickbait'")
    args = parser.parse_args()
    files = args.files
    
    videos = []
    if files:
        if ('*.csv' in files):
            for path in Path('.').glob('*.csv'):
                parse_file(path, videos)
        else:
            for file in files:
                parse_file(file, videos)
    else:
        print("Вы не указали файлы, которые необходимо обработать")
    
    reports = args.report
    if reports:
        for report in reports:
            match report:
                case "clickbait":
                    process_clickbait(videos)
                case _:
                    print(f"Отчет {report} еще не реализован")
    else:
        print("Вы не указали отчет, который необходимо вывести")


if __name__ == "__main__":
    main()
