import subprocess

def process_exists(process_name):
    call = 'TASKLIST', '/FI', '"IMAGENAME eq %s"' % process_name
    # use buildin check_output right away
    output = subprocess.check_output('TASKLIST /FI "IMAGENAME eq ModernWarfare.exe"').decode('unicode_escape')
    # check in last line for process name
    last_line = output.strip().split('\r\n')[-1]
    # because Fail message could be translated
    return last_line.lower().startswith(process_name.lower())

if __name__ == "__main__":
    print(process_exists('ModernWarfare.exe'))