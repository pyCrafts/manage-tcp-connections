import subprocess
import time
import os
import logging


def get_pids_from_process(programm_name):
    cmd = f'tasklist | find "{programm_name}"'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    pids = []
    try:
        for line in result.stdout.strip().split("\n"):
            pids.append(int(line.split()[1]))
        return pids
    except Exception:
        return []


def restart_program(program_path, program_name, language):
    # Close program
    try:
        subprocess.run(f"taskkill /IM {program_name} /F", check=True)
        print(program_name, messages.get(language, {}).get("close_program_success"))
    except subprocess.CalledProcessError as e:
        print(messages.get(language, {}).get("close_program_failed"), program_name)
        logging.error(f"Error closing program {program_name}: {e}")

    # Timeout for closed connections
    time.sleep(10)

    # Open program
    subprocess.Popen(program_path)
    print(messages.get(language, {}).get("open_program"), program_name)
    logging.info(f"{messages.get(language, {}).get('open_program')} {program_name}")


def check_connection_count(pids, program_path, program_name, language, cnt, active_cnt):
    connections_count, established_connections_count = 0, 0
    for pid in pids:
        # Search connections
        result = subprocess.run(
            f'netstat -ano | find "{pid}" /c',
            shell=True,
            capture_output=True,
            text=True,
        )
        connections_count += int(result.stdout.strip())
        if connections_count and connections_count > cnt:
            print(messages.get(language, {}).get("connections"), connections_count)
            logging.info(
                f"{messages.get(language, {}).get('connections')} {connections_count}"
            )
            restart_program(program_path, program_name, language)
            break

        # Search active connections
        result = subprocess.run(
            f'netstat -ano | find "{pid}" | find "ESTABLISHED" /c',
            shell=True,
            capture_output=True,
            text=True,
        )
        established_connections_count += int(result.stdout.strip())
        if established_connections_count and established_connections_count > active_cnt:
            print(
                messages.get(language, {}).get("active_connections"),
                established_connections_count,
            )
            logging.info(
                f"{messages.get(language, {}).get('active_connections')} {established_connections_count}"
            )
            restart_program(program_path, program_name, language)
            break


if __name__ == "__main__":
    messages = {
        "1": {
            "enter_program_path": "Enter the path to the program (for example, C:\\folder\\program.exe): ",
            "enter_connections_cnt": "Enter the maximum number of connections ",
            "enter_active_connections_cnt": "Enter the maximum number of active connections ",
            "enter_timeout": "Enter timeout for checking (seconds) ",
            "close_program_success": "closed",
            "close_program_failed": "Failed close",
            "open_program": "Open",
            "connections": "The number of connections is over",
            "active_connections": "The number of active connections is over",
            "program_not_found": "not found!",
            "program_not_running": "not running!",
            "start_checking": "Start checking ...",
            "sleep_checking": "Сheck complete, sleep",
        },
        "2": {
            "enter_program_path": "Введите путь к программе (например, C:\\папка\\программа.exe): ",
            "enter_connections_cnt": "Введите максимальное количество соединений ",
            "enter_active_connections_cnt": "Введите максимальное количество активных соединений ",
            "enter_timeout": "Введите таймаут проверки (секунды) ",
            "close_program_success": "завершена",
            "close_program_failed": "Не удалось завершить",
            "open_program": "Запущена программа",
            "connections": "Количество соединений свыше",
            "active_connections": "Количество активных соединений свыше",
            "program_not_found": "не найдена!",
            "program_not_running": "не запущена!",
            "start_checking": "Начинается проверка ...",
            "sleep_checking": "Проверка завершена, спим",
        },
    }

    logging.basicConfig(
        filename="app.log",
        level=logging.INFO,
        format="%(asctime)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    language = input("Choose language (1 - en or 2 - ru): ")
    program_path = input(messages.get(language, {}).get("enter_program_path"))
    program_name = os.path.basename(program_path)
    cnt = int(input(messages.get(language, {}).get("enter_connections_cnt")))
    active_cnt = int(
        input(messages.get(language, {}).get("enter_active_connections_cnt"))
    )
    timeout = int(input(messages.get(language, {}).get("enter_timeout")))

    if os.path.isfile(program_path):
        while True:
            pids = get_pids_from_process(program_name)
            if pids:
                print(messages.get(language, {}).get("start_checking"))
                check_connection_count(
                    pids, program_path, program_name, language, cnt, active_cnt
                )
                time.sleep(timeout)
                print(
                    messages.get(language, {}).get("sleep_checking"),
                    timeout,
                    "sec ...\n" + "-" * 32,
                )
            else:
                print(
                    program_name, messages.get(language, {}).get("program_not_running")
                )
                logging.info(
                    f"{program_name} {messages.get(language, {}).get('program_not_running')}"
                )
                break
    else:
        print(program_name, messages.get(language, {}).get("program_not_found"))
        logging.info(
            f"{program_name} {messages.get(language, {}).get('program_not_found')}"
        )
